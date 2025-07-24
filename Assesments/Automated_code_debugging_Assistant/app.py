import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import ast
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# --- Pure Python Static Inspector ---
def static_code_inspector(source: str) -> str:
    """Inspects Python code for common static issues."""
    try:
        parsed = ast.parse(source)
        findings = []

        # Discourage print usage
        for node in ast.walk(parsed):
            if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "print":
                findings.append("⚠️ Detected `print()` usage. Consider using logging.")

        # Warn on generic except
        for node in ast.walk(parsed):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                findings.append("⚠️ Found a bare `except:`. Specify the exception type.")

        # Add more checks as needed...

        if findings:
            return "Static Inspector Report:\n" + "\n".join(findings)
        return "✅ Inspector: No static issues detected."
    except SyntaxError as err:
        return f"❌ Inspector: Syntax error at line {err.lineno}: {err.msg}"

# --- LLM Setup ---
llm_engine = LLM(
    api_key=GEMINI_KEY,
    model="gemini/gemini-2.5-flash"
)

# --- Agents ---
inspector_bot = Agent(
    role="Static Inspector",
    goal="Spot static code issues without running the code",
    backstory="A vigilant code reviewer with a keen eye for static bugs.",
    llm=llm_engine,
    verbose=True
)

refactor_bot = Agent(
    role="Code Refactorer",
    goal="Revise code to resolve static issues, preserving intent",
    backstory="A Python stylist who crafts clean, robust code.",
    llm=llm_engine,
    verbose=True
)

overseer_bot = Agent(
    role="Review Overseer",
    goal="Oversee the inspection and refactoring process",
    backstory="Ensures all code reviews and fixes are coordinated smoothly.",
    llm=llm_engine,
    verbose=True
)

# --- Streamlit UI ---
st.title("🛠️ Python Static Inspector & Refactorer")
user_code = st.text_area("Paste your Python code here:", height=300)

if st.button("Run Inspection & Refactor"):
    if not user_code.strip():
        st.info("Please provide some Python code to analyze.")
    else:
        with st.spinner("Running static inspection..."):
            # Task 1: Inspection
            inspect_task = Task(
                description=f"Perform a static review of the following code. List any issues or anti-patterns you find:\n\n```python\n{user_code}\n```",
                agent=inspector_bot,
                expected_output="A concise list of static code issues."
            )

            # Task 2: Refactoring
            refactor_task = Task(
                description="Revise the code to address all issues found in the inspection. Maintain the original logic and add brief comments explaining each fix.",
                agent=refactor_bot,
                expected_output="A corrected version of the code with inline explanations.",
                context=[inspect_task]
            )

            # CrewAI Orchestration
            review_crew = Crew(
                agents=[inspector_bot, refactor_bot, overseer_bot],
                tasks=[inspect_task, refactor_task],
                verbose=True,
                process=Process.sequential
            )

            outcome = review_crew.kickoff()

            st.subheader("🧹 Refactored Code")
            st.code(outcome, language="python")