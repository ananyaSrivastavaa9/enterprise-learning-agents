import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the environment keys
load_dotenv()

# We pull your GitHub token from the environment configuration
github_token = os.environ.get("GITHUB_TOKEN", "").strip()

print("--- PHASE 2: MODEL API ENDPOINT VERIFICATION ---")

if not github_token:
    print("❌ Error: 'GITHUB_TOKEN' is missing from your .env file.")
    print("Please add GITHUB_TOKEN='your_token_here' to your .env file to authorize the engine.")
else:
    print("Initializing GitHub Models Client via Native OpenAI SDK...")
    
    try:
        # 2. Point the standard OpenAI client directly to the GitHub Models marketplace hosting base
        client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=github_token
        )
        
        print("Sending routing payload to gpt-4o...")
        
        # 3. Fire a lightweight test query to verify live processing
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a hackathon environment test script."},
                {"role": "user", "content": "Verify system pipeline link. Respond with 'API Link Fully Active'."}
            ],
            model="gpt-4o",
            max_tokens=20
        )
        
        print("\n✅ CONNECTION SUCCESSFUL!")
        print(f"[MODEL RESPONSE]: {response.choices[0].message.content.strip()}\n")
        print("We are officially clear to build out the multi-agent routing loop next!")

    except Exception as e:
        print(f"\n❌ API Endpoint Connection Failed: {e}")
        print("💡 Hint: Verify that your GITHUB_TOKEN is correct and has standard public repository permissions.")