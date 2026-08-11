# Day 6 – Outbound Voice Calls 📞

## 10 Days of Voice Agents – VoiceForBharat Challenge

For Day 6, I extended **Nexa AI**, my Learning & Literacy voice agent, with **outbound calling** capabilities.

The goal was to make the voice agent capable of initiating a real phone/SIP call and interacting with the caller through the same conversational AI experience.

## 🚀 What I Built

* Added outbound calling support to Nexa AI.
* Integrated **LiveKit SIP** for telephony.
* Used **Linphone** as the SIP endpoint for testing.
* Created a dedicated outbound dialing module instead of modifying the existing Day 1–5 implementation.
* Added a command-line interface to initiate outbound calls.
* Kept the existing Nexa AI personality, tools, memory, and voice pipeline intact.

## 🏗️ Architecture

```text
User / Caller
     ↓
Linphone SIP
     ↓
LiveKit SIP
     ↓
Nexa AI Voice Agent
     ↓
STT → LLM → Murf Falcon TTS
     ↓
Voice Response
```

## 📁 Project Structure

```text
backend/
│
├── src/
│   ├── agent.py
│   ├── memory.py
│   │
│   └── telephony/
│       └── outbound/
│           └── dial.py
│
├── .env.local
└── README6.md
```

## 📞 Outbound Dialing

The outbound dialer can be run from the backend environment using:

```powershell
python src\telephony\outbound\dial.py --help
```

The available arguments include:

```text
--to TO
    Linphone SIP destination.

--room ROOM
    Optional LiveKit room name.
```

Example:

```powershell
python src\telephony\outbound\dial.py --to <SIP_DESTINATION>
```

## 🗣️ Call Opening & Safety

The outbound call is designed to clearly communicate:

1. Who is calling.
2. Why the call is being made.
3. That the recipient can opt out/end the call.

The implementation also considers common call outcomes such as:

* No answer
* Busy
* Voicemail
* Call hang-up

## 🎙️ Voice Pipeline

Nexa AI continues to use the existing voice pipeline:

* **Speech-to-Text:** Deepgram
* **LLM:** Google Gemini
* **Text-to-Speech:** **Murf Falcon**
* **Voice/Telephony:** LiveKit + SIP
* **SIP Client:** Linphone

## 🎯 Learning & Literacy Use Case

Nexa AI is designed as a friendly educational voice assistant.

Through outbound calling, the agent can be extended to support educational use cases such as:

* Study reminders
* Learning assistance
* Academic guidance
* Student follow-ups
* Educational information delivery

## 🔐 Privacy & Safety

The agent follows the existing safety rules:

* No passwords, OTPs, PINs, or banking information.
* No harmful or illegal assistance.
* No medical diagnosis or prescription.
* Memory is saved only with user permission.
* Users can end/opt out of the conversation.

## 📌 Day 6 Outcome

Day 6 added the **telephony layer** to Nexa AI, taking the project beyond a browser-based voice assistant toward a voice agent capable of initiating outbound SIP calls.

This brings Nexa AI one step closer to becoming a practical real-world voice assistant.

---

### Technologies Used

**Python · LiveKit Agents · LiveKit SIP · Linphone · Google Gemini · Deepgram · Murf Falcon TTS**

### Challenge

**10 Days of Voice Agents – VoiceForBharat Edition**

Built as part of the **Learning & Literacy** track.
