🚀 Aurora RAG Question Answering API

A lightweight Retrieval-Augmented Generation (RAG) system that can answer natural-language questions about Aurora members.
It works by retrieving and reasoning over their messages from the /messages API — just like an intelligent assistant that reads the chat history and gives you factual, grounded insights.

🧩 Overview

This service lets you ask questions such as:

“When is Layla planning her trip to London?”

“How many cars does Vikram Desai have?”

“What are Fatima’s favorite restaurants?”

and it replies with a grounded, AI-generated answer — inferred directly from real message data.

⚙️ Tech Stack
Component	Purpose
FastAPI	- Serves the REST API

Sentence-Transformers	- Creates dense vector embeddings

FAISS	- Performs similarity search on embeddings

Anthropic Claude	- Generates human-like, context-aware answers 

Python 3.10	- Runtime environment 

🧠 Bonus 1: Design Notes
✅ Chosen Approach — RAG (Retrieval-Augmented Generation) with Dense Embeddings

How it works:

Fetch all messages from /messages

Split them into smaller text chunks

Convert each chunk into an embedding (a vector of numbers) using Sentence-Transformers

Store all embeddings in a FAISS index for fast similarity search

When a user asks a question:

The system retrieves the most relevant chunks from FAISS

These chunks + the user’s question are sent to Claude (Anthropic) to generate a precise, grounded answer

Pros

✅ Grounded answers — the model responds using actual message data

⚡ Scales well — efficient for large message sets

💰 Cost-effective — only relevant data is sent to the LLM

🧱 Embeddings can be cached to improve speed

Cons

⚙️ Requires an embedding step and lightweight vector storage

🧩 Needs prompt tuning for consistent, concise answers

Why chosen:
This design offers the best balance of accuracy, cost-efficiency, and engineering simplicity for the Aurora AI assignment.

🔍 Bonus 2: Data Insights

After exploring the /messages dataset, a few interesting issues were found:

Issue	Description
🌀 Duplicate entries	Some messages appeared multiple times

📅 Mixed date formats	Both “March 3” and “2025-03-03” styles appeared

🔁 Conflicting facts	Different messages mentioned different details (e.g., car counts)

💭 Implicit preferences	Favorites or plans were implied rather than stated

🕓 Inconsistent timestamps	Some messages were out of order or dated in the future

Fixes used:

Removed duplicate messages before embedding

Normalized date formats

When conflicts appeared, kept the most recent message

Prompted the LLM to use cautious phrasing like “appears to prefer…”

📡 API Example

Endpoint:

GET /ask?question=


Example:

https://aurora-rag-api.onrender.com/ask?question=What%20are%20Fatima's%20favorite%20restaurants%3F


Response:

{
  "answer": "Based on Fatima's message history, her favorite restaurants appear to be high-end, Michelin-starred establishments including:\n\n1. **Le Bernardin** (New York) - seafood fine dining\n2. **Osteria Francescana** (Italy) - 3-Michelin-star restaurant\n3. **Alinea** (Chicago) - 3-Michelin-star restaurant, where she specifically requests chef's table seating\n\nThese are all world-renowned, exclusive fine dining restaurants, indicating Fatima prefers exceptional culinary experiences at top-tier establishments."
}

🧰 Local Setup

1️⃣ Clone the repository

git clone https://github.com/yashiagar2507/aurora-rag-api.git

cd aurora-rag-api


2️⃣ Install dependencies

pip install -r requirements.txt


3️⃣ Add your Anthropic API key in .env

ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxx


4️⃣ Run the FastAPI server

uvicorn main:app --port 8000

🌐 Live API Demo

You can try the deployed API instantly here 👇
👉 https://aurora-rag-api.onrender.com/docs

That link opens the FastAPI Swagger UI, where you can:

Click on the /ask endpoint

Enter any natural-language question (for example: “When is Layla traveling to London?”)

Click Execute to see the JSON answer response

👩‍💻 Author

Built by: Yashi Agarwal
GitHub: @yashiagar2507

Model: Claude Sonnet 4.5 via Anthropic API
Date: November 2025
