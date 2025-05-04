from pydantic import BaseModel

class KnowledgeEntry(BaseModel):
    question: str
    keywords: str
    answer: str