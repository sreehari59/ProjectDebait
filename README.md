# Project Debait

Two agents debate a topic, e.g. "cats vs. dogs". Each agent represents a side and they go back and forth. After a short discussion the debate ends and a third agent (judge) decides who won.

As a stretch goal a forth agent (coach) optimizes the losing agents prompt and the debate repeats. Based on the outcome or score, the system improves via some kind of reinforcement learning.

[Result Presentation](https://www.canva.com/design/DAGqZ-tM9oA/EexpPjRlaOjCbpoWjshZLQ/view?utm_content=DAGqZ-tM9oA&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hf39e1a9da7)

## Installation 
Please use the below steps to run the back end code
- Clone the repository
- Create an environment and activate it
- Install the required packages:
   ```
   pip install -r requirements.txt
   ```
- Create `.env` file and update the:
```
AGENT_ID="AGENT_ID_FROM_BEYOND_PRESENCE"
MISTRAL_API_KEY="GIVE_YOUR_MISTRAL_API_KEY"
MISTRAL_API_KEY_MODEL_NAME = "GIVE_YOUR_MISTRAL_MODEL_NAME"
BEY_API_KEY="BEYOND_PRESENCE_API_KEY"
```
