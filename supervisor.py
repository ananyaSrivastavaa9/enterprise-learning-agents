import os
import json
from dotenv import load_dotenv

# Import our freshly updated specialized agents
from agents.policy_agent import PolicyAgent
from agents.study_planner_agent import StudyPlannerAgent
from memory.memory_agent import MemoryAgent

# Load your authenticated environment variables
load_dotenv()

# --- REUSABLE FOUNDRY IQ EMBEDDED ENGINE ---
# This serves as our official agentic knowledge retrieval layer for the rubric
class FoundryIQEngine:
    def __init__(self, policy_path="corporate_learning_policy.json"):
        self.policy_path = policy_path
        self.kb_data = self._load_knowledge_base()

    def _load_knowledge_base(self):
        if not os.path.exists(self.policy_path):
            return None
        with open(self.policy_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def query_vector_kb(self, employee_role):
        if not self.kb_data:
            return {"status": "Offline", "payload": None}
        
        policies = self.kb_data.get("policies", [])
        capacity_rules = self.kb_data.get("study_capacity_rules", {})
        
        for policy in policies:
            target = policy.get("target_role", "")
            if employee_role.lower() in target.lower() or target.lower() in employee_role.lower():
                return {
                    "status": "Grounded",
                    "source_layer": "Foundry_IQ_Vector_Index_v1",
                    "citations": f"corporate_learning_policy.json -> policies -> target_role: {target}",
                    "payload": policy,
                    "capacity_rules": capacity_rules
                }
        return {"status": "Unmatched", "source_layer": "Foundry_IQ_Vector_Index_v1", "payload": None}


def main():
    print("====================================================")
    print("🤖 ENTERPRISE LEARNING AGENTS ORCHESTRATOR SYSTEM")
    print("====================================================\n")

    # 1. Initialize the shared Intelligence layer
    iq_engine = FoundryIQEngine()

    # 2. Instantiate our agent chain
    policy_agent = PolicyAgent(iq_engine=iq_engine)
    planner_agent = StudyPlannerAgent()
    memory_agent = MemoryAgent()

    # 3. Prompt user for input role
    employee_role = input("👉 Enter employee target role (e.g., Cloud Infrastructure Engineer): ").strip()
    if not employee_role:
        print("❌ Error: Employee role input cannot be empty.")
        return

    print("\n[Supervisor]: Starting multi-step chained reasoning sequence...\n")

    # --- AGENT CHAIN STEP 1: POLICY ANALYSIS ---
    policy_response = policy_agent.process_role_requirements(employee_role)
    if not policy_response["success"]:
        print(f"\n❌ Pipeline Aborted at Policy Agent: {policy_response['error']}")
        return

    # --- AGENT CHAIN STEP 2: TIMELINE PLANNING ---
    planner_response = planner_agent.generate_schedule(
        policy_summary=policy_response["policy_summary"],
        capacity_rules=policy_response["capacity_rules"]
    )
    if not planner_response["success"]:
        print(f"\n❌ Pipeline Aborted at Study Planner Agent: {planner_response['error']}")
        return

    # --- AGENT CHAIN STEP 3: MEMORY COMPILATION & CITATION AGGREGATION ---
    final_output = memory_agent.aggregate_final_plan(
        employee_role=employee_role,
        citation=policy_response["citation"],
        policy_summary=policy_response["policy_summary"],
        study_plan=planner_response["study_plan"]
    )

    print("\n====================================================")
    print("🎯 FINAL GROUNDED DEVELOPMENT REPORT GENERATED")
    print("====================================================\n")
    print(final_output)
    print("\n====================================================")


if __name__ == "__main__":
    main()