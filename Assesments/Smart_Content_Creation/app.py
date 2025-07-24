import streamlit as st
import time
import google.generativeai as genai
from autogen import AssistantAgent, UserProxyAgent
from langchain_google_genai import ChatGoogleGenerativeAI
import copy
import os
from dotenv import load_dotenv 

# Environment Setup
load_dotenv()  
GOOGLE_AI_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GOOGLE_AI_KEY)

# Agent Behavioral Instructions
WRITER_PERSONA = """
You are an Expert Content Architect specializing in Generative AI technologies. Your expertise includes:
1. Crafting comprehensive, well-structured content with technical precision
2. Adapting and enhancing content based on expert feedback
3. Delivering polished markdown-formatted documentation
4. Maintaining focus on content excellence without meta-commentary
"""

REVIEWER_PERSONA = """
You are a Technical Content Evaluator with deep expertise in Generative AI. Your responsibilities include:
1. Conducting thorough analysis of content quality and technical correctness
2. Delivering actionable, specific improvement recommendations
3. Recognizing content strengths while identifying enhancement opportunities
4. Providing balanced, professional assessment with constructive guidance
"""

# Advanced AI Model Wrapper
class EnhancedGeminiInterface:
    def __init__(self, ai_model, behavioral_instructions):
        self.ai_model = ai_model
        self.behavioral_instructions = behavioral_instructions
    
    def process_request(self, user_input):
        complete_instruction = self.behavioral_instructions + "\n\n" + user_input
        try:
            ai_output = self.ai_model.invoke(complete_instruction)
            return ai_output.content
        except Exception as error:
            return f"Processing Error: {str(error)}"
    
    def __deepcopy__(self, memory_map):
        # Generate new instance preserving original configuration
        return EnhancedGeminiInterface(
            ai_model=ChatGoogleGenerativeAI(model=self.ai_model.model, google_api_key=GOOGLE_AI_KEY),
            behavioral_instructions=self.behavioral_instructions
        )

# Initialize Specialized AI Interfaces
content_architect = EnhancedGeminiInterface(
    ai_model=ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_AI_KEY),
    behavioral_instructions=WRITER_PERSONA
)

quality_assessor = EnhancedGeminiInterface(
    ai_model=ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_AI_KEY),
    behavioral_instructions=REVIEWER_PERSONA
)

# Main Application Interface
st.title("🎭 Collaborative AI Content Workshop")
st.caption("Watch Expert Content Architect and Quality Assessor agents collaborate in real-time")

# Interactive Configuration Panel
subject_matter = st.text_input("Research Focus Area", "Agentic AI")
interaction_cycles = st.slider("Collaboration Rounds", 3, 5, 3)
initiate_workshop = st.button("Launch Workshop")

if initiate_workshop:
    # Configure AutoGen Content Architect Agent
    architect_agent = AssistantAgent(
        name="ContentArchitect",
        system_message=WRITER_PERSONA,
        llm_config={
            "config_list": [
                {
                    "model": "gemini-1.5-flash",
                    "api_key": GOOGLE_AI_KEY,
                    "base_url": "https://generativelanguage.googleapis.com/v1beta/models/"
                }
            ],
            "timeout": 120
        },
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: msg.get("content", "").find("TERMINATE") >= 0,
    )
    
    # Configure AutoGen Quality Assessor Agent
    assessor_agent = AssistantAgent(
        name="QualityAssessor",
        system_message=REVIEWER_PERSONA,
        llm_config={
            "config_list": [
                {
                    "model": "gemini-1.5-flash",
                    "api_key": GOOGLE_AI_KEY,
                    "base_url": "https://generativelanguage.googleapis.com/v1beta/models/"
                }
            ],
            "timeout": 120
        },
        human_input_mode="NEVER",
        is_termination_msg=lambda msg: msg.get("content", "").find("TERMINATE") >= 0,
    )
    
    # Configure Workshop Coordinator
    workshop_coordinator = UserProxyAgent(
        name="WorkshopCoordinator",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        code_execution_config=False,
    )
    
    # Workshop Session Variables
    workshop_transcript = []
    latest_content = ""
    assessment_feedback = ""
    
    # Execute Collaborative Workshop
    for cycle in range(1, interaction_cycles + 1):
        with st.status(f"⚡ Cycle {cycle} underway...", expanded=True):
            # Content Creation Phase (odd cycles)
            if cycle % 2 == 1:
                st.subheader(f"Cycle {cycle}: Content Architect Phase")
                if cycle == 1:
                    creation_directive = f"Develop authoritative content exploring {subject_matter} using markdown structure. Include:\n- Fundamental principles and definitions\n- Technical architecture and components\n- Practical implementation scenarios\n- Emerging trends and future directions"
                else:
                    creation_directive = f"Enhance the existing content incorporating the assessor's recommendations:\n\nAssessment Feedback:\n{assessment_feedback}\n\nCurrent Material:\n{latest_content}\n\nDeliver refined markdown content:"
                
                st.markdown("**Development Brief:**")
                st.write(creation_directive)
                
                # Execute content creation
                latest_content = content_architect.process_request(creation_directive)
                
                st.markdown("**Crafted Content:**")
                st.markdown(latest_content)
                workshop_transcript.append(("ContentArchitect", latest_content))
            
            # Quality Assessment Phase (even cycles)
            else:
                st.subheader(f"Cycle {cycle}: Quality Assessment Phase")
                assessment_directive = f"Conduct comprehensive evaluation of this content across multiple dimensions:\n1. Technical precision and accuracy\n2. Communication effectiveness and clarity\n3. Content completeness and depth\n4. Strategic improvement recommendations\n\nContent Under Review:\n{latest_content}"
                
                st.markdown("**Assessment Brief:**")
                st.write(assessment_directive)
                
                # Execute quality assessment
                assessment_feedback = quality_assessor.process_request(assessment_directive)
                
                st.markdown("**Expert Assessment:**")
                st.write(assessment_feedback)
                workshop_transcript.append(("QualityAssessor", assessment_feedback))
            
            time.sleep(1)  # Rate limiting protection
    
    # Workshop Deliverable
    st.divider()
    st.subheader("🏆 Workshop Deliverable")
    st.markdown(latest_content)
    
    # Complete Workshop Documentation
    st.divider()
    st.subheader("📋 Workshop Documentation")
    for session_num, (participant_role, session_output) in enumerate(workshop_transcript, 1):
        with st.expander(f"{participant_role} - Session {session_num}"):
            st.write(session_output)