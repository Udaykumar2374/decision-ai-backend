from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Literal
import logging

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Decision AI Backend")

# ⬇️ Your allowed frontends (add more domains if needed)
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://decision-ai-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,   # avoid "*"+credentials issues
    allow_credentials=False,         # set True only if you actually use cookies/auth headers
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Models -----
class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"] = "user"
    content: str = Field(..., min_length=1)

class ChatInput(BaseModel):
    messages: List[ChatMessage]

# ----- Routes -----
@app.get("/")
def root():
    return {"ok": True, "message": "API ready"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask_chat(input: ChatInput):
    try:
        from decision_logic import get_decision_advice
        answer = await get_decision_advice(input.messages)  # assumes async
        return {"answer": answer}
    except Exception as e:
        logger.exception("Error in /ask")
        raise HTTPException(status_code=500, detail=str(e))


# For local dev only (Render will ignore this if you run via uvicorn main:app)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
