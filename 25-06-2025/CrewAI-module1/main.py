import os
from crewai import Agent, Task, Crew, LLM

# Directly set your Gemini API key
# os.environ["GOOGLE_API_KEY1"] = os.getenv("GEMINI_API_KEY")

# Gemini LLM setup
llm = LLM(
    # provider="google_genai",
    model="gemini/gemini-1.5-flash",  
    temperature=0.7,
)

# data
logistics_data = {
    "routes": [
        {"route_id": 1, "stops": ["A", "B", "C"], "distance_km": 120, "avg_time_min": 90},
        {"route_id": 2, "stops": ["D", "E"], "distance_km": 80, "avg_time_min": 60}
    ],
    "inventory": [
        {"product": "Widgets", "turnover_days": 30, "stock": 100},
        {"product": "Gadgets", "turnover_days": 45, "stock": 50},
        {"product": "Spare Parts", "turnover_days": 60, "stock": 200}
    ]
}

logistics_analyst = Agent(
    role="Logistics Analyst",
    goal="Analyze the current logistics operations to identify inefficiencies in delivery routes and inventory turnover",
    backstory="Experienced analyst...",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

optimization_strategist = Agent(
    role="Optimization Strategist",
    goal="Create optimization strategies...",
    backstory="Supply chain strategist...",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

task1 = Task(
    description=(
        "Analyze the following logistics data:\n"
        f"{logistics_data}\n"
        "Focus on delivery routes and inventory turnover trends. Identify key inefficiencies..."
    ),
    expected_output="A report highlighting inefficiencies...",
    agent=logistics_analyst
)

task2 = Task(
    description=(
        "Based on the report from the Logistics Analyst, propose optimization strategies..."
    ),
    expected_output="An optimization plan...",
    agent=optimization_strategist,
    depends_on=[task1]
)

crew = Crew(
    agents=[logistics_analyst, optimization_strategist],
    tasks=[task1, task2],
    context=logistics_data,
    verbose=True
)

results = crew.kickoff()
print("\n🔍 Final Output:\n", results)
