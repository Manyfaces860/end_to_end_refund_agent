

from pydantic import BaseModel
from constants import MAX_MESSAGES_THRESHOLD
from prompts import AGENT_INPUT_PROMPT_TEMPLATE, REFUND_AGENT_PROMPT
from setup import redis_client
from schema import ChatSessionRuntime
from db_models import *
from utility import create_new_session


class ChatSession():
    def __init__(self, query: str, chat_session_key: str = ''):

        raw = None
        if chat_session_key:
            raw = redis_client.get(
                "session:"+chat_session_key,
            )

        self.chat_session: ChatSessionRuntime
        if raw:
            self.chat_session = ChatSessionRuntime.model_validate_json(raw) # type: ignore
        else:
            self.chat_session = ChatSessionRuntime(
                query=query,
                recent_messages=[],
                refund_resolved=False,
                session_key=create_new_session()
            )
    
    def update_state(self):
        redis_client.set(
            "session:" + self.chat_session.session_key,
            self.chat_session.model_dump_json()
        )
    
    def update_recent_messages_buffer(self):
        
        for msg in self.chat_session.recent_messages:
            print(msg, "before")
        self.chat_session.recent_messages = self.chat_session.recent_messages[MAX_MESSAGES_THRESHOLD-4:]
        for msg in self.chat_session.recent_messages:
            print(msg, "after")
            
    def __build_input(self, summarise: str) -> str:
        return AGENT_INPUT_PROMPT_TEMPLATE.format(
            conversation_summary=self.chat_session.conversation_summary,
            recent_messages="\n".join(
                [
                    f"{msg['role'].upper()}: {msg['content']}" 
                    if msg else "" 
                    for msg in self.chat_session.recent_messages[:-1]
                ]
            ),
            summarise=summarise,
            user_message=self.chat_session.recent_messages[-1]['content']
        )
        
    def get_agent_input(self, summarise: str = 'NO') -> str:
        return self.__build_input(summarise) 
        
    
        
    