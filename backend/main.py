import comet_llm
import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from llama_index.core import PromptTemplate
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever

from pydantic import BaseModel

from app.settings import init_settings
from app.database import get_vector_index
from app.response import APIResponse


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

# Define a custom prompt to encourage citation
qa_citation_prompt_template_str = (
    "You are a Protestant theologian, and a careful reader of theology. Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given just this information and no prior knowledge, please answer the question: {query_str}\n"
    "Provide reference citations from the context in your answer. If the provided context uses more than one volume from the Dogmatics, use at least two volumes in your answer."
)
qa_prompt_template = PromptTemplate(qa_citation_prompt_template_str)
query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": qa_prompt_template}
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
    api_response = query_engine.query(query.text)

    # # Given the response.metadata, get the set of volumes in the response
    # volumes_set = {metadata["volume"] for metadata in response.metadata.values()}
    # volumes = " ".join(volumes_set)

    response = APIResponse(
        response_text=api_response.response, metadata=api_response.metadata
    )

    comet_llm.log_prompt(
        api_key=os.getenv("COMET_API_KEY"),
        project="barth",
        prompt=qa_citation_prompt_template_str.format(
            query_str=query.text, context_str="RETRIEVED DOCUMENTS"
        ),
        prompt_template=qa_citation_prompt_template_str,
        output=response.response_text,
        prompt_template_variables={"query": query.text},
        metadata={"volumes": response.sources},
    )

    return response.model_dump_json(
        include={"response_text", "metadata", "sources"}, exclude_none=True
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
