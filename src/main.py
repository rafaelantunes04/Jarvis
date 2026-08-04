import uvicorn
from fastapi import FastAPI

from src.api_classes import ChatRequest, ChatResponse
from src.auth import verify_credentials
from src.chatbot import chat_with_llm
from src.memory import memory

from src.config import HOST, PORT

app = FastAPI()



@app.post("/chat", response_model = ChatResponse)
async def chat(req: ChatRequest):
    verify_credentials(username=req.username, password=req.password)
    
    user_message = req.message    

    long_term_memory = memory.get_long_term_memory(message=user_message)
    buffers = memory.get_history()

    result = chat_with_llm(message=req.message, history=buffers, long_term=long_term_memory)

    memory.add(new_question=user_message, new_answer=result)

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