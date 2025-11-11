from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import os, json, faiss, numpy as np, httpx
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from anthropic import Anthropic

# -------------------------
# CONFIG
# -------------------------
load_dotenv()

API_URL = "https://november7-730026606190.europe-west1.run.app/messages/"
MODEL_NAME = "all-MiniLM-L6-v2"
CLAUDE_MODEL = "claude-opus-4-1-20250805"  # ✅ Most powerful available
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")

# Create /cache folder
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

EMB_PATH = os.path.join(CACHE_DIR, "embeddings.npy")
IDX_PATH = os.path.join(CACHE_DIR, "faiss.index")
TXT_PATH = os.path.join(CACHE_DIR, "texts.json")

app = FastAPI(title="Aurora RAG API (Claude + Cached FAISS)")

# -------------------------
# Load messages
# -------------------------
async def load_messages():
    """Load messages from Aurora API or local fallback file."""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
            r = await client.get(API_URL)
            r.raise_for_status()
            data = r.json()
            if isinstance(data, dict) and "items" in data:
                return data["items"]
            elif isinstance(data, list):
                return data
    except Exception as e:
        print("⚠️ Falling back to local file:", e)
        path = os.path.join(os.path.dirname(__file__), "messages_sample.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "items" in data:
                return data["items"]
            return data

# -------------------------
# Build or load FAISS index
# -------------------------
model = SentenceTransformer(MODEL_NAME)

def build_index(messages):
    """Create FAISS index or load cached one."""
    if os.path.exists(EMB_PATH) and os.path.exists(IDX_PATH) and os.path.exists(TXT_PATH):
        print("✅ Using cached FAISS index and embeddings from /cache/")
        vectors = np.load(EMB_PATH)
        index = faiss.read_index(IDX_PATH)
        with open(TXT_PATH, "r", encoding="utf-8") as f:
            texts = json.load(f)
        return index, texts

    print("⚙️ Building new FAISS index...")
    texts = [m["message"] for m in messages]
    vectors = model.encode(texts, convert_to_numpy=True)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(np.array(vectors, dtype=np.float32))

    np.save(EMB_PATH, vectors)
    faiss.write_index(index, IDX_PATH)
    with open(TXT_PATH, "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)

    print("💾 Saved embeddings and index in /cache/ for future runs.")
    return index, texts

# -------------------------
# Retrieve top-k matches
# -------------------------
def retrieve_top_k(question, index, texts, k=5):
    q_vec = model.encode([question], convert_to_numpy=True)
    D, I = index.search(np.array(q_vec, dtype=np.float32), k)
    return [texts[i] for i in I[0]]

# -------------------------
# Claude Query Function
# -------------------------
anthropic_client = Anthropic(api_key=ANTHROPIC_KEY)

async def query_claude(question: str, context: str):
    """Send query to Claude (Opus 4.1)."""
    prompt = f"""
You are a helpful AI that answers questions about Aurora members based on their message history.

Messages:
{context}

Question:
{question}

Answer concisely and factually, inferring likely answers even if not explicitly stated.
"""

    try:
        message = anthropic_client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Error from Claude: {e}"

# -------------------------
# Streaming version (Claude)
# -------------------------
async def stream_from_claude(question: str, context: str):
    """Stream Claude output token-by-token."""
    prompt = f"""
You are a helpful AI that answers questions about Aurora members based on their message history.

Messages:
{context}

Question:
{question}

Answer concisely and factually.
"""
    async def token_generator():
        try:
            with anthropic_client.messages.stream(
                model=CLAUDE_MODEL,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                for event in stream:
                    if hasattr(event, "delta") and hasattr(event.delta, "text"):
                        yield event.delta.text
                    elif hasattr(event, "message_stop"):
                        break
        except Exception as e:
            yield f"[Error: {e}]"

    return StreamingResponse(token_generator(), media_type="text/plain")

# -------------------------
# ASK Endpoint
# -------------------------
@app.get("/ask")
async def ask(question: str = Query(...), stream: bool = False):
    messages = await load_messages()
    index, texts = build_index(messages)
    top_texts = retrieve_top_k(question, index, texts, k=10)
    context = "\n\n".join(top_texts)

    if stream:
        return await stream_from_claude(question, context)

    answer = await query_claude(question, context)
    return {"answer": answer}

# -------------------------
# Debug Helpers
# -------------------------
@app.get("/debug")
async def debug():
    msgs = await load_messages()
    return {"count": len(msgs), "sample": msgs[:3]}

@app.get("/names")
async def names():
    msgs = await load_messages()
    names = sorted({m.get("user_name", "") for m in msgs if m.get("user_name")})
    return {"unique_names": names, "count": len(names)}
@app.get("/")
def home():
    return {
        "message": "✅ Aurora RAG API is live!",
        "endpoints": {
            "ask": "/ask?question=Your%20Query",
            "docs": "/docs"
        }
    }
