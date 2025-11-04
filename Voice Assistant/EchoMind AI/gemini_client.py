"""Lightweight Gemini client template.

This module provides a small, safe wrapper for reading the GEMINI_API_KEY from
the environment and shows where to implement real streaming calls to Gemini.

Important: This file does NOT contain any real key and does not make network
calls. Replace the `stream_response_stub` with an actual implementation that
uses your provider's streaming SDK or HTTP/gRPC/WebSocket API.
"""

import os
from typing import Generator, Optional
import requests

# Read config from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Optional: provider-specific HTTP endpoint (leave empty to use local stub)
GEMINI_API_ENDPOINT = os.getenv("GEMINI_API_ENDPOINT")
# Optional: name of header to send the API key in. If not set, Authorization: Bearer <key>
# Example for Google API key header: X-goog-api-key
GEMINI_API_KEY_HEADER = os.getenv("GEMINI_API_KEY_HEADER")


def ensure_key():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set. Put it in .env or environment variables.")


def stream_response_stub(prompt: str) -> Generator[str, None, None]:
    """Stub generator that yields chunks of text like a streaming LLM would.

    Replace this with an implementation that connects to Gemini's streaming
    endpoint and yields tokens/partial text as they arrive.
    """
    sample = (
        "This is a simulated streaming response from Gemini. Replace this stub "
        "with your provider's streaming client to receive real tokens."
    )
    for i in range(0, len(sample), 80):
        yield sample[i : i + 80]


def call_http_endpoint(prompt: str, timeout: float = 15.0) -> Optional[str]:
    """Call a configured HTTP endpoint (if set) and try to extract a text reply.

    The function is intentionally permissive about response shape to support
    different provider formats. It sends a JSON body {"prompt": prompt} and
    supplies the API key as a Bearer token. Set `GEMINI_API_ENDPOINT` in your
    environment to enable this behaviour.
    """
    if not GEMINI_API_ENDPOINT:
        return None
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY must be set to call GEMINI_API_ENDPOINT")

    # Support custom API key header (e.g., X-goog-api-key) or default to
    # Authorization: Bearer <key> when GEMINI_API_KEY_HEADER is not provided.
    if GEMINI_API_KEY_HEADER:
        headers = {GEMINI_API_KEY_HEADER: GEMINI_API_KEY, "Content-Type": "application/json"}
    else:
        headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
    payload = {"prompt": prompt}
    try:
        resp = requests.post(GEMINI_API_ENDPOINT, json=payload, headers=headers, timeout=timeout)
        resp.raise_for_status()
        # Attempt to parse JSON; if it fails we'll log raw text
        try:
            data = resp.json()
        except Exception:
            data = None
        # Log request/response for debugging (safe: do not log API keys)
        try:
            import json as _json, os as _os, datetime as _dt
            _logdir = _os.path.join(_os.getcwd(), "logs")
            _os.makedirs(_logdir, exist_ok=True)
            _entry = {"ts": _dt.datetime.utcnow().isoformat()+"Z", "endpoint": GEMINI_API_ENDPOINT, "prompt": prompt, "response_text": resp.text}
            with open(_os.path.join(_logdir, "gemini_responses.jsonl"), "a", encoding="utf-8") as _f:
                _f.write(_json.dumps(_entry, ensure_ascii=False)+"\n")
        except Exception:
            pass
        # Try a few common response shapes
        # 1) {"output": [{"content": "..."}]} or {"output": {"text": "..."}}
        if isinstance(data, dict):
            if "output" in data:
                out = data["output"]
                # nested content
                if isinstance(out, list) and out:
                    first = out[0]
                    if isinstance(first, dict) and "content" in first:
                        return first["content"]
                if isinstance(out, dict) and "text" in out:
                    return out["text"]
            # 2) OpenAI-like: {"choices": [{"message": {"content": "..."}}]}
            if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                choice = data["choices"][0]
                if isinstance(choice, dict):
                    # try message.content
                    msg = choice.get("message") or {}
                    if isinstance(msg, dict) and "content" in msg:
                        return msg["content"]
                    # try text
                    if "text" in choice:
                        return choice["text"]
            # 3) direct text field
            for key in ("text", "content", "response"):
                if key in data and isinstance(data[key], str):
                    return data[key]
        # Fallback: return raw text
        return resp.text
    except Exception:
        # Bubble up the error to the caller for logging/handling
        raise


