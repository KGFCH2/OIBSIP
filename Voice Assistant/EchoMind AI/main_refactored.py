"""
EchoMind AI - Main entry point for the voice assistant
This refactored version uses modular architecture for better maintainability
"""
import os
from dotenv import load_dotenv

# Load environment variables BEFORE importing other modules
load_dotenv()

# Import all handlers
from handlers.thank_you_handler import handle_thank_you
from handlers.greeting_handler import handle_greeting
from handlers.time_handler import handle_time
from handlers.date_handler import handle_date
from handlers.simple_weather_handler import handle_simple_city_weather
from handlers.weather_handler import handle_weather
from handlers.web_handler import handle_browser_search, handle_website_opening
from handlers.file_handler import handle_file_opening
from handlers.app_handler import handle_app_opening
from handlers.personal_handler import handle_personal_questions
from handlers.volume_handler import handle_volume
from handlers.close_app_handler import handle_app_closing
from handlers.exit_handler import handle_exit

# Import utilities
from utils.voice_io import speak, listen
from utils.text_processing import convert_spoken_symbols, is_symbol_only
from utils.time_utils import get_greeting
from utils.logger import log_interaction

# Import Gemini client
import gemini_client


def route_command(command):
    """Route command to appropriate handler"""
    handlers = [
        ("Thank you", handle_thank_you),
        ("Greeting", handle_greeting),
        ("Time", handle_time),
        ("Date", handle_date),
        ("Simple city weather", handle_simple_city_weather),
        ("Weather", handle_weather),
        ("Browser search", handle_browser_search),
        ("Website opening", handle_website_opening),
        ("File opening", handle_file_opening),
        ("App opening", handle_app_opening),
        ("Personal questions", handle_personal_questions),
        ("Volume control", handle_volume),
        ("App closing", handle_app_closing),
        ("Exit", handle_exit),
    ]
    
    for handler_name, handler in handlers:
        if handler_name == "Exit":
            # Special case for exit
            if handle_exit(command):
                return "exit"
        else:
            if handler(command):
                return "handled"
    
    return "not_handled"


def handle_gemini_fallback(command):
    """Handle unknown commands with Gemini"""
    try:
        stream_flag = os.getenv("GEMINI_API_STREAM", "").lower() in ("1", "true", "yes")
        if stream_flag:
            try:
                for chunk in gemini_client.stream_generate(command):
                    if chunk:
                        print("[stream chunk]", chunk)
                        speak(chunk)
                log_interaction(command, "(streamed response)", source="gemini_stream")
            except Exception as e:
                print("Streaming error:", e)
                speak("Sorry, there was an error with streaming response.")
        else:
            response = gemini_client.generate_response(command)
            if response:
                speak(response)
                log_interaction(command, response, source="gemini")
            else:
                speak("Sorry, I couldn't generate a response.")
                log_interaction(command, "No response returned", source="gemini")
    except Exception as e:
        print(f"Gemini integration error: {e}")
        speak("Sorry, I couldn't process that right now.")
        log_interaction(command, f"Gemini error: {e}", source="gemini")


def main():
    """Main function - voice assistant loop"""
    greeting = get_greeting()
    speak(greeting)
    
    while True:
        # Listen for command
        command = listen()
        if not command:
            continue
        
        # Convert spoken symbols to actual punctuation marks
        command = convert_spoken_symbols(command)
        
        # Skip if command is only symbols
        if command and is_symbol_only(command):
            speak("I didn't catch a complete command. Could you please say something more?")
            continue
        
        # Route the command to handlers
        result = route_command(command)
        
        if result == "exit":
            speak("Goodbye!")
            break
        elif result == "handled":
            # Handler already processed the command
            continue
        else:
            # No handler matched, try Gemini
            handle_gemini_fallback(command)


if __name__ == "__main__":
    main()
