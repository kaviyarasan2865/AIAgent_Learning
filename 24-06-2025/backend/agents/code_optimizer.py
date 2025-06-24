from langchain.tools import Tool
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from gemini_llm import get_llm
from typing import List, Dict, Any
import os
import fitz  # PyMuPDF for PDF reading

class CodeOptimizerAgent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = self._get_tools()
        self.vectorstore = self._setup_vectorstore()
        self.executor = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            agent_kwargs={"prompt": self._get_prompt()},
            verbose=True,
            handle_parsing_errors=True,
            iterations=1
        )

    def _setup_vectorstore(self) -> Chroma:
        """Setup RAG with coding best practices from PDF"""
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        db_path = "optimization_db"
        pdf_path = os.path.join(os.path.dirname(__file__), "..", "data", "WebDevelopmentBestPractices.pdf")
        if not os.path.exists(db_path):
            # Load best practices from PDF
            best_practices = self._load_best_practices(pdf_path)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            )
            texts = text_splitter.split_text(best_practices)
            vectorstore = Chroma.from_texts(
                texts=texts,
                embedding=embeddings,
                persist_directory=db_path
            )
            vectorstore.persist()
        else:
            vectorstore = Chroma(
                persist_directory=db_path,
                embedding_function=embeddings
            )
        return vectorstore

    def _load_best_practices(self, pdf_path: str) -> str:
        """Extract text from the best practices PDF."""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    def _get_tools(self) -> List[Tool]:
        tools = [
            Tool(
                name="optimize_css",
                func=self._optimize_css,
                description="Optimizes CSS code using best practices"
            ),
            Tool(
                name="optimize_javascript",
                func=self._optimize_javascript,
                description="Optimizes JavaScript code using best practices"
            ),
            Tool(
                name="optimize_html",
                func=self._optimize_html,
                description="Optimizes HTML structure using best practices"
            )
        ]
        return tools

    def _get_prompt(self) -> PromptTemplate:
        return PromptTemplate(
            template="""You are a Code Optimizer Agent using RAG-based best practices.
Your goal is to optimize code by:
- Applying industry best practices
- Improving performance
- Enhancing maintainability
- Ensuring accessibility
- Following modern standards

Input: {input}
Available tools: {tools}
Tool names: {tool_names}

{agent_scratchpad}

Think through this step-by-step:
1. Analyze current code
2. Query best practices database
3. Generate optimization suggestions
4. Ensure compatibility
5. Provide implementation steps

Response should be in JSON format with:
- optimizations: list of suggested improvements
- code_changes: specific code modifications
- rationale: explanation for each change
- performance_impact: expected improvements

Let's optimize this code!""",
            input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
        )

    def _optimize_css(self, css: str) -> Dict:
        """Optimize CSS code"""
        # Query RAG for CSS best practices
        docs = self.vectorstore.similarity_search(
            "CSS optimization best practices",
            k=3
        )
        
        optimizations = []
        for doc in docs:
            if "CSS" in doc.page_content:
                optimizations.append({
                    "type": "css_optimization",
                    "suggestion": doc.page_content,
                    "implementation": self._generate_css_implementation(doc.page_content)
                })
                
        return {"optimizations": optimizations}

    def _optimize_javascript(self, js: str) -> Dict:
        """Optimize JavaScript code"""
        # Query RAG for JavaScript best practices
        docs = self.vectorstore.similarity_search(
            "JavaScript optimization best practices",
            k=3
        )
        
        optimizations = []
        for doc in docs:
            if "JavaScript" in doc.page_content:
                optimizations.append({
                    "type": "js_optimization",
                    "suggestion": doc.page_content,
                    "implementation": self._generate_js_implementation(doc.page_content)
                })
                
        return {"optimizations": optimizations}

    def _optimize_html(self, html: str) -> Dict:
        """Optimize HTML structure"""
        # Query RAG for HTML best practices
        docs = self.vectorstore.similarity_search(
            "HTML optimization best practices",
            k=3
        )
        
        optimizations = []
        for doc in docs:
            if "HTML" in doc.page_content:
                optimizations.append({
                    "type": "html_optimization",
                    "suggestion": doc.page_content,
                    "implementation": self._generate_html_implementation(doc.page_content)
                })
                
        return {"optimizations": optimizations}

    def _generate_css_implementation(self, best_practice: str) -> Dict:
        """Generate CSS implementation from best practice"""
        return {
            "before": "/* Original CSS */",
            "after": "/* Optimized CSS following best practice */",
            "explanation": best_practice
        }

    def _generate_js_implementation(self, best_practice: str) -> Dict:
        """Generate JavaScript implementation from best practice"""
        return {
            "before": "// Original JavaScript",
            "after": "// Optimized JavaScript following best practice",
            "explanation": best_practice
        }

    def _generate_html_implementation(self, best_practice: str) -> Dict:
        """Generate HTML implementation from best practice"""
        return {
            "before": "<!-- Original HTML -->",
            "after": "<!-- Optimized HTML following best practice -->",
            "explanation": best_practice
        }

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run code optimization"""
        css = input_data.get("css", "")
        js = input_data.get("javascript", "")
        html = input_data.get("html", "")
        fixes = input_data.get("fixes", {})
        summary = f"HTML:\n{html}\n\nCSS:\n{css}\n\nJavaScript:\n{js}\n\nFixes:\n{fixes}"
        return self.executor.run(input=summary)
