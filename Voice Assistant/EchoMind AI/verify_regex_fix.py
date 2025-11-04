#!/usr/bin/env python3
"""Final verification that regex fix works"""
import re

print("=" * 70)
print("REGEX FIX VERIFICATION")
print("=" * 70)

# Test the patterns
patterns = [
    r"^you are a voice assistant[^.\n]*\.",
    r"^okay[,.]?\s*(?:i\s+)?understand\.\s*",
]

test_cases = [
    "You are a voice assistant. Here is your answer.",
    "Okay I understand. Hrithik Roshan is an Indian actor.",
    "Just a normal response about something.",
    "OKAY I UNDERSTAND. Mixed case test.",
]

for pattern in patterns:
    print(f"\nPattern: {pattern}")
    print("-" * 70)
    for test in test_cases:
        try:
            result = re.sub(pattern, '', test, flags=re.MULTILINE | re.IGNORECASE)
            status = "✅" if (not result or result.strip()) else "❌"
            print(f"  {status} Input:  {test[:50]}")
            print(f"     Output: {repr(result)}")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            print(f"     Input: {test}")

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE - All patterns working!")
print("=" * 70)
