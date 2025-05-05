import csv
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def handle_consent(lead_id: str, lead_name: str, response: str, session: dict) -> dict:
    """Handles the lead's consent response and updates session state."""
    session["lead_id"] = lead_id
    session["lead_name"] = lead_name
    session["last_interaction"] = datetime.now(ZoneInfo("UTC")).isoformat()
    session["conversation"] = [
        {"role": "system", "content": "You are a polite sales agent. Handle responses based on provided tools."},
        {"role": "user", "content": f"Hey {lead_name}, thank you for filling out the form. I'd like to gather some information from you. Is that okay?"}
    ]
    
    if response.lower() in ["yes", "y"]:
        session["stage"] = "collect_age"
        session["status"] = "active"
        session["conversation"].append({"role": "user", "content": response})
        session["conversation"].append({"role": "assistant", "content": "Great! What is your age?"})
        return {"status": "success", "message": "Great! What is your age?"}
    else:
        session["stage"] = "ended"
        session["status"] = "no_response"
        session["conversation"].append({"role": "user", "content": response})
        session["conversation"].append({"role": "assistant", "content": "Alright, no problem. Have a great day!"})
        save_to_csv(lead_id, lead_name, "", "", "", "no_response", session)
        return {"status": "success", "message": "Alright, no problem. Have a great day!"}

def collect_age(lead_id: str, age: str, session: dict) -> dict:
    """Collects the lead's age and updates session state."""
    try:
        age_int = int(age)
        if age_int < 0:
            return {"status": "error", "message": "Please provide a valid age."}
        session["age"] = age_int
        session["stage"] = "collect_country"
        session["last_interaction"] = datetime.now(ZoneInfo("UTC")).isoformat()
        session["conversation"].append({"role": "user", "content": str(age)})
        session["conversation"].append({"role": "assistant", "content": "Which country are you from?"})
        return {"status": "success", "message": "Which country are you from?"}
    except ValueError:
        return {"status": "error", "message": "Please provide a valid age."}

def collect_country(lead_id: str, country: str, session: dict) -> dict:
    """Collects the lead's country and updates session state."""
    if not country.strip():
        return {"status": "error", "message": "Please provide a valid country."}
    session["country"] = country
    session["stage"] = "collect_interest"
    session["last_interaction"] = datetime.now(ZoneInfo("UTC")).isoformat()
    session["conversation"].append({"role": "user", "content": country})
    session["conversation"].append({"role": "assistant", "content": "What product or service are you interested in?"})
    return {"status": "success", "message": "What product or service are you interested in?"}

def collect_interest(lead_id: str, interest: str, session: dict) -> dict:
    """Collects the lead's interest and triggers data saving."""
    if not interest.strip():
        return {"status": "error", "message": "Please provide a valid interest."}
    session["interest"] = interest
    session["stage"] = "completed"
    session["status"] = "secured"
    session["last_interaction"] = datetime.now(ZoneInfo("UTC")).isoformat()
    session["conversation"].append({"role": "user", "content": interest})
    session["conversation"].append({"role": "assistant", "content": "Thank you for providing the information!"})
    save_to_csv(
        lead_id,
        session.get("lead_name", ""),
        session.get("age", ""),
        session.get("country", ""),
        interest,
        "secured",
        session
    )
    return {"status": "success", "message": "Thank you for providing the information!"}

def save_to_csv(lead_id: str, name: str, age: str, country: str, interest: str, status: str, session: dict) -> dict:
    """Saves lead information to leads.csv."""
    with open("leads.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([lead_id, name, age, country, interest, status])
    return {"status": "success", "message": "Data saved successfully."}

def call_openai(message: str, session: dict) -> dict:
    """Calls OpenAI API to process conversational input."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        session["conversation"].append({"role": "user", "content": message})
        print("Making OpenAI API call with messages:", session["conversation"])  # Debug log
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=session["conversation"],
            max_tokens=200
        )
        assistant_response = response.choices[0].message.content
        print("OpenAI API response:", assistant_response)  # Debug log
        session["conversation"].append({"role": "assistant", "content": assistant_response})
        return {"status": "success", "message": assistant_response}
    except Exception as e:
        return {"status": "error", "message": f"OpenAI API error: {str(e)}"}