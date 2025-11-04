#!/usr/bin/env python3
"""Test handler logic for translation queries"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from handlers.personal_handler import handle_personal_questions

test_cases = [
    # Should be handled (return True)
    ("who are you", True, "Personal question"),
    ("how are you", True, "Personal question"),
    ("what is your name", True, "Personal question"),
    
    # Should NOT be handled (return False) - translation queries
    ("translate who are you in bengali", False, "Translation query - should go to Gemini"),
    ("who are you in bengali", False, "Language query - should go to Gemini"),
    ("translate how are you to spanish", False, "Translation query - should go to Gemini"),
    ("convert who are you to french", False, "Conversion query - should go to Gemini"),
    ("what does who are you mean in hindi", False, "Translation query - should go to Gemini"),
]

print("Testing Personal Questions Handler\n" + "="*50)
for command, expected, description in test_cases:
    result = handle_personal_questions(command)
    status = "✓ PASS" if result == expected else "✗ FAIL"
    print(f"{status}: '{command}'")
    print(f"  Expected: {expected}, Got: {result}")
    print(f"  ({description})")
    print()
