# agents.py
from gemini_llm import GeminiLLM
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentType, initialize_agent
from typing import Dict, List

# Initialize Gemini with API key
gemini = GeminiLLM(api_key="AIzaSyAPDRVzZucpwUvOClVQgbjwmCcMgRxnDU4")

# User Flow Simulation Agent Templates
user_flow_template = """
You are simulating a {persona} user navigating through this website:
{html_content}

Simulate the user journey considering:
1. Initial impressions and expectations
2. Navigation path through the site
3. Decision points and hesitations
4. Points of confusion or friction
5. Likelihood to convert

Return a detailed user journey analysis with specific friction points.
"""

# Friction Detection Agent Templates
friction_template = """
Analyze this website content for friction points:
{html_content}

Previous User Journey Analysis:
{user_journey}

Identify:
1. Unclear or conflicting CTAs
2. Complex navigation paths
3. Confusing messaging
4. Broken user flows
5. Performance bottlenecks

Provide a prioritized list of friction points with severity scores (1-10).
"""

# Benchmarking Agent Templates
benchmark_template = """
Compare this website structure:
{html_content}

With these industry best practices and patterns:
1. Navigation patterns
2. CTA placement and hierarchy
3. Content structure
4. User flow optimization
5. Conversion funnel design

Provide specific areas where the site deviates from best practices.
"""

# UX Optimization Agent Templates
ux_template = """
Based on:
User Journey: {user_journey}
Friction Points: {friction_points}
Benchmark Analysis: {benchmark_analysis}

Recommend specific improvements for:
1. Content hierarchy
2. Navigation structure
3. CTA optimization
4. Layout improvements
5. User flow streamlining

Provide actionable changes with implementation priority.
"""

# Create Tool Functions
def simulate_user_flow(input_dict: Dict[str, str]) -> str:
    template = PromptTemplate.from_template(user_flow_template)
    final_prompt = template.format(**input_dict)
    return gemini.invoke(final_prompt)

def detect_friction(input_dict: Dict[str, str]) -> str:
    template = PromptTemplate.from_template(friction_template)
    final_prompt = template.format(**input_dict)
    return gemini.invoke(final_prompt)

def benchmark_site(input_dict: Dict[str, str]) -> str:
    template = PromptTemplate.from_template(benchmark_template)
    final_prompt = template.format(**input_dict)
    return gemini.invoke(final_prompt)

def optimize_ux(input_dict: Dict[str, str]) -> str:
    template = PromptTemplate.from_template(ux_template)
    final_prompt = template.format(**input_dict)
    return gemini.invoke(final_prompt)

# Create Tools
user_flow_tool = Tool(
    name="simulate_user_flow",
    func=simulate_user_flow,
    description="Simulates user journeys through the website for different personas"
)

friction_tool = Tool(
    name="detect_friction",
    func=detect_friction,
    description="Identifies friction points and conversion barriers"
)

benchmark_tool = Tool(
    name="benchmark_site",
    func=benchmark_site,
    description="Compares site structure with industry best practices"
)

ux_tool = Tool(
    name="optimize_ux",
    func=optimize_ux,
    description="Recommends UX improvements based on analysis"
)

# Initialize Agents with error handling
user_flow_agent = initialize_agent(
    tools=[user_flow_tool],
    llm=gemini,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

friction_agent = initialize_agent(
    tools=[friction_tool],
    llm=gemini,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

benchmark_agent = initialize_agent(
    tools=[benchmark_tool],
    llm=gemini,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

ux_agent = initialize_agent(
    tools=[ux_tool],
    llm=gemini,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

# Update the analyze_and_optimize_site function
def analyze_and_optimize_site(html_content: str, personas: List[str]) -> Dict[str, str]:
    results = {
        "user_journeys": [],
        "friction_points": None,
        "benchmark_analysis": None,
        "ux_recommendations": None
    }
    
    # Step 1: Simulate user journeys for each persona
    for persona in personas:
        try:
            journey = user_flow_agent.invoke({
                "input": f"Simulate how a {persona} would interact with this website: {html_content}"
            })
            results["user_journeys"].append(journey)
        except Exception as e:
            print(f"Error in user flow simulation for {persona}: {str(e)}")
            continue
    
    # Step 2: Detect friction points
    try:
        results["friction_points"] = friction_agent.invoke({
            "input": f"Analyze this HTML for friction points: {html_content}"
        })
    except Exception as e:
        print(f"Error in friction detection: {str(e)}")
    
    # Step 3: Benchmark analysis
    try:
        results["benchmark_analysis"] = benchmark_agent.invoke({
            "input": f"Compare this website structure with industry best practices: {html_content}"
        })
    except Exception as e:
        print(f"Error in benchmark analysis: {str(e)}")
    
    # Step 4: Generate UX recommendations
    try:
        results["ux_recommendations"] = ux_agent.invoke({
            "input": f"Suggest UX improvements for this website: {html_content}"
        })
    except Exception as e:
        print(f"Error in UX optimization: {str(e)}")
    
    return results
