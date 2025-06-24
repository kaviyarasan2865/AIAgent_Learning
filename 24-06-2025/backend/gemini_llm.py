# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from dotenv import load_dotenv
# import os

# load_dotenv()

# def get_llm():
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         google_api_key=os.getenv("GOOGLE_API_KEY"),
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


# ######
# Code by GPT
import os
import time
import threading
import logging
from dotenv import load_dotenv
from collections import deque
from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load env variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LLM-Key-Rotation")

# Load and clean API keys
API_KEYS = [os.getenv(f"GOOGLE_API_KEY{i}") for i in range(1, 6)]
API_KEYS = [key for key in API_KEYS if key]

# Thread-safe key rotation
_api_key_lock = threading.Lock()
_key_queue = deque(API_KEYS)
_blacklisted_keys = {}  # key: timestamp

BLACKLIST_TIMEOUT = 300  # 5 minutes

def get_next_api_key() -> Optional[str]:
    """Get the next available API key, skipping blacklisted ones."""
    with _api_key_lock:
        for _ in range(len(_key_queue)):
            key = _key_queue[0]
            now = time.time()
            if key not in _blacklisted_keys or (now - _blacklisted_keys[key] > BLACKLIST_TIMEOUT):
                _key_queue.rotate(-1)
                return key
            else:
                logger.warning(f"Key {key[:5]}... is blacklisted, skipping.")
                _key_queue.rotate(-1)
        return None

def blacklist_api_key(key: str):
    with _api_key_lock:
        _blacklisted_keys[key] = time.time()
        logger.error(f"Blacklisted API key: {key[:5]}...")

def get_llm() -> ChatGoogleGenerativeAI:
    """Returns an LLM with the next valid API key."""
    api_key = get_next_api_key()
    if not api_key:
        raise RuntimeError("No available API keys left.")
    # print(f"[Gemini LLM] Using API key: {api_key[:8]}...{api_key[-4:]}")
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.7,
        top_p=0.9,
        verbose=True
    )

def get_llm_chain(prompt_template: str, output_key: str = "output") -> LLMChain:
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["input"]
    )
    return LLMChain(
        llm=get_llm(),
        prompt=prompt,
        output_key=output_key,
        verbose=True
    )

def run_chain_with_retries(chain: LLMChain, input_text: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            return chain.run(input=input_text)
        except Exception as e:
            logger.warning(f"[Attempt {attempt + 1}] Error during LLM call: {e}")
            current_key = chain.llm.google_api_key
            blacklist_api_key(current_key)
            chain.llm = get_llm()
    raise RuntimeError("All retries failed with available API keys.")
