"""Music playback handler - Search and play songs on YouTube"""
import re
import subprocess
import webbrowser
from config.settings import OS
from utils.voice_io import speak
from utils.logger import log_interaction


def handle_play_music(command):
    """
    Handle play music commands
    Patterns:
    - "play <song_name>"
    - "play <song_name> by <artist>"
    - "play music <song_name>"
    """
    # Check if command contains play keyword
    if not re.search(r'\bplay\b', command, re.IGNORECASE):
        return False
    
    command_lower = command.lower().strip()
    
    # Extract the song query
    song_query = None
    
    # Pattern 1: "play <song>"
    if command_lower.startswith("play "):
        song_query = command_lower[5:].strip()
    # Pattern 2: "play music <song>"
    elif "play music" in command_lower:
        song_query = command_lower.replace("play music", "", 1).strip()
    # Pattern 3: Other variations with "play"
    elif " play " in command_lower:
        # Extract after "play"
        match = re.search(r'\bplay\s+(.+)', command_lower)
        if match:
            song_query = match.group(1).strip()
    
    # If we found a song query, search it on YouTube and play
    if song_query:
        try:
            # Build YouTube search URL
            youtube_url = f"https://www.youtube.com/results?search_query={song_query.replace(' ', '+')}"
            
            # Open YouTube search in browser
            if OS == "windows":
                subprocess.Popen(["cmd", "/c", f"start chrome {youtube_url}"], shell=True)
            elif OS == "darwin":  # macOS
                subprocess.Popen(["open", "-a", "Google Chrome", youtube_url])
            elif OS == "linux":
                subprocess.Popen(["google-chrome", youtube_url])
            
            speak(f"Searching for {song_query} on YouTube")
            log_interaction(command, f"YouTube search: {song_query}", source="music")
            return True
        except Exception as e:
            speak("Sorry, I couldn't search for the music on YouTube.")
            print(f"Music search error: {e}")
            log_interaction(command, f"Music error: {e}", source="music")
            return False
    
    return False


def handle_play_on_youtube(command):
    """
    Alternative handler for explicit YouTube play commands
    Patterns:
    - "play <song> on youtube"
    - "youtube play <song>"
    """
    if not re.search(r'\b(play|youtube)\b.*\byoutube\b', command, re.IGNORECASE):
        if not re.search(r'\byoutube\s+play\b', command, re.IGNORECASE):
            return False
    
    command_lower = command.lower().strip()
    
    # Extract song query
    song_query = None
    
    # Pattern 1: "play <song> on youtube"
    if "on youtube" in command_lower or "on you tube" in command_lower:
        match = re.search(r'play\s+(.+?)\s+on\s+you\s*tube', command_lower)
        if match:
            song_query = match.group(1).strip()
    # Pattern 2: "youtube play <song>"
    elif command_lower.startswith("youtube play"):
        song_query = command_lower[12:].strip()
    
    if song_query:
        try:
            # Build YouTube search URL
            youtube_url = f"https://www.youtube.com/results?search_query={song_query.replace(' ', '+')}"
            
            # Open YouTube search in browser
            if OS == "windows":
                subprocess.Popen(["cmd", "/c", f"start chrome {youtube_url}"], shell=True)
            elif OS == "darwin":  # macOS
                subprocess.Popen(["open", "-a", "Google Chrome", youtube_url])
            elif OS == "linux":
                subprocess.Popen(["google-chrome", youtube_url])
            
            speak(f"Playing {song_query} on YouTube")
            log_interaction(command, f"YouTube play: {song_query}", source="music")
            return True
        except Exception as e:
            speak("Sorry, I couldn't play the music on YouTube.")
            print(f"YouTube play error: {e}")
            log_interaction(command, f"YouTube play error: {e}", source="music")
            return False
    
    return False
