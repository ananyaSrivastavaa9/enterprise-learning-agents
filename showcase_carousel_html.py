"""
Daily Nixtio — Standalone 14-Day Carousel Showcase
Run: streamlit run showcase_carousel_html.py
"""

CARD_WIDTH = 340

# ---------------------------------------------------------------------------
# Hardcoded 14-day learning path (serial 01–14, Day 1–Day 14)
# ---------------------------------------------------------------------------
LEARNING_DAYS = [
    {
        "serial": "01",
        "title": "Day 1: Enterprise Cloud Orientation",
        "bullets": [
            "Map Contoso role expectations to Azure responsibility zones.",
            "Complete the AZ-900 skills navigator diagnostic (baseline only).",
            "Initialize your private study ledger with weekly hour caps.",
        ],
    },
    {
        "serial": "02",
        "title": "Day 2: Identity Fabric Essentials",
        "bullets": [
            "Study Entra ID tenants, directories, and subscription boundaries.",
            "Practice assigning built-in roles at resource group scope.",
            "Summarize least-privilege patterns in three plain-language bullets.",
        ],
    },
    {
        "serial": "03",
        "title": "Day 3: Compute Provisioning Sprint",
        "bullets": [
            "Deploy two Linux VMs across availability zones (lab subscription).",
            "Configure managed disks and document redundancy trade-offs.",
            "Skip-ahead checkpoint: compare IaaS vs PaaS for your target role.",
        ],
    },
    {
        "serial": "04",
        "title": "Day 4: Virtual Networking Foundations",
        "bullets": [
            "Design a single VNet with two subnets and NSG rule sets.",
            "Validate inbound/outbound flows using Connection troubleshoot.",
        ],
    },
    {
        "serial": "05",
        "title": "Day 5: AZ-900 Spiral Review",
        "bullets": [
            "Revisit cloud economics, SLAs, and shared responsibility (90 min block).",
            "Complete 25 practice items; tag weak domains for Day 13 rehearsal.",
            "Non-linear bridge: link networking Day 4 notes to identity Day 2 controls.",
        ],
    },
    {
        "serial": "06",
        "title": "Day 6: Bicep First Contact",
        "bullets": [
            "Author a minimal Bicep template: RG, VNet, single VM.",
            "Run what-if, deploy, and capture deployment operations output.",
            "Refactor one parameter for environment naming convention.",
        ],
    },
    {
        "serial": "07",
        "title": "Day 7: Synthesis and Recovery",
        "bullets": [
            "Consolidate week-one notes into a one-page architecture sketch.",
            "Light review only — honor the 6-hour weekly corporate cap.",
        ],
    },
    {
        "serial": "08",
        "title": "Day 8: ARM Template Deep Structure",
        "bullets": [
            "Translate your Bicep module into equivalent ARM JSON sections.",
            "Practice linked templates vs nested deployments decision matrix.",
            "Document rollback strategy for a failed resource provider call.",
        ],
    },
    {
        "serial": "09",
        "title": "Day 9: Observability Stack",
        "bullets": [
            "Enable Azure Monitor metrics and diagnostic settings on lab VMs.",
            "Create one alert rule and one action group for CPU threshold.",
            "Correlate Activity Log entries with your Day 6 deployment.",
        ],
    },
    {
        "serial": "10",
        "title": "Day 10: Identity Protection Workshop",
        "bullets": [
            "Configure Conditional Access policies using the Azure portal wizard.",
            "Map enterprise users to role-based access patterns without custom scripts.",
            "Run sign-in risk reports and record remediation steps in plain text.",
            "Validate MFA enforcement for a test security group only.",
        ],
    },
    {
        "serial": "11",
        "title": "Day 11: Hub-Spoke Peering Lab",
        "bullets": [
            "Sketch hub-spoke topology on paper before any portal changes.",
            "Deploy VNet peering between two lab networks and confirm bidirectional link.",
            "Test path validation with built-in network diagnostic tools.",
            "Document asymmetric routing scenarios in your study journal.",
        ],
    },
    {
        "serial": "12",
        "title": "Day 12: Cost Governance",
        "bullets": [
            "Build a subscription cost analysis view with resource group breakdown.",
            "Apply one reservation vs pay-as-you-go comparison for compute.",
        ],
    },
    {
        "serial": "13",
        "title": "Day 13: AZ-104 Scenario Rehearsal",
        "bullets": [
            "Execute timed labs: storage ACLs, VM scale set, backup policy.",
            "Target weak domains flagged on Day 5 — identity and networking crossover.",
            "Simulate incident response: revoke access, rotate keys, redeploy NIC.",
        ],
    },
    {
        "serial": "14",
        "title": "Day 14: Capstone and Certification Readiness",
        "bullets": [
            "Present end-to-end architecture narrative (10 slides max).",
            "Finalize AZ-104 and AZ-305 alignment checklist from grounded policy.",
            "Schedule exam window and export study ledger for manager review.",
        ],
    },
]


