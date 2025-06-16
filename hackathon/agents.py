# agents.py
from gemini_llm import GeminiLLM
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentType, initialize_agent
from typing import Dict

# Initialize Gemini with API key
gemini = GeminiLLM(api_key="AIzaSyAPDRVzZucpwUvOClVQgbjwmCcMgRxnDU4")

# Create reflection prompt template
reflection_template = """
You are a UX expert and code auditor analyzing HTML code for improvements.

Given this HTML code:
{code}

Analyze the code and provide:
1. UX Issues:
   - Value proposition clarity
   - Call-to-action effectiveness
   - Visual hierarchy
   - User engagement elements
   
2. Specific Improvements:
   - Content refinements
   - Structure changes
   - Layout optimizations
   - Accessibility enhancements

Provide your analysis in clear bullet points.
"""

prompt_template = PromptTemplate.from_template(reflection_template)

def analyze_ux_with_reflection(input_dict: Dict[str, str]) -> str:
    """Analyze UX using the reflection prompt template"""
    final_prompt = prompt_template.format(**input_dict)
    return gemini.invoke(final_prompt).content

# Create the reflection analysis tool
reflection_tool = Tool(
    name="analyze_ux",
    func=analyze_ux_with_reflection,
    description="Analyzes HTML code for UX improvements and provides detailed suggestions"
)

# Create update code prompt template
update_template = """
You are a web developer implementing UX improvements.

Original HTML:
{code}

UX Analysis:
{analysis}

Update the HTML to incorporate all suggested improvements. Focus on:
1. Clear value proposition
2. Effective call-to-action hierarchy
3. Visual structure and spacing
4. Accessibility best practices
5. Modern design patterns

Return only the improved HTML code.
"""

update_prompt_template = PromptTemplate.from_template(update_template)

def update_html_with_improvements(input_dict: Dict[str, str]) -> str:
    """Update HTML based on UX analysis using the update prompt template"""
    final_prompt = update_prompt_template.format(**input_dict)
    return gemini.invoke(final_prompt).content

# Create the code update tool
update_tool = Tool(
    name="update_html",
    func=update_html_with_improvements,
    description="Updates HTML code based on UX analysis and suggestions"
)

# Initialize the reflection agent with both tools
reflection_agent = initialize_agent(
    tools=[reflection_tool, update_tool],
    llm=gemini,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,
    early_stopping_method="generate"
)
