import os

from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()


def get_vector_index() -> VectorStoreIndex:
    # Connect to the pinecone index
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    pc_index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

    # Create vector store from existing index
    vector_store = PineconeVectorStore(pinecone_index=pc_index)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    return index
