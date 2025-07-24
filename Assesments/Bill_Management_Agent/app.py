import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import tempfile
import json
import google.generativeai as genai
from autogen.agentchat import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager

# --- ENVIRONMENT & MODEL SETUP ---
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)
vision_model = genai.GenerativeModel("models/gemini-1.5-flash")

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="🧾 Smart Bill Analyzer", layout="wide")
st.markdown("""
    <style>
    .header { font-size: 24px; font-weight: bold; }
    .bubble { border-radius: 12px; background: #f9fbe7; padding: 14px; margin: 8px 0; }
    .user-msg { background: #e3f2fd; }
    .ai-msg { background: #fce4ec; }
    </style>
""", unsafe_allow_html=True)

st.title("🧮 Smart Bill Analyzer")
st.markdown("Upload a bill image and let AI break down your spending by category.")

# --- FILE UPLOAD ---
bill_image = st.file_uploader("Upload your bill image (jpg, png)", type=["jpg", "jpeg", "png"])

dialogue = []

# --- IMAGE TO EXPENSES ---
def extract_expenses_from_image(img_file):
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp.write(img_file.read())
        temp_path = temp.name
    img = Image.open(temp_path)
    prompt = (
        "Scan this bill image and extract all expenses. "
        "Organize them into: Groceries, Food, Utilities, Shopping, Entertainment, Miscellaneous. "
        "Return a JSON object: {category: [{item, cost}]}. Only output JSON."
    )
    result = vision_model.generate_content([prompt, img])
    try:
        raw = result.text.strip()
        start, end = raw.find("{"), raw.rfind("}") + 1
        parsed = json.loads(raw[start:end])
        return parsed, raw
    except Exception:
        return None, raw

# --- EXPENSE SUMMARY ---
def expense_overview(expense_dict):
    prompt = (
        f"Given these categorized expenses: {expense_dict}, "
        "calculate the total, show each category's sum, and highlight the largest category with a possible reason."
    )
    result = vision_model.generate_content(prompt)
    return result.text.strip()

# --- AGENT DEFINITIONS ---
customer_agent = UserProxyAgent(
    name="Customer",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False},
    llm_config=False
)

categorizer_agent = AssistantAgent(
    name="ExpenseCategorizer",
    llm_config=False,
    system_message="You extract and organize expenses from bills into categories."
)

insight_agent = AssistantAgent(
    name="InsightGenerator",
    llm_config=False,
    system_message="You analyze categorized expenses and generate summaries."
)

chat_group = GroupChat(agents=[customer_agent, categorizer_agent, insight_agent])
chat_manager = GroupChatManager(groupchat=chat_group)

# --- MAIN LOGIC ---
if bill_image:
    st.success("Bill received. Analyzing...")

    with st.spinner("Extracting details from your bill..."):
        expenses, ai_raw = extract_expenses_from_image(bill_image)

    if not expenses:
        st.error("Could not parse expenses from the image.")
        st.text(ai_raw)
    else:
        # Simulate agent workflow with new logic
        customer_agent.send("Bill image uploaded for analysis.", chat_manager)
        dialogue.append(("Customer → chat_manager", "Bill image uploaded for analysis."))

        customer_agent.send(f"Expenses extracted: {expenses}", categorizer_agent)
        dialogue.append(("Customer → ExpenseCategorizer", json.dumps(expenses, indent=2)))

        categorizer_reply = "Expenses have been sorted into their respective categories."
        dialogue.append(("ExpenseCategorizer", categorizer_reply))

        customer_agent.send("Please provide a summary of these expenses.", insight_agent)
        dialogue.append(("Customer → InsightGenerator", "Please provide a summary of these expenses."))

        with st.spinner("Summarizing your spending..."):
            summary_text = expense_overview(expenses)

        dialogue.append(("InsightGenerator", summary_text))

        # --- DISPLAY RESULTS ---
        st.markdown("## 🗂️ Expense Breakdown")
        for cat, items in expenses.items():
            if items:
                st.markdown(f"### {cat}")
                for entry in items:
                    st.markdown(f"- **{entry['item']}**: ₹{entry['cost']}")

        st.markdown("---")
        st.markdown("## 📊 Expense Summary")
        st.markdown(f"<div class='bubble ai-msg'>{summary_text}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("## 💬 Agent Dialogue")
        for sender, msg in dialogue:
            style = "user-msg" if "Customer" in sender else "ai-msg"
            st.markdown(f"<div class='bubble {style}'><strong>{sender}</strong>: {msg}</div>", unsafe_allow_html=True)