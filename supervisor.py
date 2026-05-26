import os
import sys
import json
from agents.policy_agent import run_policy_agent
from agents.study_planner_agent import run_study_planner_agent
from memory.memory_agent import run_memory_agent
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ.get("GITHUB_TOKEN", "").strip()
)

# Session memory — stores all turns in the current session
session_history = []

def get_available_roles() -> list:
    """Returns the list of roles defined in the corporate policy."""
    with open("corporate_learning_policy.json", "r") as f:
        policy = json.load(f)
    return [section["target_role"] for section in policy["policies"]]

def match_role(user_input: str, available_roles: list) -> str | None:
    """Tries to match user input to a known role."""
    user_lower = user_input.lower().strip()
    for role in available_roles:
        if user_lower == role.lower():
            return role
        if user_lower in role.lower() or role.lower() in user_lower:
            return role
    return None

def is_followup_question(user_input: str) -> bool:
    """
    Detects if the input is a follow-up question rather than a role name.
    Uses keyword detection for speed and reliability.
    """
    followup_signals = [
        "what", "which", "how", "why", "when", "can you",
        "tell me", "explain", "recap", "summarize", "again",
        "certif", "recommend", "suggest", "previous", "last",
        "you said", "you just", "mentioned", "remind", "repeat",
        "?", "more about", "elaborate"
    ]
    user_lower = user_input.lower().strip()
    return any(signal in user_lower for signal in followup_signals)

def handle_followup(user_input: str) -> str:
    """Uses session history to answer follow-up questions."""
    print("  [Memory] Detected follow-up question. Searching session history...")

    if not session_history:
        return "I don't have any previous context in this session yet. Please enter an employee role to get started."

    # Build context from session history
    history_text = ""
    for turn in session_history:
        history_text += f"\nRole queried: {turn['role']}\nLearning plan provided:\n{turn['response']}\n---"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an enterprise learning advisor with memory of this session. "
                    "Answer the user's follow-up question using only the context provided. "
                    "Be concise and direct."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Session history:\n{history_text}\n\n"
                    f"Follow-up question: {user_input}"
                )
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

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

    # Step 0 — Role validation
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
        sys.exit(1)

    # Step 3 — Memory aggregation
    try:
        print("\n[STEP 3/3] Routing to Memory Agent...")
        final_response = run_memory_agent(matched_role, policy_output, study_plan)
    except Exception as e:
        print(f"  ❌ ERROR in Memory Agent: {e}")
        return study_plan

    # Save to session memory
    session_history.append({
        "role": matched_role,
        "policy_analysis": policy_output,
        "study_plan": study_plan,
        "response": final_response
    })

    print("\n" + "="*60)
    print(f"  SUPERVISOR: Reasoning loop complete.")
    print(f"  SUPERVISOR: Session memory updated. ({len(session_history)} turn(s) stored)")
    print("="*60 + "\n")

    return final_response


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  🤖 ENTERPRISE LEARNING AGENT SYSTEM")
    print("  Powered by Multi-Agent Reasoning + Session Memory")
    print("  Contoso Cloud Solutions | AI Skills Fest 2026")
    print("="*60)

    if not os.environ.get("GITHUB_TOKEN"):
        print("\n❌ GITHUB_TOKEN not found in .env file.")
        sys.exit(1)

    if not os.path.exists("corporate_learning_policy.json"):
        print("\n❌ corporate_learning_policy.json not found.")
        sys.exit(1)

    available_roles = get_available_roles()
    print(f"\n✅ Environment validated. System ready.")
    print(f"📋 Roles available in policy: {len(available_roles)}")
    for role in available_roles:
        print(f"   • {role}")

    print("\nType a role for a learning plan, ask a follow-up question, or type 'quit'.\n")

    while True:
        user_input = input("Enter employee role: ").strip()

        if user_input.lower() == "quit":
            print("\n👋 Enterprise Learning Agent System shutting down.")
            print(f"   Session summary: {len(session_history)} role(s) processed.")
            break

        if not user_input:
            print("⚠️  Please enter a valid role.\n")
            continue

        # Detect follow-up vs new role query
        if is_followup_question(user_input) and session_history:
            print("\n[MEMORY] Handling follow-up question from session history...")
            answer = handle_followup(user_input)
            print("\n💬 RESPONSE:")
            print("-" * 60)
            print(answer)
            print("\n" + "="*60 + "\n")
        else:
            result = run_supervisor(user_input)
            if result:
                print("📋 FINAL LEARNING PLAN:")
                print("-" * 60)
                print(result)
                print("\n" + "="*60 + "\n")