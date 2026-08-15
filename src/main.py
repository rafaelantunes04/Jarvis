import uvicorn
from fastapi import Depends, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from src.api_classes import ChatRequest, ChatResponse, LoginRequest, MemoryResponse

from src.chatbot import chat_with_llm

from src.auth import authenticator
from src.memory import memory

from src.config import HOST, PORT

app = FastAPI()

# Safe Cookies Tauri
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:1420", "tauri://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login")
async def login(req: LoginRequest, response: Response):
    token = authenticator.verify_login(username=req.username, password=req.password)

    response.set_cookie(
        key="token",
        secure=True,
        value=token,
        httponly=True,
        samesite="strict",
        max_age=30 * 60,
        path="/",
    )


@app.post("/logout")
async def logout(response: Response, user: dict = Depends(authenticator.verify_token)):
    response.delete_cookie(key="token", path="/")
    return {"detail": "Sessão terminada."}


# @app.post("/memory", response_model = MemoryResponse)
# async def memory_request(user: dict = Depends(authenticator.verify_token)):
#     ...

@app.post("/chat", response_model = ChatResponse)
async def chat(req: ChatRequest, user: dict = Depends(authenticator.verify_token)):

    # long_term_memory = memory.get_long_term_memory(message=req.message)
    long_term_memory = None

    buffers = memory.get_history()

    result = chat_with_llm(message=req.message, history=buffers, long_term=long_term_memory)

    memory.add(new_question=req.message, new_answer=result)

    return ChatResponse(message=result)



# ----- MAIN -----
def run():
    uvicorn.run(
        "src.main:app",
        host = HOST,
        port = PORT,
        reload = False
    )


if __name__ == "__main__":
    run()