# 🤖 Nexa AI

### Multilingual Voice AI Learning Assistant

*An intelligent, real-time voice assistant designed to make learning, literacy, coding, and AI assistance more accessible through natural voice conversations.*

---

## 📑 Table of Contents

* [🚧 Project Status](#-project-status)
* [✨ Project Highlights](#-project-highlights)
* [📌 Overview](#-overview)
* [❓ Why Nexa AI?](#-why-nexa-ai)
* [✨ Features](#-features)
* [🏗️ Architecture](#️-architecture)
* [🎙️ Voice Pipeline](#️-voice-pipeline)
* [💻 Full Tech Stack](#-full-tech-stack)
* [📂 Project Structure](#-project-structure)
* [🛠️ Installation & Setup](#️-installation--setup)
* [🔐 Environment Variables](#-environment-variables)
* [▶️ Running the Application](#️-running-the-application)
* [🧠 AI Agent Personality](#-ai-agent-personality)
* [🌐 Multilingual & Mixed-Language Interaction](#-multilingual--mixed-language-interaction)
* [🚀 Challenge Progress & Changelog](#-challenge-progress--changelog)
* [🗺️ Future Roadmap](#️-future-roadmap)
* [🤝 Contributing](#-contributing)
* [📜 Built With & Acknowledgements](#-built-with--acknowledgements)
* [⚠️ Disclaimer](#️-disclaimer)
* [📄 License](#-license)
* [👩‍💻 Author](#-author)

---

## 🚧 Project Status

**Nexa AI is under active development as part of the VoiceForBharat 2026 Challenge.**

The project is being developed incrementally, with new voice AI capabilities, agent improvements, and learning-focused functionality being added throughout the challenge.

| Status                        | Progress    |
| ----------------------------- | ----------- |
| 🟢 Active Development         | Day 2       |
| 🎙️ Voice Agent               | Implemented |
| ⚡ Real-Time Audio             | Implemented |
| 🧠 AI Agent                   | Implemented |
| 🔊 Murf Falcon TTS            | Implemented |
| 🌐 Mixed-Language Interaction | Supported   |
| 📚 Learning Assistance        | Implemented |
| 💻 Coding Assistance          | Implemented |

---

## ✨ Project Highlights

* 🎙️ **Real-Time Voice AI** — Natural two-way voice interaction.
* ⚡ **Fast Voice Generation** — Powered by Murf Falcon TTS.
* 🌐 **Mixed-Language Conversations** — Designed for natural code-switching between languages.
* 📚 **Learning & Literacy Support** — Built around accessible educational assistance.
* 💻 **Programming Assistant** — Helps users understand coding and programming concepts.
* 🧠 **AI-Powered Reasoning** — Uses Google AI APIs for conversational intelligence.
* 🔊 **Speech Recognition** — Real-time speech-to-text using Deepgram.
* 🌐 **WebRTC Communication** — LiveKit provides the real-time audio infrastructure.
* 🛡️ **Agent Guardrails** — Dedicated personality and behavioral instructions for safe, helpful responses.
* 🐍 **Python Voice Agent Backend** — Built using the LiveKit Agents ecosystem.
* ⚛️ **Modern Web Frontend** — Voice-first web application interface.

---

## 📌 Overview

**Nexa AI** is a real-time, voice-first AI assistant focused on **learning, literacy, programming, and general AI assistance**.

Instead of requiring users to type every question, Nexa AI allows them to communicate naturally through voice.

The system combines speech recognition, AI reasoning, and fast speech synthesis into a single conversational pipeline.

Users can:

* Ask educational questions
* Learn programming concepts
* Get coding assistance
* Ask general AI questions
* Have natural voice conversations
* Communicate using mixed-language speech

The core idea is simple:

> **Make AI-powered learning easier to access through natural voice interaction.**

---

## ❓ Why Nexa AI?

### 1. 🎙️ Voice-First Learning

Typing can create an unnecessary barrier between a learner and an AI assistant.

Nexa AI allows users to simply **speak their questions** and receive spoken responses.

### 2. 📚 Learning & Literacy

Nexa AI is designed to support users who want help with:

* Academic learning
* Concept explanations
* Study assistance
* General knowledge
* Programming education

### 3. 💻 Coding Assistance

Learning programming often involves repeatedly asking questions about syntax, concepts, errors, and implementation.

Nexa AI provides conversational programming assistance to help learners understand these concepts.

### 4. 🌐 Natural Mixed-Language Communication

Many users naturally switch between languages while speaking.

Nexa AI is designed to support this kind of **code-switching / mixed-language communication**, making conversations feel more natural.

For example:

```text
"Mujhe Python functions simple language mein explain karo."
```

### 5. ⚡ Fast Voice Experience

A voice assistant needs to respond quickly to feel conversational.

Nexa AI uses **Murf Falcon** for fast text-to-speech generation and combines it with a real-time LiveKit audio pipeline.

---

## ✨ Features

### 🎙️ Voice Interaction

* Real-time voice conversations
* Speech-to-text processing
* AI-generated responses
* Text-to-speech output
* Full conversational voice pipeline

### 📚 Learning Assistance

* Concept explanations
* Study-related questions
* Educational guidance
* Beginner-friendly explanations
* General literacy assistance

### 💻 Coding & Programming

* Programming concept explanations
* Coding questions
* Beginner programming guidance
* Debugging assistance
* Technical explanations in conversational language

### 🤖 General AI Assistance

* General questions
* Knowledge-based conversations
* Productivity-related assistance
* AI-related questions
* Natural conversational interaction

### 🌐 Mixed-Language Conversations

Nexa AI is designed to handle natural language switching during conversations.

Examples include:

```text
"Haan, mujhe Python ka loop explain karo."

"Can you explain this concept in simple Hindi?"

"Java mein ye error kyun aa raha hai?"
```

### 🛡️ AI Agent Guardrails

The agent includes dedicated instructions for:

* Consistent personality
* Helpful responses
* Student-friendly communication
* Educational guidance
* Appropriate conversational behavior

---

# 🏗️ Architecture

Nexa AI follows a real-time voice agent architecture connecting the web client, LiveKit, speech recognition, AI reasoning, and voice synthesis.

```text
                         ┌──────────────────┐
                         │      USER        │
                         │   🎙️ Voice Input │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    FRONTEND      │
                         │  Web Voice UI    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     LIVEKIT      │
                         │ WebRTC / Audio   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   NEXA AI AGENT  │
                         │ Python Backend   │
                         └───────┬──────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
             ┌───────────┐ ┌──────────┐ ┌───────────┐
             │ Deepgram  │ │ Google AI│ │   Agent   │
             │    STT    │ │   LLM    │ │ Guardrails│
             └─────┬─────┘ └────┬─────┘ └───────────┘
                   │             │
                   └──────┬──────┘
                          ▼
                   ┌──────────────┐
                   │ Murf Falcon  │
                   │     TTS      │
                   └──────┬───────┘
                          │
                          ▼
                   🔊 Voice Response
                          │
                          ▼
                         USER
```

---

# 🎙️ Voice Pipeline

The Nexa AI voice interaction pipeline consists of multiple real-time components:

```text
[User Speech]
      │
      ▼
[LiveKit WebRTC]
      │
      ▼
[Deepgram STT]
      │
      ▼
[Google AI / LLM]
      │
      ▼
[Nexa AI Agent Logic]
      │
      ▼
[Murf Falcon TTS]
      │
      ▼
[LiveKit Audio Stream]
      │
      ▼
[User Hears Response]
```

### 1. Speech Recognition

**Deepgram** converts incoming voice into text in real time.

### 2. AI Reasoning

**Google AI APIs** process the user's request and generate the conversational response.

### 3. Agent Logic

The Python-based Nexa AI agent applies its system instructions, personality, and behavioral guardrails.

### 4. Voice Synthesis

**Murf Falcon** converts the generated response into natural speech.

### 5. Real-Time Transport

**LiveKit** handles the real-time audio communication between the frontend and the voice agent.

---

# 💻 Full Tech Stack

## 🎨 Frontend

| Technology             | Purpose                        |
| ---------------------- | ------------------------------ |
| **Next.js**            | Frontend application framework |
| **React**              | User interface components      |
| **TypeScript**         | Type-safe frontend development |
| **Tailwind CSS**       | UI styling                     |
| **LiveKit Client SDK** | Real-time voice communication  |
| **pnpm**               | Frontend package management    |

### Frontend Responsibilities

The frontend handles:

* Voice interface
* User interaction
* LiveKit connection
* Audio communication
* Agent session interface
* Real-time conversation experience

---

## 🐍 Backend

| Technology             | Purpose                       |
| ---------------------- | ----------------------------- |
| **Python 3.11+**       | Backend agent runtime         |
| **LiveKit Agents SDK** | Voice AI agent framework      |
| **uv**                 | Python dependency management  |
| **Pyproject.toml**     | Backend project configuration |

### Backend Responsibilities

The backend voice agent handles:

* Voice session management
* Agent behavior
* AI model interaction
* Speech pipeline orchestration
* System prompt
* Personality
* Guardrails
* TTS integration

---

## 🧠 Artificial Intelligence

| Technology             | Purpose                          |
| ---------------------- | -------------------------------- |
| **Google AI / Gemini** | Large Language Model / reasoning |
| **Deepgram**           | Speech-to-Text                   |
| **Murf Falcon**        | Text-to-Speech                   |

---

## 🔊 Voice & Real-Time Infrastructure

| Technology         | Purpose                      |
| ------------------ | ---------------------------- |
| **Murf Falcon**    | Fast voice synthesis         |
| **Deepgram**       | Real-time speech recognition |
| **LiveKit Cloud**  | WebRTC audio transport       |
| **LiveKit Agents** | Real-time AI agent framework |

---

## 🛠️ Development Tools

| Tool           | Purpose                                      |
| -------------- | -------------------------------------------- |
| **Git**        | Version control                              |
| **GitHub**     | Source code hosting                          |
| **VS Code**    | Development environment                      |
| **PowerShell** | Windows development / startup                |
| **uv**         | Python environment and dependency management |
| **pnpm**       | JavaScript package management                |

---

# 📂 Project Structure

```text
Nexa-AI/
│
├── backend/
│   ├── src/
│   │   └── agent.py
│   │
│   ├── pyproject.toml
│   ├── uv.lock
│   └── ...
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .gitignore
├── AGENTS.md
├── LICENSE
├── README.md
├── start_app.ps1
└── start_app.sh
```

---

# 🛠️ Installation & Setup

## Prerequisites

Before running Nexa AI, install:

* **Python 3.11+**
* **Node.js**
* **pnpm**
* **uv**
* **Git**
* **LiveKit Cloud account**
* **Murf API key**
* **Deepgram API key**
* **Google AI API key**

---

## Step 1: Clone the Repository

```bash
git clone https://github.com/riyadhiman852/Nexa-AI-.git
cd Nexa-AI-
```

---

## Step 2: Backend Setup

```powershell
cd backend
```

Create/activate the Python environment:

```powershell
uv sync
```

Activate the environment if required:

```powershell
.\.venv\Scripts\activate
```

---

## Step 3: Configure Environment Variables

Create the required environment configuration in the backend.

Example:

```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

MURF_API_KEY=your_murf_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
GOOGLE_API_KEY=your_google_api_key
```

> **Never commit API keys or secrets to GitHub.**

Keep `.env` and `.env.local` files private.

---

## Step 4: Start the Backend Agent

From the `backend` directory:

```powershell
uv run python src/agent.py dev
```

Or using the LiveKit CLI:

```powershell
lk agent dev
```

---

## Step 5: Start the Frontend

Open another terminal:

```powershell
cd frontend
```

Install dependencies:

```powershell
pnpm install
```

Start the development server:

```powershell
pnpm dev
```

Open the local URL displayed by the frontend development server.

---

# 🔐 Environment Variables

Nexa AI requires credentials for the external services used by the voice pipeline.

| Variable             | Service   | Purpose            |
| -------------------- | --------- | ------------------ |
| `LIVEKIT_URL`        | LiveKit   | WebRTC server URL  |
| `LIVEKIT_API_KEY`    | LiveKit   | API authentication |
| `LIVEKIT_API_SECRET` | LiveKit   | API authentication |
| `MURF_API_KEY`       | Murf      | Voice synthesis    |
| `DEEPGRAM_API_KEY`   | Deepgram  | Speech recognition |
| `GOOGLE_API_KEY`     | Google AI | AI model access    |

### Security Notice

Do **not** upload:

```text
.env
.env.local
.env.production
```

or any file containing private API credentials.

---

# ▶️ Running the Application

Nexa AI requires two primary services during local development:

### Terminal 1 — Backend

```powershell
cd backend
uv run python src/agent.py dev
```

### Terminal 2 — Frontend

```powershell
cd frontend
pnpm dev
```

Then open the frontend development URL in your browser.

---

# 🧠 AI Agent Personality

Nexa AI uses a dedicated system prompt to define the assistant's behavior.

The agent is designed to be:

* Friendly
* Helpful
* Student-focused
* Educational
* Conversational
* Clear and easy to understand

The personality and guardrails are maintained on the backend so the agent can consistently follow its intended behavior.

---

# 🌐 Multilingual & Mixed-Language Interaction

One of Nexa AI's key goals is to support the way people naturally communicate.

Users may combine languages within the same conversation instead of being forced to communicate in one language.

Examples:

```text
"Mujhe machine learning simple words mein samjhao."

"Can you explain recursion thoda easy way mein?"

"Python mein list aur tuple ka difference kya hai?"
```

This makes Nexa AI particularly useful for learners who are more comfortable using a combination of English and Indian languages.

---

# 🚀 Challenge Progress & Changelog

Nexa AI is being developed incrementally as part of the **VoiceForBharat 2026 Challenge**.

| Day        | Status      | Progress                                       |
| ---------- | ----------- | ---------------------------------------------- |
| **Day 1**  | ✅ Completed | Initial real-time voice agent with Murf Falcon |
| **Day 2**  | ✅ Completed | Agent personality and behavioral guardrails    |
| **Day 3**  | 🔄 Next     | Further voice agent improvements               |
| **Day 4**  | ⏳ Planned   | TBD                                            |
| **Day 5**  | ⏳ Planned   | TBD                                            |
| **Day 6**  | ⏳ Planned   | TBD                                            |
| **Day 7**  | ⏳ Planned   | TBD                                            |
| **Day 8**  | ⏳ Planned   | TBD                                            |
| **Day 9**  | ⏳ Planned   | TBD                                            |
| **Day 10** | ⏳ Planned   | Final showcase                                 |

### 📜 Day 1

* Set up the initial Nexa AI voice agent.
* Integrated LiveKit real-time communication.
* Integrated Deepgram speech recognition.
* Integrated Google AI.
* Integrated Murf Falcon TTS.
* Established the real-time voice pipeline.
* Created the initial web interface.

### 📜 Day 2

* Added Nexa AI agent personality.
* Added educational/student-focused behavior.
* Added conversational guardrails.
* Improved the system prompt.
* Refined the agent's response behavior.

---

# 🗺️ Future Roadmap

### 🎙️ Voice Improvements

* Improved response latency
* More natural conversational turn-taking
* Better interruption handling
* Improved voice quality

### 🌐 Language Support

* Expanded Indian language support
* Better Hindi-English code-switching
* Regional language interaction

### 📚 Learning Features

* Personalized study assistance
* Subject-specific learning modes
* Learning progress tracking
* Interactive educational conversations

### 💻 Developer Assistance

* Better code explanation
* Debugging assistance
* Programming learning modes
* Beginner-friendly coding tutorials

### 🤖 AI Improvements

* Better contextual memory
* More reliable responses
* Improved agent reasoning
* Specialized learning personas

---

# 🤝 Contributing

Contributions are welcome!

### 1. Fork the repository

```bash
git fork https://github.com/riyadhiman852/Nexa-AI-.git
```

### 2. Create a feature branch

```bash
git checkout -b feature/your-feature
```

### 3. Make your changes

### 4. Commit your changes

```bash
git add .
git commit -m "Add your feature"
```

### 5. Push the branch

```bash
git push origin feature/your-feature
```

### 6. Open a Pull Request

Please describe what you changed and why the change is useful.

---

# 📜 Built With & Acknowledgements

Nexa AI is powered by several technologies and open-source platforms:

* **Murf AI** — Murf Falcon text-to-speech
* **LiveKit** — Real-time WebRTC infrastructure and Agents SDK
* **Deepgram** — Speech recognition
* **Google AI** — AI/LLM capabilities
* **Python** — Voice agent backend
* **Next.js & React** — Web frontend

Special thanks to the teams building the tools and infrastructure that make real-time voice AI applications possible.

---

# ⚠️ Disclaimer

Nexa AI is an **educational and experimental voice AI project** developed as part of the VoiceForBharat 2026 Challenge.

AI-generated responses may occasionally be inaccurate. Users should independently verify important information and should not rely on Nexa AI as a substitute for qualified professional advice.

---

# 📄 License

This project is licensed under the terms specified in the [`LICENSE`](LICENSE) file.

---

# 👩‍💻 Author

**Riya Dhiman**

BCA AI/ML Student & AI Developer

Building and exploring:

* 🤖 Artificial Intelligence
* 🎙️ Voice AI
* 🧠 Generative AI
* 💻 Programming
* 📚 AI-powered learning tools

### 🔗 Project

**Nexa AI — Multilingual Voice AI Learning Assistant**

⭐ If you find Nexa AI interesting, consider starring the repository and sharing your feedback!
