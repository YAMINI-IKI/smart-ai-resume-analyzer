import os
import google.generativeai as genai

# Your API key

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

print("✅ Available Models for generateContent:\n")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")