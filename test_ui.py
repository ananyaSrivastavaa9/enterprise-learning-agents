import streamlit as st

st.set_page_config(layout="wide")

# Direct inline element assembly block
st.markdown('''
<div style="background-color: #030708; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px; font-family: sans-serif;">
    
    <div style="filter: drop-shadow(0 0 25px #7bf0ff); margin-bottom: 20px;">
        <svg width="180" height="180" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="40" r="22" stroke="#7bf0ff" stroke-width="1" stroke-dasharray="2 2"/>
            <path d="M35 40C35 28.9543 43.9543 20 50 20C56.0457 20 65 28.9543 65 40C65 46 59 52 50 52C41 52 35 46 35 40Z" fill="url(#metal)" stroke="#ffffff" stroke-width="1.5"/>
            <circle cx="43" cy="38" r="2.5" fill="#7bf0ff"/>
            <circle cx="57" cy="38" r="2.5" fill="#7bf0ff"/>
            <path d="M46 45Q50 48 54 45" stroke="#7bf0ff" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M26 66C26 59 36 57 50 57C64 57 74 59 74 66V78H26V66Z" fill="rgba(123,240,255,0.05)" stroke="#7bf0ff" stroke-width="1.2"/>
            <defs>
                <linearGradient id="metal" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ffffff"/><stop offset="50%" stop-color="#a1a8b8"/><stop offset="100%" stop-color="#334155"/>
                </linearGradient>
            </defs>
        </svg>
    </div>

    <div style="filter: drop-shadow(0 0 15px #7bf0ff); margin-bottom: 25px;">
        <svg width="70" height="70" viewBox="0 0 24 24" fill="none" stroke="#7bf0ff" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v5"/>
            <path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v6"/>
            <path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8.5"/>
            <path d="M6 14v.5A4.5 4.5 0 0 0 10.5 19h3.5a6 6 0 0 0 6-6V11.5a1.5 1.5 0 0 0-3 0V12"/>
        </svg>
    </div>

    <h1 style="font-size: 3.2rem; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin: 0; background: linear-gradient(180deg, #ffffff 0%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 15px rgba(255,255,255,0.1));">
        Contoso Agents League
    </h1>
    
    <p style="color: #475569; font-size: 0.85rem; letter-spacing: 2px; margin-top: 15px; text-transform: uppercase;">
        Grounded Enterprise Layer Verified
    </p>
</div>
''', unsafe_allow_html=True)