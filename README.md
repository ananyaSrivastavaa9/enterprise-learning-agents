<div align="center">

# 🔮 Daily Nixtio
## Grounded Multi-Agent Learning Workspace

**Where enterprise policy meets cinematic intelligence.**

*Contoso Agents League · Microsoft Agents League Hackathon 2026*  
*Reasoning Agents Track · Microsoft Foundry IQ · GitHub Models · gpt-4o*

---

| | |
| :--- | :--- |
| **Product Surface** | Premium Streamlit workspace (`app.py`) |
| **Reasoning Core** | Sequential multi-agent pipeline with policy-grounded outputs |
| **Inference Plane** | `https://models.inference.ai.azure.com` via GitHub token |
| **Knowledge Anchor** | `corporate_learning_policy.json` (Contoso Cloud Solutions) |

</div>

---

## The Vision in One Line

**Daily Nixtio** transforms a single job designation into a **verifiable, day-sequenced learning environment**—not by guessing certifications, but by routing every decision through a **grounded knowledge gate**, an **audit-grade summarizer**, and a **capacity-aware scheduler** wrapped in a **surreal light metallic** interface built for executive clarity.

---

<br>

## 🎬 Product Experience

> *Embed your cinematic walkthrough below—this is the first impression layer for reviewers, stakeholders, and new engineers.*

### Primary Demo

**<img width="1893" height="901" alt="image" src="https://github.com/user-attachments/assets/d11067c6-c319-4f7d-baa7-e0d4a3ede802" />
**

### Supplementary Captures *(optional)*

| View | Asset |
| :--- | :--- |
| Hero intake & Submit flow | **<img width="1885" height="898" alt="image" src="https://github.com/user-attachments/assets/3b0c692b-d9b2-4cc9-b8e9-0be79b2d481b" />
** |
| Grounded vs. extrapolated citation banner | **<img width="1879" height="892" alt="image" src="https://github.com/user-attachments/assets/65cd8983-448f-4f78-8611-3e013820c77c" />
** |
| Horizontal collectible-card carousel | **<img width="1888" height="891" alt="image" src="https://github.com/user-attachments/assets/d05f6b71-b73e-413e-8292-24d5f2654ebf" />
** |

---

<br>

## 🧬 Core Architecture & Reasoning Engine

Daily Nixtio operates as a **deterministic reasoning cascade**: each stage consumes structured artifacts from the prior stage. No agent invents corporate mandates—the **Microsoft Foundry IQ Engine** binds the pipeline to document-backed truth before language models elaborate.

### Orchestration Flow

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                     DAILY NIXTIO · REASONING CASCADE                    │
└─────────────────────────────────────────────────────────────────────────┘

  Employee Designation (Streamlit intake)
              │
              ▼
┌──────────────────────────────┐
│  MICROSOFT FOUNDRY IQ ENGINE │  ◄── corporate_learning_policy.json
│  (Knowledge Retrieval Gate)  │
└──────────────────────────────┘
              │
              │  Grounded match  ──►  policy payload + capacity_rules
              │  Adaptive baseline ──►  extrapolated payload + citations
              ▼
┌──────────────────────────────┐
│     SAGE AUDITOR AGENT       │  ◄── gpt-4o · low temperature
│  Compliance-grade distillation│
└──────────────────────────────┘
              │
              │  Concise competency & certification summary
              ▼
┌──────────────────────────────┐
│   CHRONOS SCHEDULER AGENT    │  ◄── gpt-4o · capacity-constrained
│  Timeline synthesis layer    │
└──────────────────────────────┘
              │
              │  Structured raw HTML collectible-card fragments
              ▼
┌──────────────────────────────┐
│  SURREAL UI RENDER SURFACE   │  ◄── cards-scroll-container carousel
│  (Streamlit · unsafe HTML)   │
└──────────────────────────────┘
```

### Agent Responsibilities

| Layer | Agent / Engine | Mandate | Output Artifact |
| :--- | :--- | :--- | :--- |
| **0 — Retrieval** | **Microsoft Foundry IQ Engine** | Role-to-policy vector match against enterprise JSON; emits citations and study-capacity rules | `Grounded` policy payload or `Adaptive Baseline` with traceable citation string |
| **1 — Audit** | **Sage Auditor Agent** | Compress grounded payload into an executive-readable competency brief—no external assumptions | Markdown-aligned summary of certifications, competencies, and mandatory skills |
| **2 — Schedule** | **Chronos Scheduler Agent** | Synthesize a **5–7 day** learning arc honoring `study_capacity_rules` (weekly hour caps, focus blocks) | Raw HTML `<div class="collectible-card">` fragments ready for carousel injection |
| **3 — Presentation** | **Streamlit Session Controller** | Persist `cached_audit` / `cached_report`; render grounded status, pipeline telemetry, and card theatre | Premium in-browser learning workspace |

### Grounding Philosophy

| Principle | Implementation |
| :--- | :--- |
| **Citation-first** | Every grounded track displays `corporate_learning_policy.json → policies → target_role` lineage |
| **Capacity enforcement** | Chronos ingests `maximum_weekly_hours_allowed` and `recommended_focus_block_duration_minutes` from policy |
| **Hallucination resistance** | Sage Auditor receives only IQ-engine payloads—never free-form enterprise lore |
| **Resilient inference** | Extended API timeouts, bounded `max_tokens`, and retry logic on scheduler-critical paths |

### Dual Runtime Surfaces

Daily Nixtio ships two complementary entry points for the same intellectual property:

| Surface | Entry | Best For |
| :--- | :--- | :--- |
| **Product UI** | `streamlit run app.py` | Demo, design review, hackathon judging |
| **CLI Orchestrator** | `python supervisor.py` | Terminal-native agent chain (`PolicyAgent` → `StudyPlannerAgent` → `MemoryAgent`) |

---

<br>

## ✨ Surreal Light Metallic UI/UX Design

The interface is not a skin on top of a chatbot—it is a **designed cognition theatre**. Typography, motion, and material depth communicate that the user is inside a **premium planning instrument**, not a generic LLM wrapper.

### Design Language

| Element | Behavior |
| :--- | :--- |
| **Surreal Light Metallic palette** | Layered radial gradients (`--bg0` → `--bg4`) with drifting atmospheric bloom |
| **Frosted glass emissions** | `backdrop-filter: blur(20px) saturate(180%)` on collectible cards and hero shell |
| **Metallic stroke system** | `--stroke` and `--glow` tokens for luminous edge definition without visual noise |
| **Hero shell** | Wide-layout command center with floating robot orb, badge chips, and executive copy hierarchy |

### Carousel & Card System

The learning plan materializes as a **fluid horizontal carousel**—a cinematic reel of daily milestones rather than a vertical document wall.

| UX Capability | Technical Expression |
| :--- | :--- |
| **Horizontal scroll theatre** | `.cards-scroll-container` — flex row, smooth `scroll-behavior`, custom chromatic scrollbar |
| **Collectible card objects** | Fixed flex basis (`340px`), glass surface, hover lift (`translateY` + scale), staggered `fadeIn` via `--delay` |
| **Dynamic card bounds** | `height: auto` + `align-self: flex-start` — cards grow with content; no forced equal-height stretching |
| **Agent-native HTML injection** | Chronos output passes directly into the scroll wrapper—zero redundant parsing loops |
| **Role-responsive banner** | `.role-heading-banner` animates on reveal with grounded-track typography |

### Interaction Model

```text
  Designation input  ──►  Submit ↗
         │
         ├── Session invalidation on role change (prevents stale plans)
         ├── Pipeline insight capsules (live agent telemetry)
         └── Carousel reveal with grounded / extrapolated status ribbon
