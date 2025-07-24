import streamlit as st
import json
import autogen
from autogen import AssistantAgent, UserProxyAgent
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv('GOOGLE_API_KEY')
if not GEMINI_KEY:
    raise RuntimeError("Missing Gemini API key.")

GEMINI_CONFIG = [{
    "model": "gemini-2.5-flash",
    "api_key": GEMINI_KEY,
    "api_type": "google"
}]

st.title("🪙 Smart Wealth Insights")
st.markdown("Let AI craft your custom investment roadmap.")

with st.form("wealth_form"):
    income = st.text_input("Yearly Income (₹)", placeholder="1500000")
    user_age = st.number_input("Age", min_value=18, max_value=100, step=1)
    yearly_spend = st.text_input("Yearly Spending (₹)", placeholder="600000")
    aspirations = st.text_area("Aspirations", placeholder="Early retirement, world travel, home purchase")
    risk_pref = st.selectbox("Risk Appetite", ["Low", "Medium", "High"])

    st.subheader("💰 Asset Breakdown")
    mf_holdings = st.text_area("Mutual Funds (Name, Category, Value)", placeholder="HDFC Flexi Cap - Equity - ₹3L")
    equity_holdings = st.text_area("Stocks (Name, Qty, Buy Price)", placeholder="TCS - 8 shares - ₹3500")
    property_assets = st.text_area("Real Estate (Type, City, Value)", placeholder="Villa - Pune - ₹20L")
    fd_total = st.text_input("Fixed Deposits (₹)", placeholder="400000")

    trigger = st.form_submit_button("Get My Report")

# --- AGENT DEFINITIONS ---

profile_evaluator = AssistantAgent(
    name="ProfileEvaluator",
    llm_config={"config_list": GEMINI_CONFIG},
    system_message="""
    Review the user's financial snapshot and classify their investment orientation as either "Expansion" or "Preservation".
    Respond strictly in JSON: {"orientation": "Expansion" or "Preservation", "justification": "short reason"}
    """
)

expansion_recommender = AssistantAgent(
    name="ExpansionRecommender",
    llm_config={"config_list": GEMINI_CONFIG},
    system_message="""
    For users seeking growth, suggest dynamic assets: emerging market funds, innovative tech stocks, or digital assets.
    Reply in JSON: {"ideas": ["suggestion1", "suggestion2", ...], "why": "short rationale"}
    """
)

preservation_recommender = AssistantAgent(
    name="PreservationRecommender",
    llm_config={"config_list": GEMINI_CONFIG},
    system_message="""
    For users prioritizing safety, recommend: government bonds, blue-chip equities, or secure deposits.
    Reply in JSON: {"ideas": ["suggestion1", "suggestion2", ...], "why": "short rationale"}
    """
)

report_compiler = AssistantAgent(
    name="ReportCompiler",
    llm_config={"config_list": GEMINI_CONFIG},
    system_message="""
    Assemble a detailed investment report with:
    - Overview of user's finances
    - Chosen investment orientation
    - Tailored asset suggestions
    - Step-by-step action plan
    - Risk considerations
    Format in Markdown. End with "END-OF-REPORT".
    """
)

user_agent = UserProxyAgent(
    name="UserAgent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x: "END-OF-REPORT" in x.get("content", ""),
    code_execution_config=False
)

def parse_orientation(json_str):
    try:
        obj = json.loads(json_str.strip())
        return obj.get("orientation", "Expansion")
    except Exception:
        return "Expansion"

def build_user_profile():
    return f"""
Profile:
- Age: {user_age}
- Income: ₹{income}
- Spending: ₹{yearly_spend}
- Risk Appetite: {risk_pref}
- Aspirations: {aspirations}

Assets:
- Mutual Funds: {mf_holdings or 'None'}
- Stocks: {equity_holdings or 'None'}
- Real Estate: {property_assets or 'None'}
- Fixed Deposits: ₹{fd_total or '0'}
"""

def generate_wealth_report():
    profile_text = build_user_profile()

    # 1. Evaluate profile for investment orientation
    orientation_result = user_agent.initiate_chat(
        profile_evaluator,
        message=profile_text,
        summary_method="last_msg",
        silent=True
    )
    orientation_json = orientation_result.chat_history[-1]["content"]
    orientation = parse_orientation(orientation_json)

    # 2. Get asset suggestions
    recommender = expansion_recommender if orientation == "Expansion" else preservation_recommender
    ideas_result = user_agent.initiate_chat(
        recommender,
        message=f"{profile_text}\nOrientation: {orientation}",
        summary_method="last_msg",
        silent=True
    )
    ideas_json = ideas_result.chat_history[-1]["content"]

    # 3. Compile the final report
    report_result = user_agent.initiate_chat(
        report_compiler,
        message=f"""
User Profile:
{profile_text}

Orientation Analysis:
{orientation_json}

Asset Suggestions:
{ideas_json}

Sections to include:
- Financial Overview
- Investment Orientation
- Asset Suggestions
- Action Plan
- Risk Review
""",
        summary_method="last_msg",
        silent=True
    )
    report_md = report_result.chat_history[-1]["content"]
    if "END-OF-REPORT" in report_md:
        return report_md.split("END-OF-REPORT")[0].strip()
    return report_md

# --- UI OUTPUT ---
if trigger:
    with st.spinner("🔎 Reviewing your finances... Please wait a moment."):
        try:
            output = generate_wealth_report()
            st.subheader("📈 Your Wealth Strategy Report")
            st.markdown(output)
        except Exception as err:
            st.error(f"Could not generate report: {str(err)}")
            st.info("Please review your entries and try again. If issues persist, simplify your inputs.")