"""Simple PoC: simulated streaming LLM -> incremental local TTS

This PoC does NOT call any external LLM or TTS cloud service. It demonstrates
the streaming UX by yielding token-chunks from a simulated LLM and speaking
them incrementally with local TTS (pyttsx3). The example shows where to plug
in a real streaming Gemini client (WebSocket/gRPC/WebRTC) and a real streaming
TTS service.

Usage:
    python realtime_poc/poc.py

The script reads GEMINI_API_KEY from the environment if present and warns if
missing, but it will still run the simulation without a key.
"""

import os
import time
import threading
import queue
from typing import Generator

try:
    import pyttsx3
except Exception:
    pyttsx3 = None


class GeminiClientStub:
    """A stub that simulates streaming token generation from an LLM.

    Replace the stream_response method with real streaming client calls when
    integrating a provider that supports token-level streaming.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def stream_response(self, prompt: str) -> Generator[str, None, None]:
        # A simple simulation: partition a long response into chunks
        response = (
            "Sure — here's a brief summary: The weather today in your city is "
            "pleasant with mild temperatures. If you plan to go out, bring a light jacket. "
            "I can also show a detailed forecast if you'd like."
        )
        words = response.split()
        chunk = []
        for i, w in enumerate(words, 1):
            chunk.append(w)
            # yield every 6 words to simulate incremental token streaming
            if i % 6 == 0:
                yield " ".join(chunk)
                chunk = []
                time.sleep(0.18)  # simulate network + model delay
        if chunk:
            yield " ".join(chunk)


class LocalTTS:
    """Threaded, queued TTS using a single pyttsx3 engine instance.

    pyttsx3 is not safe to run multiple `runAndWait` loops concurrently. This
    class creates one engine and a worker thread that consumes text chunks from
    a queue and runs them sequentially, avoiding the `run loop already started`
    RuntimeError seen when creating many threads calling runAndWait.
    """

    def __init__(self):
        if pyttsx3 is None:
            raise RuntimeError("pyttsx3 is required for LocalTTS. Install it via pip.")
        # Single engine instance for the process
        self.engine = pyttsx3.init()
        self.queue: "queue.Queue[str]" = queue.Queue()
        self._stop_event = threading.Event()
        self._worker_thread = threading.Thread(target=self._worker, daemon=True)
        self._worker_thread.start()

    def _worker(self):
        while not self._stop_event.is_set():
            try:
                text = self.queue.get(timeout=0.1)
            except queue.Empty:
                continue
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print("TTS engine error:", e)
            finally:
                try:
                    self.queue.task_done()
                except Exception:
                    pass

    def speak_async(self, text: str):
        """Queue a text chunk to be spoken by the worker thread."""
        self.queue.put(text)

    def shutdown(self, timeout: float = 5.0):
        """Attempt to gracefully stop the worker and engine."""
        self._stop_event.set()
        # Wait for queue to drain
        try:
            self.queue.join()
        except Exception:
            pass
        try:
            self.engine.stop()
        except Exception:
            pass


def run_poc():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found in environment — running in simulated mode.")
    else:
        print("GEMINI_API_KEY found. (PoC still runs in simulated mode unless connected.)")

    client = GeminiClientStub(api_key=api_key)

    try:
        tts = LocalTTS()
    except RuntimeError as e:
        print(e)
        print("Install requirements: pip install pyttsx3")
        return

    prompt = "What's the weather like today?"
    print("Prompt ->", prompt)
    print("Simulating streaming response and incremental TTS (speak as chunks arrive)...\n")

    for chunk in client.stream_response(prompt):
        print("[chunk]", chunk)
        # Speak each chunk as it arrives
        tts.speak_async(chunk)
        # In a real pipeline you may want to buffer a little to avoid choppy audio
        time.sleep(0.05)

    # Wait for queued speech to finish, then shutdown the TTS worker
    try:
        tts.queue.join()
    except Exception:
        pass
    tts.shutdown()
    print("Done streaming simulation.")


if __name__ == "__main__":
    run_poc()
