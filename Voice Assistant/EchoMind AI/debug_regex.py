#!/usr/bin/env python3
"""Debug personal handler regex"""
import re

test_queries = [
    "translate who are you in bengali",
    "i want to translate in quotation who are you in bengali",
    "who are you",
]

# Current pattern
override_keywords = r'\b(translate|convert|language|meaning|definition|spell|pronounce|write|encode|decode|in\s+(bengali|hindi|spanish|french|german|gujarati|tamil|telugu|kannada|marathi|punjabi|urdu|arabic|chinese|japanese|korean|russian|portuguese|italian|thai|vietnamese))\b'

print("Testing Override Pattern:")
print("=" * 60)
for query in test_queries:
    match = re.search(override_keywords, query, re.IGNORECASE)
    print(f"Query: '{query}'")
    print(f"Match: {match}")
    if match:
        print(f"Matched: '{match.group()}'")
    print()
