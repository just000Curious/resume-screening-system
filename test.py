"""Test script to verify API keys are working"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("="*50)
print("Testing API Configuration")
print("="*50)

# Check if keys are loaded
openai_key = os.getenv("OPENAI_API_KEY")
langsmith_key = os.getenv("LANGCHAIN_API_KEY")

print(f"\n✅ OpenAI API Key loaded: {openai_key[:20]}...{openai_key[-10:]}" if openai_key else "❌ OpenAI API Key NOT found")
print(f"✅ LangSmith API Key loaded: {langsmith_key[:20]}...{langsmith_key[-10:]}" if langsmith_key else "❌ LangSmith API Key NOT found")

# Test OpenAI API
if openai_key:
    print("\n📡 Testing OpenAI API connection...")
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=openai_key
        )
        
        response = llm.invoke("Say 'OpenAI API is working correctly!'")
        print(f"✅ Success! Response: {response.content}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "="*50)