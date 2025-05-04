from pydantic import BaseModel
from typing import List, Optional

class BotSettings(BaseModel):
    ai_model: str
    name: str
    role: str
    goal: str
    tasks: List[str]
    restrictions: List[str]
    group_trigger_name: Optional[str]
    check_subscription: bool
    group_type: Optional[str]
    subscription_group: Optional[str]
    subscription_group_id: Optional[str]
    subscription_message: Optional[str]
    language: str = "ru"
    show_typing_message: bool = False
    typing_message_text: Optional[str] = "Панда пишет..."
    knowledge_bases: List[str] = ["default"]