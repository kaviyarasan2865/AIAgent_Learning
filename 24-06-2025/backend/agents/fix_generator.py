from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from gemini_llm import get_llm
from typing import List, Dict, Any
import json

class FixGeneratorAgent:
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
                name="generate_layout_fix",
                func=self._generate_layout_fix,
                description="Generates fixes for layout issues"
            ),
            Tool(
                name="generate_content_fix",
                func=self._generate_content_fix,
                description="Generates fixes for content issues"
            ),
            Tool(
                name="generate_js_fix",
                func=self._generate_js_fix,
                description="Generates fixes for JavaScript issues"
            )
        ]
        return tools

    def _get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template="""You are a Fix Generator Agent specialized in creating solutions for web development issues.
Your goal is to analyze issues and generate specific, actionable fixes.

Input: {input}
Available tools: {tools}
Tool names: {tool_names}

{agent_scratchpad}

IMPORTANT: You must return your response in valid JSON format with the following structure:

{{
  "fixes": [
    {{
      "type": "html_fix|css_fix|js_fix",
      "before": "exact problematic code snippet",
      "after": "exact corrected code snippet", 
      "explanation": "brief explanation of the fix"
    }}
  ]
}}

Guidelines:
1. Analyze the reported issues carefully
2. Generate specific fixes for each issue type (HTML, CSS, JavaScript)
3. Use exact code snippets in "before" and "after" fields
4. Ensure the "before" code matches what's actually in the source code
5. Make fixes that are practical and implementable
6. Include explanations that are clear and concise

Common fix types:
- html_fix: For placeholder text, missing images, semantic issues
- css_fix: For positioning, responsive design, layout problems  
- js_fix: For missing elements, error handling, functionality issues

Return ONLY the JSON response. Do not include any other text or explanations outside the JSON structure.""",
            input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
        )

    def _generate_layout_fix(self, issue) -> Dict:
        """Generate fixes for layout issues"""
        fixes = []
        
        # Accept both dict and string
        if isinstance(issue, str):
            # Optionally, you could parse the string for keywords
            return {"fixes": [{"type": "layout_fix", "before": "", "after": "", "explanation": issue}]}
        
        if issue.get("type") == "positioning":
            fixes.append({
                "type": "css_fix",
                "before": "position: absolute;",
                "after": "position: relative;\nz-index: 1;",
                "explanation": "Changed to relative positioning to prevent overlap"
            })
        elif issue.get("type") == "responsive":
            fixes.append({
                "type": "css_fix",
                "before": "width: 300px;",
                "after": "width: 100%;\nmax-width: 300px;",
                "explanation": "Made width responsive with max-width constraint"
            })
            
        return {"fixes": fixes}

    def _generate_content_fix(self, issues) -> Dict:
        """Generate fixes for content issues. Accepts a list of issues or a single issue."""
        fixes = []
        # Accept both a single dict or a list
        if isinstance(issues, dict):
            issues = [issues]
        for issue in issues:
            if not isinstance(issue, dict):
                # Optionally log or skip non-dict issues
                continue
            if issue.get("type") == "placeholder":
                fixes.append({
                    "type": "html_fix",
                    "before": "Lorem ipsum dolor sit amet",
                    "after": "Welcome to our website! This is where you can add your main content.",
                    "explanation": "Replace placeholder text with meaningful content"
                })
            elif issue.get("type") == "missing_image":
                fixes.append({
                    "type": "html_fix",
                    "before": '<img src="#" alt="">',
                    "after": '<img src="https://via.placeholder.com/300x200" alt="Sample image">',
                    "explanation": "Add proper image source and descriptive alt text"
                })
        return {"fixes": fixes}

    def _generate_js_fix(self, issue) -> Dict:
        """Generate fixes for JavaScript issues. Accepts a dict or a string."""
        fixes = []
        if not isinstance(issue, dict):
            # Optionally log or skip non-dict issues
            return {"fixes": fixes}
        if issue.get("type") == "syntax_error":
            fixes.append({
                "type": "js_fix",
                "before": "function() { console.log('error'",
                "after": "function() { console.log('error'); }",
                "explanation": "Fixed missing closing bracket and semicolon"
            })
        elif issue.get("type") == "potential_null":
            fixes.append({
                "type": "js_fix",
                "before": "if (obj.property)",
                "after": "if (obj && obj.property)",
                "explanation": "Added null check for obj"
            })
        elif issue.get("type") == "missing_element":
            fixes.append({
                "type": "js_fix",
                "before": "document.getElementById('missing-id').innerText = 'Clicked!';",
                "after": "var el = document.getElementById('missing-id');\nif (el) { el.innerText = 'Clicked!'; }",
                "explanation": "Added check for missing element before accessing innerText"
            })
        return {"fixes": fixes}

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fixes for all issues using the LLM agent"""
        issues = input_data.get('issues', {})
        layout_issues = issues.get('layout', [])
        content_issues = issues.get('content', [])
        
        # Create a comprehensive prompt for the agent to analyze and generate fixes
        analysis_prompt = f"""
