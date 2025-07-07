from typing import Dict, List
from pydantic import BaseModel

class ConversationMemory(BaseModel):
    history: List[Dict[str, str]] = []
    context: Dict[str, str] = {}
    
    def add_interaction(self, user_query: str, system_response: str):
        self.history.append({
            'user': user_query,
            'system': system_response
        })
        # Keep only last N interactions
        if len(self.history) > 5:
            self.history.pop(0)
            
    def get_context(self) -> str:
        return "\n".join(
            f"User: {item['user']}\nSystem: {item['system']}" 
            for item in self.history
        )

memory = ConversationMemory()