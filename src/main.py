import ollama
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from src.auth import LoginRequest, verify_credentials

load_dotenv()

app = FastAPI()


class ChatRequest(BaseModel):
    username: str
    password: str
    message: str
    model: str = "llama3.2:1b"


class ChatResponse(BaseModel):
    message: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    verify_credentials(LoginRequest(username=req.username, password=req.password))

    response = ollama.chat(
        model=req.model,
        messages=[{"role": "user", "content": req.message}],
    )

    return ChatResponse(message=response.message.content)


def run():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()