# Searching Barth's Church Dogmatics

Karl Barth's *Church Dogmatics* is a massive theological work, and while it's very possible for a single person to read and grasp the whole, it's difficult for an individual to retrieve minute details from across the full scope. 

Given the expansive character of Barth's *Dogmatics* and its particular rhetorical approaches, I've been experimenting with computational methods for understanding, analyzing, and reading the *Dogmatics* for many years. It's both a source of academic interest and a useful example corpus for learning new methods and libraries. 

This particular repository covers a few things (so far):
- a Python notebook for parsing the TEI version of the English translation of the *Dogmatics*
- a Python notebook for generating embeddings of the text with Cohere and using retrieval augmented generation (RAG) across those embeddings. The notebook currently uses llama-index as a framework, with Pinecone as a vector store. 
- To come: a full front-end interface using `create-llama`, with a larger set of parsed texts.

## Running code from the repository

Clone this repository with `git` following the directions opened by clicking the green "Code" button in the repo. 

I'm using `poetry` for managing dependencies and environment management. See [poetry](https://python-poetry.org/) for instructions on installation and use. 

Install dependencies:

```poetry install```

The code for generating and storing embeddings depends on Cohere and Pinecone, and reads API keys from a `.env` file. 

Copy the `.env-sample` file to `.env` and replace the values with your own. 

