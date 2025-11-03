## Realtime voice assistant architecture

This document describes a practical architecture for building a low-latency, streaming voice assistant that can use an LLM (e.g., Gemini) for generation and synthesize audio while the model is still producing tokens.

### Goal
- Support near-real-time conversation: user speaks, the assistant understands (ASR), generates responses incrementally (streaming LLM), and speaks them as audio chunks (streaming TTS).

### Components
- Client (browser or native app): captures microphone audio, plays back audio, shows transcripts.
- Signaling / Transport: WebRTC is recommended for real-time audio transport (bidirectional, low-latency). Alternately use a WebSocket + RTP gateway.
- ASR (Streaming Speech-to-Text): converts audio to text in small chunks (partial transcripts). Choices: Whisper Realtime, Google Speech-to-Text streaming, or other low-latency ASR.
- Orchestrator / Server: receives transcripts and user events, manages session context, calls LLM streaming endpoints and TTS, and forwards audio back to client. Can be serverless or a dedicated server.
- LLM (Gemini or other): use a streaming endpoint that returns tokens incrementally (websocket/gRPC/WebRTC). The orchestrator feeds it transcripts and tool outputs.
- Tooling / Retrieval: connectors for live data (weather, stock, search) — these are invoked synchronously or asynchronously and their results injected into the model context.
- TTS (Streaming): synthesize speech from partial text. Options include cloud streaming TTS or local TTS models for lower latency.

### Dataflow (simplified)
1. Client streams microphone audio to server via WebRTC.
2. Server runs streaming ASR → emits partial transcript.
3. Server adds transcript to session context and forwards it to the LLM streaming endpoint.
4. LLM returns tokens as they are generated. The server groups tokens into small chunks and forwards each chunk to the TTS subsystem.
5. TTS streams back audio chunks to server which forwards them to client (WebRTC audio track) and/or the server plays them locally.
6. If the user interrupts, VAD triggers a stop signal to the TTS and LLM (if supported).

### Implementation options
- Transport: WebRTC (recommended) or WebSocket + RTP.
- ASR: Whisper Realtime (open-source), Google Speech-to-Text streaming, Deepgram, Vosk.
- LLM streaming: Provider streaming APIs (WebSocket/gRPC/WebRTC). If Gemini has a WebRTC or streaming gRPC API, use that for lowest-latency.
- TTS: cloud streaming TTS (Google, AWS) or local TTS (Coqui TTS, Tacotron/Glow-TTS + vocoder) for lower latency and privacy.
- Orchestration language: Python (asyncio), Node.js, or Go are common choices.

### Latency tuning
- Keep chunk sizes small (200–600 ms of text) but not too small to avoid choppy speech.
- Pre-warm sessions and reuse connections.
- Collocate services (ASR/LLM/TTS) in same cloud region.
- Use hardware acceleration for TTS when available.

### Security and privacy
- Never log or store raw audio or keys unnecessarily.
- Use end-to-end encryption for audio transport (WebRTC does this by default).
- Use secret managers for API keys (do not commit keys to repo).

### Costs and operational concerns
- Streaming many tokens and audio minutes is billed by providers — monitor usage.
- Keep an economy mode (short replies) to limit costs.

### Example next steps / PoC
- Build a server that simulates streaming using a local LLM stub and local TTS to demonstrate UX and timing.
- Replace stubs with real ASR/LLM/TTS in stages, validating latency and UX at each step.

---
This file is a concise plan and reference for implementing the realtime features in this repo.
