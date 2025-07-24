import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew
import google.generativeai as genai
import requests
import re
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize environment configuration
load_dotenv()
GOOGLE_GEMINI_KEY = os.getenv("GEMINI_API_KEY")
SERPER_SEARCH_KEY = os.getenv("SERPER_API_KEY")

# Setup Gemini AI configuration
genai.configure(api_key=GOOGLE_GEMINI_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize ChatGoogleGenerativeAI for CrewAI integration
chat_gemini = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_GEMINI_KEY,
    temperature=0.7
)

# Core Resource Discovery Functions
def discover_educational_content(subject: str) -> Dict[str, Any]:
    """Discover comprehensive educational resources for a specific subject."""
    try:
        search_endpoint = "https://google.serper.dev/search"
        request_headers = {"X-API-KEY": SERPER_SEARCH_KEY}
        
        # Fetch video tutorials
        video_search_terms = f"{subject} comprehensive tutorial video"
        video_response = requests.post(search_endpoint, json={"q": video_search_terms}, headers=request_headers).json()
        
        # Fetch written guides
        guide_search_terms = f"{subject} detailed guide documentation"
        guide_response = requests.post(search_endpoint, json={"q": guide_search_terms}, headers=request_headers).json()
        
        # Fetch practice materials
        practice_search_terms = f"{subject} hands-on practice problems"
        practice_response = requests.post(search_endpoint, json={"q": practice_search_terms}, headers=request_headers).json()
        
        video_resources = []
        guide_resources = []
        practice_resources = []
        
        # Process video results
        for video_item in video_response.get("organic", [])[:3]:
            video_resources.append(f"{video_item['title']}: {video_item['link']}")
        
        # Process guide results
        for guide_item in guide_response.get("organic", [])[:3]:
            guide_resources.append(f"{guide_item['title']}: {guide_item['link']}")
            
        # Process practice results
        for practice_item in practice_response.get("organic", [])[:3]:
            practice_resources.append(f"{practice_item['title']}: {practice_item['link']}")
        
        return {
            "subject": subject,
            "videos": video_resources,
            "articles": guide_resources,
            "exercises": practice_resources
        }
    except Exception as error:
        return {
            "subject": subject,
            "videos": [f"Video search failed: {str(error)}"],
            "articles": [f"Article search failed: {str(error)}"],
            "exercises": [f"Exercise search failed: {str(error)}"]
        }

def craft_assessment_questions(subject: str) -> List[Dict[str, Any]]:
    """Create engaging assessment questions for knowledge evaluation."""
    try:
        assessment_prompt = f"""Design 3 thought-provoking multiple-choice questions about {subject}. 
        Structure each question using this exact format:

Question: [Write your question here]
A) [First option]
B) [Second option]
C) [Third option]
D) [Fourth option]
Answer: [Letter of correct choice]

Ensure questions test comprehension and practical understanding."""
        
        ai_response = gemini_model.generate_content(assessment_prompt).text
        parsed_questions = []
        
        # Extract question segments
        question_segments = ai_response.split("Question:")
        for segment in question_segments[1:]:  # Skip initial empty segment
            segment_lines = [line.strip() for line in segment.strip().split("\n") if line.strip()]
            if len(segment_lines) >= 6:
                question_text = segment_lines[0]
                choice_options = []
                correct_answer = ""
                
                for line in segment_lines[1:]:
                    if line.startswith(('A)', 'B)', 'C)', 'D)')):
                        choice_options.append(line[3:].strip())
                    elif line.startswith("Answer:"):
                        correct_answer = line.split(":")[-1].strip()
                
                if len(choice_options) == 4 and correct_answer:
                    # Map letter to actual answer content
                    answer_position = ord(correct_answer.upper()) - ord('A')
                    if 0 <= answer_position < 4:
                        parsed_questions.append({
                            "question": question_text,
                            "options": choice_options,
                            "answer": choice_options[answer_position]
                        })
        
        return parsed_questions[:3]
    except Exception as error:
        return [{"question": f"Assessment generation error: {str(error)}", "options": ["Error", "Error", "Error", "Error"], "answer": "Error"}]

