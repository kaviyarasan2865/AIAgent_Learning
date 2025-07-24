# academic_companion.py
import streamlit as st
from PyPDF2 import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
import json
import re
import os
from dotenv import load_dotenv

# Environment configuration
load_dotenv()
GOOGLE_GEMINI_TOKEN = os.getenv("GEMINI_API_KEY")

# Application setup
st.set_page_config(page_title="Academic Learning Companion", page_icon="🎓", layout="wide")
st.title("🎓 Academic Learning Companion")
st.caption("Transform your PDF documents into comprehensive study materials with AI-powered insights")

# Initialize AI learning engine
learning_engine = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=GOOGLE_GEMINI_TOKEN,
    temperature=0.3,
    max_output_tokens=2048
)

def parse_document_content(document_file):
    """Parse and extract content from uploaded PDF document"""
    extracted_content = ""
    document_reader = PdfReader(document_file)
    for document_page in document_reader.pages:
        extracted_content += document_page.extract_text() or ""
    return extracted_content

def create_knowledge_synthesis(content):
    """Synthesize comprehensive knowledge summary using AI"""
    synthesis_template = """
    You are an advanced academic content synthesizer. Transform the provided study material 
    into a structured knowledge synthesis following these academic standards:
    - Identify and extract fundamental concepts and critical insights
    - Employ precise academic terminology and scholarly language
    - Structure information using logical academic hierarchy
    - Limit each synthesis point to 1-2 comprehensive sentences
    - Prioritize the most essential 10-15 knowledge components
    
    Academic Material for Synthesis:
    {content}

    Structured Knowledge Synthesis:
    """
    synthesis_prompt = ChatPromptTemplate.from_template(synthesis_template)
    synthesis_chain = (
        {"content": RunnablePassthrough()}
        | synthesis_prompt
        | learning_engine
        | StrOutputParser()
    )
    return synthesis_chain.invoke(content)

def craft_assessment_battery(knowledge_synthesis):
    """Craft comprehensive assessment questions based on synthesized knowledge"""
    assessment_template = """
    Design a comprehensive assessment battery consisting of 5 expertly crafted multiple-choice evaluations 
    based on the provided knowledge synthesis. Adhere to these assessment design principles:
    1. Questions must evaluate deep conceptual understanding and analytical thinking
    2. Develop 4 academically rigorous options (A-D) for each assessment item
    3. Ensure clear identification of the optimal response
    4. Structure your response as valid JSON using this precise format:
    {{
        "questions": [
            {{
                "question": "Assessment question content here",
                "options": {{
                    "A": "Option A content",
                    "B": "Option B content", 
                    "C": "Option C content",
                    "D": "Option D content"
                }},
                "correct_answer": "A"
            }}
        ]
    }}
    
    Knowledge Synthesis:
    {knowledge_synthesis}
    """
    assessment_prompt = ChatPromptTemplate.from_template(assessment_template)
    assessment_chain = (
        {"knowledge_synthesis": RunnablePassthrough()}
        | assessment_prompt
        | learning_engine
        | StrOutputParser()
    )
    assessment_output = assessment_chain.invoke(knowledge_synthesis)
    
    # Parse and validate JSON response
    try:
        # Clean potential markdown formatting
        sanitized_output = re.sub(r'```json|```', '', assessment_output).strip()
        return json.loads(sanitized_output)
    except json.JSONDecodeError as parsing_error:
        st.error(f"Assessment parsing failed: {str(parsing_error)}")
        st.text("Raw AI output for diagnostics:")
        st.text(assessment_output)
        return {"questions": []}

# Session state initialization
if 'assessment_repository' not in st.session_state:
    st.session_state.assessment_repository = {}
if 'learner_responses' not in st.session_state:
    st.session_state.learner_responses = {}
if 'evaluation_completed' not in st.session_state:
    st.session_state.evaluation_completed = False
if 'active_document' not in st.session_state:
    st.session_state.active_document = None
if 'knowledge_synthesis' not in st.session_state:
    st.session_state.knowledge_synthesis = ""

# Document upload interface
academic_document = st.file_uploader("Upload Academic PDF Document", type="pdf")

