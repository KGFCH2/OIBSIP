#!/usr/bin/env python3
"""Test raw streaming response"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")

if not GEMINI_API_KEY or not GEMINI_API_ENDPOINT:
    print("Missing API key or endpoint")
    exit(1)

headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}
payload = {"contents": [{"parts": [{"text": "Who is Hrithik Roshan? Answer in one short sentence."}]}]}

print("Making streaming request...")
try:
    with requests.post(GEMINI_API_ENDPOINT, json=payload, headers=headers, stream=True, timeout=30) as resp:
        print(f"Status: {resp.status_code}")
        resp.raise_for_status()
        print("\n--- Raw streaming lines ---")
        for i, raw in enumerate(resp.iter_lines(decode_unicode=True)):
            print(f"[{i}] RAW: {repr(raw)}")
            if i > 20:  # Limit output
                print("...")
                break
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
