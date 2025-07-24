import os
import requests
import streamlit as st
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv 

# Environment setup and configuration
load_dotenv()
WEATHER_SERVICE_KEY = os.getenv("WEATHER_API_KEY")
GEMINI_SERVICE_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the AI model with Gemini configuration
travel_ai_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key=GEMINI_SERVICE_KEY
)

@tool
def fetch_weather_conditions(destination: str) -> str:
    """Retrieve real-time weather conditions and forecast for any destination."""
    try:
        # Primary weather service - WeatherAPI
        primary_endpoint = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_SERVICE_KEY}&q={destination}&aqi=no"
        weather_response = requests.get(primary_endpoint)
        weather_data = weather_response.json()
        
        if "error" in weather_data:
            # Backup weather service - OpenWeatherMap
            backup_endpoint = f"http://api.openweathermap.org/data/2.5/weather?q={destination}&appid=9b929a9d9c3f5a5e610cbf9163121d1e&units=metric"
            backup_response = requests.get(backup_endpoint)
            backup_data = backup_response.json()
            
            if backup_data.get("cod") != 200:
                return f"Weather service unavailable: {weather_data.get('error', {}).get('message', 'Unable to fetch weather information')}"
            
            return (f"Current conditions in {destination}: "
                    f"Temperature {backup_data['main']['temp']}°C, "
                    f"conditions: {backup_data['weather'][0]['description']}. "
                    f"Real feel: {backup_data['main']['feels_like']}°C. "
                    f"Humidity levels: {backup_data['main']['humidity']}%, "
                    f"Wind speed: {backup_data['wind']['speed']} m/s")
        
        return (f"Live weather for {destination}: "
                f"Currently {weather_data['current']['temp_c']}°C, "
                f"sky conditions: {weather_data['current']['condition']['text']}. "
                f"Feels like temperature: {weather_data['current']['feelslike_c']}°C. "
                f"Atmospheric humidity: {weather_data['current']['humidity']}%, "
                f"Wind velocity: {weather_data['current']['wind_kph']} km/h")
    except Exception as error:
        return f"Weather information currently unavailable: {str(error)}"

@tool
def discover_local_highlights(destination: str) -> str:
    """Discover and curate the most compelling attractions and landmarks for any destination."""
    try:
        # Enhanced search with DuckDuckGo
        location_search = DuckDuckGoSearchAPIWrapper()
        search_terms = f"must-visit attractions landmarks {destination} tourist guide recommendations"
        search_findings = location_search.run(search_terms)
        
        # AI-powered content curation
        curation_instructions = (
            f"Extract and present the top 5 must-see attractions in {destination} from this research:"
            f"\n\n{search_findings}\n\n"
            "Structure each attraction with:"
            "\n- Attraction name"
            "\n- Category (historical site, natural wonder, cultural venue, etc.)"
            "\n- Compelling description (single impactful sentence)"
            "\n- Unique appeal factor"
            "\nPresent as:"
            "\n1. **Attraction Name** (Category) - Description. Special because: ..."
        )
        
        return travel_ai_model.invoke(curation_instructions).content
    except Exception as error:
        return f"Unable to discover attractions: {str(error)}"

@tool
def suggest_accommodation_options(destination: str, preference_style: str) -> str:
    """Generate personalized accommodation suggestions based on traveler preferences and destination."""
    try:
        # Targeted accommodation search
        lodging_search = DuckDuckGoSearchAPIWrapper()
        search_parameters = f"recommended {preference_style.lower()} accommodation lodging {destination}"
        accommodation_data = lodging_search.run(search_parameters)
        
        # AI-driven recommendation engine
        recommendation_logic = (
            f"Curate 3-5 accommodation choices in {destination} perfect for {preference_style} travelers:"
            f"\n\n{accommodation_data}\n\n"
            "Present each option with:"
            "\n- Property name"
            "\n- Accommodation type (boutique hotel, resort, guesthouse, etc.)"
            "\n- Standout amenities and features"
            "\n- Suitability for {preference_style} travel experience"
            "\nStructure as:"
            "\n1. **Property Name** (Type) - Notable features. Perfect for {preference_style} because: ..."
        )
        
        return travel_ai_model.invoke(recommendation_logic).content
    except Exception as error:
        return f"Accommodation suggestions unavailable: {str(error)}"


# Comprehensive tool suite for the travel agent
agent_toolkit = [fetch_weather_conditions, discover_local_highlights, suggest_accommodation_options]

