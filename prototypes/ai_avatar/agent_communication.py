import os
from mistralai import Mistral
import requests
from dotenv import load_dotenv
load_dotenv()
API_URL = "https://api.bey.dev/v1"


def fetch_transcript(api_key: str, agent_id: str) -> None:
    calls_response = requests.get(
        f"{API_URL}/calls",
        headers={"x-api-key": api_key},
    )

    if calls_response.status_code != 200:
        print(
            f"Error fetching calls: {calls_response.status_code} - {calls_response.text}"
        )
        exit(1)
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

        print("Messages:")

        # print(messages_response.json())
        return messages_response.json()

def llm_judge(topic, transcript):    
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    model = os.getenv("MISTRAL_API_KEY_MODEL_NAME")

    client = Mistral(api_key=mistral_api_key)

    prompt = f"""You are judging the debate on: {topic}.
            Debate transcript: \n{transcript}
            Format response EXACTLY as:\nWINNER: [User/AI]\nREASON: [one clear sentence explanation]"""

    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )
    return chat_response.choices[0].message.content


topic = "dog vs cat"
transcript = fetch_transcript(api_key=os.getenv("BEY_API_KEY"), agent_id=os.getenv("AGENT_ID"))
result = llm_judge(topic, transcript)

print(transcript)
print("=========")
print(result)



# Role: You are to take on the role of a debater.
# Objective: You will be given a debate topic, and your task is to present arguments either in support of or against the topic

# 1. Opening & Rapport Building –
# acknowledge the opponent and judges, and briefly outline your stance or theme. 

# 2. If the user is supporting the topic you would have to be talking against the topic or choosing the other side of the topic. Similarly if the user is opposing the topic then you should support the topic. 
# For example:
# 2.1 if the topic is dog vs cat and user chooses the topic dog then you should choose the topic cat
# 2.2 If the topic is gender equality, the user choose to support gender equality then you should choose to oppose gender equality.


# 3. Instruction: Avoid repeating the user's points verbatim. Instead, respond thoughtfully, you may reference their arguments only to critique, challenge, or counter them based on your position.
