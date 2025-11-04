#!/usr/bin/env python
"""Test script to debug Gemini API calls"""

import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, r"d:\Vs Code\PROJECT\OIBSIP\Voice Assistant\EchoMind AI")

load_dotenv()

import gemini_client

print("=" * 60)
print("GEMINI API DEBUG TEST")
print("=" * 60)

print("\n1. Checking environment variables:")
print(f"   GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY')[:20]}..." if os.getenv('GEMINI_API_KEY') else "   GEMINI_API_KEY: NOT SET")
print(f"   GEMINI_API_ENDPOINT: {os.getenv('GEMINI_API_ENDPOINT')}")
print(f"   GEMINI_API_STREAM: {os.getenv('GEMINI_API_STREAM')}")
print(f"   GEMINI_RESPONSE_MODE: {os.getenv('GEMINI_RESPONSE_MODE')}")

print("\n2. Testing blocking API call (generate_response):")
test_prompt = "Who is Hrithik Roshan? Answer in one sentence."
print(f"   Prompt: {test_prompt}")

try:
    response = gemini_client.generate_response(test_prompt)
    print(f"   Response: {response}")
    if "simulated" in response.lower() or "trouble" in response.lower():
        print("   ⚠️  Got error/stub response!")
    else:
        print("   ✅ Got real response!")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print("\n3. Testing streaming API call (stream_generate):")
print(f"   Prompt: {test_prompt}")

try:
    chunks = []
    for chunk in gemini_client.stream_generate(test_prompt):
        chunks.append(chunk)
        print(f"   - Chunk: {chunk[:50]}..." if len(chunk) > 50 else f"   - Chunk: {chunk}")
    
    if not chunks:
        print("   ⚠️  No chunks yielded!")
    else:
        full_response = "".join(chunks)
        print(f"   Full response: {full_response}")
        if "simulated" in full_response.lower():
            print("   ⚠️  Got stub response!")
        else:
            print("   ✅ Got real streaming response!")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
