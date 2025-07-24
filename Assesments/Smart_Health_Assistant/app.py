import streamlit as st
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import google.generativeai as genai

# Application Configuration
st.set_page_config(page_title="AI-Powered Wellness Advisory Platform", layout="wide")
st.title("🏃‍♀️ AI-Powered Wellness Advisory Platform")

with st.sidebar:
    st.header("System Configuration")
    google_api_token = st.text_input("Insert Gemini 1.5 Flash Authentication Token:", type="password")
    st.markdown("[Obtain Gemini Authentication Token](https://aistudio.google.com/app/apikey)")
    st.divider()
    st.caption("This platform performs body composition analysis, delivers wellness guidance, crafts nutritional blueprints, and designs fitness regimens tailored to your profile.")

#Application State Management
if "dialogue_history" not in st.session_state:
    st.session_state.dialogue_history = []
if "comprehensive_wellness_program" not in st.session_state:
    st.session_state.comprehensive_wellness_program = ""
if "agent_communications" not in st.session_state:
    st.session_state.agent_communications = []

#  AI Model Configuration Helper 
def configure_gemini_interface(authentication_token: str, ai_model: str = "gemini-1.5-flash"):
    return [{
        "model": ai_model,
        "api_key": authentication_token,
        "api_type": "google",
        "base_url": "https://generativelanguage.googleapis.com/v1beta"
    }]

#  Body Mass Index Computation Tool 
def compute_body_mass_index(body_weight_kg: float, body_height_cm: float) -> float:
    height_in_meters = body_height_cm / 100
    return round(body_weight_kg / (height_in_meters ** 2), 1)

