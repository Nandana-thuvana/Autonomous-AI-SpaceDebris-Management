import os

key = os.getenv("GEMINI_API_KEY")

if key:
    print("✅ API Key is set")
    print("First 10 chars:", key[:10])
else:
    print("❌ API Key is NOT set")