if academic_document:
    # Reset learning session for new document
    if st.session_state.active_document != academic_document.name:
        st.session_state.assessment_repository = {}
        st.session_state.learner_responses = {}
        st.session_state.evaluation_completed = False
        st.session_state.active_document = academic_document.name
    
    # Process document content if not already synthesized
    if not st.session_state.knowledge_synthesis:
        with st.spinner("Processing document content..."):
            raw_content = parse_document_content(academic_document)
        
        if not raw_content.strip():
            st.error("Content extraction failed. Please verify document format and try again.")
            st.stop()
        
        # Generate knowledge synthesis
        with st.spinner("Creating knowledge synthesis with Gemini 1.5 Flash..."):
            st.session_state.knowledge_synthesis = create_knowledge_synthesis(raw_content)
    
    # Present knowledge synthesis
    st.subheader("📖 Knowledge Synthesis")
    st.markdown(st.session_state.knowledge_synthesis)
    
    # Generate assessment battery if not already created
    if not st.session_state.assessment_repository:
        with st.spinner("Crafting comprehensive assessment battery..."):
            assessment_data = craft_assessment_battery(st.session_state.knowledge_synthesis)
            st.session_state.assessment_repository = assessment_data
    
    # Present interactive assessment
    if st.session_state.assessment_repository.get('questions'):
        st.subheader("🧠 Comprehensive Assessment")
        st.caption("Evaluate your understanding by selecting appropriate responses and submitting for analysis")
        
        with st.form(key='academic_assessment_form'):
            for question_index, assessment_item in enumerate(st.session_state.assessment_repository['questions']):
                st.markdown(f"**Assessment {question_index+1}:** {assessment_item['question']}")
                
                # Present response options
                response_options = list(assessment_item['options'].items())
                selected_response = st.radio(
                    label="Choose your response:",
                    options=[option[0] for option in response_options],
                    format_func=lambda x: f"{x}) {assessment_item['options'][x]}",
                    key=f"assessment_{question_index}",
                    index=None
                )
                st.session_state.learner_responses[question_index] = selected_response
                st.divider()
            
            evaluation_trigger = st.form_submit_button("Submit Assessment")
        
        # Process assessment submission
        if evaluation_trigger:
            st.session_state.evaluation_completed = True
        
        # Display evaluation results
        if st.session_state.evaluation_completed:
            st.subheader("📈 Assessment Analysis")
            correct_responses = 0
            
            for question_index, assessment_item in enumerate(st.session_state.assessment_repository['questions']):
                learner_response = st.session_state.learner_responses.get(question_index)
                optimal_response = assessment_item['correct_answer']
                
                if learner_response == optimal_response:
                    correct_responses += 1
                    st.success(f"Assessment {question_index+1}: Excellent! ✅ (Your response: {learner_response})")
                else:
                    st.error(
                        f"Assessment {question_index+1}: Needs review ❌ "
                        f"(Your response: {learner_response or 'Not selected'}, "
                        f"Optimal response: {optimal_response})"
                    )
                
                # Provide detailed explanation
                with st.expander(f"Detailed analysis for Assessment {question_index+1}"):
                    st.markdown(f"**Question:** {assessment_item['question']}")
                    for option_key, option_content in assessment_item['options'].items():
                        indicator = "✓ " if option_key == optimal_response else "• "
                        st.markdown(f"{indicator}**{option_key}:** {option_content}")
            
            # Present performance analytics
            st.divider()
            total_assessments = len(st.session_state.assessment_repository['questions'])
            st.success(f"🎯 Performance Analysis: **{correct_responses}/{total_assessments}** ({correct_responses/total_assessments:.0%})")
            
            # Reset assessment option
            if st.button("Retake Assessment"):
                st.session_state.evaluation_completed = False
                st.session_state.learner_responses = {}
                st.rerun()
    
    st.success("Document processing completed successfully!")
    st.caption(f"Document: {academic_document.name} | Pages analyzed: {len(PdfReader(academic_document).pages)}")
    st.divider()
    st.info("💡 Learning Strategy: Thoroughly review the knowledge synthesis before attempting the assessment for optimal performance!")