def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_card_html(day: dict, index: int) -> str:
    delay = round(index * 0.12, 2)
    bullets_html = "".join(
        f"<li>{_escape_html(b)}</li>" for b in day["bullets"]
    )
    serial = _escape_html(day["serial"])
    title = _escape_html(day["title"])
    return f"""
<div class="collectible-card" style="--delay: {delay}s; width: {CARD_WIDTH}px; max-width: {CARD_WIDTH}px; min-width: {CARD_WIDTH}px; flex: 0 0 {CARD_WIDTH}px;">
  <div style="font-size:2rem; font-weight:900; color:#4f46e5; opacity:0.85; margin-bottom:6px; font-family:ui-monospace,monospace;">{serial}</div>
  <div class="card-title">{title}</div>
  <div class="card-body-text"><ul>{bullets_html}</ul></div>
</div>"""


def build_carousel_html(days: list) -> str:
    cards = "".join(build_card_html(day, i) for i, day in enumerate(days))
    return f'<div class="cards-scroll-container">{cards}</div>'


SHOWCASE_CAROUSEL_HTML = build_carousel_html(LEARNING_DAYS)

SHOWCASE_CSS = """
<style>
:root {
  --bg0: #f8f9ff;
  --bg1: #edebff;
  --bg2: #dde6ff;
  --text: #1c1f2b;
  --card: rgba(255, 255, 255, 0.75);
  --stroke: rgba(128, 140, 255, 0.22);
}

.stApp {
  background:
    radial-gradient(circle at 18% 16%, rgba(255,255,255,0.98) 0%, rgba(255,255,255,0.72) 14%, transparent 33%),
    radial-gradient(circle at 82% 18%, rgba(236,232,255,0.98) 0%, rgba(236,232,255,0.70) 14%, transparent 35%),
    radial-gradient(circle at 50% 90%, rgba(216,224,255,0.92) 0%, rgba(216,224,255,0.55) 16%, transparent 42%),
    linear-gradient(180deg, var(--bg0) 0%, var(--bg1) 42%, var(--bg2) 100%) !important;
  color: var(--text) !important;
  font-family: Inter, Poppins, system-ui, -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at 20% 20%, rgba(184,192,255,0.30), transparent 22%),
    radial-gradient(circle at 80% 25%, rgba(255,255,255,0.45), transparent 18%),
    radial-gradient(circle at 60% 80%, rgba(221,230,255,0.48), transparent 24%);
  filter: blur(10px);
  opacity: 0.9;
  animation: drift 16s ease-in-out infinite alternate;
}

@keyframes drift {
  from { transform: translate3d(0, 0, 0) scale(1); }
  to { transform: translate3d(0, -10px, 0) scale(1.03); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.block-container {
  padding-top: 2.2rem !important;
  padding-bottom: 2rem !important;
  max-width: 1500px !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"] {
  background: transparent !important;
}

.hero-shell {
  background: var(--card) !important;
  backdrop-filter: blur(16px) saturate(180%) !important;
  -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
  border: 1px solid var(--stroke) !important;
  border-radius: 30px !important;
  padding: 28px !important;
  box-shadow: 0 20px 40px rgba(132, 146, 255, 0.06) !important;
  margin-bottom: 28px !important;
}

.badge-soft {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.62);
  border: 1px solid rgba(141, 154, 255, 0.18);
  color: #49557a;
  font-size: 0.82rem;
}

.role-heading-banner {
  background: linear-gradient(135deg, rgba(255,255,255,0.85), rgba(240,243,255,0.65)) !important;
  border: 1px solid rgba(141, 154, 255, 0.25) !important;
  box-shadow: 0 12px 30px rgba(132, 146, 255, 0.08) !important;
  border-radius: 20px !important;
  padding: 24px 30px !important;
  margin-bottom: 25px !important;
  text-align: center;
  animation: fadeIn 0.5s ease-out;
}

.cards-scroll-container {
  display: flex !important;
  flex-direction: row !important;
  gap: 24px !important;
  overflow-x: auto !important;
  overflow-y: hidden !important;
  padding: 15px 10px 30px 10px !important;
  width: 100% !important;
  scroll-behavior: smooth !important;
}

.cards-scroll-container::-webkit-scrollbar { height: 8px !important; }
.cards-scroll-container::-webkit-scrollbar-track {
  background: rgba(128, 140, 255, 0.05) !important;
  border-radius: 10px !important;
}
.cards-scroll-container::-webkit-scrollbar-thumb {
  background: rgba(128, 140, 255, 0.25) !important;
  border-radius: 10px !important;
}

.collectible-card {
  flex: 0 0 340px !important;
  background: var(--card) !important;
  backdrop-filter: blur(20px) saturate(180%) !important;
  -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
  border: 1px solid var(--stroke) !important;
  border-radius: 24px !important;
  padding: 24px !important;
  height: auto !important;
  align-self: flex-start !important;
  box-shadow: 0 15px 35px rgba(132, 146, 255, 0.06), inset 0 1px 0 rgba(255,255,255,0.6) !important;
  animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
  animation-delay: var(--delay, 0s);
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease !important;
}

.collectible-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 30px 65px rgba(132, 146, 255, 0.18), inset 0 1px 0 rgba(255,255,255,0.9) !important;
}

.card-title {
  font-size: 1.15rem !important;
  font-weight: 700 !important;
  color: #1e1b4b !important;
  margin-bottom: 12px !important;
  line-height: 1.4 !important;
}

.card-body-text {
  color: #49557a !important;
  font-size: 0.96rem !important;
  line-height: 1.65 !important;
}

.card-body-text ul { padding-left: 18px !important; margin-top: 6px !important; }
.card-body-text li { margin-bottom: 6px !important; }
</style>
"""


