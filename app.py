import os
import json
from flask import Flask, request, jsonify, render_template_string
from supervisor import run_supervisor, handle_followup, is_followup_question, session_history, get_available_roles
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Enterprise Learning Agents</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;700;800&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #080c14;
    --surface: #0d1520;
    --border: #1a2a3a;
    --accent: #00d4ff;
    --accent2: #7c3aed;
    --accent3: #10b981;
    --text: #e2e8f0;
    --muted: #64748b;
  }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Syne', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 32px 16px;
  }
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
  }
  .header {
    text-align: center;
    margin-bottom: 32px;
  }
  .badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(124,58,237,0.15));
    border: 1px solid rgba(0,212,255,0.3);
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    padding: 6px 16px;
    border-radius: 20px;
    margin-bottom: 12px;
    text-transform: uppercase;
  }
  h1 {
    font-size: clamp(22px, 4vw, 38px);
    font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, var(--accent) 50%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
  }
  .subtitle {
    font-family: 'JetBrains Mono', monospace;
    color: var(--muted);
    font-size: 12px;
  }
  .main {
    width: 100%;
    max-width: 860px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .roles-bar {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  .role-chip {
    background: rgba(0,212,255,0.08);
    border: 1px solid rgba(0,212,255,0.2);
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    padding: 6px 14px;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s;
    letter-spacing: 0.5px;
  }
  .role-chip:hover {
    background: rgba(0,212,255,0.18);
    border-color: var(--accent);
  }
  .input-row {
    display: flex;
    gap: 10px;
  }
  input[type="text"] {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    color: var(--text);
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    outline: none;
    transition: border-color 0.2s;
  }
  input[type="text"]:focus {
    border-color: var(--accent);
  }
  input[type="text"]::placeholder { color: var(--muted); }
  button {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border: none;
    border-radius: 10px;
    padding: 14px 28px;
    color: #fff;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 14px;
    cursor: pointer;
    transition: opacity 0.2s;
    white-space: nowrap;
  }
  button:hover { opacity: 0.85; }
  button:disabled { opacity: 0.5; cursor: not-allowed; }
  .chat-window {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    min-height: 420px;
    max-height: 560px;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .empty-state {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    text-align: center;
  }
  .empty-icon { font-size: 40px; }
  .message {
    display: flex;
    flex-direction: column;
    gap: 6px;
    animation: slideIn 0.3s ease;
  }
  @keyframes slideIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .message-user {
    align-self: flex-end;
    background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(124,58,237,0.1));
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 10px 10px 2px 10px;
    padding: 10px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--accent);
    max-width: 70%;
  }
  .message-agent {
    align-self: flex-start;
    max-width: 92%;
  }
  .agent-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
  }
  .agent-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--accent3);
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .agent-steps {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-bottom: 8px;
  }
  .step-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid;
  }
  .step-1 { color: #a78bfa; border-color: rgba(124,58,237,0.3); background: rgba(124,58,237,0.08); }
  .step-2 { color: var(--accent3); border-color: rgba(16,185,129,0.3); background: rgba(16,185,129,0.08); }
  .step-3 { color: var(--accent); border-color: rgba(0,212,255,0.3); background: rgba(0,212,255,0.08); }
  .memory-badge { color: #f59e0b; border-color: rgba(245,158,11,0.3); background: rgba(245,158,11,0.08); }
  .agent-body {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    line-height: 1.7;
    white-space: pre-wrap;
    color: var(--text);
  }
  .error-msg {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 8px;
    padding: 12px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #f87171;
  }
  .loading {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--muted);
    padding: 10px 0;
  }
  .dots span {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    margin: 0 2px;
    animation: bounce 1.2s infinite;
  }
  .dots span:nth-child(2) { animation-delay: 0.2s; }
  .dots span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
    40% { transform: translateY(-6px); opacity: 1; }
  }
  .session-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    padding: 0 4px;
  }
  .session-count {
    color: var(--accent3);
  }
  .clear-btn {
    background: transparent;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 4px 12px;
    color: var(--muted);
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    cursor: pointer;
    transition: all 0.2s;
  }
  .clear-btn:hover {
    border-color: #ef4444;
    color: #f87171;
    background: transparent;
  }
</style>
</head>
<body>

<div class="header">
  <div class="badge">🏆 Microsoft Agents League Hackathon 2026</div>
  <h1>Enterprise Learning Agents</h1>
  <p class="subtitle">Multi-Agent Reasoning System · Contoso Cloud Solutions · Foundry IQ</p>
</div>

<div class="main">

  <div class="roles-bar" id="rolesBar">
    <!-- populated by JS -->
  </div>

  <div class="input-row">
    <input type="text" id="userInput"
      placeholder="Enter employee role or ask a follow-up question..." />
    <button id="sendBtn" onclick="sendMessage()">Run Agents →</button>
  </div>

  <div class="session-bar">
    <span>Session memory: <span class="session-count" id="turnCount">0 turns</span></span>
    <button class="clear-btn" onclick="clearSession()">Clear session</button>
  </div>

  <div class="chat-window" id="chatWindow">
    <div class="empty-state" id="emptyState">
      <div class="empty-icon">🤖</div>
      <div>Enter an employee role to start the reasoning loop</div>
      <div style="color:#334155">e.g. "Cloud Infrastructure Engineer"</div>
    </div>
  </div>