```

### Responsive Posture

| Breakpoint | Adaptation |
| :--- | :--- |
| **Desktop (wide)** | Full carousel stride, hero grid `1.1fr · 0.9fr`, max container `1500px` |
| **≤ 900px** | Tightened padding, compressed hero radius—carousel remains horizontally navigable |

---

<br>

## 🚀 Quick Start & Installation

### Requirements

| Category | Specification |
| :--- | :--- |
| **Python** | 3.10+ recommended |
| **OS** | Windows, macOS, or Linux |
| **Network** | Outbound HTTPS to `models.inference.ai.azure.com` |
| **Credentials** | GitHub personal access token with Models access |

### 1 · Clone & Enter

```bash
git clone https://github.com/YOUR_USERNAME/enterprise-learning-agents.git
cd enterprise-learning-agents
```

### 2 · Virtual Environment

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 3 · Install Dependencies

```bash
pip install streamlit openai python-dotenv
```

| Package | Role |
| :--- | :--- |
| `streamlit` | Premium product surface & session state |
| `openai` | GitHub Models client (OpenAI-compatible SDK) |
| `python-dotenv` | Secure `.env` token loading |

### 4 · Configure Environment

Create a `.env` file at the project root:

```env
GITHUB_TOKEN=your_github_personal_access_token_here
```

> **Security note:** Never commit `.env` to version control. The token authorizes inference against GitHub Models—treat it as production-grade secret material.

**Optional connectivity check:**

```bash
python test_connection.py
```

Expected signal: `API Link Fully Active` from `gpt-4o`.

### 5 · Launch Daily Nixtio

```bash
streamlit run app.py
```

| Step | Action |
| :--- | :--- |
| 1 | Open the local URL Streamlit prints (typically `http://localhost:8501`) |
| 2 | Enter a designation—e.g., `Cloud Infrastructure Engineer` |
| 3 | Press **Submit ↗** |
| 4 | Review grounded citations, pipeline capsules, and the collectible-card carousel |

### 6 · CLI Orchestrator *(optional)*

```bash
python supervisor.py
```

---

<br>

## 📁 Repository Topology

```text
enterprise-learning-agents/
│
├── app.py                              # Daily Nixtio · Streamlit product surface
├── corporate_learning_policy.json      # Foundry IQ knowledge anchor
├── test_connection.py                  # GitHub Models endpoint verification
├── supervisor.py                         # CLI multi-agent orchestrator
│
├── agents/
│   ├── policy_agent.py
│   └── study_planner_agent.py
│
├── memory/
│   └── memory_agent.py
│
├── index.html                          # Static design reference
└── .env                                # Local secrets (git-ignored)
```

---

<br>

## 🎯 Enterprise Value Matrix

| Stakeholder Concern | Daily Nixtio Response |
| :--- | :--- |
| **Compliance** | Policy-grounded retrieval before generative elaboration |
| **Transparency** | Visible citation strings for grounded vs. extrapolated tracks |
| **Operator experience** | Executive-grade UI with zero terminal friction |
| **Scalability of content** | HTML card fragments decouple presentation from scheduler logic |
| **Reliability** | Timeout-aware client, token budgets, and session-safe caching |

---

<br>

## 👨‍💻 Attribution

Built for the **Microsoft Agents League Hackathon @ AI Skills Fest 2026**  
**Track:** Reasoning Agents · **Stack:** Microsoft Foundry IQ · GitHub Models · gpt-4o · Streamlit

---

<div align="center">

**Daily Nixtio v2.6** · *Grounded. Scheduled. Beautiful.*

🔮 *Contoso Agents League — Premium AI Planning Workspace*

</div>
