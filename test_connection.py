import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

token = os.environ["GITHUB_TOKEN"].strip()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=token,
)

print("Testing connection to GitHub Models (gpt-4o)...")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an enterprise learning agent supervisor."},
        {"role": "user", "content": "Confirm connection. Reply with: SYSTEM ACTIVE"}
    ],
    max_tokens=20
)

print("\n✅ CONNECTION SUCCESSFUL")
print(f"Model reply: {response.choices[0].message.content}")
print(f"Model used: {response.model}")