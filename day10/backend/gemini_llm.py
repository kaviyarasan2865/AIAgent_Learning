from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7,
        top_p=0.9,
        verbose=True
    )
    return llm

def get_llm_chain(prompt_template: str, output_key: str = "output"):
    llm = get_llm()
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["input"]
    )
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        output_key=output_key,
        verbose=True
    )
    return chain
