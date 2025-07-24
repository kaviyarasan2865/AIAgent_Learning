# competitor_intel_dashboard.py
import streamlit as st
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict, Callable
import copy

# --- Streamlit UI Setup ---
st.set_page_config(
    page_title="Retail Competitor Radar",
    page_icon="🧵",
    layout="centered"
)

def gemini_response_factory(api_key: str) -> Callable:
    """Returns a function that generates Gemini LLM responses for agent messages."""
    def responder(messages: List[Dict], **kwargs) -> str:
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.25,
                max_output_tokens=2048
            )
            chat_history = []
            for m in messages:
                if m["role"] == "user":
                    chat_history.append(HumanMessage(content=m["content"]))
                else:
                    chat_history.append(AIMessage(content=m["content"]))
            reply = llm.invoke(chat_history)
            return reply.content
        except Exception as exc:
            return f"LLM error: {exc}"
    return responder

def build_llm_config(api_key: str, with_functions=True) -> Dict:
    config = {
        "config_list": [{
            "model": "gemini-1.5-flash",
            "api_type": "google",
            "api_key": api_key,
        }],
        "timeout": 600
    }
    if with_functions:
        config["functions"] = [gemini_response_factory(api_key)]
    return config

def competitor_intel_app():
    st.title("🧵 Retail Competitor Radar")
    st.caption("Multi-agent market intelligence for clothing stores (Gemini 1.5 Flash)")

    with st.sidebar:
        st.header("Setup")
        api_key = st.text_input("Gemini API Key", type="password", value="")
        area = st.text_input("Target Area", "Indiranagar, Bangalore")
        n_competitors = st.slider("How many competitors?", 3, 10, 4)
        report_depth = st.radio("Report Depth", ["Quick", "Standard", "In-depth"])
        run_btn = st.button("Run Market Scan", type="primary")

    if run_btn:
        if not api_key:
            st.error("Gemini API key required.")
            return

        with st.spinner("Agents are gathering competitive insights..."):
            try:
                base_config = build_llm_config(api_key, with_functions=True)
                mgr_config = build_llm_config(api_key, with_functions=False)

                # --- Agent Definitions ---
                scout_agent = AssistantAgent(
                    name="Scout",
                    llm_config=copy.deepcopy(base_config),
                    system_message=(
                        f"You are a local retail scout. List the top {n_competitors} clothing stores in {area}."
                        " For each, note their style (luxury, value, trendy, etc.), and estimate their busiest hours."
                        f" Keep it concise. Report depth: {report_depth}."
                    )
                )

                analyst_agent = AssistantAgent(
                    name="Analyst",
                    llm_config=copy.deepcopy(base_config),
                    system_message=(
                        "You are a market analyst. Using the Scout's findings, compare pricing, product variety, and customer appeal."
                        " Identify any market gaps or unique selling points. Suggest one opportunity for a new entrant."
                    )
                )

                advisor_agent = AssistantAgent(
                    name="Advisor",
                    llm_config=copy.deepcopy(base_config),
                    system_message=(
                        "You are a business advisor. Based on the Analyst's review, recommend:"
                        " - Best opening hours"
                        " - Promotional timing"
                        " - Differentiation tactics"
                        " Format as actionable bullet points."
                    )
                )

                summary_agent = AssistantAgent(
                    name="SummaryWriter",
                    llm_config=copy.deepcopy(base_config),
                    system_message=(
                        f"Summarize the findings into a markdown business report for {area}."
                        " Include: 1) Competitor Table, 2) Market Gaps, 3) Actionable Advice, 4) Executive Summary."
                        f" Use {report_depth.lower()} detail. Format for easy reading."
                    )
                )

                user_agent = UserProxyAgent(
                    name="Retailer",
                    human_input_mode="NEVER",
                    code_execution_config=False,
                    max_consecutive_auto_reply=2,
                    default_auto_reply="Continue with the next step."
                )

                # --- Group Chat Setup ---
                chat = GroupChat(
                    agents=[user_agent, scout_agent, analyst_agent, advisor_agent, summary_agent],
                    messages=[],
                    max_round=7,
                    speaker_selection_method="round_robin"
                )
                chat_mgr = GroupChatManager(groupchat=chat, llm_config=mgr_config)

                # --- Start the Agent Workflow ---
                user_agent.initiate_chat(
                    chat_mgr,
                    message=(
                        f"Please generate a {report_depth.lower()} competitor intelligence report for clothing stores in {area}."
                        f" Focus on {n_competitors} competitors. Include actionable insights for a new business."
                    )
                )

                # --- Display Results ---
                st.success("Market scan complete!")
                st.markdown("---")

                # Find the summary report
                report = None
                for msg in reversed(chat.messages):
                    if msg["name"] == "SummaryWriter" and "Competitor Table" in msg.get("content", ""):
                        report = msg["content"]
                        break

                if report:
                    st.markdown(report)
                    st.download_button(
                        label="Download Report",
                        data=report,
                        file_name=f"retail_competitor_radar_{area.replace(' ', '_')}.md",
                        mime="text/markdown"
                    )
                else:
                    st.warning("No summary found. Showing agent conversation:")
                    for msg in chat.messages:
                        st.write(f"**{msg['name']}:**")
                        st.markdown(msg["content"])
                        st.markdown("---")
            except Exception as exc:
                st.error(f"Error during analysis: {exc}")
                st.info("Check your API key and try again.")

if __name__ == "__main__":
    competitor_intel_app()