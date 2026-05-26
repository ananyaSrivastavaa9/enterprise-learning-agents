import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"].strip()
)

def run_policy_agent(employee_role: str) -> str:
    """Reads the corporate policy JSON and returns cert + skill recommendations."""
    
    # Load the policy document
    with open("corporate_learning_policy.json", "r") as f:
        policy = json.load(f)
    
    # Convert policy to string for the agent to reason over
    policy_text = json.dumps(policy, indent=2)
    
    print(f"  [Policy Agent] Analyzing policy for role: {employee_role}")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a corporate learning policy specialist. "
                    "You read enterprise policy documents and extract precise, "
                    "role-specific certification and skill requirements. "
                    "Be concise and structured."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Using the policy document below, extract all recommended certifications, "
                    f"core competencies, and mandatory skills for the role: '{employee_role}'.\n\n"
                    f"POLICY DOCUMENT:\n{policy_text}"
                )
            }
        ],
        max_tokens=300
    )
    
    result = response.choices[0].message.content
    print(f"  [Policy Agent] Done.")
    return result