import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"].strip()
)

def run_study_planner_agent(employee_role: str, policy_analysis: str) -> str:
    """Builds a weekly study plan based on policy analysis and capacity rules."""

    # Load capacity rules from policy
    with open("corporate_learning_policy.json", "r") as f:
        policy = json.load(f)

    capacity = policy["study_capacity_rules"]
    max_hours = capacity["maximum_weekly_hours_allowed"]
    block_minutes = capacity["recommended_focus_block_duration_minutes"]

    print(f"  [Study Planner Agent] Building study plan for: {employee_role}")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a corporate learning coach who builds practical, "
                    "structured weekly study plans. You work within strict time "
                    "constraints and always produce realistic, actionable schedules."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Build a weekly study plan for a '{employee_role}' based on this analysis:\n\n"
                    f"{policy_analysis}\n\n"
                    f"CONSTRAINTS:\n"
                    f"- Maximum {max_hours} hours of study per week\n"
                    f"- Each focus block must be exactly {block_minutes} minutes\n"
                    f"- Spread sessions across the week realistically\n"
                    f"- Assign specific certifications to specific days\n"
                    f"Output a clean day-by-day schedule."
                )
            }
        ],
        max_tokens=400
    )

    result = response.choices[0].message.content
    print(f"  [Study Planner Agent] Done.")
    return result