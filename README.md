# Advanced-Multiagent-Debugger
# Multi-Agent AI Debugging System using CrewAI + LangGraph

A production-style **multi-agent AI debugging framework** built with **CrewAI**, **LangGraph**, and **Ollama**.
This system simulates an autonomous software engineering workflow where multiple AI agents collaborate to:

* Analyze bugs
* Research root causes
* Generate fixes
* Create automated tests
* Execute validation pipelines
* Perform QA verification
* Iterate until the issue is resolved

Designed for learning **Agentic AI systems**, **LLM orchestration**, and **autonomous debugging workflows** using fully local LLMs.



---

# Features

* Multi-agent collaboration architecture
* Autonomous debugging workflow
* Local LLM inference using Ollama
* LangGraph state-machine orchestration
* Automated pytest execution
* Self-correcting iterative loop
* Structured JSON communication between agents
* Temporary sandbox execution environment
* Production-style QA validation
* Retry mechanism for failed fixes

---

# Architecture

The system uses a graph-based workflow powered by LangGraph.

```text
            ┌─────────────┐
            │ Research AI │
            └──────┬──────┘
                   │
                   ▼
            ┌─────────────┐
            │ Debug AI    │
            └──────┬──────┘
                   │
                   ▼
            ┌─────────────┐
            │ Test Runner │
            └──────┬──────┘
                   │
                   ▼
            ┌─────────────┐
            │ QA Validator│
            └──────┬──────┘
                   │
        PASS ──────┘
                   │
                 FAIL
                   │
                   ▼
              Retry Loop
```

---

# Tech Stack

| Technology    | Purpose                   |
| ------------- | ------------------------- |
| Python        | Core programming language |
| CrewAI        | Multi-agent collaboration |
| LangGraph     | Workflow orchestration    |
| Ollama        | Local LLM serving         |
| Mistral / Phi | Language models           |
| Pytest        | Automated testing         |
| Subprocess    | Sandbox execution         |

---

# Workflow Overview

## 1. Research Agent

The **Research Engineer Agent** analyzes the bug report and identifies:

* Possible root causes
* Concurrency issues
* Scaling problems
* Fixing strategies

Example output:

```json
{
  "root_causes": [
    "Race condition in shared cache",
    "Improper thread synchronization"
  ],
  "strategy": "Remove shared mutable state and implement thread-safe logic"
}
```

---

## 2. Debug Agent

The **Senior Debug Engineer Agent**:

* Generates production-safe Python fixes
* Removes unsafe global state
* Creates pytest test cases
* Returns structured JSON outputs

Example:

```json
{
  "module_code": "FULL PYTHON CODE",
  "tests": "PYTEST CODE"
}
```

---

## 3. Execution Engine

The framework:

* Creates temporary execution directories
* Writes generated code dynamically
* Runs pytest automatically
* Captures stdout/stderr logs
* Detects execution failures

---

## 4. QA Validation

The QA node validates:

* Test pass/fail status
* Runtime errors
* Unsafe patterns
* Global state usage

If validation fails, the workflow loops back for another iteration.

---

# Project Structure

```text
project/
│
├── main.py
├── README.md
│
├── Agents
│   ├── Research Agent
│   └── Debug Agent
│
├── LangGraph Workflow
│
├── Execution Sandbox
│
└── Pytest Validation
```

---

# Installation

## 1. Clone Repository

```bash
git clone <your-repo-url>
cd multi-agent-debugger
```

---

## 2. Install Dependencies

```bash
pip install crewai langgraph pytest
```

---

## 3. Install Ollama

Download Ollama from:

[Ollama Official Website](https://ollama.com/?utm_source=chatgpt.com)

---

## 4. Pull Model

```bash
ollama pull mistral
```

Or:

```bash
ollama pull phi
```

---

# Running the Project

Start Ollama locally:

```bash
ollama serve
```

Then run:

```bash
python main.py
```

---

# Example Bug Input

```python
"API returns 500 error under concurrent requests"
```

---

# Example Output

```text
===== FINAL RESULT =====

Verdict: PASS

Test Output:
3 passed in 0.42s
```

---

# Key Concepts Demonstrated

## Agentic AI

The project demonstrates how multiple autonomous agents collaborate to solve engineering problems.

## AI Software Engineering

Simulates a real-world AI-assisted debugging pipeline.

## LangGraph State Management

Shows how graph-based orchestration can manage complex workflows.

## Self-Healing Systems

The retry loop enables iterative self-correction until tests pass.

## Local LLM Infrastructure

Uses Ollama for fully offline/private inference.

---

# Future Improvements

* Docker sandbox execution
* Multi-file code generation
* Memory-enhanced debugging
* Vector database integration
* RAG-powered bug analysis
* Human-in-the-loop approval
* CI/CD integration
* GitHub issue ingestion
* Parallel agent execution
* Observability dashboards

---

# Learning Outcomes

This project helps developers understand:

* Multi-agent orchestration
* Agentic AI systems
* LangGraph workflows
* AI-powered debugging
* Autonomous testing systems
* LLM structured outputs
* Local LLM deployment
* Production AI pipelines

---

# Use Cases

* AI-powered debugging assistants
* Autonomous DevOps systems
* Software reliability engineering
* Intelligent QA automation
* Self-healing backend systems
* AI engineering portfolio projects

---

# Author

Built for experimenting with:

* Agentic AI
* Multi-agent systems
* AI software engineering
* Autonomous debugging pipelines

---

