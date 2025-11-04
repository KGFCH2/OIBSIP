# 🔴 THE ERROR EXPLAINED & FIXED

## What The Error Was

```
Streaming error: global flags not at the start of the expression at position 1
```

This error happens when you use inline regex flags like `(?i)` in the middle of a pattern **AND** also pass flags to `re.sub()`.

## Why It Happened

### ❌ BEFORE (BROKEN CODE):

```python
system_prompt_patterns = [
    r"(?i)you are a voice assistant\b.*?(?:plain text|...).*?\.",  
    r"(?i)okay[,.]?\s*(?:i\s+)?understand\..*?(?=\n|$)",
    # ... more patterns with inline (?i) flag
]

for pattern in system_prompt_patterns:
    text = re.sub(pattern, '', text, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
```

**Problem**: 
- Pattern has inline `(?i)` flag AND
- Also passing `flags=re.IGNORECASE` to re.sub()
- This creates a conflict → regex compilation error!

### ✅ AFTER (FIXED CODE):

```python
system_prompt_patterns = [
    r"^you are a voice assistant[^.\n]*\.",  # NO inline flag
    r"^okay[,.]?\s*(?:i\s+)?understand\.\s*",  # NO inline flag
    # ... patterns without inline flags
]

for pattern in system_prompt_patterns:
    text = re.sub(pattern, '', text, flags=re.MULTILINE | re.IGNORECASE)  # Flags passed here
```

**Solution**: 
- Removed all inline flags from patterns
- Pass all flags via the `flags` parameter

## Bonus Fix: Over-Aggressive Matching

The old code had another bug beyond the regex error:

### ❌ OLD PATTERN BEHAVIOR:
```python
r"(?i)okay[,.]?\s*(?:i\s+)?understand\..*?(?=\n|$)"
```

With `re.DOTALL` flag, `.` matches NEWLINES too! So:
```
Input:  "Okay I understand. Hrithik Roshan is an actor."
Match:  "Okay I understand. Hrithik Roshan is an actor." (removes EVERYTHING!)
Output: "" (empty!)
```

### ✅ NEW PATTERN BEHAVIOR:
```python
r"^okay[,.]?\s*(?:i\s+)?understand\.\s*"
```

Now it only removes the system prompt itself:
```
Input:  "Okay I understand. Hrithik Roshan is an actor."
Match:  "Okay I understand. " (only the prompt)
Output: "Hrithik Roshan is an actor." (preserves the answer!)
```

## The Real Cause of Your "No Response" Issue

Your queries were failing because:

1. ✅ API call succeeded
2. ✅ Streaming returned chunks
3. ❌ `strip_json_noise()` regex failed with "global flags not at start" error
4. ❌ Exception caught in try/except, printed as "Streaming error"
5. ❌ Code tried fallback but eventually gave up
6. ❌ User heard nothing

Now with the fix:

1. ✅ API call succeeds
2. ✅ Streaming returns chunks
3. ✅ `strip_json_noise()` properly cleans response (no error)
4. ✅ Response reaches user

## Verification

All tests passing:

```
✅ Test 1: Direct streaming - Got chunk(s)
✅ Test 2: Through speak_stream() - Got response
✅ Test 3: Full pipeline - Got final response
✅ Test 4: Fallback API call - Got response
```

**File Changed**: `gemini_client.py` - Function: `strip_json_noise()`

**Now Ready**: Restart assistant and test!
