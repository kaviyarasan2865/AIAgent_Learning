import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Conversion Obstacle Analyzer",
    page_icon="🔍",
    layout="wide"
)

def analyze_website(html_content, personas):
    url = "http://localhost:8000/analyze"
    payload = {
        "html_content": html_content,
        "personas": personas
    }
    response = requests.post(url, json=payload)
    return response.json()

st.title("🔍 Conversion Obstacle Analyzer")

with st.form("website_analysis"):
    html_content = st.text_area("Enter your website HTML:", height=200)
    
    st.subheader("User Personas")
    persona1 = st.text_input("Persona 1:", "busy professional seeking quick solutions")
    persona2 = st.text_input("Persona 2:", "detail-oriented researcher comparing options")
    persona3 = st.text_input("Persona 3:", "first-time visitor exploring the site")
    
    submitted = st.form_submit_button("Analyze Website")
    
    if submitted:
        personas = [persona1, persona2, persona3]
        with st.spinner("Analyzing website..."):
            results = analyze_website(html_content, personas)
            
            st.success("Analysis Complete!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("User Journey Analysis")
                for journey in results["user_journeys"]:
                    st.write(journey)
                    
                st.subheader("Friction Points")
                if results["friction_points"]:
                    st.write(results["friction_points"])
            
            with col2:
                st.subheader("Benchmark Analysis")
                if results["benchmark_analysis"]:
                    st.write(results["benchmark_analysis"])
                
                st.subheader("UX Recommendations")
                if results["ux_recommendations"]:
                    st.write(results["ux_recommendations"])