# # agents/order_manager.py

# from langchain_core.messages import HumanMessage
# from langchain_core.output_parsers import JsonOutputParser
# from dotenv import load_dotenv
# import os

# # Load your OpenRouter API Key
# load_dotenv()
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# from langchain.chat_models import ChatOpenAI


# # Setup OpenRouter LLM (Mixtral)
# llm = ChatOpenAI(
#     openai_api_base="https://openrouter.ai/api/v1",
#     openai_api_key=OPENROUTER_API_KEY,
#     model="mistralai/mixtral-8x7b",
#     temperature=0.3
# )

# parser = JsonOutputParser()

# def extract_order_info(state):
#     order_text = state["order_text"]
    
#     prompt = f"""
# You are an order processing assistant. Extract the following structured data from the user's order:

# - product: what item they want
# - quantity: how many units
# - destination: where the order should be delivered

# Return only valid JSON. Here is the order:
# {order_text}
# """

#     response = llm.invoke([HumanMessage(content=prompt)])
    
#     try:
#         structured_data = parser.invoke(response.content)
#     except Exception as e:
#         structured_data = {"error": str(e), "raw_response": response.content}

#     return {
#         "order": order_text,
#         "product": structured_data.get("product"),
#         "quantity": structured_data.get("quantity"),
#         "destination": structured_data.get("destination"),
#     }



# agents/order_manager.py

from langchain_core.messages import HumanMessage
from agents.openrouter_chat import ChatOpenRouter
import os
from dotenv import load_dotenv

load_dotenv()
import streamlit as st
# Get API key from Streamlit secrets first, fallback to .env
openai_api_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))

llm = ChatOpenRouter(model_name="mistralai/mixtral-8x7b-instruct")
print(openai_api_key)
from langchain_core.prompts import ChatPromptTemplate

system_prompt = """You are an assistant that extracts order information from text.
Only return JSON in this format:
{{
    "product": "<product_name>",
    "quantity": <integer>,
    "destination": "<destination>"
}}

Do NOT include explanations or extra text.
"""

user_prompt = """Order text: {order_text}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", user_prompt)
])

import json
from langchain_core.output_parsers import StrOutputParser

def extract_order_info(state: dict):
    order_text = state["order_text"]
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"order_text": order_text})

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print("❌ Failed to parse LLM response:", response)
        return {"product": None, "quantity": None, "destination": None}
