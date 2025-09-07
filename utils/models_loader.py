import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq

# Load environment variables from .env
load_dotenv()


class ConfigLoader:
    """Loads configuration from YAML and provides dictionary-like access."""

    def __init__(self):
        print("Loaded config.....")
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]


class ModelLoader(BaseModel):

    model_provider: Literal["groq"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def model_post_init(self, __context: Any = None) -> None:
        self.config = ConfigLoader()

    def load_llm(self):
        
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")

        if self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY is missing in environment variables!")
            
            model_name = self.config["llm"]["groq"]["model_name"]
            llm = ChatGroq(model=model_name, api_key=groq_api_key)

        else:
            raise ValueError(f"Unknown model provider: {self.model_provider}")

        print("LLM loaded successfully.")
        return llm
