# This approach to setting up model is heavily take from
# create-llama (https://github.com/run-llama/create-llama)

import os

from dotenv import load_dotenv
from llama_index.core.settings import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.cohere import Cohere

load_dotenv()


# Hardcoding this to Cohere at the moment, but could be refactored to handle different llm providers
def configure_llm() -> dict:
    llm_model_name = os.getenv("LLM_MODEL_NAME")
    llm_api_key = os.getenv("COHERE_API_KEY")

    config = {
        "model": llm_model_name,
        "api_key": llm_api_key,
    }

    return config


# Hardcoding this to OpenAI at the moment, but could be refactored to handle different embedding model providers
def configure_embedding_model() -> dict:
    embed_model_name = os.getenv("EMBED_MODEL_NAME")
    embed_api_key = os.getenv("OPENAI_API_KEY")
    embed_dimensions = int(os.getenv("EMBED_DIMENSIONS"))

    config = {
        "model": embed_model_name,
        "api_key": embed_api_key,
        "dimensions": embed_dimensions,
    }

    return config


def init_settings():
    llm_config = configure_llm()
    embed_config = configure_embedding_model()

    Settings.llm = Cohere(**llm_config)
    Settings.embed_model = OpenAIEmbedding(**embed_config)
