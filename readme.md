🚀 Aurora RAG Question Answering API

A lightweight Retrieval-Augmented Generation (RAG) system that answers natural language questions about Aurora members by retrieving and reasoning over their messages from the /messages API.

🧩 Overview

This service accepts a natural-language question such as:

“When is Layla planning her trip to London?”
“How many cars does Vikram Desai have?”
“What are Fatima’s favorite restaurants?”

and returns a grounded, AI-generated answer inferred from real message data.

⚙️ Tech Stack

FastAPI – for serving the API

Sentence-Transformers – for dense embeddings

FAISS – for similarity search

Anthropic Claude – for reasoning and language generation

Python 3.10 – runtime environment

🧠 Bonus 1: Design Notes
B) RAG (Retrieval-Augmented Generation) with dense embeddings ✅ (Chosen)
How it works:

Fetch all messages from /messages.

Split them into smaller text chunks.

Convert each chunk into an embedding (vector of numbers) using Sentence-Transformers.

Store all embeddings inside a FAISS index for fast similarity search.

When the user asks a question:

The system retrieves the top relevant chunks from FAISS.

These chunks, plus the question, are sent to the Claude model (Anthropic) to generate the answer.

Pros

✅ Gives grounded answers based on real data.
⚡ Scales well for large message sets.
💰 Cheaper than sending all data to the model every time.
🧱 Embeddings can be cached for speed.

Cons

⚙️ Needs an embedding step and light storage.
🧩 Requires prompt tuning for consistent answers.

Why chosen:
This approach provides the best balance of accuracy, cost efficiency, and engineering simplicity for the assignment.

🔍 Bonus 2: Data Insights

After exploring the /messages dataset, a few issues were observed:

Issue	Description
🌀 Duplicate entries	Some messages appear multiple times, leading to redundancy.
📅 Mixed date formats	Dates appear both as “March 3” and “2025-03-03”.
🔁 Conflicting facts	Users occasionally mention inconsistent details (e.g., different car counts).
💭 Implicit preferences	Favorites and plans are often implied, not explicitly stated.
🕓 Inconsistent timestamps	Some entries are misordered or future-dated.
Fixes Used

Removed duplicate messages before embedding.

Normalized date formats for clarity.

When conflicts appeared, prioritized the most recent message.

Prompted the LLM to hedge uncertain facts (e.g., “appears to prefer…”).

📡 API Example
Endpoint:
GET /ask?question=<your-question>

Example:
curl "http://127.0.0.1:8000/ask?question=What are Fatima's favorite restaurants?"


Response:

{
  "answer": "Fatima appears to favor high-end, Michelin-starred restaurants like Le Bernardin, Osteria Francescana, and Alinea."
}

🧰 Local Setup

1️⃣ Clone the repo

git clone https://github.com/yashiagar2507/aurora-rag-api.git

cd aurora-rag-api


2️⃣ Install dependencies

pip install -r requirements.txt


3️⃣ Add your Anthropic API key in .env

ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxx


4️⃣ Run the FastAPI server

uvicorn main:app --port 8000

Built by Yashi Agarwal
GitHub: @yashiagar2507

Model: Claude Sonnet 4.5 via Anthropic API
Date: November 2025