def design_practical_projects(subject: str, proficiency: str) -> List[Dict[str, Any]]:
    """Design hands-on projects tailored to learner proficiency level."""
    try:
        project_prompt = f"""Create 3 engaging project concepts for a {proficiency}-level learner studying {subject}.
Each project should include:
- An inspiring title
- Comprehensive description of objectives and implementation
- Justification for {proficiency} level appropriateness

Structure each project as:
Project: [Compelling Title]
Description: [Comprehensive explanation of the project]
"""
        
        ai_response = gemini_model.generate_content(project_prompt).text
        designed_projects = []
        
        # Parse project segments
        project_segments = ai_response.split("Project:")
        for segment in project_segments[1:]:  # Skip initial empty segment
            segment_lines = [line.strip() for line in segment.strip().split("\n") if line.strip()]
            
            project_title = segment_lines[0] if segment_lines else "Unnamed Project"
            project_description = ""
            
            for line in segment_lines[1:]:
                if line.startswith("Description:"):
                    project_description = line.split(":", 1)[1].strip()
                    break
            
            if project_description:
                designed_projects.append({
                    "title": project_title,
                    "description": project_description,
                    "level": proficiency
                })
        
        return designed_projects[:3]
    except Exception as error:
        return [{"title": f"Project generation error: {str(error)}", "description": "Unable to create project recommendations", "level": proficiency}]

# Specialized AI Agents
resource_curator = Agent(
    role="Educational Resource Specialist",
    goal="Curate high-quality learning resources through intelligent web discovery",
    backstory="""You are a seasoned educational technologist with expertise in digital learning curation. 
    Your specialization lies in identifying and organizing premium educational content across multiple formats.
    You leverage advanced search techniques to uncover the most valuable learning resources available online.""",
    llm=chat_gemini,
    verbose=True
)

assessment_designer = Agent(
    role="Learning Assessment Architect",
    goal="Develop comprehensive assessments that measure true understanding",
    backstory="""You are an expert in educational psychology and assessment design. 
    Your passion lies in creating meaningful evaluations that go beyond rote memorization.
    You craft questions that challenge learners to demonstrate genuine comprehension and application.""",
    llm=chat_gemini,
    verbose=True
)

project_architect = Agent(
    role="Experiential Learning Designer",
    goal="Create immersive project experiences that bridge theory and practice",
    backstory="""You are a master of project-based learning methodologies. 
    Your expertise lies in designing authentic, real-world projects that solidify learning.
    You understand how to calibrate project complexity to match learner capabilities perfectly.""",
    llm=chat_gemini,
    verbose=True
)

# Task Generation Functions
def build_resource_discovery_task(subject: str):
    return Task(
        description=f"""Conduct comprehensive resource discovery for '{subject}' learning materials. 
        Your mission is to identify diverse, high-quality educational content that supports multiple learning preferences.
        
        Search and curate:
        1. Engaging video tutorials and demonstrations
        2. Authoritative articles and comprehensive guides
        3. Interactive exercises and practical applications
        
        Organize findings with clear titles and accessible links for immediate use.""",
        agent=resource_curator,
        expected_output=f"""A meticulously organized collection of {subject} learning resources featuring:
        - Videos: Curated video tutorials with descriptive titles and direct links
        - Articles: Authoritative guides and documentation with titles and links  
        - Exercises: Practical learning exercises with titles and links"""
    )

def build_assessment_creation_task(subject: str):
    return Task(
        description=f"""Design a comprehensive assessment battery for '{subject}' consisting of 3 expertly crafted multiple-choice questions. 
        Your objective is to create evaluations that assess deep understanding and practical application.
        
        Each assessment item must include:
        - A thought-provoking question statement
        - 4 plausible multiple-choice alternatives (A, B, C, D)
        - Clear identification of the correct response
        
        Prioritize questions that evaluate conceptual understanding over mere factual recall.""",
        agent=assessment_designer,
        expected_output=f"""A professionally designed assessment suite for {subject} containing:
        - Question content
        - Four distinct answer choices
        - Clearly marked correct responses"""
    )

def build_project_development_task(subject: str, proficiency: str):
    return Task(
        description=f"""Architect 3 compelling project experiences for '{subject}' specifically calibrated for {proficiency}-level practitioners. 
        Your goal is to design authentic, engaging projects that bridge theoretical knowledge with practical application.
        
        Calibrate project complexity according to {proficiency} proficiency:
        - Beginner: Structured projects with comprehensive guidance and clear milestones
        - Intermediate: Semi-autonomous projects requiring creative problem-solving
        - Advanced: Complex, open-ended projects demanding expertise and innovation
        
        Each project should inspire learners while reinforcing core concepts through hands-on experience.""",
        agent=project_architect,
        expected_output=f"""3 thoughtfully designed project experiences for {proficiency}-level {subject} learners, each featuring:
        - Compelling project title
        - Comprehensive implementation description
        - Clear rationale for {proficiency} level alignment"""
    )