def run_showcase_app() -> None:
    import streamlit as st

    st.set_page_config(
        page_title="Daily Nixtio | Showcase Carousel",
        page_icon="🔮",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown(SHOWCASE_CSS, unsafe_allow_html=True)

    st.markdown(
        """
<div class="hero-shell">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
    <span class="badge-soft">Presentation Mode</span>
    <span class="badge-soft">Daily Nixtio v2.6</span>
  </div>
  <h1 style="margin:20px 0 8px; font-size:clamp(1.8rem,3vw,2.8rem); font-weight:800; color:#161a2b;">
    Grounded Multi-Agent Learning Workspace
  </h1>
  <p style="color:#5f6b8a; font-size:1.02rem; max-width:720px; margin:0;">
    Static 14-day collectible carousel — no API keys, no session state, no external imports.
  </p>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="role-heading-banner">
  <span style="font-size:0.85rem; text-transform:uppercase; letter-spacing:2px; color:#4f46e5; font-weight:700;">
    Grounded Optimization Track
  </span>
  <h2 style="margin:8px 0 0; color:#161a2b; font-size:1.8rem; font-weight:800;">
    Custom Learning Environment: Cloud Infrastructure Engineer
  </h2>
</div>
<p style="text-align:center; color:#10b981; font-weight:600; font-size:0.9rem;">
  ✅ Grounded Organization Record Attached — corporate_learning_policy.json
</p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(SHOWCASE_CAROUSEL_HTML, unsafe_allow_html=True)
    st.markdown(
        "<br><div style='text-align:center; color:#94a3b8; font-size:0.8rem;'>"
        "Daily Nixtio Showcase · 14-Day Fluid Learning Path</div>",
        unsafe_allow_html=True,
    )


def _should_run_standalone_app() -> bool:
    if __name__ == "__main__":
        return True
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        ctx = get_script_run_ctx()
        if ctx and getattr(ctx, "script_path", None):
            return ctx.script_path.replace("\\", "/").endswith("showcase_carousel_html.py")
    except Exception:
        pass
    return False


if _should_run_standalone_app():
    run_showcase_app()