</div>

<script>
  let turnCount = 0;

  // Load available roles and render chips
  fetch('/roles').then(r => r.json()).then(data => {
    const bar = document.getElementById('rolesBar');
    data.roles.forEach(role => {
      const chip = document.createElement('div');
      chip.className = 'role-chip';
      chip.textContent = role;
      chip.onclick = () => {
        document.getElementById('userInput').value = role;
        sendMessage();
      };
      bar.appendChild(chip);
    });
  });

  document.getElementById('userInput').addEventListener('keydown', e => {
    if (e.key === 'Enter') sendMessage();
  });

  function clearSession() {
    fetch('/clear', {method: 'POST'}).then(() => {
      document.getElementById('chatWindow').innerHTML =
        '<div class="empty-state" id="emptyState"><div class="empty-icon">🤖</div><div>Session cleared. Enter a role to start again.</div></div>';
      turnCount = 0;
      document.getElementById('turnCount').textContent = '0 turns';
    });
  }

  function addUserMessage(text) {
    const el = document.createElement('div');
    el.className = 'message-user';
    el.textContent = text;
    return el;
  }

  function addLoading() {
    const el = document.createElement('div');
    el.className = 'loading';
    el.id = 'loadingMsg';
    el.innerHTML = 'Agents reasoning <div class="dots"><span></span><span></span><span></span></div>';
    return el;
  }

  function renderResponse(data) {
    const wrap = document.createElement('div');
    wrap.className = 'message message-agent';

    const header = document.createElement('div');
    header.className = 'agent-header';
    const label = document.createElement('div');
    label.className = 'agent-label';
    label.textContent = data.type === 'memory' ? '🧠 Memory Agent' : '🤖 Supervisor → Multi-Agent Response';
    header.appendChild(label);
    wrap.appendChild(header);

    if (data.steps) {
      const steps = document.createElement('div');
      steps.className = 'agent-steps';
      data.steps.forEach((s, i) => {
        const b = document.createElement('span');
        b.className = `step-badge step-${i+1}`;
        b.textContent = s;
        steps.appendChild(b);
      });
      wrap.appendChild(steps);
    }

    if (data.type === 'memory') {
      const b = document.createElement('div');
      b.className = 'agent-steps';
      const badge = document.createElement('span');
      badge.className = 'step-badge memory-badge';
      badge.textContent = '⚡ Answered from session memory';
      b.appendChild(badge);
      wrap.appendChild(b);
    }

    const body = document.createElement('div');
    body.className = 'agent-body';
    body.textContent = data.response;
    wrap.appendChild(body);
    return wrap;
  }

  async function sendMessage() {
    const input = document.getElementById('userInput');
    const btn = document.getElementById('sendBtn');
    const chatWindow = document.getElementById('chatWindow');
    const text = input.value.trim();
    if (!text) return;

    // Remove empty state
    const empty = document.getElementById('emptyState');
    if (empty) empty.remove();

    // Add user message
    chatWindow.appendChild(addUserMessage(text));
    input.value = '';
    btn.disabled = true;

    // Add loading
    const loader = addLoading();
    chatWindow.appendChild(loader);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    try {
      const res = await fetch('/query', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({input: text})
      });
      const data = await res.json();
      loader.remove();

      if (data.error) {
        const err = document.createElement('div');
        err.className = 'error-msg';
        err.textContent = data.error;
        chatWindow.appendChild(err);
      } else {
        chatWindow.appendChild(renderResponse(data));
        if (data.type !== 'memory') {
          turnCount++;
          document.getElementById('turnCount').textContent = `${turnCount} turn${turnCount !== 1 ? 's' : ''}`;
        }
      }
    } catch(e) {
      loader.remove();
      const err = document.createElement('div');
      err.className = 'error-msg';
      err.textContent = 'Network error. Is the server running?';
      chatWindow.appendChild(err);
    }

    btn.disabled = false;
    chatWindow.scrollTop = chatWindow.scrollHeight;
    input.focus();
  }
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/roles")
def roles():
    return jsonify({"roles": get_available_roles()})

@app.route("/clear", methods=["POST"])
def clear():
    session_history.clear()
    return jsonify({"status": "cleared"})

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_input = data.get("input", "").strip()

    if not user_input:
        return jsonify({"error": "Please enter a role or question."})

    # Detect follow-up
    if is_followup_question(user_input) and session_history:
        answer = handle_followup(user_input)
        return jsonify({
            "type": "memory",
            "response": answer
        })

    # Run full supervisor loop
    result = run_supervisor(user_input)

    if result is None:
        available = get_available_roles()
        return jsonify({
            "error": f"Role not found in corporate policy. Available roles: {', '.join(available)}"
        })

    return jsonify({
        "type": "agent",
        "steps": ["✅ Policy Agent", "✅ Study Planner Agent", "✅ Memory Agent"],
        "response": result
    })

if __name__ == "__main__":
    print("\n🤖 Enterprise Learning Agents — Web Interface")
    print("   Open http://localhost:5000 in your browser\n")
    app.run(debug=False, port=5000)