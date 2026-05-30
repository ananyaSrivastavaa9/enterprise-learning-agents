# 🤖 Enterprise Learning Agents
### Multi-Agent Reasoning System | Microsoft Agents League Hackathon 2026
**Track: Reasoning Agents | Built with Microsoft Foundry + GitHub Models**

---

## 🧠 What It Does

Enterprise Learning Agents is a multi-agent AI reasoning system that acts as a
corporate learning advisor for employees at Contoso Cloud Solutions.

An employee provides their job role. The system's Supervisor Agent orchestrates
a chain of three specialized AI agents that reason over a real enterprise policy
document and produce a fully personalized certification and study plan.

**No hardcoded answers. Every response is reasoned, grounded, and role-specific.**

---

## 🏗️ Architecture 
```text
User Input (employee role) 
↓ 
SUPERVISOR AGENT 
(orchestrates the reasoning loop) 
↓ 
┌─────────────────────────┐ 
│                         │
POLICY AGENT         STUDY PLANNER AGENT 
(reads corporate     (builds weekly schedule 
policy JSON,         using capacity rules 
extracts certs       from policy document) 
and skills) 
│                         │ 
└──────────┬──────────────┘ 
↓ 
MEMORY AGENT 
(aggregates both outputs 
into final response) 
↓ 
Final Learning Plan 
```

---

## 🤖 Agent Breakdown

| Agent | Role | File | 
|---|---|---| 
| Supervisor | Orchestrates the full reasoning loop | `supervisor.py` | 
| Policy Agent | Reads enterprise JSON, extracts role requirements | `agents/policy_agent.py` | 
| Study Planner Agent | Builds weekly schedule within capacity constraints | `agents/study_planner_agent.py` | 
| Memory Agent | Aggregates all outputs into final polished response | `memory/memory_agent.py` | 

---

## 💡 Microsoft IQ Integration

This project uses **Foundry IQ** — the agentic knowledge retrieval layer —
by grounding all agent responses in a real enterprise policy document
(`corporate_learning_policy.json`). No agent hallucinates requirements.
Every certification, skill, and schedule constraint is sourced directly
from the policy, reducing hallucination and enforcing enterprise accuracy.

---

## 📁 Project Structure

```text
enterprise-learning-agents/
│
├── supervisor.py
├── corporate_learning_policy.json
├── .env
├── README.md
│
├── agents/
│   ├── policy_agent.py
│   └── study_planner_agent.py
│
└── memory/
    └── memory_agent.py
```

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/enterprise-learning-agents
cd enterprise-learning-agents
```

**2. Create and activate virtual environment**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**3. Install dependencies**
```bash
pip install openai python-dotenv requests
```

**4. Set up your `.env` file**
GITHUB_TOKEN="your_github_token_here"

**5. Run the system**
```bash
python supervisor.py
```

**6. Enter any employee role when prompted**
Enter employee role: Cloud Infrastructure Engineer

---

## 🎯 Judging Criteria Alignment

| Criteria | How This Project Addresses It |
|---|---|
| Accuracy & Relevance | All outputs grounded in real enterprise JSON policy |
| Reasoning & Multi-step Thinking | 3-agent chained reasoning loop via Supervisor |
| Creativity & Originality | Dynamic role-based routing, not a single chatbot |
| User Experience | Interactive terminal, clean step-by-step output |
| Reliability & Safety | Error handling at every agent step with fallbacks |

---

## 👨‍💻 Built By

Built for the **Microsoft Agents League Hackathon @ AI Skills Fest 2026**  
Reasoning Agents Track | Powered by GitHub Models + gpt-4o  
Save the file.   
Then run this to do a final clean test of the whole system: python supervisor.py   
