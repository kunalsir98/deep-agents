---
name: langgraph
description: Build LangGraph workflows with state management, conditional routing, tools, and multi-agent orchestration.
---

# LangGraph Skill

## Purpose
Help build reliable stateful applications and multi-agent workflows.

## Core concepts
- Define state using TypedDict or MessagesState.
- Build workflows using StateGraph.
- Connect nodes using add_node and add_edge.
- Implement conditional routing with add_conditional_edges.
- Compile graphs before invoking or streaming.
- Use checkpointers with thread_id for conversation memory.

## Best practices
- Keep node responsibilities focused.
- Define clear routing conditions.
- Handle errors and tool failures.
- Use ToolNode and tools_condition when appropriate.
- Explain state transitions with practical examples.
