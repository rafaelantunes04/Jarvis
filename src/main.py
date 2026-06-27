import uvicorn
from fastapi import FastAPI

from src.api_classes import ChatRequest, ChatResponse
from src.auth import verify_credentials
from src.chatbot import chat_with_llm

from src.config import HOST, PORT

app = FastAPI()



@app.post("/chat", response_model = ChatResponse)
async def chat(req: ChatRequest):
    """
    Function to call directly with llm
    """
    verify_credentials(username=req.username, password=req.password)

    result = chat_with_llm(message=req.message)

    return ChatResponse(message=result)



# ----- MAIN -----
def run():
    uvicorn.run(
        "src.main:app",
        host = HOST,
        port = PORT,
        reload = True
    )


if __name__ == "__main__":
    run()