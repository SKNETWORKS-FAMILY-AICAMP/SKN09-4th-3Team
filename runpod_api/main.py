from fastapi import FastAPI, Request
from pydantic import BaseModel
from inference import ask_question
from langchain_core.messages import HumanMessage, AIMessage
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 프론트 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    question: str
    history: list

@app.post("/chat")
async def chat_handler(data: ChatInput):
    history_msgs = [
        HumanMessage(content=m["content"]) if m["type"] == "human" else AIMessage(content=m["content"])
        for m in data.history
    ]
    answer, new_history = ask_question(data.question, history_msgs)
    return {
        "answer": answer,
        "history": [{"type": "human" if isinstance(m, HumanMessage) else "ai", "content": m.content} for m in new_history]
    }
