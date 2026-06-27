from pydantic import BaseModel

"""
Every class is inherited from BaseModel because its something from FastAPI to do Error Checks while sending/recieving headers
"""

class ChatRequest(BaseModel):
    """
    (Recieved Header)
    Class used by FastAPI for the login + message header

    (Used in main.py on Login \POST arguments)
    """
    username: str
    password: str
    message: str



class ChatResponse(BaseModel):
    """
    (Sent Header)
    Class used by FastAPI to send the message to the user

    (Used in main.py on Login \POST return)
    """
    message: str
