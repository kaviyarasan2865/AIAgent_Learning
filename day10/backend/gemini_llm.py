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


# trying with multiple api keys

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from dotenv import load_dotenv
# import os
# import threading

# load_dotenv()

# # Prepare a list of API keys from the environment
# API_KEYS = [
#     os.getenv(f"GOOGLE_API_KEY{i}") for i in range(1, 6)
# ]
# API_KEYS = [k for k in API_KEYS if k]
# _api_key_lock = threading.Lock()
# _api_key_index = [0]  # Use a list for mutability in closure

# def get_next_api_key():
#     with _api_key_lock:
#         key = API_KEYS[_api_key_index[0] % len(API_KEYS)]
#         _api_key_index[0] = (_api_key_index[0] + 1) % len(API_KEYS)
#         return key

# def get_llm():
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         google_api_key=get_next_api_key(),
#         temperature=0.7,
#         top_p=0.9,
#         verbose=True
#     )
#     return llm

# def get_llm_chain(prompt_template: str, output_key: str = "output"):
#     llm = get_llm()
#     prompt = PromptTemplate(
#         template=prompt_template,
#         input_variables=["input"]
#     )
#     chain = LLMChain(
#         llm=llm,
#         prompt=prompt,
#         output_key=output_key,
#         verbose=True
#     )
#     return chain
