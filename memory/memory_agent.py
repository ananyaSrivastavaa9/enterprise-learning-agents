import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"].strip()
)

def run_memory_agent(employee_role: str, policy_analysis: str, study_plan: str) -> str:
    """Aggregates all agent outputs into one final polished response."""

    print(f"  [Memory Agent] Aggregating outputs for: {employee_role}")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise learning advisor who synthesizes "
                    "analysis from multiple specialist agents into a single, "
                    "clear, executive-level summary. "
                    "Your output is the final response shown to the employee. "
                    "Be warm, professional, and actionable."
                )
            },
            {
                "role": "user",
                "content": (
                    f"An employee with role '{employee_role}' has requested a learning plan.\n\n"
                    f"POLICY SPECIALIST ANALYSIS:\n{policy_analysis}\n\n"
                    f"STUDY PLANNER OUTPUT:\n{study_plan}\n\n"
                    f"Synthesize both into one clean final response. "
                    f"Start with a one-sentence welcome, then present the key "
                    f"certifications, then the weekly schedule summary. "
                    f"End with one motivational sentence."
                )
            }
        ],
        max_tokens=400
    )

    result = response.choices[0].message.content
    print(f"  [Memory Agent] Done.")
    return result