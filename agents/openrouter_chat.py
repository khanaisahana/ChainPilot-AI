# agents/openrouter_chat.py

import os
from dotenv import load_dotenv
from typing import Optional
from pydantic import Field, SecretStr
from langchain_openai import ChatOpenAI
from langchain_core.utils.utils import secret_from_env
import streamlit as st
load_dotenv()

class ChatOpenRouter(ChatOpenAI):
    openai_api_key: Optional[SecretStr] = Field(
        alias="api_key", default_factory=secret_from_env("OPENROUTER_API_KEY", default=None)
    )

    @property
    def lc_secrets(self) -> dict[str, str]:
        return {"openai_api_key": "OPENROUTER_API_KEY"}

    def __init__(self, model_name: str = None, **kwargs):
        # Get API key from Streamlit secrets first, fallback to .env
        api_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))
        super().__init__(
            model=model_name,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            **kwargs
        )
