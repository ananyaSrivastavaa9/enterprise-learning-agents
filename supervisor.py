import os
import sys
import json
from agents.policy_agent import run_policy_agent
from agents.study_planner_agent import run_study_planner_agent
from memory.memory_agent import run_memory_agent
from dotenv import load_dotenv

load_dotenv()

def get_available_roles() -> list:
    """Returns the list of roles defined in the corporate policy."""
    with open("corporate_learning_policy.json", "r") as f:
        policy = json.load(f)
    return [section["target_role"] for section in policy["policies"]]

def match_role(user_input: str, available_roles: list) -> str | None:
    """
    Tries to match user input to a known role.
    Returns matched role name or None if no match found.
    """
    user_lower = user_input.lower().strip()
    for role in available_roles:
        if user_lower == role.lower():
            return role
        # Partial match — catches "cloud infra" matching "Cloud Infrastructure Engineer"
        if user_lower in role.lower() or role.lower() in user_lower:
            return role
    return None

def run_supervisor(employee_role: str) -> str:
    """
    Supervisor Agent — orchestrates the full multi-agent reasoning loop.
    Step 0: Validates role against corporate policy
    Step 1: Policy Agent analyzes role requirements
    Step 2: Study Planner Agent builds a schedule
    Step 3: Memory Agent aggregates into final response
    """

    print("\n" + "="*60)
    print(f"  SUPERVISOR: Starting reasoning loop")
    print(f"  SUPERVISOR: Employee role received → '{employee_role}'")
    print("="*60 + "\n")

    # Step 0 — Role validation against policy
    try:
        available_roles = get_available_roles()
    except FileNotFoundError:
        print("  ❌ ERROR: corporate_learning_policy.json not found.")
        sys.exit(1)

    matched_role = match_role(employee_role, available_roles)

    if not matched_role:
        print(f"[STEP 0/3] Validating role against corporate policy...")
        print(f"  ⚠️  Role '{employee_role}' not found in corporate policy.\n")
        print("  📋 Available roles in Contoso Cloud Solutions policy:")
        for i, role in enumerate(available_roles, 1):
            print(f"     {i}. {role}")
        print(f"\n  💡 Please enter one of the roles listed above.")
        print("     The system only provides plans grounded in verified policy data.")
        return None

    if matched_role != employee_role:
        print(f"[STEP 0/3] Role matched → '{matched_role}'")

    # Step 1 — Policy analysis
    try:
        print("[STEP 1/3] Routing to Policy Agent...")
        policy_output = run_policy_agent(matched_role)
    except FileNotFoundError:
        print("  ❌ ERROR: corporate_learning_policy.json not found.")
        sys.exit(1)
    except Exception as e:
        print(f"  ❌ ERROR in Policy Agent: {e}")
        sys.exit(1)

    # Step 2 — Study planning
    try:
        print("\n[STEP 2/3] Routing to Study Planner Agent...")
        study_plan = run_study_planner_agent(matched_role, policy_output)
    except Exception as e:
        print(f"  ❌ ERROR in Study Planner Agent: {e}")
        print("  💡 Policy Agent output was saved. Partial results available.")
        sys.exit(1)

    # Step 3 — Memory aggregation
    try:
        print("\n[STEP 3/3] Routing to Memory Agent...")
        final_response = run_memory_agent(matched_role, policy_output, study_plan)
    except Exception as e:
        print(f"  ❌ ERROR in Memory Agent: {e}")
        print("  💡 Returning Study Plan directly as fallback.")
        return study_plan

    print("\n" + "="*60)
    print("  SUPERVISOR: Reasoning loop complete.")
    print("="*60 + "\n")

    return final_response


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  🤖 ENTERPRISE LEARNING AGENT SYSTEM")
    print("  Powered by Multi-Agent Reasoning")
    print("  Contoso Cloud Solutions | AI Skills Fest 2026")
    print("="*60)

    # Validate environment
    if not os.environ.get("GITHUB_TOKEN"):
        print("\n❌ GITHUB_TOKEN not found in .env file.")
        print("💡 Add GITHUB_TOKEN to your .env and restart.")
        sys.exit(1)

    # Validate policy file exists
    if not os.path.exists("corporate_learning_policy.json"):
        print("\n❌ corporate_learning_policy.json not found.")
        sys.exit(1)

    # Show available roles on startup
    available_roles = get_available_roles()
    print(f"\n✅ Environment validated. System ready.")
    print(f"📋 Roles available in policy: {len(available_roles)}")
    for role in available_roles:
        print(f"   • {role}")

    print("\nType an employee role to generate a learning plan.")
    print("Type 'quit' to exit.\n")

    while True:
        role = input("Enter employee role: ").strip()

        if role.lower() == "quit":
            print("\n👋 Enterprise Learning Agent System shutting down.")
            break

        if not role:
            print("⚠️  Please enter a valid role.\n")
            continue

        result = run_supervisor(role)

        if result:
            print("📋 FINAL LEARNING PLAN:")
            print("-" * 60)
            print(result)
            print("\n" + "="*60 + "\n")