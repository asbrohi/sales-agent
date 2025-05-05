import csv
import os
from multi_tool_agent.mock_adk import Agent
from .tools import handle_consent, collect_age, collect_country, collect_interest, save_to_csv, call_openai

class SalesAgent:
    def __init__(self):
        self.agent = Agent(
            name="sales_agent",
            description="A conversational sales agent using OpenAI API for language processing.",
            instruction="""
You are a polite sales agent. Your goal is to engage leads, collect information step-by-step, and store it in a CSV file. Use the provided tools to:
1. Greet leads: "Hey [Lead Name], thank you for filling out the form. I'd like to gather some information from you. Is that okay?"
2. If agreed, ask for age, country, interest sequentially.
3. If declined, respond: "Alright, no problem. Have a great day!" and set status to 'no_response'.
4. Save data to leads.csv with status 'secured' after all answers.
5. For unresponsive leads (24 hours), send: "Just checking in to see if you're still interested. Let me know when you're ready to continue."
Use the call_openai tool for conversational responses when needed, and other tools for structured tasks.
""",
            tools=[handle_consent, collect_age, collect_country, collect_interest, save_to_csv, call_openai]
        )
        self.session_service = None

    def initialize_csv(self):
        if not os.path.exists("leads.csv"):
            with open("leads.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["lead_id", "name", "age", "country", "interest", "status"])

    def set_session_service(self, session_service):
        self.session_service = session_service