import csv
import os
import uuid
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from multi_tool_agent import agent

def test_full_response():
    """Test a lead providing all information."""
    lead_id = str(uuid.uuid4())
    lead_name = "TestUser"
    session_id = f"session_{lead_id}"
    user_id = f"user_{lead_id}"
    
    agent.initialize_csv()
    session_service = InMemorySessionService()
    agent.set_session_service(session_service)
    
    runner = Runner(agent=agent.agent, session_service=session_service)
    session = session_service.get_session(user_id, session_id)
    session.state["lead_id"] = lead_id
    session.state["lead_name"] = lead_name
    session.state["stage"] = "initial"
    
    responses = ["yes", "30", "Canada", "Consulting"]
    for response in responses:
        events = runner.stream_query(user_id=user_id, session_id=session_id, message=response)
        for event in events:
            pass
    
    # Verify CSV
    with open("leads.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        assert any(row[0] == lead_id and row[5] == "secured" for row in rows), "Full response test failed"

def test_no_consent():
    """Test a lead declining consent."""
    lead_id = str(uuid.uuid4())
    lead_name = "TestUser"
    session_id = f"session_{lead_id}"
    user_id = f"user_{lead_id}"
    
    agent.initialize_csv()
    session_service = InMemorySessionService()
    agent.set_session_service(session_service)
    
    runner = Runner(agent=agent.agent, session_service=session_service)
    session = session_service.get_session(user_id, session_id)
    session.state["lead_id"] = lead_id
    session.state["lead_name"] = lead_name
    session.state["stage"] = "initial"
    
    events = runner.stream_query(user_id=user_id, session_id=session_id, message="no")
    for event in events:
        pass
    
    # Verify CSV
    with open("leads.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        assert any(row[0] == lead_id and row[5] == "no_response" for row in rows), "No consent test failed"

def run_tests():
    """Run all test cases."""
    print("Running test cases...")
    test_full_response()
    print("Full response test passed.")
    test_no_consent()
    print("No consent test passed.")
    print("All tests passed.")

if __name__ == "__main__":
    run_tests()