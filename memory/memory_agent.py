import os
from openai import OpenAI

class MemoryAgent:
    def __init__(self):
        # Establish connection to our verified active engine backend
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ.get("GITHUB_TOKEN", "")
        )

    def aggregate_final_plan(self, employee_role, citation, policy_summary, study_plan):
        print("[Memory Agent]: Running final orchestration aggregation and citation mapping...")

        # Structure strict guardrails for the aggregation format
        system_instruction = (
            "You are an executive enterprise communications expert. Your job is to compile separate "
            "policy summaries and technical study plans into a single, beautifully polished, cohesive "
            "Corporate Development Report. You must explicitly include the provided data source citation "
            "at the very top of the response to ensure complete grounding transparency."
        )

        user_prompt = (
            f"Employee Target Designation: {employee_role}\n"
            f"Verified Grounding Source: {citation}\n\n"
            f"--- Section A: Policy Summary Input ---\n{policy_summary}\n\n"
            f"--- Section B: Dynamic Study Plan Input ---\n{study_plan}\n\n"
            f"Compile these into a professional document using clean Markdown syntax."
        )

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "system_instruction" if False else "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                model="gpt-4o",
                max_tokens=1000,
                temperature=0.4 # Slightly higher temperature allows for elegant, professional layout styling
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Memory aggregation layer failed: {e}"