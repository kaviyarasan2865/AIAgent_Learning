import os
import pandas as pd
import streamlit as st
import google.generativeai as genai
from autogen.agentchat import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY in environment.")

genai.configure(api_key=GEMINI_API_KEY)

def gemini_respond(prompt, model="models/gemini-1.5-flash"):
    return genai.GenerativeModel(model).generate_content(prompt).text

# === Custom Agent Definitions ===
class CleanerAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        df = st.session_state["dataset"]
        prompt = (
            "Act as a Data Cleaning Specialist.\n"
            "- Identify and handle missing values\n"
            "- Correct data types\n"
            "- Remove duplicates\n"
            f"Sample data:\n{df.head().to_string()}\n"
            f"Stats:\n{df.describe(include='all').to_string()}\n"
            "Provide Python code for cleaning and a brief rationale."
        )
        return gemini_respond(prompt)

class ExplorerAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        df = st.session_state["dataset"]
        prompt = (
            "You are an Exploratory Data Analyst.\n"
            "- Summarize the dataset\n"
            "- Extract at least three interesting insights\n"
            "- Recommend visualizations\n"
            f"Sample data:\n{df.head().to_string()}"
        )
        return gemini_respond(prompt)

class SummaryAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        findings = st.session_state.get("explore_output", "")
        prompt = (
            "You are a Data Summary Writer.\n"
            "Draft a concise EDA report using these insights:\n"
            f"{findings}\n"
            "Include:\n"
            "- Overview\n"
            "- Main Discoveries\n"
            "- Visualization Ideas\n"
            "- Final Thoughts"
        )
        return gemini_respond(prompt)

class ReviewerAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        report = st.session_state.get("summary_output", "")
        prompt = (
            "You are a Data Report Reviewer.\n"
            "Evaluate the following EDA report for clarity, accuracy, and completeness. Suggest improvements.\n"
            f"{report}"
        )
        return gemini_respond(prompt)

class CodeVerifierAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        code = st.session_state.get("clean_output", "")
        prompt = (
            "You are a Python Code Validator.\n"
            "Check if this data cleaning code is executable and correct. Suggest fixes if needed.\n"
            f"{code}"
        )
        return gemini_respond(prompt)

# === Admin Proxy Agent ===
orchestrator = UserProxyAgent(
    name="Orchestrator",
    human_input_mode="NEVER",
    code_execution_config=False
)

# === Streamlit UI ===
st.set_page_config(layout="wide")
st.title("📊 Gemini-Powered EDA Workflow")
st.markdown("Upload a CSV and let a team of agents analyze and critique your data step by step.")

uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.session_state["dataset"] = data
    st.subheader("🔎 Data Preview")
    st.dataframe(data.head())

    if st.button("Start EDA Agents"):
        with st.spinner("Booting up agents..."):
            agent_team = [
                orchestrator,
                CleanerAgent(name="Cleaner"),
                ExplorerAgent(name="Explorer"),
                SummaryAgent(name="Summarizer"),
                ReviewerAgent(name="Reviewer"),
                CodeVerifierAgent(name="Verifier"),
            ]
            chat_group = GroupChat(agents=agent_team, messages=[])
            group_mgr = GroupChatManager(groupchat=chat_group)

        with st.spinner("Agents are working through your data..."):
            # --- Data Cleaning ---
            clean_code = agent_team[1].generate_reply([], "Orchestrator")
            st.session_state["clean_output"] = clean_code
            with st.expander("🧹 Cleaning Code & Notes", expanded=True):
                st.code(clean_code, language="python")

            # --- EDA Insights ---
            explore = agent_team[2].generate_reply([], "Orchestrator")
            st.session_state["explore_output"] = explore
            with st.expander("📈 EDA Insights", expanded=True):
                st.markdown(explore)

            # --- Report Generation ---
            summary = agent_team[3].generate_reply([], "Orchestrator")
            st.session_state["summary_output"] = summary
            with st.expander("📝 EDA Report", expanded=True):
                st.markdown(summary)

            # --- Critique ---
            review = agent_team[4].generate_reply([], "Orchestrator")
            with st.expander("🧐 Report Review", expanded=False):
                st.markdown(review)

            # --- Code Validation ---
            verify = agent_team[5].generate_reply([], "Orchestrator")
            with st.expander("✅ Code Validation", expanded=False):
                st.markdown(verify)

        st.success("EDA pipeline finished! Review the outputs above.")
else:
    st.info("Please upload a CSV file to get started.")