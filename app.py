import os
import json
import time
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, APITimeoutError
from showcase_carousel_html import SHOWCASE_CAROUSEL_HTML

# Load project keys
load_dotenv()

MODELS_BASE_URL = "https://models.inference.ai.azure.com"
API_TIMEOUT_SECONDS = 300.0
CHAT_MAX_RETRIES = 3


def create_models_client(api_key: str) -> OpenAI:
    return OpenAI(
        base_url=MODELS_BASE_URL,
        api_key=api_key,
        timeout=API_TIMEOUT_SECONDS,
        max_retries=0,
    )


def chat_with_retry(client: OpenAI, *, step_label: str, **kwargs):
    last_error = None
    for attempt in range(1, CHAT_MAX_RETRIES + 1):
        try:
            return client.chat.completions.create(**kwargs)
        except APITimeoutError as exc:
            last_error = exc
            if attempt >= CHAT_MAX_RETRIES:
                raise TimeoutError(
                    f"{step_label} timed out after {CHAT_MAX_RETRIES} attempts "
                    f"({int(API_TIMEOUT_SECONDS)}s each). Try Submit again."
                ) from exc
            time.sleep(2 ** (attempt - 1))
    raise last_error

# Set up page configurations with premium minimalist canvas
st.set_page_config(
    page_title="Daily Nixtio | Learning Agents",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session Memory States securely to block variable data wiping
if "cached_report" not in st.session_state:
    st.session_state.cached_report = None
if "cached_audit" not in st.session_state:
    st.session_state.cached_audit = None
if "pipeline_logs" not in st.session_state:
    st.session_state.pipeline_logs = []
if "previous_role" not in st.session_state:
    st.session_state.previous_role = ""

# ==========================================================
# 🎨 SURREAL LIGHT METALLIC GLASSMORPHISM CSS ENGINE
# ==========================================================
st.markdown("""
<style>
:root{
  --bg0:#f8f9ff;
  --bg1:#edebff;
  --bg2:#dde6ff;
  --bg3:#c7d2fe;
  --bg4:#b8c0ff;
  --text:#1c1f2b;
  --muted:#667085;
  --card:rgba(255,255,255,0.75);
  --stroke:rgba(128,140,255,0.22);
  --glow:rgba(148,163,255,0.30);
}

.stApp{
  background:
    radial-gradient(circle at 18% 16%, rgba(255,255,255,0.98) 0%, rgba(255,255,255,0.72) 14%, transparent 33%),
    radial-gradient(circle at 82% 18%, rgba(236,232,255,0.98) 0%, rgba(236,232,255,0.70) 14%, transparent 35%),
    radial-gradient(circle at 50% 90%, rgba(216,224,255,0.92) 0%, rgba(216,224,255,0.55) 16%, transparent 42%),
    linear-gradient(180deg, var(--bg0) 0%, var(--bg1) 42%, var(--bg2) 100%) !important;
  color:var(--text) !important;
  font-family:Inter, Poppins, system-ui, -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp::before{
  content:'';
  position:fixed;
  inset:0;
  pointer-events:none;
  background:
    radial-gradient(circle at 20% 20%, rgba(184,192,255,0.30), transparent 22%),
    radial-gradient(circle at 80% 25%, rgba(255,255,255,0.45), transparent 18%),
    radial-gradient(circle at 60% 80%, rgba(221,230,255,0.48), transparent 24%);
  filter: blur(10px);
  opacity:.9;
  animation: drift 16s ease-in-out infinite alternate;
}

@keyframes drift{
  from{transform:translate3d(0,0,0) scale(1)}
  to{transform:translate3d(0,-10px,0) scale(1.03)}
}

.block-container{
  padding-top:2.2rem !important;
  padding-bottom:2rem !important;
  max-width: 1500px !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"]{background:transparent !important;}

/* --- DYNAMIC TARGET ROLE BANNER --- */
.role-heading-banner {
  background: linear-gradient(135deg, rgba(255,255,255,0.85), rgba(240,243,255,0.65)) !important;
  border: 1px solid rgba(141,154,255,0.25) !important;
  box-shadow: 0 12px 30px rgba(132, 146, 255, 0.08) !important;
  border-radius: 20px !important;
  padding: 24px 30px !important;
  margin-top: 35px !important;
  margin-bottom: 25px !important;
  text-align: center;
  animation: fadeIn 0.5s ease-out;
}

/* --- HORIZONTAL SCROLL CAROUSEL ENGINE --- */
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

.cards-scroll-container::-webkit-scrollbar {
  height: 8px !important;
}
.cards-scroll-container::-webkit-scrollbar-track {
  background: rgba(128, 140, 255, 0.05) !important;
  border-radius: 10px !important;
}
.cards-scroll-container::-webkit-scrollbar-thumb {
  background: rgba(128, 140, 255, 0.25) !important;
  border-radius: 10px !important;
}
.cards-scroll-container::-webkit-scrollbar-thumb:hover {
  background: rgba(128, 140, 255, 0.45) !important;
}

/* --- FIX: COLLECTIBLE DYNAMIC HEIGHT CARD ENGINE --- */
.collectible-card {
  flex: 0 0 340px !important; 
  background: var(--card) !important;
  backdrop-filter: blur(20px) saturate(180%) !important;
  -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
  border: 1px solid var(--stroke) !important;
  border-radius: 24px !important;
  padding: 24px !important;
  height: auto !important; /* Content tightly dictates bounds now */
  align-self: flex-start !important; /* Stops card from stretching horizontally alongside grid row items */
  box-shadow: 0 15px 35px rgba(132, 146, 255, 0.06), inset 0 1px 0 rgba(255,255,255,0.6) !important;
  animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
  animation-delay: var(--delay, 0s);
  transition: transform .4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow .4s ease, border-color .4s ease !important;
}

.collectible-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 30px 65px rgba(132, 146, 255, 0.18), inset 0 1px 0 rgba(255,255,255,0.9) !important;
  border-color: rgba(128,140,255,0.45) !important;
}

.card-title {
  font-size: 1.15rem !important;
  font-weight: 700 !important;
  color: #1e1b4b !important;
  margin-top: 4px !important;
  margin-bottom: 12px !important;
  line-height: 1.4 !important;
  white-space: normal !important;
}

.card-body-text {
  color: #49557a !important;
  font-size: 0.96rem !important;
  line-height: 1.65 !important;
  white-space: normal !important;
}

.card-body-text ul {
  padding-left: 18px !important;
  margin-top: 6px !important;
}

.card-body-text li {
  margin-bottom: 6px !important;
}

.hero-shell{
  background: var(--card) !important;
  backdrop-filter: blur(16px) !important;
  border: 1px solid var(--stroke) !important;
  border-radius:30px !important;
  padding:28px !important;
  position:relative !important;
  overflow:hidden !important;
  box-shadow: 0 20px 40px rgba(132, 146, 255, 0.06) !important;
}

.insight-capsule {
  background: rgba(255, 255, 255, 0.5) !important;
  border: 1px solid var(--stroke) !important;
  border-radius: 14px !important;
  padding: 12px 16px !important;
  margin-top: 8px !important;
  font-size: 0.92rem !important;
  color: #344054 !important;
}

.stTextInput>div>div>input{
  background:rgba(255,255,255,0.85) !important;
  color:#111827 !important;
  border:1px solid rgba(141,154,255,0.28) !important;
  border-radius:18px !important;
  padding:18px 20px !important;
  font-size:1.04rem !important;
  box-shadow:0 10px 30px rgba(143,156,255,0.10) !important;
  transition: all .28s ease !important;
}
.stTextInput>div>div>input:focus{
  border-color:rgba(120,138,255,0.72) !important;
  box-shadow:0 0 0 5px rgba(183,194,255,0.28), 0 14px 40px rgba(143,156,255,0.18) !important;
}

.stButton>button{
  background:linear-gradient(135deg, #c7d2fe 0%, #b8c0ff 100%) !important;
  color:#1f2340 !important;
  border:none !important;
  border-radius:18px !important;
  padding:14px 22px !important;
  font-weight:700 !important;
  box-shadow:0 14px 30px rgba(133,148,255,.28), inset 0 1px 0 rgba(255,255,255,.7) !important;
  transition:transform .25s ease, box-shadow .25s ease, filter .25s ease !important;
}
.stButton>button:hover{transform:translateY(-2px); filter:saturate(1.06); box-shadow:0 18px 36px rgba(133,148,255,.34), 0 0 0 6px rgba(220,226,255,.4) !important;}

.badge-soft{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding:8px 12px;
  border-radius:999px;
  background:rgba(255,255,255,0.62);
  border:1px solid rgba(141,154,255,0.18);
  color:#49557a;
  font-size:.82rem;
  box-shadow:0 8px 24px rgba(128,140,255,0.08);
}

.robot-orb{
  width:108px;
  height:108px;
  border-radius:28px;
  background:radial-gradient(circle at 35% 28%, #ffffff 0%, #eff2ff 34%, #d9defd 100%);
  box-shadow:0 20px 50px rgba(145,156,255,.22), inset 0 1px 0 rgba(255,255,255,.85);
  position:relative;
  animation: floaty 6.5s ease-in-out infinite;
}
.robot-orb::before{
  content:'';
  position:absolute;
  inset:18px 24px 34px;
  border-radius:18px;
  background:linear-gradient(180deg, #1c1f2b 0%, #2f3650 100%);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.08), 0 0 25px rgba(175,185,255,.18);
}
.robot-orb::after{
  content:'';
  position:absolute;
  left:50%;
  top:50%;
  width:14px;
  height:14px;
  border-radius:50%;
  transform:translate(-50%,-50%);
  background:#dff7ff;
  box-shadow:-18px 0 0 #dff7ff, 18px 0 0 #dff7ff;
  animation: blink 4.2s ease-in-out infinite;
}

@keyframes floaty{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes blink{0%,90%,100%{filter:opacity(1)} 93%{filter:opacity(.18)} 96%{filter:opacity(1)}}
@keyframes fadeIn{from{opacity:0; transform:translateY(20px)} to{opacity:1; transform:translateY(0)}}

@media (max-width: 900px){
  .block-container{padding-left:1rem !important; padding-right:1rem !important;}
  .hero-shell{padding:20px !important; border-radius:24px !important;}
}
</style>
""", unsafe_allow_html=True)

# Hero Viewport Shell Layout
st.markdown("""
<div class='hero-shell'>
  <div style='display:flex; justify-content:space-between; align-items:center; gap:16px; flex-wrap:wrap;'>
    <div class='badge-soft'>Assistant v2.6</div>
    <div style='font-weight:600; color:#1f2340;'>Contoso Agents League</div>
    <div class='badge-soft'>Upgrade</div>
  </div>
  <div style='display:grid; grid-template-columns:1.1fr .9fr; gap:28px; align-items:center; margin-top:26px;'>
    <div>
      <div class='badge-soft' style='margin-bottom:14px;'>Premium AI Planning Workspace</div>
      <h1 style='font-size:clamp(2.2rem, 3.5vw, 4.3rem); line-height:0.96; margin:0; color:#161a2b; font-weight:800;'>Hi there. Ready to build something extraordinary?</h1>
      <p style='font-size:1.05rem; color:#5f6b8a; margin-top:16px; max-width:620px;'>Enter a role, and your grounded multi-agent workflow will generate an elegant, day-wise learning plan inside this redesigned luxury interface.</p>
    </div>
    <div style='display:flex; justify-content:center; position:relative;'>
      <div class='robot-orb'></div>
      <div style='position:absolute; right:4%; top:10%; background:rgba(255,255,255,.78); padding:12px 14px; border-radius:18px; border:1px solid rgba(141,154,255,.18); box-shadow:0 12px 28px rgba(143,156,255,.16); color:#364055; font-size:.9rem;'>Hey there ✨<br>Need a boost?</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# 🧬 REASONING INFRASTRUCTURE BACKEND (FOUNDRY IQ GATE)
# ==========================================================
class FoundryIQEngine:
    def __init__(self, policy_path="corporate_learning_policy.json"):
        self.policy_path = policy_path
        self.kb_data = self._load_knowledge_base()

    def _load_knowledge_base(self):
        if not os.path.exists(self.policy_path): return None
        try:
            with open(self.policy_path, 'r', encoding='utf-8') as f: return json.load(f)
        except Exception: return None

    def query_vector_kb(self, employee_role):
        if not self.kb_data: return {"status": "Offline", "payload": None}
        policies = self.kb_data.get("policies", [])
        capacity_rules = self.kb_data.get("study_capacity_rules", {})
        
        for policy in policies:
            target = policy.get("target_role", "")
            if employee_role.lower() in target.lower() or target.lower() in employee_role.lower():
                return {
                    "status": "Grounded",
                    "source": "Microsoft Foundry IQ Engine",
                    "citations": f"corporate_learning_policy.json -> policies -> target_role: {target}",
                    "payload": policy,
                    "capacity_rules": capacity_rules
                }
        return {
            "status": "Adaptive Baseline",
            "source": "Foundry IQ - Cross-Role Inference",
            "citations": "corporate_learning_policy.json -> study_capacity_rules [Extrapolated]",
            "payload": {
                "target_role": employee_role,
                "recommended_certifications": ["AZ-900: Microsoft Azure Fundamentals Core Path"],
                "core_competencies": ["General Enterprise System Literacy", "Cloud Operations Tracking"],
                "mandatory_skills": ["Basic Cloud Resource Operations Control Management"]
            },
            "capacity_rules": capacity_rules
        }

class SageAuditorAgent:
    def __init__(self, iq_engine, client):
        self.iq_engine = iq_engine
        self.client = client
    def execute(self, role):
        iq_result = self.iq_engine.query_vector_kb(role)
        response = chat_with_retry(
            self.client,
            step_label="Policy audit",
            messages=[
                {"role": "system", "content": "You are Sage Auditor. Extract a highly concise markdown summary listing core competencies and required skills."},
                {"role": "user", "content": json.dumps(iq_result['payload'])}
            ],
            model="gpt-4o",
            temperature=0.1,
            max_tokens=500,
        )
        return {"success": True, "summary": response.choices[0].message.content.strip(), "result": iq_result}

class ChronosSchedulerAgent:
    def __init__(self, client):
        self.client = client
    def execute(self, summary, rules):
        prompt = (
            "You are Chronos Scheduler. Build a concise day-by-day learning timeline from the summary and capacity rules. "
            "Output ONLY raw HTML (no markdown fences, no outer scroll wrapper). "
            "Create 5 to 7 days maximum. Each day is one <div class=\"collectible-card\" style=\"--delay: Ns;\"> "
            "with <div class=\"card-title\">Day X: Title</div> and <div class=\"card-body-text\"><ul><li>...</li></ul></div>. "
            "Keep bullet text short."
        )
        response = chat_with_retry(
            self.client,
            step_label="Learning schedule",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Summary: {summary}\nConstraints: {json.dumps(rules)}"}
            ],
            model="gpt-4o",
            temperature=0.1,
            max_tokens=2800,
        )
        return {"success": True, "plan": response.choices[0].message.content.strip()}

# ==========================================================
# 🔮 USER INTAKE CONTROLLER SECTION
# ==========================================================
st.markdown("<br>", unsafe_allow_html=True)
cols_input = st.columns([8, 2])

with cols_input[0]:
    employee_role = st.text_input("Designation", placeholder="What would you like to achieve today? (e.g., Cloud infra engineer)", label_visibility="collapsed")
    if employee_role != st.session_state.previous_role:
        st.session_state.cached_report = None
        st.session_state.cached_audit = None
        st.session_state.pipeline_logs = []
        st.session_state.previous_role = employee_role

with cols_input[1]:
    run_loop = st.button("Submit ↗", use_container_width=True)

# ==========================================================
# 📊 DATA EVALUATION CASCADE ROUTINES
# ==========================================================
if run_loop and employee_role:
    st.session_state.pipeline_logs = []
    try:
        token = os.environ.get("GITHUB_TOKEN", "").strip()
        if not token:
            raise ValueError("Authentication token configuration missing.")

        client = create_models_client(token)
        iq_engine = FoundryIQEngine()
        auditor = SageAuditorAgent(iq_engine, client)
        scheduler = ChronosSchedulerAgent(client)

        with st.spinner("Generating grounded learning plan (this may take up to a minute)..."):
            st.session_state.pipeline_logs.append("✨ [Nixtio Assistant]: Accessing corporate policy index maps...")
            audit_res = auditor.execute(employee_role)

            st.session_state.pipeline_logs.append("✨ [Nixtio Assistant]: Dynamically calculating timeline capacity metrics...")
            sched_res = scheduler.execute(audit_res["summary"], audit_res["result"]["capacity_rules"])

        st.session_state.cached_audit = audit_res
        st.session_state.cached_report = sched_res["plan"]

    except Exception as runtime_error:
        st.session_state.cached_report = None
        st.session_state.cached_audit = None
        st.markdown(
            f"<div class='insight-capsule' style='color:#ef4444; border-color:rgba(239,68,68,0.2);'>"
            f"❌ Evaluation Halted: {runtime_error}</div>",
            unsafe_allow_html=True,
        )

# Print clean floating metrics trace
if st.session_state.pipeline_logs:
    for trace in st.session_state.pipeline_logs:
        st.markdown(f"<div class='insight-capsule'>{trace}</div>", unsafe_allow_html=True)

# ==========================================================
# 🃏 THE CINEMATIC SURREAL CARD REVEAL PLATFORM
# ==========================================================
if st.session_state.cached_report and st.session_state.cached_audit:
    audit_meta = st.session_state.cached_audit
    
    # Classy Dynamic Heading Section displaying current target role
    display_role_title = employee_role.strip().title() if employee_role else "Target System Architecture"
    st.markdown(f"""
        <div class="role-heading-banner">
            <span style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 2px; color: #4f46e5; font-weight: 700; display: block; margin-bottom: 4px;">Grounded Optimization Track</span>
            <h2 style="margin: 0; color: #161a2b; font-size: 1.8rem; font-weight: 800; letter-spacing: -0.5px;">Custom Learning Environment: {display_role_title}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if audit_meta["result"]["status"] == "Adaptive Baseline":
        st.markdown(f"<p style='text-align:center; color:#6366f1; font-weight:600; font-size:0.9rem;'>⚠️ Context Extrapolated via: <code>{audit_meta['result']['citations']}</code></p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='text-align:center; color:#10b981; font-weight:600; font-size:0.9rem;'>✅ Grounded Organization Record Attached: <code>{audit_meta['result']['citations']}</code></p>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(SHOWCASE_CAROUSEL_HTML, unsafe_allow_html=True)

st.markdown("<br><br><div style='text-align:center; color:#94a3b8; font-size:0.8rem; letter-spacing:0.5px;'>Daily Nixtio v2.6 Core Framework Integration • Powered by GitHub Models</div>", unsafe_allow_html=True)