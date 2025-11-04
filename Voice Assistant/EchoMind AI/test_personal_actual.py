#!/usr/bin/env python3
"""Test personal handler with actual imports"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from handlers.personal_handler import handle_personal_questions

queries = [
    "i want to translate in quotation who are you in bengali",
    "translate who are you in bengali",
]

print("Testing with actual handler function:")
print("=" * 60)

for query in queries:
    print(f"\nQuery: '{query}'")
    result = handle_personal_questions(query)
    print(f"Handler returned: {result}")
    print(f"Expected: False (should NOT handle, should go to Gemini)")
