from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from gemini_llm import get_llm
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import esprima
import re

class ContentHealerAgent:
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
                name="check_content",
                func=self._check_content,
                description="Checks for placeholder or missing content"
            ),
            Tool(
                name="validate_javascript",
                func=self._validate_javascript,
                description="Validates JavaScript code for errors"
            ),
            Tool(
                name="check_references",
                func=self._check_references,
                description="Checks for broken references and links"
            )
        ]
        return tools

    def _get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template="""You are a Content Healer Agent specialized in finding and fixing content and logic issues.
Your goal is to identify problems like:
- Placeholder content (lorem ipsum)
- Missing images or broken links
- JavaScript errors
- Event handler issues
- Null references

Input: {input}
Available tools: {tools}
Tool names: {tool_names}

{agent_scratchpad}

Think through this step-by-step:
1. Scan for placeholder content
2. Check all links and references
3. Validate JavaScript logic
4. Test event handlers
5. Generate a detailed report

Response should be in JSON format with:
- content_issues: list of content problems
- logic_issues: list of JavaScript issues
- references: list of broken references
- suggestions: proposed fixes

Let's heal this content!""",
            input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
        )

    def _check_content(self, html: str) -> Dict:
        """Check for placeholder or missing content"""
        soup = BeautifulSoup(html, 'lxml')
        issues = []
        
        # Check for lorem ipsum
        lorem_elements = soup.find_all(text=re.compile(r'lorem ipsum', re.I))
        for elem in lorem_elements:
            issues.append({
                "type": "placeholder",
                "location": str(elem.parent.sourceline),
                "description": "Lorem ipsum placeholder text found"
            })
            
        # Check for missing images
        images = soup.find_all('img')
        for img in images:
            if not img.get('src') or img['src'].startswith('#'):
                issues.append({
                    "type": "missing_image",
                    "location": str(img.sourceline),
                    "description": "Missing or invalid image source"
                })
                
        return {"issues": issues}

    def _validate_javascript(self, js: str) -> Dict:
        """Validate JavaScript code"""
        issues = []
        try:
            # Parse JavaScript code
            esprima.parseScript(js)
        except esprima.Error as e:
            issues.append({
                "type": "syntax_error",
                "location": str(e.lineNumber),
                "description": str(e)
            })
            
        # Check for potential null references
        if 'null' in js or 'undefined' in js:
            issues.append({
                "type": "potential_null",
                "description": "Potential null/undefined references found"
            })
            
        return {"issues": issues}

    def _check_references(self, html: str) -> Dict:
        """Check for broken references"""
        soup = BeautifulSoup(html, 'lxml')
        issues = []
        
        # Check links
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if not href or href == '#' or href.startswith('javascript:void(0)'):
                issues.append({
                    "type": "broken_link",
                    "location": str(link.sourceline),
                    "description": "Empty or JavaScript void link found"
                })
                
        # Check IDs referenced in JavaScript events
        elements_with_events = soup.find_all(attrs=lambda attr: attr and any(x.startswith('on') for x in attr))
        for elem in elements_with_events:
            issues.append({
                "type": "event_check",
                "location": str(elem.sourceline),
                "description": f"Event handler found on {elem.name}, verify functionality"
            })
            
        return {"issues": issues}

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        combined = f"HTML:\n{input_data.get('html', '')}\n\nCSS:\n{input_data.get('css', '')}\n\nJavaScript:\n{input_data.get('javascript', '')}"
        return self.executor.run(input=combined)
