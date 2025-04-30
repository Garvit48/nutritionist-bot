import json
from agent import agent_executor
from schemas import routine_schema
from jsonschema import validate, ValidationError
from pathlib import Path

# Load user preferences
with open("configs/user_preferences.json", "r") as f:
    user_data = json.load(f)


def build_prompt_with_user_request(user_data, routine_schema, current_routine, user_prompt):
    return f"""
You are a nutritionist AI. Based on the following user data, generate a meal routine for the rest of the day. 
Return the output strictly in the following JSON format:

{json.dumps(routine_schema, indent=2)}

User data:
{json.dumps(user_data, indent=2)}

Current Routine: 
{json.dumps(current_routine, indent=2)}

ALSO the user said the following: {user_prompt}
If the user said "-", ignore the rest of the prompt

If the user request is compatible with the user's dietary preferences, allergies, goals, and calorie limit, return a JSON object with:
- "response_text": a brief message confirming the change (e.g. "Removed dinner", or "Switched lunch to oats").
- "routine_change": true
- "routine": the updated routine in the above schema

If the request is unacceptable (e.g. asks for an allergen, exceeds calories, violates goals), return:
- "response_text": a brief message explaining why it can't be done
- "routine_change": false
- "routine": the original routine unchanged
"""



def query(user_data, routine_schema, current_routine={}, user_prompt="-"):
    prompt = build_prompt_with_user_request(
        user_data=user_data,
        routine_schema=routine_schema,
        current_routine=current_routine,
        user_prompt=user_prompt
    )

    # Run the agent
    response = agent_executor.run(prompt)

    try:
        response_data = json.loads(response)

        # Validate required fields
        if not all(key in response_data for key in ["response_text", "routine_change", "routine"]):
            raise ValueError("Missing keys in response.")

        # If routine changed, validate and save it
        if response_data["routine_change"]:
            validate(instance=response_data["routine"], schema=routine_schema)

            Path("configs").mkdir(exist_ok=True)
            with open("configs/daily_routine.json", "w") as f:
                json.dump(response_data["routine"], f, indent=2)

            print("Routine updated and saved to daily_routine.json")
        else:
            print("No routine change made.")

        return response_data["response_text"]

    except (json.JSONDecodeError, ValidationError, ValueError) as e:
        print("Failed to process response:")
        print(e)
        return "Sorry, I couldn't understand or apply the requested change."
