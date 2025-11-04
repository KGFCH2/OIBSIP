"""Web search and browser handlers"""
import re
import subprocess
import webbrowser
from config.settings import OS, WEBSITE_MAP
from utils.voice_io import speak, listen
from utils.logger import log_interaction

def handle_web_search(command):
    """Handle web search commands"""
    url = f"https://www.google.com/search?q={command}"
    webbrowser.open(url)
    speak(f"Searching for {command} on Google")
    log_interaction(command, f"Search opened: {command}", source="local")

def handle_browser_search(command):
    """Handle browser-based search and opening"""
    # Pattern: "open/search <query> on/in <browser>"
    if not re.search(r'\b(open|search)\b.*\b(on|in)\b.*\b(chrome|firefox|edge|google)\b', command, re.IGNORECASE):
        return False
    
    command_lower = command.lower()
    
    # Extract browser
    browser = None
    browser_name = None
    if "chrome" in command_lower or "google" in command_lower:
        browser = "chrome"
        browser_name = "chrome"
    elif "firefox" in command_lower:
        browser = "firefox"
        browser_name = "firefox"
    elif "edge" in command_lower:
        browser = "edge"
        browser_name = "microsoft edge"
    
    # Extract search query
    query = None
    if " on " in command_lower:
        parts = command_lower.split(" on ")
        if len(parts) >= 2:
            query_part = parts[0]
            if query_part.startswith("open "):
                query = query_part[5:].strip()
            elif query_part.startswith("search "):
                query = query_part[7:].strip()
            else:
                query = query_part.strip()
    elif " in " in command_lower:
        parts = command_lower.split(" in ")
        if len(parts) >= 2:
            query_part = parts[0]
            if query_part.startswith("open "):
                query = query_part[5:].strip()
            elif query_part.startswith("search "):
                query = query_part[7:].strip()
            else:
                query = query_part.strip()
    
    if browser and query:
        try:
            # Check if query is a URL or a search term
            if query.startswith("http://") or query.startswith("https://") or "." in query:
                url = query if query.startswith("http") else f"https://{query}"
            else:
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            
            # Launch the browser
            if browser == "chrome":
                if OS == "windows":
                    subprocess.Popen(["cmd", "/c", f"start chrome {url}"], shell=True)
                elif OS == "darwin":
                    subprocess.Popen(["open", "-a", "Google Chrome", url])
                elif OS == "linux":
                    subprocess.Popen(["google-chrome", url])
            elif browser == "firefox":
                if OS == "windows":
                    subprocess.Popen(["cmd", "/c", f"start firefox {url}"], shell=True)
                elif OS == "darwin":
                    subprocess.Popen(["open", "-a", "Firefox", url])
                elif OS == "linux":
                    subprocess.Popen(["firefox", url])
            elif browser == "edge":
                if OS == "windows":
                    subprocess.Popen(["cmd", "/c", f"start msedge {url}"], shell=True)
                elif OS == "darwin":
                    subprocess.Popen(["open", "-a", "Microsoft Edge", url])
                elif OS == "linux":
                    subprocess.Popen(["microsoft-edge", url])
            
            speak(f"Opening {query} on {browser_name}")
            log_interaction(command, f"Opened {query} on {browser_name}", source="local")
            return True
        except Exception as e:
            speak("Sorry, I couldn't open that in the browser.")
            print(f"Browser opening error: {e}")
            return False
    
    return False

def handle_website_opening(command):
    """Handle website opening commands"""
    if not re.search(r'\b(open|visit|go to)\b\s+(youtube|wikipedia|reddit|github|facebook|twitter|instagram|gmail|google\.com|stack\s*overflow)', command, re.IGNORECASE):
        return False
    
    command_lower = command.lower()
    
    # Find which website was mentioned
    website = None
    for site_key in WEBSITE_MAP:
        if site_key in command_lower:
            website = site_key
            break
    
    if website:
        try:
            url = WEBSITE_MAP[website]
            if OS == "windows":
                subprocess.Popen(["cmd", "/c", f"start chrome {url}"], shell=True)
            elif OS == "darwin":
                subprocess.Popen(["open", "-a", "Google Chrome", url])
            elif OS == "linux":
                subprocess.Popen(["google-chrome", url])
            speak(f"Opening {website}")
            log_interaction(command, f"Opened {website}", source="local")
            return True
        except Exception as e:
            speak(f"Sorry, I couldn't open {website}.")
            print(f"Error: {e}")
            return False
    
    return False
