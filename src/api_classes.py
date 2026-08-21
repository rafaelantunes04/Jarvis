from pydantic import BaseModel

"""
Every class is inherited from BaseModel because its something from FastAPI to do Error Checks while sending/recieving headers
"""

class LoginRequest(BaseModel):
    """
    (Recieved Header)
    Class used by FastAPI for the login

    (Used in main.py on Login /POST arguments)
    """
    username: str
    password: str


class MemoryResponse(BaseModel):
    """
    (Recieved Header)
    Class used by FastAPI for the memory response

    (Used in main.py on Memory Response /POST arguments)
    """
    conv_buffer: list[dict]
    token_buffer: list[dict]
    long_term_memory: list


class ChatRequest(BaseModel):
    """
    (Recieved Header)
    Class used by FastAPI for the login + message header

    (Used in main.py on Login /POST arguments)
    """
    message: str


class ChatResponse(BaseModel):
    """
    (Sent Header)
    Class used by FastAPI to send the message to the user

    (Used in main.py on Login \POST return)
    """
    message: str
