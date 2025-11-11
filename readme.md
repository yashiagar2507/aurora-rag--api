Bonus 1: Design Notes
🧠 B) RAG (Retrieval-Augmented Generation) with dense embeddings ✅ (Chosen)

How it works:

Fetch all messages from /messages.

Split them into smaller text chunks.

Convert each chunk into an embedding (a vector of numbers) using Sentence-Transformers.

Store all embeddings inside a FAISS index for fast similarity search.

When the user asks a question:

The system retrieves the top relevant chunks from FAISS.

These chunks, plus the question, are sent to the Claude model (Anthropic) to generate the answer.

Pros:

Gives grounded answers based on real data.

Scales well for large message sets.

Cheaper than sending all data to the model every time.

Embeddings can be cached for speed.

Cons:

Needs an embedding step and light storage.

Requires some prompt design for consistent answers.

Why chosen:
It’s the best balance between accuracy, cost, and engineering effort for this project.