import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever

from pydantic import BaseModel

from app.settings import init_settings
from app.database import get_vector_index


# Set up llm and embedding model
init_settings()

# Instantiate vector index
index = get_vector_index()

# Create retriever and query engine
# We're using the MetadataReplacementPostProcessor since we used the SentenceWindowNodeProcessor for chunking
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

# Instantiate app w/ CORS
app = FastAPI(
    title="Ask the Dogmatics",
    description="Ask the Dogmatics is an API for using retrieval augmented generation of the English translation of Karl Barth's Church Dogmatics",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define a query model - for now it's just a single string
class Query(BaseModel):
    text: str


# Redirect root url to API docs
@app.get("/")
def root():
    return RedirectResponse(url="/docs")


# Define a query route that takes a query and returns
# a generated response from an LLM
@app.post("/query")
def query_index(query: Query):
    return query_engine.query(query.text)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
