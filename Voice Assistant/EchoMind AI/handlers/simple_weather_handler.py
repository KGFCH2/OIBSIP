"""Simple city weather handler"""
import re
import os
from utils.weather import get_weather
from utils.voice_io import speak
from utils.logger import log_interaction

def handle_simple_city_weather(command):
    """Handle simple city name as weather query"""
    try:
        words = command.split()
        simple_city_candidate = False
        
        # Single word city - check blacklist of common question/command words
        if len(words) == 1 and re.match(r"^[a-zA-Z]{3,40}$", command):
            blacklist_tokens = ("why", "what", "when", "where", "how", "do", "did", "does", "don't", "didn't", "tell", "is", "are", "be", "open", "hello", "hi")
            if command.lower() not in blacklist_tokens:
                simple_city_candidate = True
        
        if simple_city_candidate:
            weather_info = get_weather(command)
            if weather_info and not weather_info.lower().startswith("sorry"):
                speak(weather_info)
                log_interaction(command, weather_info, source="local")
                return True
    except Exception:
        pass
    
    return False
