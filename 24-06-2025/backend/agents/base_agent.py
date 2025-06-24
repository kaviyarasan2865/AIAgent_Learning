from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from gemini_llm import get_llm
from langchain.prompts import PromptTemplate

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm = get_llm()
        self.tools = self._get_tools()
        self.executor = self._create_executor()

    @abstractmethod
    def _get_tools(self) -> List[Tool]:
        """Return list of tools available to the agent"""
        pass

    def _create_executor(self):
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            agent_kwargs={"prompt": self._get_prompt()},
            verbose=True,
            handle_parsing_errors=True
        )

    @abstractmethod
    def _get_prompt(self) -> PromptTemplate:
        """Return the PromptTemplate for the agent"""
        pass

    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent with input data"""
        return self.executor.run(input=input_data)
