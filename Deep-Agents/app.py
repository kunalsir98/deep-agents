
import uuid
import streamlit as st

from agent import build_agent, run_agent

st.set_page_config(
    page_title="DeepAgent Studio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp {
    background: #0b1020;
    color: #edf2ff;
}
[data-testid="stSidebar"] {
    background: #11182b;
    border-right: 1px solid #293450;
}
.hero {
    padding: 26px;
    border: 1px solid #35416a;
    border-radius: 18px;
    background: linear-gradient(120deg, #171f3c, #22214a, #172c43);
    margin-bottom: 24px;
}
.hero h1 {
    font-size: 38px;
    margin-bottom: 8px;
}
.hero p {
    color: #c4cce5;
    font-size: 16px;
}
div[data-testid="stChatMessage"] {
    border: 1px solid #28344f;
    border-radius: 14px;
    padding: 12px;
    background: #11182b;
}
.stButton button {
    border-radius: 10px;
    border: 1px solid #5669a7;
}
</style>
""", unsafe_allow_html=True)

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "history" not in st.session_state:
    st.session_state.history = []

if "agent" not in st.session_state:
    st.session_state.agent = None

st.markdown("""
<div class="hero">
    <h1>🧠 DeepAgent Studio</h1>
    <p>
        A skills-aware AI assistant with delegated web research,
        structured findings, and technical knowledge workflows.
    </p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ Workspace")
    mode = st.radio(
        "Choose a workflow",
        ["Research", "Skills Assistant", "Technical Report"],
    )

    st.divider()
    st.markdown("### Agent capabilities")
    st.markdown("""
    - 🔎 Tavily web research
    - 🧩 Specialized research subagent
    - 📚 Markdown skill library
    - 🧱 Pydantic structured findings
    - 💬 Thread-based conversation memory
    """)

    st.divider()
    st.caption("Model: Groq · GPT-OSS 20B")
    st.caption("Orchestration: DeepAgents")

    if st.button("🗑️ New conversation", use_container_width=True):
        st.session_state.history = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Workflows", "3")

with col2:
    st.metric("Skill libraries", "4")

with col3:
    st.metric("Research tools", "Tavily")

st.subheader(f"💬 {mode}")

examples = {
    "Research": (
        "Research the leading open-source LLM gateways, "
        "compare their features, and provide sources."
    ),
    "Skills Assistant": (
        "Explain LangGraph conditional routing with a "
        "working Python example."
    ),
    "Technical Report": (
        "Create a structured technical report explaining "
        "how to deploy a FastAPI application on AWS EC2."
    ),
}

with st.expander("💡 Try an example"):
    st.write(examples[mode])

for item in st.session_state.history:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

prompt = st.chat_input(
    "Ask a research or technical question..."
)

if prompt:
    st.session_state.history.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    if mode == "Research":
        question = (
            "Research task: investigate the following question using "
            "the research-agent and web search. Present a detailed "
            "summary, important findings, an estimated confidence "
            "score, and clickable source URLs. Clearly identify "
            "uncertainty. Question: " + prompt
        )
    elif mode == "Skills Assistant":
        question = (
            "Technical skills task: use the relevant Markdown skill "
            "and provide a clear explanation, practical steps, and "
            "a code example where appropriate. Question: " + prompt
        )
    else:
        question = (
            "Technical report task: produce a well-structured report "
            "with an executive summary, technical approach, "
            "implementation steps, limitations, and sources when "
            "web research is used. Question: " + prompt
        )

    with st.chat_message("assistant"):
        try:
            with st.spinner("DeepAgent is working..."):
                if st.session_state.agent is None:
                    st.session_state.agent = build_agent()

                answer = run_agent(
                    st.session_state.agent,
                    question,
                    st.session_state.thread_id,
                )

            st.markdown(answer)

            st.session_state.history.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as exc:
            st.error(f"Agent error: {exc}")
            st.info(
                "Check your API keys, installed package versions, "
                "skill files, and DeepAgents configuration."
            )

st.divider()
st.caption(
    "DeepAgent Studio · Research responsibly and verify important claims."
)
