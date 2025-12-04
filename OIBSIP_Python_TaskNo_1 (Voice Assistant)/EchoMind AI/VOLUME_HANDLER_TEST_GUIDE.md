# Quick Testing Guide - Volume Handler

## How to Test the Fixes

### Setup
1. Start the application:
   ```powershell
   & "C:\Program Files\Python313\python.exe" 'd:\Vs Code\PROJECT\OIBSIP\Voice Assistant\EchoMind AI\main_refactored.py'
   ```

2. Wait for:
   ```
   Speaking: Hey there! I am EchoMind AI, your voice assistant...
   Listening...
   ```

---

## Test Cases

### ✅ Test 1: Set Volume to Specific Percentage
```
Say: "set volume to 50"
Expected Output:
  You said: set volume to 50
  Speaking: Volume set to 50 percent
  
Check: Volume should actually change on your system
```

### ✅ Test 2: Set Volume with "Percent" Word
```
Say: "set volume to 75 percent"
Expected Output:
  You said: set volume to 75 percent
  Speaking: Volume set to 75 percent
  
Check: Volume should be at 75%
```

### ✅ Test 3: Mute Device Sound (with Article)
```
Say: "mute the device sound"
Expected Output:
  You said: mute the device sound
  Speaking: Muting sound
  
Check: F5 key should be pressed (system muted)
```

### ✅ Test 4: Mute Simple
```
Say: "mute yourself"
Expected Output:
  You said: mute yourself
  Speaking: Muting sound
  
Check: F5 should be pressed
```

### ✅ Test 5: Unmute Simple
```
Say: "unmute sound"
Expected Output:
  You said: unmute sound
  Speaking: Unmuting sound
  
Check: F5 should be pressed (system unmuted)
```

### ✅ Test 6: Unmute Complex
```
Say: "unmute the device"
Expected Output:
  You said: unmute the device
  Speaking: Unmuting sound
  
Check: F5 should be pressed
```

### ✅ Test 7: Volume Up
```
Say: "volume up"
Expected Output:
  You said: volume up
  Speaking: Increasing volume
  
Check: Volume should increase gradually (5 key presses)
```

### ✅ Test 8: Volume Down
```
Say: "volume down"
Expected Output:
  You said: volume down
  Speaking: Decreasing volume
  
Check: Volume should decrease gradually
```

### ✅ Test 9: Volume Louder
```
Say: "make it louder"
Expected Output:
  You said: make it louder
  Listening... (no match, passed to Gemini)
  
Note: "louder" alone without "volume" won't trigger handler
```

### ✅ Test 10: Volume Louder (Proper)
```
Say: "volume louder"
Expected Output:
  You said: volume louder
  Speaking: Increasing volume
  
Check: Volume should increase
```

### ✅ Test 11: Question Exclusion - How to Mute
```
Say: "how to mute device"
Expected Output:
  You said: how to mute device
  Speaking: (Gemini response about how to mute)
  
Check: F5 should NOT be pressed
        Should be handled by Gemini, not volume handler
```

### ✅ Test 12: Question Exclusion - Can You Mute
```
Say: "can you mute the device"
Expected Output:
  You said: can you mute the device
  Speaking: (Gemini response)
  
Check: F5 should NOT be pressed
        Should pass to Gemini handler
```

### ✅ Test 13: Unrelated Number
```
Say: "but it did not set"
Expected Output:
  You said: but it did not set
  Speaking: I'm sorry, I'm not sure what you mean...
  
Check: Volume handler should NOT match
        Should pass to Gemini or personal handler
```

### ✅ Test 14: Invalid Percentage
```
Say: "set volume to 150"
Expected Output:
  You said: set volume to 150
  Speaking: Volume must be between 0 and 100 percent. You said 150 percent which is invalid.
  
Check: Volume should NOT change
```

### ✅ Test 15: Zero Volume
```
Say: "set volume to 0"
Expected Output:
  You said: set volume to 0
  Speaking: Volume set to 0 percent
  
Check: Volume should be muted (0%)
```

---

## Expected Log Entries

When checking logs, you should see entries like:

```json
{"ts": "2024-11-08T10:30:45", "user": "set volume to 50", "response": "Volume set to 50%", "source": "local"}
{"ts": "2024-11-08T10:31:12", "user": "mute the device sound", "response": "Sound muted via F5 key press", "source": "local"}
{"ts": "2024-11-08T10:32:05", "user": "unmute yourself", "response": "Sound unmuted via F5 key press", "source": "local"}
{"ts": "2024-11-08T10:32:40", "user": "volume up", "response": "Volume increased", "source": "local"}
```

---

## Troubleshooting

### Issue: "F5 key method unavailable"
**Solution:** Install keyboard library
```bash
pip install keyboard
```

### Issue: Volume up/down doesn't work
**Check:**
1. Ensure `keyboard` or `pyautogui` is installed
2. Try pressing F5 hotkey separately - if that works, check your system volume hardware
3. Check Windows Sound mixer isn't muting the device

### Issue: "set volume to 50" still doesn't work
**Check:**
1. Full log entry shows action was attempted
2. Verify Windows Sound mixer is not grayed out
3. Try manual volume change to ensure hardware works
4. Check if nircmd is installed (fallback method)

### Issue: Mute not working but handler triggers
**Solution:**
- F5 pressing is working but system might already be in that state
- Try pressing F5 on keyboard manually to verify it toggles mute
- Check your system's mute hotkey (might be different than F5)

---

## Success Criteria

All tests should show:
- ✅ Correct speech output
- ✅ Correct log entries
- ✅ Actual system changes (volume changes, mute/unmute works)
- ✅ Questions don't trigger volume handler
- ✅ Unrelated commands don't accidentally trigger volume handler
