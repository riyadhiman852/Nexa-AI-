# Day 7 – Know When to Ask for Human Help

## Nexa AI

Day 7 of the **10 Days of Voice Agents** challenge focuses on teaching Nexa AI when it should stop trying to solve a student's problem and ask for human help.

Nexa is built for the **Learning & Literacy** track.

## Objective

For Day 7, Nexa was upgraded to:

- Recognize when a student needs human support
- Ask for permission before sharing information
- Create a human-help request
- Store a short summary of the issue
- Generate a unique reference ID
- Give the caller a clear next step
- Avoid unnecessary escalation

## When Nexa Asks for Human Help

Nexa creates a human-help request in two situations:

1. The student is clearly upset, frustrated, or overwhelmed and needs human support.
2. The student explicitly asks to speak with a teacher or human.

Normal study questions, coding questions, quizzes, and exercises do not create an escalation.

## Permission Before Sharing

Before creating a request, Nexa explains what information will be shared and asks the caller for permission.

Example:

> "I can create a human-help request for you. Would you like me to share what happened and what I've already checked with a human?"

The request is created only after the caller clearly agrees.

If the caller says no, Nexa does not create the request.

## Human-Help Tool

A new function tool was added: `create_escalation()`.

The tool collects:

- Reason for escalation
- Problem description
- What Nexa already checked or tried
- Urgency
- Caller language
- Preferred follow-up method

The tool generates a unique reference ID such as `ESC-ABC123`.

## Escalation Storage

Requests are stored locally in `escalations.json`.

Initially, the file contains an empty list:

`[]`

After an escalation is created, the request is saved automatically.

Example request:

- ID: ESC-ABC123
- Reason: Student needs teacher support
- Problem: Student is frustrated with studies
- Checked: Nexa provided study guidance
- Urgency: Medium
- Language: English
- Follow-up method: Human follow-up
- Status: Open
- Created at: 2026-08-12

## Privacy

The escalation contains only useful information required by a human reviewer.

Nexa does not include:

- Passwords
- OTPs
- PINs
- Bank details
- Account numbers
- Unnecessary private information

The full conversation is not copied into the request.

## Workflow

Student describes a problem
↓
Nexa identifies need for human help
↓
Nexa explains what will be shared
↓
Nexa asks for permission
↓
Caller gives permission
↓
create_escalation()
↓
Request is saved
↓
Reference ID is generated
↓
Nexa gives the reference ID
↓
Nexa explains the next step

If the caller says no:

Caller says NO
↓
No escalation is created
↓
Nexa continues helping normally

## Testing

### Test 1 – Human Help Required

The caller told Nexa:

> "I'm really frustrated with my studies and I need to talk to a teacher."

Nexa recognized that human support was needed, asked for permission, and created an escalation after the caller agreed.

The agent generated a reference ID and saved the request in `escalations.json`.

### Test 2 – Normal Conversation

A normal educational request was tested, such as asking for a beginner Python question.

Nexa handled the request normally and did not create an unnecessary escalation.

## Result

Day 7 is complete.

Nexa can now:

- Recognize when human help is needed
- Ask for permission before sharing information
- Create a human-help request
- Save a useful summary
- Generate a reference ID
- Give the caller an honest next step
- Avoid unnecessary escalation

## Technologies Used

- Python
- LiveKit Agents
- Gemini
- Deepgram
- Murf Falcon TTS
- JSON
- SQLite
- Browser-based voice agent

## Day 7

**Challenge:** 10 Days of Voice Agents  
**Track:** Learning & Literacy  
**Agent:** Nexa AI  
**Day:** 7 – Know When to Ask for Human Help

Built using **Murf Falcon**, a fast TTS API.

#10DaysofAIVoiceAgents #MurfFalcon #VoiceForBharat