Sales Agent with Google ADK and OpenAI API
This project implements a conversational sales agent using Google's Agent Development Kit (ADK) for orchestration and OpenAI’s API (GPT-4o-mini) for language processing, as a workaround for Vertex AI API issues. The agent meets the AI Assessment task requirements, handling multiple lead interactions, collecting information, and managing follow-ups.
Features

External Trigger: Simulates lead form submissions.
Lead Identification: Uses unique lead_id.
Conversational Flow: Collects consent, age, country, interest via OpenAI API.
Concurrent Conversations: Uses asyncio and ADK’s session service.
Follow-Up Mechanism: Sends follow-up messages after a 5-second delay (simulating 24 hours).
Data Storage: Saves to leads.csv with columns: lead_id, name, age, country, interest, status.
Session Management: ADK’s InMemorySessionService.

Setup Instructions
Prerequisites

Python 3.10+
OpenAI API key (free trial at platform.openai.com)
Local IDE (e.g., VS Code)


Install Dependencies:
pip install google-adk openai python-dotenv aiohttp


Configure Environment Variables:

Create multi_tool_agent/.env:OPENAI_API_KEY=your-openai-api-key


Initialize CSV File:

The agent creates leads.csv automatically.



Usage Guide
Running the Agent

Start the Agent:
python simulations/simulate_leads.py

Simulates three leads:

Alice: Full response.
Bob: Declines consent.
Charlie: Unresponsive, triggers follow-up.


Interact with the Agent:

View console output.
Check leads.csv.


Run Test Cases:
python simulations/test_cases.py

Verifies full response and no-consent scenarios.


Simulating Lead Interactions

simulate_leads.py generates lead_ids and response patterns.
Modify leads list to add new leads.
Follow-up delay is 5 seconds.

Design Decisions

Agent Architecture:
ADK orchestrates the agent; OpenAI’s GPT-4o-mini handles conversation due to Vertex AI issues.
Tools (handle_consent, etc.) modularize tasks.


Session Management:
ADK’s InMemorySessionService for context.
Conversation history stored in session for OpenAI.


Concurrent Handling:
asyncio for lead simulations.
ADK ensures thread-safe sessions.


Data Storage:
CSV with thread-safe writes.


Follow-Up Simulation:
5-second delay, tracked via last_interaction.



Assumptions

External trigger simulated.
24-hour delay shortened to 5 seconds.
Leads provide simple inputs.

Test Cases

Full Response:
Expected: status=secured in leads.csv.


No Consent:
Expected: status=no_response.


Unresponsive Lead:
Expected: Follow-up after delay.



Demonstration Video

Record a 5-10 minute video showing:
simulate_leads.py execution.
leads.csv output.
Follow-up message.
Code walkthrough, explaining ADK and OpenAI usage.


Save as demo.mp4 or link in README.

Troubleshooting

OpenAI API Errors: Verify API key and trial credits. Check rate limits.
ADK Issues: Ensure google-adk is installed correctly.
CSV Issues: Check directory permissions.

Notes

OpenAI’s API was used due to Vertex AI API issues, with ADK handling orchestration to meet task requirements.
Monitor OpenAI usage to stay within free trial limits.

References

ADK Quickstart
OpenAI API Docs

