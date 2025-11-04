#!/usr/bin/env python3
"""Quick test of API connectivity"""
import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Test imports
try:
    import gemini_client
    print("✓ gemini_client imported successfully")
except Exception as e:
    print(f"✗ Failed to import gemini_client: {e}")
    sys.exit(1)

# Check environment variables
print(f"\nEnvironment Variables:")
print(f"  GEMINI_API_KEY: {('*' * 10) + os.getenv('GEMINI_API_KEY', '')[-10:] if os.getenv('GEMINI_API_KEY') else 'NOT SET'}")
print(f"  GEMINI_API_ENDPOINT: {os.getenv('GEMINI_API_ENDPOINT', 'NOT SET')}")
print(f"  GEMINI_API_STREAM: {os.getenv('GEMINI_API_STREAM', 'NOT SET')}")

# Test blocking call
print("\n--- Testing Blocking API Call ---")
try:
    response = gemini_client.generate_response("Who is Hrithik Roshan?")
    print(f"Response received: {response[:100] if response else 'EMPTY'}")
except Exception as e:
    print(f"✗ Blocking call failed: {e}")
    import traceback
    traceback.print_exc()

# Test streaming call
print("\n--- Testing Streaming API Call ---")
try:
    print("Starting stream_generate...")
    gen = gemini_client.stream_generate("Who is Hrithik Roshan?")
    print(f"Generator created: {gen}")
    chunks = []
    for i, chunk in enumerate(gen):
        print(f"  [{i}] Chunk: {chunk[:80] if len(str(chunk)) > 80 else chunk}")
        chunks.append(chunk)
    print(f"Total chunks received: {len(chunks)}")
    if len(chunks) == 0:
        print("WARNING: No chunks received from streaming!")
except Exception as e:
    print(f"✗ Streaming call failed: {e}")
    import traceback
    traceback.print_exc()

print("\n✓ Test complete")
