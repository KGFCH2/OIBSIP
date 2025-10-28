import argparse
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
from datetime import datetime
from urllib.parse import quote_plus
import time


def init_tts(rate: int = 150, text_only: bool = False):
    """Initialize and return a pyttsx3 engine, or None when text-only mode is requested.

    Try a platform-appropriate driver (sapi5 on Windows) and fall back to default.
    If initialization fails, return None so the program continues in text-only mode.
    """
    if text_only:
        return None
    try:
        # On Windows, sapi5 is usually the best choice
        engine = None
        try:
            engine = pyttsx3.init(driverName='sapi5')
        except Exception:
            # fallback to default driver
            engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        return engine
    except Exception as e:
        print(f"TTS initialization failed: {e}. Continuing in text-only mode.")
        return None


def speak(engine, text: str):
    """Speak the provided text (and print for feedback).

    If engine is None (text-only mode), only print the text.
    """
    print("EchoMind:", text)
    if engine is not None:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            # If TTS fails at runtime, print the error and continue with text only
            print(f"TTS error: {e}")


def take_command(recognizer, microphone):
    """Listen from the microphone and return recognized lowercase text.

    Returns empty string on failure so caller can decide next steps.
    """
    with microphone as source:
        # reduce ambient noise for a short moment
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            print("No speech detected (timeout).")
            return ""

    try:
        query = recognizer.recognize_google(audio, language='en-US')
        print("You said:", query)
        return query.lower()
    except sr.UnknownValueError:
        print("Speech unintelligible.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from recognition service; {e}")
        return ""


def handle_query(query: str, engine):
    if not query:
        speak(engine, "Sorry, I didn't catch that. Please repeat.")
        return False

    # Greetings
    if any(g in query for g in ["hello", "hi", "how are you"]):
        speak(engine, "Hello! I'm EchoMind. How can I help you today?")
        return False

    # Time
    if "time" in query:
        now = datetime.now().strftime("%I:%M %p")
        speak(engine, f"The time is {now}")
        return False

    # Date
    if "date" in query or "day" in query:
        today = datetime.now().strftime("%A, %B %d, %Y")
        speak(engine, f"Today is {today}")
        return False

    # Wikipedia search
    if "wikipedia" in query or query.startswith("search wikipedia for"):
        # extract topic
        topic = query.replace("wikipedia", "").replace("search", "").replace("for", "").strip()
        if not topic:
            speak(engine, "What should I search on Wikipedia?")
            return False
        speak(engine, f"Searching Wikipedia for {topic}")
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(engine, summary)
        except wikipedia.DisambiguationError as e:
            speak(engine, "The topic is ambiguous. Please be more specific.")
        except Exception as e:
            speak(engine, "Sorry, I couldn't find information on that topic.")
        return False

    # Open websites
    if "open youtube" in query:
        speak(engine, "Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        return False

    if "open google" in query:
        speak(engine, "Opening Google")
        webbrowser.open("https://www.google.com")
        return False

    # Google search
    if query.startswith("search google for") or query.startswith("search for"):
        # accept: "search google for cats" or "search for cats"
        search_term = query
        for prefix in ("search google for", "search for"):
            if search_term.startswith(prefix):
                search_term = search_term.replace(prefix, "").strip()
                break
        if search_term:
            speak(engine, f"Searching Google for {search_term}")
            url = f"https://www.google.com/search?q={quote_plus(search_term)}"
            webbrowser.open(url)
        else:
            speak(engine, "What should I search for on Google?")
        return False

    # Exit commands
    if any(term in query for term in ["stop", "quit", "exit"]):
        speak(engine, "Goodbye!")
        return True

    # If no known command matched
    speak(engine, "Sorry, I don't know that command. Try asking the time, date, or to open a website.")
    return False


def main():
    parser = argparse.ArgumentParser(description="EchoMind Basic voice assistant")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--text-only', action='store_true', help='Disable TTS; print responses only')
    group.add_argument('--tts', action='store_true', help='Force enable TTS (override any local defaults)')
    args = parser.parse_args()

    recognizer = sr.Recognizer()
    try:
        microphone = sr.Microphone()
    except OSError:
        print("No microphone found or microphone not accessible.")
        return

    # Decide TTS mode: if --text-only provided -> text-only; if --tts provided -> enable TTS;
    # otherwise keep default (TTS enabled unless --text-only passed)
    text_only_mode = False
    if args.text_only:
        text_only_mode = True
    elif args.tts:
        text_only_mode = False

    engine = init_tts(text_only=text_only_mode)

    speak(engine, "EchoMind Basic initialized. Say something to begin.")

    try:
        while True:
            query = take_command(recognizer, microphone)
            should_exit = handle_query(query, engine)
            if should_exit:
                break
            # small pause so TTS finishes and next recognition doesn't pick it up
            time.sleep(0.3)
    except KeyboardInterrupt:
        print("Interrupted by user.")
        speak(engine, "Goodbye!")


if __name__ == "__main__":
    main()
