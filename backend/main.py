import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.cohere import Cohere
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever


from pinecone import Pinecone
from pydantic import BaseModel

load_dotenv()

embed_model = OpenAIEmbedding(
    api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-small", dimensions=1024
)

llm = Cohere(api_key=os.getenv("COHERE_API_KEY"), model="command-r")

# Set llm and embedding model for llama-index
Settings.llm = llm
Settings.embed_model = embed_model

# Connect to Pinecone index
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pc_index = pc.Index("dogmatics")

# Create vector store from existing index
vector_store = PineconeVectorStore(pinecone_index=pc_index)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

# Create retriever and query engine
# We're using the MetadataReplacementPostProcessor since we used the SentenceWindowNodeProcessor
retriever = VectorIndexRetriever(index=index, similarity_top_k=5)
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    node_postprocessors=[
        MetadataReplacementPostProcessor(target_metadata_key="window")
    ],
)

# Set up CORS for local development
origins = [
    "http://localhost:4321",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    text: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/query")
def query_index(query: Query):
    return query_engine.query(query.text)


# TODO
# Abstract llm, model, pinecone setup
# Add more documentation
