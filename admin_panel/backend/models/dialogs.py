from pydantic import BaseModel

class DialogEntry(BaseModel):
    question: str
    answer: str