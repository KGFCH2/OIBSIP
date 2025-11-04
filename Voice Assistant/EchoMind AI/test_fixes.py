#!/usr/bin/env python
"""Test script to verify JSON parsing and system prompt removal works"""

import re
import json

def test_json_decoder():
    """Test the improved JSONDecoder approach"""
    print("=" * 60)
    print('TEST: JSONDecoder approach for extracting "text" field')
    print("=" * 60)
    
    # Simulate streaming JSON lines from API
    test_lines = [
        '{"candidates": [{"content": {"parts": [{"text": "The most common and natural way to say"}]}}]}',
        '{"candidates": [{"content": {"parts": [{"text": " \\"good night\\" in"}]}}]}',
        '{"candidates": [{"content": {"parts": [{"text": " Bengali is \\"শুভ"}]}}]}',
        '{"candidates": [{"content": {"parts": [{"text": "রাত্রি\\" or \\"Shubho"}]}}]}',
        '{"candidates": [{"content": {"parts": [{"text": " ratri\\""}]}}]}',
    ]
    
    def extract_text_from_line(raw):
        """Extract text using JSONDecoder like the fixed code"""
        text_match = re.search(r'"text"\s*:\s*', raw)
        if text_match:
            start_pos = text_match.end()
            try:
                decoder = json.JSONDecoder()
                text_content, _ = decoder.raw_decode(raw[start_pos:])
                if text_content and isinstance(text_content, str):
                    return text_content
            except Exception as e:
                print(f"  ERROR: {e}")
                return None
        return None
    
    all_text = []
    for line in test_lines:
        text = extract_text_from_line(line)
        if text:
            print(f"  Extracted: {repr(text)}")
            all_text.append(text)
    
    result = ''.join(all_text)
    print(f"\nFull text joined: {repr(result)}")
    print(f"Readable: {result}\n")
    
    return result


def test_system_prompt_removal():
    """Test that system prompt removal works"""
    print("=" * 60)
    print("TEST: System prompt removal")
    print("=" * 60)
    
    test_cases = [
        "Okay, I understand. I will provide complete and detailed answers in plain text, without JSON, code blocks, or any special formatting. I will also close the conversation when asked. Just let me know what you need! ... conversation closed.",
        "You are a helpful voice assistant. Provide complete, detailed answers. Do not include JSON, code blocks, or formatting - just plain text.\n\nAnswer: Some content here",
        "I will provide complete and detailed answers. Here's the real answer to your question.",
        "I understand. I will provide complete answers in plain text. The actual response starts here.",
    ]
    
    patterns = [
        r"(?i)you are a helpful voice assistant\s*\..*?plain text\.",
        r"(?i)i will provide complete.*?plain text\.",
        r"(?i)okay.*?i understand.*?plain text\.",
        r"(?i)i understand.*?i will provide.*?plain text\.",
        r"(?i)\s*i will provide complete and detailed answers.*?\.",
        r"(?i)^\s*okay, i understand\..*?(?=\n|$)",
        r"(?i)okay[,.].*?close the conversation.*?\.",
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest case {i}:")
        print(f"  Before: {repr(test[:60])}..." if len(test) > 60 else f"  Before: {repr(test)}")
        
        result = test
        for pattern in patterns:
            result = re.sub(pattern, '', result, flags=re.MULTILINE | re.DOTALL)
        
        result = result.strip()
        print(f"  After:  {repr(result[:60])}..." if len(result) > 60 else f"  After:  {repr(result)}")
    
    print()


def test_backslash_truncation():
    """Test that backslash truncation is fixed"""
    print("=" * 60)
    print("TEST: Backslash truncation fix")
    print("=" * 60)
    
    # This is what was failing with the old regex
    problem_json = r'{"candidates": [{"content": {"parts": [{"text": "Whether or not that makes me \\"smart\\" depends on how you define intelligence."}]}}]}'
    
    print(f"\nProblem JSON: {problem_json}\n")
    
    # Old approach (BROKEN)
    print("OLD APPROACH (broken):")
    old_regex = r'"text":\s*"([^"]*(?:\\.[^"]*)*)"'
    old_match = re.search(old_regex, problem_json)
    if old_match:
        old_text = old_match.group(1)
        print(f"  Extracted: {repr(old_text)}")
    else:
        print("  No match!")
    
    # New approach (FIXED)
    print("\nNEW APPROACH (fixed):")
    text_match = re.search(r'"text"\s*:\s*', problem_json)
    if text_match:
        start_pos = text_match.end()
        try:
            decoder = json.JSONDecoder()
            text_content, _ = decoder.raw_decode(problem_json[start_pos:])
            print(f"  Extracted: {repr(text_content)}")
            print(f"  Readable: {text_content}")
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ECHOMIND AI - JSON PARSING & PROMPT REMOVAL TEST SUITE")
    print("=" * 60 + "\n")
    
    test_json_decoder()
    test_system_prompt_removal()
    test_backslash_truncation()
    
    print("=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)
