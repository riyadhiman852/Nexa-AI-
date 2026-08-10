# Day 5 — Adding the Tools 🛠️

## 🎯 Objective

Today’s goal is to make the voice agent more useful by giving it **tools/function calling capabilities**.

Instead of only having a conversation, the agent should be able to **perform actions using tools** when the user asks for them.

---

## 🧠 What We Are Building

Our voice agent will be able to:

* Understand the user's request
* Decide whether a tool is required
* Call the appropriate tool
* Get the tool's result
* Give the result back to the user through voice

### Example

**User:**

> What's the weather today?

**Agent:**

> Let me check that for you.

The agent calls a weather tool → receives the result → speaks the answer.

---

## 🔧 Main Concepts

### 1. Function Tools

We use LiveKit's function-tool support to expose Python functions to the LLM.

A tool can be defined for a specific action, for example:

```python
@function_tool
async def get_weather(city: str):
    ...
```

The LLM can then decide when this function should be called.

---

### 2. Tool Calling Flow

```text
User Voice
    ↓
Speech-to-Text
    ↓
LLM
    ↓
Does the request require a tool?
    ↓
   YES
    ↓
Function Tool
    ↓
Tool Result
    ↓
LLM
    ↓
Text-to-Speech
    ↓
Agent Voice
```

---

## 📂 Project Changes

The main implementation is done in:

```text
backend/
└── src/
    ├── agent.py
    └── memory.py
```

For today's task, the primary changes are made in **`agent.py`** to add and register the tools.

`memory.py` is only changed if the particular tool requires persistent user information.

---

## 🛠️ Tools

The agent can be extended with tools such as:

### Weather Tool

Gets weather information for a requested location.

### Calculator Tool

Performs calculations when the user asks the agent to calculate something.

### Search / Information Tool

Allows the agent to retrieve information instead of relying only on its existing knowledge.

---

## 🎙️ Voice Interaction

The important part is that the user does **not** need to type commands.

The complete interaction happens through voice:

```text
User speaks
      ↓
Agent understands
      ↓
Agent selects a tool
      ↓
Tool executes
      ↓
Agent speaks the result
```

This makes the voice agent more capable of performing real-world tasks.

---

## 🧪 Testing

After implementing the tools:

1. Start the backend.
2. Connect the frontend to LiveKit.
3. Start a voice conversation.
4. Ask something that requires a tool.
5. Check the terminal logs.
6. Confirm that the correct tool is called.
7. Verify that the agent speaks the returned result.

---

## ▶️ Run the Backend

From the backend directory:

```bash
python src/agent.py dev
```

If the project uses `uv`:

```bash
uv run python src/agent.py dev
```

---

## ✅ Day 5 Checklist

* [x] Add function tools
* [x] Register tools with the agent
* [x] Allow the LLM to decide when to call a tool
* [x] Execute the selected function
* [x] Return the tool result to the LLM
* [x] Speak the final result using the voice agent
* [x] Test the complete voice → tool → voice flow
* [x] Record a short demonstration
* [x] Post the completed task on LinkedIn

---

## 🎥 Demo Video

The video should demonstrate:

1. User asks the agent something that requires a tool.
2. Agent understands the request.
3. Tool gets called.
4. Tool returns the result.
5. Agent speaks the final response.

---

## 🚀 Result

After completing Day 5, the voice agent is no longer just a conversational assistant.

It can **understand a request, choose an appropriate tool, execute an action, and communicate the result back to the user through voice.**

Built using **LiveKit + Murf Falcon + LLM + Function Tools**.
