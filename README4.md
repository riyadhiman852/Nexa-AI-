# 🧠 Nexa AI — Day 4: Persistent Memory

Nexa AI is a voice assistant built with **LiveKit**, **Gemini**, **Deepgram**, and **Murf Falcon TTS**.
For Day 4 of the **10 Days of Voice Agents** challenge, Nexa AI was upgraded with **persistent caller memory** so that the assistant can remember useful information across separate calls.

## 🚀 Day 4 Goal

The goal of Day 4 was to make Nexa AI remember a returning caller instead of treating every call as a completely new conversation.

The assistant can now:

* Identify a returning user
* Retrieve previously saved information
* Remember useful caller details across calls
* Greet returning callers using their stored information
* Persist memory even after restarting the backend
* Ask for explicit consent before saving personal information

## 🧠 Memory System

Nexa AI uses a database-backed memory system instead of hardcoding information inside the prompt.

The stored information includes:

* `user_id`
* `name`
* 2–4 useful personal/track-related facts
* Preferred language
* Last interaction

For the **Education track**, useful facts can include:

* Current education level
* Topics being studied
* Areas where the user needs help
* Preferred language

### 🔐 Consent-Based Memory

Privacy is an important part of the memory system.

Before saving information, Nexa AI asks the caller for permission.

* If the caller says **yes**, the information is saved.
* If the caller says **no**, the information is **not saved**.

This ensures that memory is created only with explicit user consent.

## 💾 Database

The project uses **SQLite** for persistent storage.

The memory functionality is implemented through dedicated lookup and save functions rather than putting user information directly into the system prompt.

Because the data is stored in a database, the memory remains available even after restarting the voice agent.

## 🔄 Returning Caller Flow

The basic flow is:

```text
Caller
   ↓
Nexa AI identifies user
   ↓
Lookup existing memory
   ↓
Memory found?
   ├── Yes → Use stored information → Personalized greeting
   │
   └── No → Start new conversation
                ↓
          Ask for consent
                ↓
        ┌───────┴───────┐
       Yes              No
        ↓                ↓
   Save memory       Don't save
```

### Example

**First Call**

> User: My name is Riya. I'm a BCA student and I prefer English.

Nexa AI asks for permission before storing this information.

**Second Call**

Nexa AI retrieves the stored information and can recognize the caller as a returning user.

## 🧪 Testing

The memory feature was tested using **two separate calls**:

### Call 1

* Introduce the user
* Share relevant information
* Give consent to save the information

### Call 2

* Return to the assistant
* Verify that previously saved information is retrieved
* Verify that Nexa AI can personalize the interaction

The persistence was also verified by restarting the backend and checking that the stored memory was still available.

## 🛠️ Tech Stack

* **Python**
* **LiveKit Agents**
* **Gemini**
* **Deepgram**
* **Murf Falcon TTS**
* **SQLite**
* **Nexa AI Frontend**

## 📁 Memory Architecture

The memory layer provides functions for:

```text
get_user()
    ↓
Lookup existing caller memory

save_user()
    ↓
Store/update caller memory after consent
```

This keeps memory management separate from the main voice-agent logic and allows the assistant to retrieve information dynamically.

## 🎯 Day 4 Requirements Completed

* [x] Persistent caller memory
* [x] Database-backed storage
* [x] SQLite implementation
* [x] User ID storage
* [x] Name and useful caller facts
* [x] Language preference
* [x] Last interaction tracking
* [x] Lookup memory
* [x] Save memory
* [x] Explicit consent before saving
* [x] "No" means information is not saved
* [x] Memory survives backend restart
* [x] Returning caller personalization
* [x] Tested across two calls
* [x] Voice-agent memory demonstrated in a short video

## 🎥 Demo

The Day 4 demo demonstrates:

1. A first conversation with the assistant
2. The assistant asking for memory consent
3. Information being saved after consent
4. A second call from the same user
5. Nexa AI retrieving the previous memory
6. A personalized returning-caller interaction

## 📌 Challenge

**10 Days of Voice Agents — Day 4**

Nexa AI is being developed as part of the **#VoiceForBharat** challenge, using **Murf Falcon** for fast, natural voice generation.

## 👩‍💻 Project

**Nexa AI — Personalized Voice Assistant**

Built with ❤️ using LiveKit, Gemini, Deepgram, Murf Falcon, and persistent memory.
