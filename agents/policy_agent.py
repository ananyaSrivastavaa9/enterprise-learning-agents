import os
import json
from openai import OpenAI

class PolicyAgent:
    def __init__(self, iq_engine):
        """Initialize with our verified Foundry IQ Simulator Engine"""
        self.iq_engine = iq_engine
        # Connect to our active GitHub Models client backend
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ.get("GITHUB_TOKEN", "")
        )

    def process_role_requirements(self, employee_role):
        print(f"[Policy Agent]: Querying Foundry IQ plane for role: '{employee_role}'...")
        
        # 1. Direct Grounding Check via our Microsoft IQ simulation layer
        iq_result = self.iq_engine.query_vector_kb(employee_role)
        
        if iq_result["status"] != "Grounded":
            return {
                "success": False,
                "error": f"Role '{employee_role}' could not be grounded in enterprise policy data."
            }

        # Extract the real document snippet and citation link
        policy_payload = iq_result["payload"]
        citation = iq_result["citations"]
        
        print(f"[Policy Agent]: ✅ Found grounded match via {citation}")

        # 2. Use gpt-4o to reason over the extracted policy data and clean up the schema requirements
        system_instruction = (
            "You are an expert corporate policy compliance auditor. Analyze the provided policy snippet "
            "and extract a clean, explicit bulleted summary of recommended certifications, core competencies, "
            "and mandatory skills. Do not add outside assumptions. Stick entirely to the grounded text."
        )
        
        user_prompt = f"Policy Document Snippet:\n{json.dumps(policy_payload, indent=2)}\n\nAnalyze and summarize."

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                model="gpt-4o",
                max_tokens=500,
                temperature=0.2  # Keep deterministic for high compliance accuracy
            )
            
            return {
                "success": True,
                "citation": citation,
                "policy_summary": response.choices[0].message.content.strip(),
                "capacity_rules": iq_result["capacity_rules"] # Pass down the line to the study planner agent
            }
        except Exception as e:
            return {"success": False, "error": f"Model reasoning failed: {e}"}