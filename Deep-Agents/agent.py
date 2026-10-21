
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from tavily import TavilyClient

from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver

from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from deepagents.backends.utils import create_file_data


# --------------------------------------------------
# 1. Environment configuration
# --------------------------------------------------

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
SKILLS_DIR = BASE_DIR / "skills"

groq_api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not groq_api_key:
    raise ValueError(
        "GROQ_API_KEY is missing from your .env file."
    )

if not tavily_api_key:
    raise ValueError(
        "TAVILY_API_KEY is missing from your .env file."
    )


# --------------------------------------------------
# 2. Initialize Groq model
# --------------------------------------------------

model = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=groq_api_key,
    temperature=0.2,
)


# --------------------------------------------------
# 3. Initialize Tavily search
# --------------------------------------------------

tavily_client = TavilyClient(api_key=tavily_api_key)


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
) -> dict:
    """Search the internet and return results with source URLs."""

    return tavily_client.search(
        query=query,
        max_results=max_results,
        topic=topic,
        include_raw_content=False,
    )


# --------------------------------------------------
# 4. Define research subagent
# --------------------------------------------------
# IMPORTANT:
# Do not set response_format=ResearchFinding here.
# This subagent uses tools, and the JSON response mode
# caused the Groq 400 error in your original code.

research_subagent = {
    "name": "research-agent",
    "description": (
        "Research current or complex topics using internet search. "
        "Use for technical research, comparisons, fact-checking, "
        "and evidence gathering."
    ),
    "system_prompt": """
You are a careful technical research analyst.

Instructions:
1. Search the web before answering research questions.
2. Use multiple relevant sources when practical.
3. Distinguish verified information from assumptions.
4. Never invent sources, URLs, benchmarks, or statistics.
5. Summarize findings clearly and concisely.
6. Include source URLs that actually appear in search results.
7. Explain conflicting evidence or important limitations.
8. Give a subjective confidence score from 0 to 1.

Use this structure for your final answer:

## Summary
Present the evidence-based findings.

## Confidence
Provide a score between 0 and 1 and explain uncertainty.

## Sources
List the source URLs used to support the findings.
""",
    "tools": [internet_search],
    "model": model,
}


# --------------------------------------------------
# 5. Load skills
# --------------------------------------------------

def load_skills() -> dict:
    """Load skill Markdown files into the virtual file state."""

    skill_names = [
        "langgraph",
        "python",
        "aws",
        "report-generator",
    ]

    skill_files = {}

    for skill_name in skill_names:
        skill_path = SKILLS_DIR / skill_name / "SKILL.md"

        if not skill_path.is_file():
            raise FileNotFoundError(
                f"Missing skill file: {skill_path}\n"
                "Check the skills directory and folder names."
            )

        virtual_path = f"/skills/{skill_name}/SKILL.md"

        content = skill_path.read_text(encoding="utf-8")

        skill_files[virtual_path] = create_file_data(content)

    return skill_files


# --------------------------------------------------
# 6. Build the main DeepAgent
# --------------------------------------------------

def build_agent():
    """Create the main skills-aware agent."""

    agent = create_deep_agent(
        model=model,
        backend=StateBackend(),
        skills=["/skills/"],
        tools=[internet_search],
        subagents=[research_subagent],
        checkpointer=MemorySaver(),
        system_prompt="""
You are DeepAgent Studio, a helpful technical AI assistant.

Your capabilities:
- Python programming, debugging, and automation.
- LangGraph workflows and multi-agent systems.
- AWS and cloud infrastructure concepts.
- Technical research using internet search.
- Technical report writing with source citations.

Operating rules:
1. Use relevant skills when answering technical questions.
2. Delegate complex or current research to research-agent.
3. Use internet search when current facts need verification.
4. Cite source URLs for claims based on web research.
5. Distinguish facts, assumptions, and recommendations.
6. Never invent citations, statistics, or source URLs.
7. Do not claim that a file was created or a task completed
   unless the operation actually succeeded.
8. If information is uncertain, explain the limitation.
""",
    )

    return agent


# --------------------------------------------------
# 7. Run the agent
# --------------------------------------------------

def run_agent(agent, question: str, thread_id: str) -> str:
    """Run a question and return the final assistant response."""

    if not question or not question.strip():
        return "Please enter a question."

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question.strip(),
                }
            ],
            "files": load_skills(),
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    messages = result.get("messages", [])

    # Return the latest assistant message.
    for message in reversed(messages):
        if getattr(message, "type", None) == "ai":
            content = message.content

            if isinstance(content, str):
                return content

            return str(content)

    return "The agent completed without returning an assistant response."


# --------------------------------------------------
# 8. Local smoke test
# --------------------------------------------------

if __name__ == "__main__":
    print("Loading skills...")

    skills = load_skills()
    print(f"Loaded {len(skills)} skill files:")
    for skill_path in skills:
        print(f" - {skill_path}")

    print("\nBuilding DeepAgent...")
    agent = build_agent()

    print("\nDeepAgent is ready. Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            answer = run_agent(
                agent=agent,
                question=question,
                thread_id="local-test",
            )
            print(f"\nAssistant:\n{answer}\n")

        except Exception as exc:
            print(f"\nAgent error: {exc}\n")
