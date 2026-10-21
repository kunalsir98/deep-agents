# AGENTS.md

## DeepAgents Architecture Guide

This document defines the architecture, conventions, responsibilities, and development guidelines for this DeepAgents-based project.

The goal is to build a modular, reliable, and extensible agent system where a main agent can reason about tasks, use tools, delegate complex work to subagents, maintain context, and produce structured results.

---

## 1. Architecture Overview

The application follows a hierarchical agent architecture:

```text
                         ┌──────────────────────┐
                         │       User           │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Main / Root Agent │
                         │     Orchestrator     │
                         └──────────┬───────────┘
                                    │
               ┌────────────────────┼────────────────────┐
               │                    │                    │
               ▼                    ▼                    ▼
       ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
       │   Research   │     │    Coding    │     │   Analysis   │
       │   Subagent   │     │   Subagent   │     │   Subagent   │
       └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
              │                    │                    │
              ▼                    ▼                    ▼
       ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
       │ Search Tools │     │ File / Shell │     │ Data Tools   │
       │ Web Tools    │     │ Code Tools   │     │ Python Tools │
       └──────────────┘     └──────────────┘     └──────────────┘

                         ┌──────────────────────┐
                         │ Memory / Filesystem  │
                         │   Shared Context     │
                         └──────────────────────┘
```

The Root Agent is responsible for orchestration.

Subagents should be used when a task requires specialized reasoning or independent execution.

---

# 2. Core Principles

Follow these principles when developing the agent system.

### 2.1 Separation of Responsibilities

Each agent should have one clear responsibility.

Bad:

```text
One agent handles research + coding + data analysis + deployment.
```

Preferred:

```text
Root Agent
 ├── Research Agent
 ├── Coding Agent
 ├── Analysis Agent
 └── Documentation Agent
```

---

### 2.2 Tool-Driven Architecture

Agents should interact with external systems through tools rather than directly embedding implementation logic into prompts.

Example:

```text
Agent
  │
  ├── search_web()
  ├── read_file()
  ├── write_file()
  ├── execute_python()
  └── run_command()
```

Tools should have:

* Clear names
* Clear descriptions
* Validated inputs
* Predictable outputs
* Minimal side effects

---

### 2.3 Delegate Complex Tasks

The Root Agent should delegate work when:

* The task is large.
* Multiple independent tasks exist.
* Specialized expertise is required.
* Research and implementation can happen independently.
* A subtask requires many tool calls.

Example:

```text
User:
"Research LangGraph and build a working RAG application."

Root Agent:
    ↓
Research Agent
    ↓
Research findings
    ↓
Coding Agent
    ↓
Application
    ↓
Root Agent
    ↓
Final response
```

---

# 3. Recommended Project Structure

Use the following structure for a typical DeepAgents project:

```text
deepagents-project/
│
├── AGENTS.md
├── README.md
├── .env
├── .gitignore
├── requirements.txt
│
├── app/
│   ├── __init__.py
│   │
│   ├── main.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── root_agent.py
│   │   ├── research_agent.py
│   │   ├── coding_agent.py
│   │   ├── analysis_agent.py
│   │   └── documentation_agent.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── web_tools.py
│   │   ├── file_tools.py
│   │   ├── code_tools.py
│   │   └── database_tools.py
│   │
│   ├── prompts/
│   │   ├── root_prompt.py
│   │   ├── research_prompt.py
│   │   └── coding_prompt.py
│   │
│   ├── state/
│   │   ├── __init__.py
│   │   └── agent_state.py
│   │
│   └── config/
│       ├── __init__.py
│       └── settings.py
│
├── workspace/
│   ├── input/
│   ├── output/
│   └── temporary/
│
└── tests/
    ├── test_agents.py
    ├── test_tools.py
    └── test_workflows.py
```

---

# 4. Root Agent

The Root Agent is the main orchestrator.

Its responsibilities are:

1. Understand the user's request.
2. Break the request into subtasks.
3. Decide whether tools are required.
4. Decide whether subagents are required.
5. Delegate tasks.
6. Track progress.
7. Validate results.
8. Return the final response.

The Root Agent should NOT perform every task itself.

Conceptually:

```python
root_agent
    |
    ├── Understand task
    |
    ├── Create plan
    |
    ├── Delegate
    |      ├── Research Agent
    |      ├── Codin
```
