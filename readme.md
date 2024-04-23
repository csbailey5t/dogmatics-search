# Searching Barth's Church Dogmatics

## Overview

Karl Barth's *Church Dogmatics* is a massive theological work, and while it's very possible for a single person to read and grasp the whole, it's difficult for an individual to retrieve minute details from across the full scope. 

Given the expansive character of Barth's *Dogmatics* and its particular rhetorical approaches, I've been experimenting with computational methods for understanding, analyzing, and reading the *Dogmatics* for many years. It's both a source of academic interest and a useful example corpus for learning new methods and libraries.

N.B. — The TEI of the Church Dogmatics is under copyright, and provided to me years ago for research purposes by the Center for Barth Studies at Princeton. Given copyright restrictions, the XML files are not shared here, outputs from notebooks are cleared, and I've built the backend and frontend applications to be run locally, though they could be deployed under permissions at a later point. 

This current effort is effectively an attempt to build a research assistant for working Barth's Dogmatics, and this particular repository covers a few things (so far)

`data-prep` contains code for parsing the TEI version of the English translation of the *Dogmatics*, generating embeddings of the chunked text with OpenAI, and storing the embeddings in a Pinecone vector database. I use `llama-index` as a convenient framework to handle chunking, embedding, and upload to Pinecone. I've also used Jupyter notebooks given the iterative character of data cleaning and preparation. 

`backend` contains a simple FastAPI app for retrieval augemented generation over the Dogmatics embeddings. For now, there's a single route at `/query` that takes a question (prompt) and returns a response. I'm using `llama-index` again to take advantage of the query engine and `MetadataReplacementPostProceesor`, which pairs with the `SentenceWindowNodeParser` I used to provide additional sentence context for embeddings during generation. Given the character of Barth's writing, the additional window *may* provide higher quality generation, but I'll test against other approaches in future iterations. 

`frontend` contains a simple Astro application with a bit of React and Tailwind for styles. For now, there's a single form to submit a query to the backend and display a response. I chose Astro for ease of use (I have prior experience), and it will enable me to quick build other pages and interfaces as I develop this project and document results. 

Next steps:
- Create a chat endpoint and frontend interface for iterative response development
- Implement `dev` vs `production` environments to facilitate deployment

## Running code from the repository

Each major directory in the repository has its own dependencies and runs differently, though `data-prep` and `backend` both use Poetry for dependency and environment management. See [poetry](https://python-poetry.org/) for instructions on installation and use. 

Clone this repository with `git` following the directions opened by clicking the green "Code" button in the repo. 

### Setting up and running `data-prep` and `backend`

For `data-prep` and `backend`, navigate into the directory, then install dependencies:

```poetry install```

There is a `.env.example` file in both directories; copy it to `.env` and replace with your own API keys or LLM configuration. 

The notebooks in `data-prep` can be run in VS Code or through any preferred Jupyter notebook server/application. 

From within the `backend` dir, run the FastAPI app:

```poetry run python main.py```

and navigate to the url provided. 

### Setting up and running the `frontend` application

Within the `frontend` directory, run

```pnpm install``` 

to install dependencies. 

To run the application locally: 

```pnpm run dev```

and navigate to the url provided. 

See the `readme.md` file in `frontend` for additional options for building the application.