# Advanced conversational prompt engineering
travel_agent_instructions = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an expert travel consultant with deep local knowledge. Your approach:"
     "\n1. START with real-time weather insights and climate considerations"
     "\n2. FOLLOW with curated local attractions and experiences"
     "\n3. CONTINUE with personalized accommodation recommendations"
     "\n4. CONCLUDE with insider travel wisdom and practical advice"
     "\n\nOrganize your expertise as:"
     "\n### Climate & Weather Insights ☀️🌦️❄️"
     "\n[detailed weather analysis]"
     "\n\n### Premier Destinations & Experiences 🏛️🌄🎨"
     "\n[curated attraction highlights]"
     "\n\n### Accommodation Recommendations 🏨🛏️🏡"
     "\n[personalized lodging options]"
     "\n\n### Expert Travel Insights 🧳💡"
     "\n[professional tips and recommendations]"
     "\n\nMaintain an engaging tone with strategic emoji use. Handle any service disruptions gracefully."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Travel intelligence agent construction
travel_consultant = create_tool_calling_agent(travel_ai_model, agent_toolkit, travel_agent_instructions)

# Executive agent with enhanced capabilities
travel_agent_executor = AgentExecutor(
    agent=travel_consultant,
    tools=agent_toolkit,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=4,
    return_intermediate_steps=True
)

st.set_page_config(page_title="🗺️ Smart Travel Companion", page_icon="🧳", layout="wide")
st.title("🗺️ Your Personal Travel Intelligence Assistant")

# Advanced preference panel
with st.sidebar:
    st.header("🎯 Travel Customization")
    chosen_destination = st.text_input("Target Destination", "Chennai")
    journey_type = st.selectbox("Journey Style", 
                               ["Adventure", "Relaxation", "Cultural", "Foodie", "Family", "Business", "Spiritual"])
    trip_length = st.slider("Journey Duration (days)", 1, 14, 3)
    spending_tier = st.selectbox("Budget Category", ["Budget", "Mid-range", "Luxury"])
    
    if st.button("🔄 Reset Conversation"):
        st.session_state.chat_history = []
        st.rerun()

# Conversation memory initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Ready to plan your next adventure? Tell me where you'd like to explore! 🌍"}]

# Dynamic chat interface
for chat_entry in st.session_state.chat_history:
    user_icon = "👤" if chat_entry["role"] == "user" else "🤖"
    with st.chat_message(chat_entry["role"], avatar=user_icon):
        st.markdown(chat_entry["content"])

# Interactive query processing
if user_query := st.chat_input("Describe your travel dreams..."):
    # Archive user input
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)
    
    # Generate intelligent response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🌟 Crafting your personalized travel guide..."):
            try:
                # Execute comprehensive travel analysis
                travel_intelligence = travel_agent_executor.invoke(
                    {"input": f"Create a complete travel guide for {chosen_destination} "
                              f"optimized for a {trip_length}-day {journey_type.lower()} experience within {spending_tier} budget constraints"}
                )
                
                # Present the curated response
                response_container = st.empty()
                response_container.markdown(travel_intelligence["output"])
                
                # Archive assistant response
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": travel_intelligence["output"]}
                )
                
                # Technical insight panel
                with st.expander("🔧 Processing Intelligence"):
                    st.write("**Agent Processing Steps:**")
                    for processing_step in travel_intelligence.get("intermediate_steps", []):
                        st.json(processing_step)
                
            except Exception as processing_error:
                error_notification = f"🚨 Service Interruption: {str(processing_error)}"
                st.error(error_notification)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": error_notification}
                )

# Application footer with attribution
st.divider()
st.caption("""
    Intelligence Powered by: 
    <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_resting_v2_darkmode_2d4785dff9491523d32a.svg" width="20"> Google Gemini | 
    <img src="https://langchain.com/img/brand/theme-image.png" width="20"> LangChain Framework | 
    WeatherAPI.com Services
    """, unsafe_allow_html=True)

# Custom styling enhancements
st.markdown("""
    <style>
    .stChatFloatingInputContainer {
        bottom: 25px;
    }
    .stSpinner > div > div {
        border-top-color: #00d4aa;
    }
    .st-b7 {
        background-color: #f8fafc;
    }
    .st-c0 {
        background-color: #ffffff;
    }
    .st-emotion-cache-4oy321 {
        background-color: #f0f9ff;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)