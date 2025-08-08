from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from decision_logic import get_decision_advice

app = FastAPI()

# Allow CORS from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatInput(BaseModel):
    messages: List[ChatMessage]

@app.post("/ask")
async def ask_chat(input: ChatInput):
    response = await get_decision_advice(input.messages)
    return {"answer": response}
