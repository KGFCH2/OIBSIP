#!/usr/bin/env python3
"""Test the complete streaming pipeline that was failing"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables BEFORE importing other modules
load_dotenv()

# Import what we need
import gemini_client
from utils.voice_io import speak_stream

print("=" * 60)
print("STREAMING PIPELINE TEST")
print("=" * 60)

# Test 1: Direct streaming
print("\n1. Testing stream_generate() directly:")
print("-" * 60)
try:
    gen = gemini_client.stream_generate("Who is Hrithik Roshan?")
    chunks = []
    for chunk in gen:
        print(f"   Got chunk: {repr(chunk)}")
        chunks.append(chunk)
    
    if chunks:
        print(f"✅ Got {len(chunks)} chunk(s)")
    else:
        print(f"❌ No chunks returned!")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Through speak_stream (what actually fails in assistant)
print("\n2. Testing through speak_stream():")
print("-" * 60)
try:
    gen = gemini_client.stream_generate("Who is Hrithik Roshan?")
    result = speak_stream(gen)
    print(f"   Result: {repr(result)}")
    if result:
        print(f"✅ Got response: {result}")
    else:
        print(f"❌ speak_stream returned empty!")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Full pipeline (streaming -> normalize -> clean)
print("\n3. Testing full pipeline (stream -> normalize -> clean):")
print("-" * 60)
try:
    gen = gemini_client.stream_generate("Who is Hrithik Roshan?")
    final_text = speak_stream(gen)
    print(f"   After speak_stream: {repr(final_text)}")
    
    if not final_text or not final_text.strip():
        print(f"❌ Empty response from stream_generate")
    else:
        # Normalize and clean
        cleaned = gemini_client.normalize_response(final_text)
        print(f"   After normalize_response: {repr(cleaned)}")
        
        final_clean = gemini_client.strip_json_noise(cleaned)
        print(f"   After strip_json_noise: {repr(final_clean)}")
        
        response_to_use = final_clean if final_clean else final_text
        if response_to_use and response_to_use.strip():
            print(f"✅ Final response to user: {response_to_use}")
        else:
            print(f"❌ Final response is empty!")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Test blocking call as fallback
print("\n4. Testing blocking API call (fallback):")
print("-" * 60)
try:
    response = gemini_client.generate_response("Who is Mia Khalifa?")
    print(f"   Response: {repr(response)}")
    if response and "trouble" not in response.lower():
        print(f"✅ Got response: {response}")
    else:
        print(f"❌ Got error: {response}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
