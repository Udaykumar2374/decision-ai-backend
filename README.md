# Decidely API (FastAPI + Uvicorn)

Stateless API that processes user questions and returns structured AI advice. Designed to be called by the Decidely Next.js frontend.

---

## 1) Prerequisites

- Python 3.10+
- Git + GitHub account
- (Optional) Render account for hosting

---

## 2) Environment Variables

Create `./.env` (or set in Render dashboard):

\`\`\`env
# Model provider (example: OpenRouter)
OPENROUTER_API_KEY=replace_me

# Optional CORS allowlist (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app

# Optional: port override (Render uses its own)
PORT=10000
\`\`\`

---

## 3) Install & Run

\`\`\`bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
\`\`\`

- API will run on `http://localhost:8000`.

**Minimal `requirements.txt` example:**

\`\`\`
fastapi==0.111.0
uvicorn[standard]==0.30.0
pydantic==2.7.0
python-dotenv==1.0.1
httpx==0.27.0
\`\`\`

---

## 4) Example `main.py`

\`\`\`py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

class AskRequest(BaseModel):
    question: str
    context: str | None = None
    sessionId: str | None = None

class AskResponse(BaseModel):
    sessionId: str
    answer: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    # TODO: call your model provider (OpenRouter, etc.)
    answer = f"Here’s a structured take on: {req.question}"
    return {"sessionId": req.sessionId or "new-session-id", "answer": answer}
\`\`\`

---

## 5) API Endpoints

### `GET /health`
- Health probe.
- **200** → `{ "status": "ok" }`

### `POST /ask`
Request:
\`\`\`json
{
  "question": "Should I move to NYC?",
  "context": "Offer: $120k, rent $2.8k",
  "sessionId": "optional-existing-session-id"
}
\`\`\`

Response:
\`\`\`json
{
  "sessionId": "existing-or-new-id",
  "answer": "Concise, structured advice..."
}
\`\`\`

---

## 6) cURL Test

\`\`\`bash
curl -X POST http://localhost:8000/ask   -H "Content-Type: application/json"   -d '{"question":"Should I switch jobs?","context":"Offer +20% pay"}'
\`\`\`

---

## 7) Deploy (Render)

1. Push backend to GitHub.
2. In **Render** → **New +** → **Web Service** → connect repo.
3. Settings:
   - **Environment**: Python 3.10+
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
   - **Port**: `10000`
   - **Env Vars**:
     - `OPENROUTER_API_KEY=...`
     - `ALLOWED_ORIGINS=https://your-frontend.vercel.app`
4. Deploy → note the public URL like `https://decidely-api.onrender.com`.

Update your frontend `.env.local`:

\`\`\`env
NEXT_PUBLIC_BACKEND_API=https://decidely-api.onrender.com
\`\`\`

---

## 8) Security & CORS

- Always set `ALLOWED_ORIGINS` to your production frontend domain(s).
- Add rate limiting / auth gates if you expose more endpoints.
- Never commit real API keys.

---

## 9) Troubleshooting

- **CORS blocked**: Check `ALLOWED_ORIGINS` matches the exact scheme + host.
- **502 / timeouts on Render**: cold starts on free tier; try restarting or upgrading instance.
- **Model errors**: verify `OPENROUTER_API_KEY` and provider request payloads.

---

## 10) License

MIT (or your choice)

---

## Quick Launch Checklist

- [ ] Frontend `.env.local` set (Firebase + `NEXT_PUBLIC_BACKEND_API`)
- [ ] Backend `.env` set (`OPENROUTER_API_KEY`, `ALLOWED_ORIGINS`)
- [ ] Firestore rules published
- [ ] Local test: `npm run dev` (frontend) + `uvicorn` (backend)
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend to Render
- [ ] Update frontend to use deployed API URL
