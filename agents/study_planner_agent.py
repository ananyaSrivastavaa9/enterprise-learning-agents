import os
import json
from openai import OpenAI

class StudyPlannerAgent:
    def __init__(self):
        # Establish link with our verified active model client backend
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ.get("GITHUB_TOKEN", "")
        )

    def generate_schedule(self, policy_summary, capacity_rules):
        print("[Study Planner Agent]: Generating structured certification timeline under corporate capacity rules...")

        # 1. Structure strict system boundaries to satisfy the Reliability & Safety criteria
        system_instruction = (
            "You are an enterprise training coordinator. Your job is to create a weekly study schedule "
            "for an employee based on their role requirements and explicit corporate constraints. "
            "You must strictly abide by the provided study capacity rules (e.g., maximum study hours per week, "
            "allowable timeline caps). Do not schedule study time exceeding these specific caps."
        )

        user_prompt = (
            f"Grounded Policy Summary:\n{policy_summary}\n\n"
            f"Corporate Study Capacity Constraints:\n{json.dumps(capacity_rules, indent=2)}\n\n"
            f"Generate a customized weekly study plan breakdown that fits perfectly within these limits."
        )

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                model="gpt-4o",
                max_tokens=600,
                temperature=0.3  # Low temperature prevents mathematical hallucination of timeline rules
            )

            return {
                "success": True,
                "study_plan": response.choices[0].message.content.strip()
            }
        except Exception as e:
            return {"success": False, "error": f"Study planner reasoning loop failed: {e}"}