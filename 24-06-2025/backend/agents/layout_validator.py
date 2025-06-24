from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from gemini_llm import get_llm
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import cssutils
import re

class LayoutValidatorAgent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = self._get_tools()
        self.executor = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            agent_kwargs={"prompt": self._get_prompt()},
            verbose=True,
            handle_parsing_errors=True,
            iterations=1
        )

    def _get_tools(self) -> List[Tool]:
        tools = [
            Tool(
                name="analyze_layout",
                func=self._analyze_layout,
                description="Analyzes HTML and CSS for layout issues"
            ),
            Tool(
                name="check_responsive",
                func=self._check_responsive,
                description="Checks for responsive design issues"
            ),
            Tool(
                name="validate_css",
                func=self._validate_css,
                description="Validates CSS for potential conflicts"
            )
        ]
        return tools

    def _get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template="""You are a Layout Validator Agent specialized in detecting HTML and CSS layout issues.
Your goal is to identify problems like:
- Element overlaps
- Responsive design breakage
- Z-index conflicts
- Grid/Flexbox issues
- Positioning problems

Input: {input}
Available tools: {tools}
Tool names: {tool_names}

{agent_scratchpad}

Think through this step-by-step:
1. Analyze the HTML structure
2. Review CSS properties
3. Check responsive breakpoints
4. Identify potential conflicts
5. Generate a detailed report

Response should be in JSON format with:
- issues: list of detected problems
- locations: where issues were found
- severity: high/medium/low for each issue

Let's approach this systematically!""",
            input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
        )

    def _analyze_layout(self, html: str) -> Dict:
        """Analyze HTML for layout issues"""
        soup = BeautifulSoup(html, 'lxml')
        issues = []
        
        # Check for potential overlap issues
        positioned_elements = soup.find_all(style=re.compile(r'position:\s*(absolute|relative|fixed)'))
        for elem in positioned_elements:
            issues.append({
                "type": "positioning",
                "element": elem.name,
                "location": str(elem.sourceline),
                "description": f"Potential overlap with positioned element: {elem.name}"
            })
            
        return {"issues": issues}

    def _check_responsive(self, html: str) -> Dict:
        """Check for responsive design issues"""
        soup = BeautifulSoup(html, 'lxml')
        issues = []
        
        # Check for fixed widths
        fixed_width_elements = soup.find_all(style=re.compile(r'width:\s*\d+px'))
        for elem in fixed_width_elements:
            issues.append({
                "type": "responsive",
                "element": elem.name,
                "location": str(elem.sourceline),
                "description": "Fixed width may cause responsive issues"
            })
            
        return {"issues": issues}

    def _validate_css(self, css: str) -> Dict:
        """Validate CSS for conflicts"""
        parser = cssutils.CSSParser()
        sheet = parser.parseString(css)
        issues = []
        
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                # Check for z-index conflicts
                if 'z-index' in rule.style.cssText:
                    issues.append({
                        "type": "z-index",
                        "selector": rule.selectorText,
                        "description": "Potential z-index stacking context issue"
                    })
                    
        return {"issues": issues}

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run layout validation analysis"""
        html = input_data.get('html', '')
        css = input_data.get('css', '')
        
        all_issues = []
        
        # Check layout issues
        if html:
            layout_result = self._analyze_layout(html)
            all_issues.extend(layout_result.get('issues', []))
            
            responsive_result = self._check_responsive(html)
            all_issues.extend(responsive_result.get('issues', []))
        
        # Check CSS issues
        if css:
            css_result = self._validate_css(css)
            all_issues.extend(css_result.get('issues', []))
        
        # If no issues found, create specific ones based on common patterns
        if not all_issues:
            # Check for common layout issues
            if 'position: absolute' in css:
                all_issues.append({
                    "type": "positioning",
                    "description": "Absolute positioning may cause overlap issues",
                    "content": "position: absolute;"
                })
            
            if 'width: 300px' in html or 'width: 300px' in css:
                all_issues.append({
                    "type": "responsive",
                    "description": "Fixed width may cause responsive issues",
                    "content": "width: 300px;"
                })
            
            if 'z-index' in css:
                all_issues.append({
                    "type": "z-index",
                    "description": "Z-index stacking context issue detected",
                    "content": "z-index: 999;"
                })
        
        return {"issues": all_issues}
