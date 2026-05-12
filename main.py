import os
import json
import subprocess
import tempfile
import re
from typing import TypedDict, Dict, Any

from langgraph.graph import StateGraph, END
from crewai import Agent, Task, Crew, LLM

# -------------------------
# Config
# -------------------------
MAX_ITERS = 3
TIMEOUT = 60

# CrewAI quirk
os.environ["OPENAI_API_KEY"] = "dummy"

# -------------------------
# LLM (CrewAI + Ollama)
# -------------------------
llm = LLM(
    model="ollama/mistral",   # change to ollama/phi if needed
    base_url="http://localhost:11434"
)

# -------------------------
# Agents (MUST be before nodes)
# -------------------------
research_agent = Agent(
    role="Research Engineer",
    goal="Find root causes of concurrency bugs",
    backstory="Expert in multithreading, race conditions, and scaling",
    llm=llm,
    verbose=True
)

debug_agent = Agent(
    role="Senior Debug Engineer",
    goal="Produce FIX with NO global state and pytest tests",
    backstory="Writes production-safe concurrent systems",
    llm=llm,
    verbose=True
)

# -------------------------
# State
# -------------------------
class RnDState(TypedDict):
    bug: str
    research_notes: str
    fix_code: str
    test_code: str
    test_stdout: str
    test_stderr: str
    verdict: str
    iterations: int

# -------------------------
# Helpers
# -------------------------
def extract_json(text: str, default: Dict[str, Any]):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print("⚠️ JSON parse error:", e)
    return default

def ensure_imports(test_code: str):
    if "from solution import" not in test_code:
        return "from solution import *\n\n" + test_code
    return test_code

def ensure_pytest_installed():
    try:
        subprocess.run(["python", "-m", "pytest", "--version"], capture_output=True)
    except:
        subprocess.run(["python", "-m", "pip", "install", "pytest"], check=True)

def run_crew(agent, task):
    try:
        result = Crew(agents=[agent], tasks=[task], verbose=True).kickoff()
        print("\n🔍 RAW LLM OUTPUT:\n", result)
        return str(result)
    except Exception as e:
        print("❌ CREW ERROR:", e)
        return f"ERROR: {e}"

# -------------------------
# Execution
# -------------------------
def run_pytest(module_code, test_code):
    ensure_pytest_installed()

    with tempfile.TemporaryDirectory() as td:
        module_path = os.path.join(td, "solution.py")
        test_path = os.path.join(td, "test_solution.py")

        with open(module_path, "w") as f:
            f.write(module_code)

        with open(test_path, "w") as f:
            f.write(test_code)

        try:
            proc = subprocess.run(
                ["python", "-m", "pytest", "-q"],
                cwd=td,
                capture_output=True,
                text=True,
                timeout=TIMEOUT
            )
            return proc.stdout, proc.stderr
        except subprocess.TimeoutExpired:
            return "", "TIMEOUT"

# -------------------------
# Nodes
# -------------------------
def research_node(state: RnDState):
    task = Task(
        description=f"""
Analyze this bug:

{state['bug']}

STRICT RULES:
- Return ONLY valid JSON
- No explanation
- No markdown

Format:
{{
  "root_causes": ["..."],
  "strategy": "..."
}}
""",
        agent=research_agent,
        expected_output="Valid JSON"
    )

    result = run_crew(research_agent, task)
    data = extract_json(result, {"root_causes": [], "strategy": result})

    return {
        **state,
        "research_notes": json.dumps(data, indent=2),
        "iterations": state["iterations"] + 1
    }

def debug_node(state: RnDState):
    task = Task(
        description=f"""
Bug:
{state['bug']}

Research:
{state['research_notes']}

STRICT RULES:
- ONLY JSON
- NO explanation
- NO markdown
- Provide FULL working Python code

Format:
{{
  "module_code": "FULL PYTHON CODE",
  "tests": "PYTEST CODE"
}}
""",
        agent=debug_agent,
        expected_output="Valid JSON"
    )

    result = run_crew(debug_agent, task)
    data = extract_json(result, {"module_code": "", "tests": ""})

    module_code = data.get("module_code", "")
    test_code = ensure_imports(data.get("tests", ""))

    return {
        **state,
        "fix_code": module_code,
        "test_code": test_code
    }

def execute_node(state: RnDState):
    stdout, stderr = run_pytest(state["fix_code"], state["test_code"])
    return {
        **state,
        "test_stdout": stdout,
        "test_stderr": stderr
    }

def qa_node(state: RnDState):
    out = state["test_stdout"].lower()
    err = state["test_stderr"].lower()

    if "global " in state["fix_code"]:
        return {**state, "verdict": "FAIL"}

    if "failed" in out or "error" in err:
        verdict = "FAIL"
    elif "passed" in out:
        verdict = "PASS"
    else:
        verdict = "LIKELY_PASS"

    return {**state, "verdict": verdict}

# -------------------------
# Control
# -------------------------
def should_continue(state: RnDState):
    if state["verdict"] == "PASS":
        return "end"
    if state["iterations"] >= MAX_ITERS:
        return "end"
    return "loop"

# -------------------------
# Graph
# -------------------------
graph = StateGraph(RnDState)

graph.add_node("research", research_node)
graph.add_node("debug", debug_node)
graph.add_node("execute", execute_node)
graph.add_node("qa", qa_node)

graph.set_entry_point("research")

graph.add_edge("research", "debug")
graph.add_edge("debug", "execute")
graph.add_edge("execute", "qa")

graph.add_conditional_edges(
    "qa",
    should_continue,
    {"loop": "research", "end": END}
)

app = graph.compile()

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    print("🚀 Multi-Agent Debugging System (Ollama Local)\n")

    state = {
        "bug": "API returns 500 error under concurrent requests",
        "research_notes": "",
        "fix_code": "",
        "test_code": "",
        "test_stdout": "",
        "test_stderr": "",
        "verdict": "FAIL",
        "iterations": 0
    }

    result = app.invoke(state)

    print("\n===== FINAL RESULT =====")
    print("Verdict:", result["verdict"])
    print("\nTest Output:\n", result["test_stdout"])
    print("\nErrors:\n", result["test_stderr"])
