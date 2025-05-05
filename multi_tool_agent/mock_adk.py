from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic import BaseModel, Field, SkipValidation
from typing import List, Optional
class InMemorySessionService:
    def __init__(self):
        self.sessions = {}

    def get_session(self, user_id, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = Session(user_id, session_id)
        return self.sessions[session_id]

class Session:
    def __init__(self, user_id, session_id):
        self.user_id = user_id
        self.session_id = session_id
        self.state = {}

class Agent(BaseModel):
    name: str
    model: str = Field(default="gpt-4o-mini")
    description: str
    instruction: str
    tools: List[SkipValidation[callable]]

    class Config:
        arbitrary_types_allowed = True

class Runner:
    def __init__(self, agent, session_service):
        self.agent = agent
        self.session_service = session_service

    def stream_query(self, user_id, session_id, message):
        session = self.session_service.get_session(user_id, session_id)
        current_stage = session.state.get("stage", "initial")
        
        tools = {
            "initial": self.agent.tools[0],  # handle_consent
            "collect_age": self.agent.tools[1],  # collect_age
            "collect_country": self.agent.tools[2],  # collect_country
            "collect_interest": self.agent.tools[3]  # collect_interest
        }
        
        tool = tools.get(current_stage)
        if not tool:
            if current_stage == "completed":
                result = self.agent.tools[5](message, session.state)  # call_openai
            else:
                return [{"content": {"parts": [{"text": "Conversation ended."}]}}]
        else:
            lead_id = session.state.get("lead_id", "unknown")
            lead_name = session.state.get("lead_name") if current_stage == "initial" else None
            if current_stage == "initial":
                result = tool(lead_id, lead_name, message, session.state)
            else:
                result = tool(lead_id, message, session.state)
        
        return [{"content": {"parts": [{"text": result["message"]}]}}]