def call_google_generate(prompt: str, timeout: float = 15.0) -> Optional[str]:
    """Call Google Generative Language `generateContent` endpoint.

    Builds the request body matching the curl example and attempts to extract
    a useful text reply from the JSON response. This function does not embed
    any key; it uses GEMINI_API_KEY and GEMINI_API_KEY_HEADER from environment.
    """
    if not GEMINI_API_ENDPOINT:
        return None
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY must be set to call Google endpoint")

    headers = {"Content-Type": "application/json"}
    if GEMINI_API_KEY_HEADER:
        headers[GEMINI_API_KEY_HEADER] = GEMINI_API_KEY
    else:
        headers["Authorization"] = f"Bearer {GEMINI_API_KEY}"

    # Google generateContent expects `contents: [{parts: [{text: ...}]}]`
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        resp = requests.post(GEMINI_API_ENDPOINT, json=payload, headers=headers, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        # Google response shapes can vary. Try common locations:
        # 1) data['candidates'][0]['content']['parts'][0]['text']
        if isinstance(data, dict):
            if "candidates" in data and isinstance(data["candidates"], list) and data["candidates"]:
                cand = data["candidates"][0]
                # candidate may have 'content' dict with 'parts' array
                if isinstance(cand, dict):
                    content = cand.get("content")
                    if isinstance(content, dict):
                        parts = content.get("parts")
                        if isinstance(parts, list) and parts:
                            first_part = parts[0]
                            if isinstance(first_part, dict) and "text" in first_part:
                                return first_part["text"]
                    # also try if content is a list
                    elif isinstance(content, list) and content:
                        first = content[0]
                        if isinstance(first, dict) and "text" in first:
                            return first["text"]
                    # candidate may have 'text' directly
                    if "text" in cand and isinstance(cand["text"], str):
                        return cand["text"]
            # 2) data['output'][0]['content'][0]['text']
            if "output" in data and isinstance(data["output"], list) and data["output"]:
                out0 = data["output"][0]
                if isinstance(out0, dict) and "content" in out0:
                    cont = out0["content"]
                    if isinstance(cont, list) and cont:
                        c0 = cont[0]
                        if isinstance(c0, dict) and "text" in c0:
                            return c0["text"]
            # 3) fallback: keys 'text' or 'response'
            for k in ("text", "response", "content"):
                if k in data and isinstance(data[k], str):
                    return data[k]
        return resp.text
    except requests.exceptions.Timeout:
        print(f"WARNING: API timeout calling {GEMINI_API_ENDPOINT}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"WARNING: API HTTP error {resp.status_code}: {e}")
        return None
    except Exception as e:
        print(f"WARNING: API error: {e}")
        return None


__all__ = ["GEMINI_API_KEY", "GEMINI_API_ENDPOINT", "ensure_key", "stream_response_stub", "call_http_endpoint"]


def generate_response(prompt: str) -> str:
    """Convenience blocking helper that returns a full response string.

    Behavior:
    - If GEMINI_API_ENDPOINT is set, call the HTTP endpoint using the API key
      and return the best-effort text extraction from the response.
    - If API fails, return a user-friendly error message instead of stub.
    """
    # If the configured endpoint looks like Google's Generative API or the key
    # header indicates Google, try the Google-specific caller first.
    try_google = False
    if GEMINI_API_ENDPOINT and "generativelanguage.googleapis.com" in GEMINI_API_ENDPOINT:
        try_google = True
    if GEMINI_API_KEY_HEADER and "goog" in GEMINI_API_KEY_HEADER.lower():
        try_google = True

    if try_google and GEMINI_API_ENDPOINT:
        try:
            out = call_google_generate(prompt)
            if out is not None:
                return out
        except Exception as e:
            # Don't print - let it continue to fallback
            pass

    # Try generic HTTP endpoint next (real provider)
    if GEMINI_API_ENDPOINT:
        try:
            out = call_http_endpoint(prompt)
            if out is not None:
                return out
        except Exception as e:
            # Don't print - let it continue to fallback
            pass

    # If both API calls failed/returned None, return error message instead of stub
    return "I'm having trouble connecting to my AI backend right now. Please try again in a moment."


def stream_generate(prompt: str):
    """Generator that yields incremental text chunks.

    Behavior:
    - If GEMINI_API_STREAM is set (true/1) and GEMINI_API_ENDPOINT is configured,
      attempt a streaming HTTP POST and yield incoming lines/chunks.
    - Otherwise, fall back to the local `stream_response_stub`.
    """
    stream_flag = os.getenv("GEMINI_API_STREAM", "").lower() in ("1", "true", "yes")
    
    if stream_flag and GEMINI_API_ENDPOINT and GEMINI_API_KEY:
        # Check if it's a Google endpoint
        is_google = "generativelanguage.googleapis.com" in GEMINI_API_ENDPOINT
        
        headers = {"Content-Type": "application/json"}
        if GEMINI_API_KEY_HEADER:
            headers[GEMINI_API_KEY_HEADER] = GEMINI_API_KEY
        else:
            headers["Authorization"] = f"Bearer {GEMINI_API_KEY}"
        
        # Use proper payload format for Google API
        if is_google:
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
        else:
            payload = {"prompt": prompt}
        
        try:
            with requests.post(GEMINI_API_ENDPOINT, json=payload, headers=headers, stream=True, timeout=30) as resp:
                resp.raise_for_status()
                for raw in resp.iter_lines(decode_unicode=True):
                    if not raw:
                        continue
                    # Try to parse JSON lines reasonably; otherwise yield raw text chunk
                    try:
                        import json as _json
                        part = _json.loads(raw)
                        # Try to extract quick text fields from the JSON chunk
                        if isinstance(part, dict):
                            # For Google API, check the proper structure
                            if is_google and "candidates" in part:
                                cands = part.get("candidates", [])
                                if cands and isinstance(cands[0], dict):
                                    content = cands[0].get("content", {})
                                    if isinstance(content, dict):
                                        parts = content.get("parts", [])
                                        if parts and isinstance(parts[0], dict):
                                            text = parts[0].get("text", "")
                                            if text:
                                                yield text
                                                continue
                            # Generic key search
                            for key in ("text", "content", "response"):
                                if key in part and isinstance(part[key], str):
                                    yield part[key]
                                    break
                            else:
                                # No known key, yield the raw chunk
                                yield raw
                        else:
                            yield raw
                    except Exception:
                        yield raw
            return
        except Exception as e:
            # Fall through to stub if streaming attempt fails
            print(f"Streaming failed: {e}")
            pass

    # Fallback: use blocking call instead of stub stream
    try:
        response = generate_response(prompt)
        if response and "simulated" not in response.lower():
            yield response
            return
    except Exception:
        pass
    
    # Last resort: stubbed stream
    for p in stream_response_stub(prompt):
        yield p

