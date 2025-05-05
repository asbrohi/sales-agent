# Sales Agent with Google ADK (Mock Implementation)

This project implements a conversational sales agent using a mock version of Google's Agent Development Kit (ADK) in Python. The agent engages leads, collects information (age, country, interest) through a step-by-step conversational flow, handles multiple concurrent conversations, and follows up with unresponsive leads. Lead data is stored in a CSV file (`leads.csv`).

## Objective

The goal is to simulate a sales agent that:
- Initiates conversations with leads upon an external trigger (e.g., form submission).
- Collects information sequentially if the lead consents.
- Stores lead data in `leads.csv` with statuses (`secured`, `no_response`, `pending`).
- Manages concurrent lead interactions with independent session contexts.
- Sends follow-up messages to unresponsive leads after a simulated 24-hour delay.

## Features

- **Conversational Flow**: Greets leads, asks for consent, and collects age, country, and interest sequentially.
- **Consent Handling**: Proceeds with questions if the lead agrees; otherwise, ends the conversation politely.
- **Data Storage**: Saves lead information to `leads.csv` with appropriate status updates.
- **Concurrent Conversations**: Uses asyncio to handle multiple leads simultaneously, maintaining session state.
- **Follow-Up Mechanism**: Simulates a 24-hour delay (compressed to 5 seconds for testing) and sends follow-up messages to unresponsive leads.
- **Test Cases**: Includes tests for full response and no-consent scenarios.
- **OpenAI Integration**: Uses OpenAI's API for conversational responses when structured tools are insufficient.

## Prerequisites

- **Python**: 3.8 or higher
- **Dependencies**:
  - `openai`
  - `python-dotenv`
  - `pydantic`
- **OpenAI API Key**: Required for conversational processing. Set it in a `.env` file.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/sales-agent-adk.git
   cd sales-agent-adk
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install openai python-dotenv pydantic
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-openai-api-key
   ```

5. **Initialize the CSV File**:
   The agent automatically creates `leads.csv` if it doesn't exist when running the simulation.

## Usage Guide

### Running the Simulation

The `simulate_leads.py` script simulates interactions with three leads (Alice, Bob, Charlie) with different response patterns:
- Alice: Provides full responses (age, country, interest).
- Bob: Declines consent.
- Charlie: Provides partial responses and triggers a follow-up after a simulated delay.

To run the simulation:
```bash
python simulate_leads.py
```

**Output**:
- Console logs show the conversational flow for each lead.
- `leads.csv` is updated with lead data (e.g., `lead_id`, `name`, `age`, `country`, `interest`, `status`).

**Sample leads.csv**:
```
lead_id,name,age,country,interest,status
2740104f-507c-4a3d-9527-3ccb71a678ce,Bob,,,,no_response
4907584c-8d37-4a10-be06-93f59f357381,Alice,25,USA,Software,secured
0eaf780c-a0b2-4e99-9828-6c7ba7317c24,Charlie,30,,,pending
```

### Running Test Cases

The `test_cases.py` script includes two test cases:
- `test_full_response`: Verifies a lead providing all information results in a `secured` status.
- `test_no_consent`: Verifies a lead declining consent results in a `no_response` status.

To run the tests:
```bash
python test_cases.py
```

**Output**:
```
Running test cases...
Full response test passed.
No consent test passed.
All tests passed.
```

### File Structure

- `simulate_leads.py`: Main script to simulate lead interactions.
- `leads.csv`: Stores lead data (created/updated during execution).
- `test_cases.py`: Test cases for validating agent behavior.
- `agent.py`: Defines the `SalesAgent` class and initializes the agent.
- `tools.py`: Contains tools for handling consent, collecting data, saving to CSV, and calling OpenAI.
- `mock_adk.py`: Mock implementation of Google ADK components (`Agent`, `Runner`, `InMemorySessionService`).
- `__init__.py`: Initializes the `multi_tool_agent` package.
- `.env`: Stores the OpenAI API key (not included in the repository).

## Design Decisions

1. **Mock ADK Implementation**:
   - Since the actual Google ADK is not publicly available, a mock version (`mock_adk.py`) was created to simulate its functionality, including `Agent`, `Runner`, and `InMemorySessionService`.
   - The mock ADK supports tool-based interactions and session management, aligning with the task requirements.

2. **Session Management**:
   - Used an in-memory session service (`InMemorySessionService`) to store lead-specific states (e.g., `lead_id`, `stage`, `conversation`).
   - Each lead has a unique `session_id` tied to their `lead_id`, ensuring independent conversation contexts.

3. **Concurrent Conversations**:
   - Leveraged Python's `asyncio` to handle multiple lead interactions concurrently via `asyncio.gather`.
   - Ensures scalability for real-world scenarios with many leads.

4. **Follow-Up Mechanism**:
   - Simulated a 24-hour delay as 5 seconds for testing, as specified in the sandbox simulation requirement.
   - Tracks the last interaction time and triggers follow-ups for unresponsive leads.

5. **OpenAI Integration**:
   - Used OpenAI's `gpt-4o-mini` model for conversational responses when structured tools (e.g., `handle_consent`) are insufficient, such as for open-ended questions.
   - Stores conversation history in the session state to maintain context.

6. **Error Handling**:
   - Validated inputs (e.g., age as a positive integer, non-empty country/interest) to ensure data integrity.
   - Gracefully handles OpenAI API errors and logs them for debugging.

7. **Testing**:
   - Included test cases to cover critical scenarios (full response, no consent).
   - Tests verify CSV updates, ensuring data persistence and status accuracy.

## Assumptions

- The Google ADK is assumed to provide components like `Agent`, `Runner`, and `SessionService`, which were mocked based on typical agent framework patterns.
- Leads provide responses in a structured format for simulation purposes (e.g., "yes", "25", "USA").
- The OpenAI API key is available and properly configured in the `.env` file.
- The 24-hour delay is simulated as 5 seconds for testing, as per the sandbox requirement.

## Demonstration Video

A demonstration video (to be recorded) will showcase:
- Running `simulate_leads.py` to demonstrate concurrent lead interactions.
- Showing `leads.csv` updates for Alice (secured), Bob (no_response), and Charlie (pending with follow-up).
- Running `test_cases.py` to verify functionality.
- Explaining the codebase structure and key design decisions.
- 

## Additional Notes

- The project prioritizes showcasing agent orchestration, session management, and engineering thought process, as emphasized in the task.
- The CSV storage requirement is strictly followed, while session state is managed in-memory for simplicity.
- Future improvements could include persistent session storage (e.g., database) and more robust error handling for production use.

Good luck with the review, and thank you for evaluating this project!