#  User Profile Input Interface 
with st.form("wellness_profile_form"):
    input_col1, input_col2 = st.columns(2)
    with input_col1:
        body_weight = st.number_input("Body Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        body_height = st.number_input("Body Height (cm)", min_value=100, max_value=250, value=170)
        user_age = st.number_input("Age", min_value=18, max_value=100, value=30)
    with input_col2:
        biological_gender = st.selectbox("Biological Gender", ["Male", "Female", "Other"])
        nutrition_preference = st.selectbox("Nutritional Preference", ["Veg", "Non-Veg", "Vegan"])
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        generate_wellness_plan = st.form_submit_button("Create Wellness Strategy")

#  Specialized AI Agent Initialization 
def establish_wellness_agents(authentication_token):
    genai.configure(api_key=authentication_token)
    ai_configuration = configure_gemini_interface(authentication_token)

    body_composition_specialist = AssistantAgent(
        name="BodyComposition_Analyst",
        llm_config={"config_list": ai_configuration, "cache_seed": None},
        system_message="""You are a Body Composition Analysis Expert. Your specialized responsibilities encompass:
        1. Computing Body Mass Index from weight (kg) and height (cm) measurements
        2. Classifying composition status (underweight, optimal, overweight, obese)
        3. Delivering evidence-based health optimization strategies
        Always incorporate the precise BMI calculation in your comprehensive assessment."""
    )

    nutrition_strategist = AssistantAgent(
        name="Nutrition_Strategist",
        llm_config={"config_list": ai_configuration, "cache_seed": None},
        system_message=f"""You are a Clinical Nutrition Strategist. Develop comprehensive nutritional blueprints incorporating:
        1. Body composition insights from BodyComposition_Analyst
        2. Nutritional lifestyle preference ({nutrition_preference})
        Design complete meal architecture including breakfast, lunch, dinner, and strategic snacks with precise portions."""
    )

    fitness_architect = AssistantAgent(
        name="Fitness_Architect",
        llm_config={"config_list": ai_configuration, "cache_seed": None},
        system_message=f"""You are a Performance Fitness Architect. Engineer comprehensive weekly training protocols based on:
        1. Demographic profile (Age: {user_age}, Gender: {biological_gender})
        2. Body composition recommendations
        3. Nutritional strategy from Nutrition_Strategist
        Integrate cardiovascular conditioning, resistance training with precise duration and intensity specifications."""
    )

    wellness_coordinator = UserProxyAgent(
        name="Wellness_Coordinator",
        human_input_mode="NEVER",
        code_execution_config=False,
        llm_config={"config_list": ai_configuration, "cache_seed": None},
        system_message="Orchestrates user profile data integration and facilitates inter-agent collaboration."
    )

    wellness_coordinator.register_function(function_map={"compute_body_mass_index": compute_body_mass_index})

    return wellness_coordinator, body_composition_specialist, nutrition_strategist, fitness_architect, ai_configuration

#  Wellness Plan Generation Handler 
if generate_wellness_plan and google_api_token:
    try:
        wellness_coordinator, body_composition_specialist, nutrition_strategist, fitness_architect, ai_configuration = establish_wellness_agents(google_api_token)

        collaborative_wellness_session = GroupChat(
            agents=[wellness_coordinator, body_composition_specialist, nutrition_strategist, fitness_architect],
            messages=[],
            max_round=6,
            speaker_selection_method="round_robin"
        )

        session_orchestrator = GroupChatManager(
            groupchat=collaborative_wellness_session,
            llm_config={"config_list": ai_configuration, "cache_seed": None}
        )

        comprehensive_user_profile = f"""
        Complete Wellness Profile Assessment:
        - Biometric Measurements:
          • Body Weight: {body_weight} kg
          • Body Height: {body_height} cm
          • Chronological Age: {user_age}
          • Biological Gender: {biological_gender}
        - Lifestyle Preferences:
          • Nutritional Philosophy: {nutrition_preference}

        Execute comprehensive wellness analysis following this strategic sequence:
        1. Perform body composition analysis using 'compute_body_mass_index' function with weight={body_weight} and height={body_height}
        2. Conduct thorough BMI interpretation and generate optimization recommendations
        3. Architect personalized nutritional blueprint based on composition analysis and dietary philosophy
        4. Engineer comprehensive fitness protocol integrating age, gender, and nutritional strategy
        """

        with st.spinner("Engineering your personalized wellness optimization strategy..."):
            wellness_coordinator.initiate_chat(
                session_orchestrator,
                message=comprehensive_user_profile,
                clear_history=True
            )

            st.session_state.dialogue_history = []
            for communication in collaborative_wellness_session.messages:
                if communication['role'] != 'system' and communication['content'].strip():
                    st.session_state.dialogue_history.append((communication['name'], communication['content']))
                    if communication['name'] == "Fitness_Architect":
                        st.session_state.comprehensive_wellness_program = communication['content']

        st.success("Wellness optimization strategy successfully engineered!")

    except Exception as system_error:
        st.error(f"System processing error encountered: {str(system_error)}")
        st.info("Please verify: 1) Valid authentication token 2) Stable network connectivity 3) Accurate input parameters")

#  Wellness Strategy Results Presentation 
if st.session_state.dialogue_history:
    st.divider()
    st.subheader("Wellness Strategy Development Process")

    for specialist, expert_analysis in st.session_state.dialogue_history:
        with st.expander(f"{specialist} Professional Analysis:"):
            st.markdown(expert_analysis)

    st.divider()
    st.subheader("🎯 Your Comprehensive Wellness Optimization Strategy")

    if st.session_state.comprehensive_wellness_program:
        st.markdown(st.session_state.comprehensive_wellness_program)
        st.download_button(
            label="Export Wellness Strategy",
            data=st.session_state.comprehensive_wellness_program,
            file_name="personalized_wellness_optimization_strategy.txt",
            mime="text/plain"
        )
    else:
        st.warning("Fitness protocol generation incomplete. Please reinitiate process.")

elif not generate_wellness_plan:
    st.divider()
    st.info("""
    **Platform Operation Instructions:**
    1. Input your Gemini authentication token in the configuration panel
    2. Complete your comprehensive wellness profile
    3. Activate "Create Wellness Strategy"
    4. Review your personalized optimization recommendations
    """)