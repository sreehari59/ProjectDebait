import requests
from typing import Any, Dict 
import json
import re

def fetch_transcript(api_key: str, agent_id: str) -> Dict[str, Any]:
    API_URL = "https://api.bey.dev/v1"
    calls_response = requests.get(
        f"{API_URL}/calls",
        headers={"x-api-key": api_key},
    )

    if calls_response.status_code != 200:
        print(
            f"Error fetching calls: {calls_response.status_code} - {calls_response.text}"
        )
        exit(1)
    print(calls_response.json())
    calls = calls_response.json()
    for call in calls:
        if call["agent_id"] != agent_id:
            continue

        call_id = call["id"]
        call_started_at = call["started_at"]
        call_ended_at = call["ended_at"]

        print(f"=== Call {call_id} ===")
        print(f"Started at: {call_started_at}")
        print(f"Ended at: {call_ended_at}")

        messages_response = requests.get(
            f"{API_URL}/calls/{call_id}/messages",
            headers={"x-api-key": api_key},
        )
        if messages_response.status_code != 200:
            print(
                f"Error fetching messages for call {call_id}: "
                f"{messages_response.status_code} - {messages_response.text}"
            )
            continue

        print("Messages:", messages_response.json())

        return messages_response.json()
    
def extract_json(text):
    # Use regex to extract JSON block from mixed content
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            data = json.loads(json_str)
            return data
        except json.JSONDecodeError as e:
            print("JSON parsing failed:", e)
    else:
        print("No JSON found in input.")
        data ={
            "winner": "",
            "reason": ""
        }
    return data