# Main Orchestration Function
def orchestrate_learning_experience(subject: str, proficiency: str):
    """Orchestrate a complete personalized learning experience."""
    
    try:
        # Execute core functions directly for optimal performance
        educational_resources = discover_educational_content(subject)
        assessment_questions = craft_assessment_questions(subject)
        project_concepts = design_practical_projects(subject, proficiency)

        return {
            "learning_materials": educational_resources,
            "quiz_questions": assessment_questions,
            "project_ideas": project_concepts
        }
    except Exception as error:
        st.error(f"❌ Learning experience generation failed: {str(error)}")
        return {
            "learning_materials": {},
            "quiz_questions": [],
            "project_ideas": []
        }

# Streamlit Application Interface
def launch_application():
    st.set_page_config(page_title="Adaptive Learning Path Generator", page_icon="🎯", layout="wide")
    
    st.title("🎯 Adaptive Learning Path Generator")
    st.markdown("Transform any subject into a comprehensive learning journey with AI-powered content curation!")
    st.markdown("---")
    
    # Validate API credentials
    if not GOOGLE_GEMINI_KEY:
        st.error("⚠️ GEMINI_API_KEY environment variable is required.")
        st.stop()
    
    if not SERPER_SEARCH_KEY:
        st.error("⚠️ SERPER_API_KEY environment variable is required.")
        st.stop()
    
    input_col1, input_col2 = st.columns(2)
    
    with input_col1:
        learning_subject = st.text_input("🎓 What would you like to master?", placeholder="e.g., Artificial Intelligence, React Development, Digital Marketing")
    
    with input_col2:
        skill_level = st.selectbox("⚡ Current expertise level:", ["Beginner", "Intermediate", "Advanced"])
    
    if st.button("🚀 Create My Learning Path", type="primary"):
        if not learning_subject.strip():
            st.error("Please specify a subject you'd like to learn about.")
            return
        
        with st.spinner("🎯 Crafting your personalized learning experience..."):
            learning_experience = orchestrate_learning_experience(learning_subject, skill_level)
            
            if learning_experience:
                st.success("✨ Your adaptive learning path is ready!")
                st.markdown("---")
                
                # Present results in organized tabs
                resources_tab, assessment_tab, projects_tab = st.tabs(["📖 Learning Resources", "🧠 Knowledge Assessment", "🛠️ Practical Projects"])
                
                with resources_tab:
                    st.subheader("📖 Curated Learning Resources")
                    
                    resource_data = learning_experience.get("learning_materials", {})
                    
                    if resource_data.get("videos"):
                        st.markdown("### 🎬 Video Learning")
                        for video_resource in resource_data["videos"]:
                            st.write(f"• {video_resource}")
                    
                    if resource_data.get("articles"):
                        st.markdown("### 📚 Written Guides")
                        for article_resource in resource_data["articles"]:
                            st.write(f"• {article_resource}")
                    
                    if resource_data.get("exercises"):
                        st.markdown("### 🎯 Practice Exercises")
                        for exercise_resource in resource_data["exercises"]:
                            st.write(f"• {exercise_resource}")
                
                with assessment_tab:
                    st.subheader("🧠 Knowledge Assessment")
                    
                    assessment_items = learning_experience.get("quiz_questions", [])
                    
                    if assessment_items:
                        for idx, assessment in enumerate(assessment_items, 1):
                            st.markdown(f"**Assessment {idx}: {assessment['question']}**")
                            for option_idx, choice in enumerate(assessment['options'], 1):
                                st.write(f"   {chr(64+option_idx)}) {choice}")
                            st.write(f"**✅ Correct Response:** {assessment['answer']}")
                            st.markdown("---")
                    else:
                        st.write("Assessment generation unavailable.")
                
                with projects_tab:
                    st.subheader("🛠️ Hands-On Projects")
                    
                    project_portfolio = learning_experience.get("project_ideas", [])
                    
                    if project_portfolio:
                        for project_idx, project_concept in enumerate(project_portfolio, 1):
                            st.markdown(f"### Project {project_idx}: {project_concept['title']}")
                            st.write(f"**Implementation Guide:** {project_concept['description']}")
                            st.write(f"**Skill Level:** {project_concept['level']}")
                            st.markdown("---")
                    else:
                        st.write("Project generation unavailable.")
                
                # Optional debugging information
                if learning_experience.get("raw_result"):
                    with st.expander("🔍 Technical Details"):
                        st.text(str(learning_experience["raw_result"]))
    
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🤖 Powered by Google Gemini Intelligence | 🌐 Enhanced with Serper Search</p>
            <p>🎯 Adaptive learning experiences tailored to your unique journey</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    launch_application()