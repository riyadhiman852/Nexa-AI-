# Nexa AI — Personalised Voice Agent Frontend

## Day 3 — Personalise Your Agent's Frontend

Nexa AI is a personalised voice AI assistant built as part of **10 Days of Voice Agents**. For Day 3, the starter frontend was customised to create a simple, user-friendly interface that matches the **Education** track.

The frontend provides a clear voice interaction experience and makes the agent's current state visible to the user.

---

## 🎯 Day 3 Objective

The goal of Day 3 was to personalise the voice agent's frontend and make the complete voice interaction flow easy to understand and use.

The frontend was customised from the starter repository with:

* Personalised branding and text
* Education-focused interface
* Clear call controls
* Voice-agent state indicators
* Connection and conversation feedback
* Microphone permission handling
* Live voice interaction through LiveKit

---

## ✨ Frontend Features

### 1. Personalised User Interface

The original starter frontend was customised for **Nexa AI** and the Education track.

The interface focuses on keeping the experience:

* Simple
* Clean
* Easy to understand
* Focused on voice interaction
* Suitable for an educational voice assistant

---

### 2. Agent States

The frontend communicates the agent's current state clearly during the conversation.

| State          | What the user sees                                  |
| -------------- | --------------------------------------------------- |
| **Ready**      | The agent is ready to start                         |
| **Connecting** | The agent is connecting to the voice session        |
| **Listening**  | The agent is listening to the user                  |
| **Speaking**   | The agent is responding                             |
| **Call Ended** | The conversation has ended and can be started again |

This helps the user understand what the voice agent is doing without confusion.

---

### 3. Voice Activity Feedback

The interface provides visual feedback during voice interaction so the user can understand whether the agent is listening or speaking.

This creates a more natural voice-assistant experience instead of making the interaction feel like a static webpage.

---

### 4. Microphone Permission Handling

Nexa AI requires microphone access for voice conversations.

If microphone permission is blocked, the frontend provides a clear indication that microphone access is required so the user can enable it and continue the conversation.

---

### 5. Complete Voice Flow

The frontend was tested through the complete interaction flow:

```text
Page Load
    ↓
Ready
    ↓
Connect
    ↓
Connecting
    ↓
Listening
    ↓
User Speaks
    ↓
Agent Responds
    ↓
Speaking
    ↓
Conversation Continues
    ↓
Call Ended
    ↓
Start Again
```

---

## 🎙️ Voice Agent

The frontend connects to the voice agent through **LiveKit** for real-time voice communication.

The agent uses **Murf Falcon** for text-to-speech, providing fast and natural voice responses.

This project is being developed as part of:

**10 Days of Voice Agents**

and the **#VoiceForBharat** challenge.

---

## 🌐 Language Interaction

Nexa AI is designed with Indian users in mind.

The voice interaction can support English conversations and can also respond in **Hindi** when requested, making the assistant more accessible for Indian users.

---

## 🛠️ Technology Stack

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS
* LiveKit Components

### Voice / AI

* LiveKit
* Murf Falcon TTS
* Google Gemini
* Deepgram

---

## 📁 Frontend Structure

The frontend is based on the LiveKit starter application and was personalised for Nexa AI.

Important areas include:

```text
frontend/
├── app/
├── components/
├── hooks/
├── lib/
├── public/
├── styles/
├── app-config.ts
├── package.json
└── ...
```

---

## 🚀 Running the Frontend

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
pnpm install
```

Start the development server:

```bash
pnpm dev
```

Then open the local development URL shown in the terminal.

---

## 🔐 Environment Variables

Create a local environment file based on the provided example:

```text
.env.local
```

Required configuration values should be added locally.

**API keys and secrets are not committed to the repository.**

---

## 🧪 Day 3 Testing

The following flow was tested from the frontend:

* [x] Page loads successfully
* [x] Agent is initially ready
* [x] User can start the voice session
* [x] Connecting state is displayed
* [x] User can speak to the agent
* [x] Agent can respond through voice
* [x] Listening/speaking states are visible
* [x] Call can be ended
* [x] User can start another conversation
* [x] Microphone permission handling is included

---

## 📱 Responsive Experience

The frontend was designed to keep the important controls, text, and interaction elements clear and accessible across screen sizes.

---

## 🎥 Day 3 Demo

The Day 3 demonstration video shows:

1. Frontend page loading
2. Nexa AI personalised interface
3. Starting the voice session
4. Agent connecting
5. Voice conversation
6. Listening and speaking states
7. Ending the call
8. Starting the interaction again

The demo also shows how the frontend has been customised for the **Education track**.

---

## 🏆 Day 3 Completion

This implementation fulfils the main Day 3 objective:

> **Personalise Your Agent's Frontend**

The Nexa AI frontend has been adapted from the starter application to provide a simple, education-focused voice-agent experience with clear interaction states and a complete voice conversation flow.

---

## 🔗 Resources

* [LiveKit Starter Apps](https://docs.livekit.io/frontends/start/starter-apps/)
* [LiveKit Agent Starter React](https://github.com/livekit-examples/agent-starter-react)
* [LiveKit Text Streams](https://docs.livekit.io/transport/data/text-streams/)

---

## 🙌 Challenge

Built as part of **10 Days of Voice Agents** using **Murf Falcon**.

**#VoiceForBharat**
