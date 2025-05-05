import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import uuid
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from multi_tool_agent.mock_adk import Runner, InMemorySessionService
from multi_tool_agent import agent
from multi_tool_agent.tools import save_to_csv

class Session:
    def __init__(self):
        self.state = {}

class SimpleSessionService:
    def __init__(self):
        self.sessions = {}

    def get_session(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = Session()
        return self.sessions[session_id]

async def simulate_lead(lead_id, lead_name, response_pattern, delay_simulation=False):
    print(f"Starting simulation for Lead {lead_id} ({lead_name})")  # Debug log
    session_id = f"session_{lead_id}"
    user_id = f"user_{lead_id}"
    runner = Runner(agent=agent.agent, session_service=agent.session_service)
    
    # Initialize session state
    session = agent.session_service.get_session(user_id, session_id)
    session.state["lead_id"] = lead_id
    session.state["lead_name"] = lead_name
    session.state["stage"] = "initial"
    session.state["status"] = "pending"
    session.state["last_interaction"] = datetime.now(ZoneInfo("UTC")).isoformat()
    
    initial_message = f"Hey {lead_name}, thank you for filling out the form. I'd like to gather some information from you. Is that okay?"
    print(f"[Lead {lead_id}] Agent: {initial_message}")
    
    for response in response_pattern:
        if response is None and delay_simulation:
            print(f"[Lead {lead_id}] Simulating 24-hour delay...")
            await asyncio.sleep(5)  # Simulate 24-hour delay as 5 seconds
            last_interaction = datetime.fromisoformat(session.state["last_interaction"])
            if datetime.now(ZoneInfo("UTC")) - last_interaction > timedelta(seconds=5):
                follow_up = "Just checking in to see if you're still interested. Let me know when you're ready to continue."
                print(f"[Lead {lead_id}] Agent: {follow_up}")
                session.state["status"] = "pending"
                save_to_csv(
                    lead_id,
                    session.state.get("lead_name", ""),
                    session.state.get("age", ""),
                    session.state.get("country", ""),
                    session.state.get("interest", ""),
                    "pending",
                    session.state
                )
                session.state["last_interaction"] = datetime.now(ZoneInfo("UTC")).isoformat()
            continue
        print(f"[Lead {lead_id}] Lead: {response}")   
        # Process response
        events = runner.stream_query(user_id=user_id, session_id=session_id, message=response)
        for event in events:
            if event["content"].get("parts"):
                message = event["content"]["parts"][0]["text"]
                print(f"[Lead {lead_id}] Agent: {message}")
                session.state["last_interaction"] = datetime.now(ZoneInfo("UTC")).isoformat()
        await asyncio.sleep(random.uniform(0.5, 2.0))

async def main():
    agent.initialize_csv()
    agent.set_session_service(InMemorySessionService())  # Reset session service
    
    leads = [
        {"lead_id": str(uuid.uuid4()), "lead_name": "Alice", "responses": ["yes", "25", "USA", "Software", "Can you tell me more about the software?"]},
        {"lead_id": str(uuid.uuid4()), "lead_name": "Bob", "responses": ["no"]},
        {"lead_id": str(uuid.uuid4()), "lead_name": "Charlie", "responses": ["yes", "30", None]},
    ]
    
    tasks = [
        simulate_lead(lead["lead_id"], lead["lead_name"], lead["responses"], delay_simulation=(lead["lead_name"] == "Charlie"))
        for lead in leads
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())