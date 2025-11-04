"""Personal questions handler"""
import re
from utils.voice_io import speak
from utils.logger import log_interaction

def handle_personal_questions(command):
    """Handle personal questions about the assistant"""
    if re.search(r'\b(how are you|how do you do)\b', command, re.IGNORECASE):
        speak("I'm doing well, thank you! How can I assist you?")
        log_interaction(command, "I'm doing well, thank you! How can I assist you?", source="local")
        return True
    elif re.search(r'\b(your name|who are you|what are you)\b', command, re.IGNORECASE):
        speak("I am EchoMind AI, your voice assistant.")
        log_interaction(command, "I am EchoMind AI, your voice assistant.", source="local")
        return True
    
    return False