Analyze the following web development issues and generate specific fixes:

LAYOUT ISSUES:
{layout_issues}

CONTENT ISSUES:
{content_issues}

Please generate fixes for:
1. HTML content issues (placeholder text, missing images, etc.)
2. CSS layout issues (positioning, responsive design, etc.)
3. JavaScript functionality issues (missing elements, error handling, etc.)

For each fix, provide:
- type: "html_fix", "css_fix", or "js_fix"
- before: the problematic code snippet
- after: the corrected code snippet
- explanation: why this fix is needed

Return the fixes in JSON format with a "fixes" array containing the fix objects.
"""

        try:
            # Use the LLM agent to generate fixes
            result = self.executor.run(input=analysis_prompt)
            
            # Parse the result
            if isinstance(result, str):
                # Try to extract JSON from the result
                if "{" in result and "}" in result:
                    start = result.find("{")
                    end = result.rfind("}") + 1
                    json_str = result[start:end]
                    try:
                        parsed_result = json.loads(json_str)
                        if "fixes" in parsed_result and isinstance(parsed_result["fixes"], list):
                            return {"fixes": parsed_result["fixes"]}
                    except json.JSONDecodeError:
                        pass
                
                # If JSON parsing failed, try to extract fixes from the text
                fixes = self._extract_fixes_from_text(result)
                if fixes:
                    return {"fixes": fixes}
            
            # If agent approach failed, fall back to basic fixes
            return self._generate_basic_fixes(issues)
            
        except Exception as e:
            print(f"Agent-based fix generation failed: {e}")
            # Fall back to basic fixes
            return self._generate_basic_fixes(issues)

    def _extract_fixes_from_text(self, text: str) -> List[Dict]:
        """Extract fixes from agent response text when JSON parsing fails"""
        fixes = []
        
        # Look for common patterns in the text
        lines = text.split('\n')
        current_fix = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for fix type indicators
            if "html_fix" in line.lower() or "html fix" in line.lower():
                if current_fix:
                    fixes.append(current_fix)
                current_fix = {"type": "html_fix"}
            elif "css_fix" in line.lower() or "css fix" in line.lower():
                if current_fix:
                    fixes.append(current_fix)
                current_fix = {"type": "css_fix"}
            elif "js_fix" in line.lower() or "javascript fix" in line.lower():
                if current_fix:
                    fixes.append(current_fix)
                current_fix = {"type": "js_fix"}
            
            # Look for before/after patterns
            elif "before:" in line.lower():
                before_content = line.split("before:", 1)[1].strip()
                if current_fix:
                    current_fix["before"] = before_content
            elif "after:" in line.lower():
                after_content = line.split("after:", 1)[1].strip()
                if current_fix:
                    current_fix["after"] = after_content
            elif "explanation:" in line.lower():
                explanation = line.split("explanation:", 1)[1].strip()
                if current_fix:
                    current_fix["explanation"] = explanation
        
        # Add the last fix if it exists
        if current_fix and len(current_fix) > 1:
            fixes.append(current_fix)
        
        return fixes

    def _generate_basic_fixes(self, issues: Dict) -> Dict[str, Any]:
        """Generate basic fixes as fallback when agent fails"""
        all_fixes = []
        
        # Generate basic fixes based on common patterns
        layout_issues = issues.get('layout', [])
        content_issues = issues.get('content', [])
        
        # HTML fixes for common issues
        if any("lorem" in str(issue).lower() for issue in [layout_issues, content_issues]):
            all_fixes.append({
                "type": "html_fix",
                "before": "Lorem ipsum dolor sit amet",
                "after": "Welcome to our website! This is where you can add your main content.",
                "explanation": "Replace placeholder text with meaningful content"
            })
        
        if any("img" in str(issue).lower() and "src" in str(issue).lower() for issue in [layout_issues, content_issues]):
            all_fixes.append({
                "type": "html_fix",
                "before": '<img src="#" alt="">',
                "after": '<img src="https://via.placeholder.com/300x200" alt="Sample image">',
                "explanation": "Add proper image source and descriptive alt text"
            })
        
        # CSS fixes for common issues
        if any("position" in str(issue).lower() for issue in [layout_issues, content_issues]):
            all_fixes.append({
                "type": "css_fix",
                "before": "position: absolute;",
                "after": "position: relative;\nz-index: 1;",
                "explanation": "Changed to relative positioning to prevent overlap"
            })
        
        # JavaScript fixes for common issues
        if any("javascript" in str(issue).lower() or "missing" in str(issue).lower() for issue in [layout_issues, content_issues]):
            all_fixes.append({
                "type": "js_fix",
                "before": "const element = document.getElementById('missing-id');\nelement.style.display = 'none';",
                "after": "const element = document.getElementById('missing-id');\nif (element) {\n    element.style.display = 'none';\n}",
                "explanation": "Added null check for missing element before accessing properties"
            })
        
        return {"fixes": all_fixes}
