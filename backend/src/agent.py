
import json
import logging
import uuid
from datetime import datetime

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    RunContext,
    cli,
    function_tool,
    tokenize,
    room_io,
)
from livekit.plugins import (
    murf,
    silero,
    google,
    deepgram,
    noise_cancellation,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from memory import get_user, save_user
from analytics import init_analytics_db, record_call


logger = logging.getLogger("agent")

load_dotenv(".env.local")


SYSTEM_PROMPT = """
IDENTITY

You are Nexa, a friendly AI voice assistant for students.

You help students with:

- study planning
- programming
- coding
- AI
- productivity
- general academic guidance

OBJECTIVES

1. Help students create effective study plans.
2. Explain programming and academic concepts in simple language.
3. Remember useful learning-related information only when the student gives clear permission.
4. When a returning student is recognized, greet them by name and naturally use relevant information from their previous conversation.
5. End every conversation with a clear next step or helpful suggestion.

CALL SUCCESS

A successful call means the learner successfully completes a requested
learning exercise or clearly achieves the learning goal.

A call is NOT successful just because:

- the learner asks a question
- Nexa explains a concept
- Nexa provides an exercise
- the learner ends the conversation

If the learner successfully completes the requested learning exercise
or clearly achieves the learning goal, use the mark_call_success tool.

MEMORY

Caller memory is loaded automatically before the conversation begins.

- Use only the memory information provided to you.
- Never claim to remember something unless it is actually provided.
- You may use saved learning-related information naturally when it is available.
- Never invent or guess saved memories.

PERMISSION RULE

Before saving any new personal or learning information, ask clearly:

"Would you like me to remember that for our future conversations?"

Only call save_user_memory after the caller clearly agrees.

If the caller says no, do not call save_user_memory.

Never save:

- passwords
- OTPs
- PINs
- bank details
- other sensitive information

Save only useful educational information such as:

- learning level
- programming languages being learned
- topics being studied
- learning difficulties
- educational goals
- language preference

RETURNING CALLERS

If saved caller memory is available:

- Welcome them back by name.
- Use one relevant saved learning fact naturally.
- Do not dump the entire memory record.
- Do not mention the database.
- Do not pretend to remember information that is not actually saved.

LANGUAGE & SCRIPT

Reply in the same language as the user.

- English → English.
- Hindi → Hindi using Devanagari script.
- Hinglish → natural Hinglish.
- Never write Hindi in Romanized script when the user is clearly speaking Hindi.

Example:

Hindi: "नमस्ते, आपका स्वागत है।"

Not:

"Namaste, aapka swagat hai."

TOOLS

You have access to a learning exercise tool called get_next_exercise.

Use get_next_exercise automatically when the student asks for:

- a practice question
- a quiz
- an exercise
- coding practice
- a question at a particular difficulty level

For example:

- "Give me a beginner Python question."
- "Quiz me on JavaScript."
- "I want an intermediate Python exercise."

When using the tool:

- Do not read the returned JSON aloud.
- Convert the result into a natural conversational response.
- Give the question and options clearly.
- Do not invent exercise data if the tool fails.
- If the tool reports that data is unavailable, explain that naturally and suggest another supported topic or level.
- Mention that the exercise comes from the local educational practice dataset when relevant.

SUCCESS TRACKING

You have access to a tool called mark_call_success.

Use mark_call_success only when:

- the student has completed the requested learning exercise successfully, or
- the student has clearly achieved the learning goal.

Do not mark a call successful just because:

- the student asked a question
- you explained a concept
- you provided an exercise
- the student ended the call

KNOWLEDGE

You know programming, AI, study techniques, productivity, and general educational topics.

If you don't know something, say so honestly.

STYLE

Be:

- friendly
- calm
- encouraging
- concise

Keep responses short and natural for voice conversations.

Avoid long paragraphs and complicated words.

GUARDRAILS

Refuse:

- illegal or harmful activities
- harmful or abusive requests
- hateful content

Do not:

- provide medical diagnosis
- prescribe medicines
- ask for or store passwords
- ask for or store OTPs
- ask for or store PINs
- ask for or store bank details
- store sensitive personal information

Never claim:

- you are a human
- you have real-time internet access unless you actually do
- you know something when you do not

ESCALATION

You are a Learning & Literacy assistant.

Create a human-help request only in these two situations:

1. The student is clearly upset, frustrated, or overwhelmed and needs human support.
2. The student explicitly asks to speak with a teacher or human.

Before calling create_escalation:

- Explain that you can create a human-help request.
- Tell the caller what information will be shared:
  - their user identity/reference
  - what happened
  - what Nexa already checked or tried
  - urgency
  - language preference
  - preferred follow-up method
- Ask for clear permission.

Only call create_escalation after the caller clearly says yes.

If the caller says no:

- Do not call create_escalation.
- Continue helping within your capabilities.

Never include:

- passwords
- OTPs
- PINs
- bank details
- account numbers
- unnecessary private information

After create_escalation succeeds:

- Give the caller the returned reference ID.
- Tell them the request is open.
- Explain that a human can review it.
- Do not promise an immediate response.

Do not create an escalation for normal study questions, coding questions, quizzes, or exercises that you can reasonably answer yourself.
"""


EXERCISES = {
    "python": {
        "beginner": [
            {
                "question": "What is the correct way to print Hello World in Python?",
                "options": [
                    "A. print('Hello World')",
                    "B. echo('Hello World')",
                    "C. printf('Hello World')",
                    "D. console.log('Hello World')",
                ],
                "answer": "A",
                "explanation": "In Python, the print function is used to display text.",
            }
        ],
        "intermediate": [
            {
                "question": "Which Python data structure stores key-value pairs?",
                "options": [
                    "A. List",
                    "B. Tuple",
                    "C. Dictionary",
                    "D. Set",
                ],
                "answer": "C",
                "explanation": "A dictionary stores data as key-value pairs.",
            }
        ],
    },
    "javascript": {
        "beginner": [
            {
                "question": "Which keyword is commonly used to declare a variable in JavaScript?",
                "options": [
                    "A. variable",
                    "B. let",
                    "C. define",
                    "D. int",
                ],
                "answer": "B",
                "explanation": "The let keyword declares a block-scoped variable.",
            }
        ]
    },
    "ai": {
        "beginner": [
            {
                "question": "What does AI stand for?",
                "options": [
                    "A. Automated Internet",
                    "B. Artificial Intelligence",
                    "C. Advanced Information",
                    "D. Automated Intelligence",
                ],
                "answer": "B",
                "explanation": "AI stands for Artificial Intelligence.",
            }
        ]
    },
}


class Assistant(Agent):
    def __init__(self, user_id: str, user_memory=None) -> None:
        self.user_id = user_id
        self.returning_user = user_memory is not None
        self.user_memory = user_memory

        # Day 8 analytics:
        # The call starts as unsuccessful.
        # It becomes successful only when mark_call_success is used.
        self.call_successful = False

        memory_context = self._build_memory_context()

        super().__init__(
            instructions=SYSTEM_PROMPT + memory_context
        )

    def _build_memory_context(self) -> str:
        """Build the caller-memory context for the agent."""

        if not self.user_memory:
            return """

CALLER MEMORY

No saved memory is available for this caller.

Do not claim that you remember previous conversations.
"""

        return f"""

CALLER MEMORY

The following information was previously saved with the caller's permission.

Use it naturally when relevant.

Do not mention the database.
Do not dump the entire memory record.
Do not invent information that is not present here.

{json.dumps(self.user_memory, ensure_ascii=False, indent=2)}
"""

    @function_tool
    async def get_next_exercise(
        self,
        context: RunContext,
        topic: str,
        level: str,
    ) -> str:
        """Fetch the next practice exercise for a student's topic and level."""

        logger.info(
            "Fetching exercise: topic=%s level=%s",
            topic,
            level,
        )

        try:
            topic_key = topic.strip().lower()
            level_key = level.strip().lower()

            topic_data = EXERCISES.get(topic_key)

            if not topic_data:
                return (
                    f"I don't currently have a practice exercise for "
                    f"{topic}. Please try Python, JavaScript, or AI."
                )

            exercises = topic_data.get(level_key)

            if not exercises:
                return (
                    f"I don't currently have a {level} exercise for "
                    f"{topic}. Please try another difficulty level."
                )

            exercise = exercises[0]

            return json.dumps(
                {
                    "source": "Local educational practice dataset",
                    "data_updated": "August 10, 2026",
                    "topic": topic_key,
                    "level": level_key,
                    "question": exercise["question"],
                    "options": exercise["options"],
                    "answer": exercise["answer"],
                    "explanation": exercise["explanation"],
                },
                ensure_ascii=False,
            )

        except Exception:
            logger.exception("Exercise lookup failed")

            return (
                "I couldn't access the exercise data right now. "
                "Please try again in a moment."
            )

    @function_tool
    async def mark_call_success(
        self,
        context: RunContext,
    ) -> str:
        """Mark the current learning call as successful.

        Use only when the student has successfully completed
        the learning exercise or clearly achieved the learning goal.
        """

        self.call_successful = True

        logger.info(
            "Call marked successful for user_id=%s",
            self.user_id,
        )

        return "The learning call has been marked as successful."

    @function_tool
    async def save_user_memory(
        self,
        context: RunContext,
        name: str,
        language_preference: str,
        facts: str,
    ) -> str:
        """Save educational information after the caller gives permission."""

        logger.info(
            "Saving memory for user_id=%s",
            self.user_id,
        )

        try:
            parsed_facts = json.loads(facts)

            if not isinstance(parsed_facts, dict):
                return (
                    "Memory was not saved because facts "
                    "must be an object."
                )

        except json.JSONDecodeError:
            return (
                "Memory was not saved because the facts "
                "format was invalid."
            )

        save_user(
            user_id=self.user_id,
            name=name,
            language_preference=language_preference,
            facts=parsed_facts,
        )

        self.user_memory = get_user(self.user_id)
        self.returning_user = True

        logger.info(
            "Memory saved successfully for user_id=%s",
            self.user_id,
        )

        return (
            "The caller's approved learning information "
            "has been saved."
        )

    @function_tool
    async def create_escalation(
        self,
        context: RunContext,
        reason: str,
        problem: str,
        checked: str,
        urgency: str,
        language: str,
        follow_up_method: str,
    ) -> str:
        """Create a human-help request when a student needs human assistance."""

        logger.info(
            "Creating escalation for user_id=%s reason=%s urgency=%s",
            self.user_id,
            reason,
            urgency,
        )

        escalation_id = f"ESC-{uuid.uuid4().hex[:6].upper()}"

        escalation = {
            "id": escalation_id,
            "user_id": self.user_id,
            "reason": reason,
            "problem": problem,
            "checked": checked,
            "urgency": urgency,
            "language": language,
            "follow_up_method": follow_up_method,
            "status": "open",
            "created_at": datetime.now().isoformat(),
        }

        try:
            with open("escalations.json", "r", encoding="utf-8") as f:
                escalations = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            escalations = []

        escalations.append(escalation)

        with open("escalations.json", "w", encoding="utf-8") as f:
            json.dump(
                escalations,
                f,
                ensure_ascii=False,
                indent=2,
            )

        logger.info(
            "Human-help request created: %s",
            json.dumps(escalation, ensure_ascii=False),
        )

        return json.dumps(
            {
                "success": True,
                "reference_id": escalation_id,
                "status": "open",
                "message": (
                    "Human-help request created successfully. "
                    "Give the caller the reference ID and explain "
                    "that a human can review the request."
                ),
            },
            ensure_ascii=False,
        )


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: JobContext):
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Initialize Day 8 analytics database.
    init_analytics_db()

    await ctx.connect()

    # Get the caller's LiveKit participant identity.
    participant = await ctx.wait_for_participant()

    user_id = participant.identity

    # Generate a unique ID for this call.
    call_id = f"CALL-{uuid.uuid4().hex[:8].upper()}"

    logger.info(
        "Caller connected: identity=%s room=%s call_id=%s",
        user_id,
        ctx.room.name,
        call_id,
    )

    # Load caller memory directly in Python.
    user_memory = get_user(user_id)

    if user_memory:
        logger.info(
            "Saved memory found for user_id=%s",
            user_id,
        )
    else:
        logger.info(
            "No saved memory found for user_id=%s",
            user_id,
        )

    session = AgentSession(
        stt=deepgram.STT(
            model="nova-3",
            language="multi",
        ),
        llm=google.LLM(
            model="gemini-flash-latest",
        ),
        tts=murf.TTS(
            voice="Anisha",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(
                min_sentence_len=2
            ),
            text_pacing=True,
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=False,
    )

    assistant = Assistant(
        user_id=user_id,
        user_memory=user_memory,
    )

    await session.start(
        agent=assistant,
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: (
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind
                    == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC()
                ),
            ),
        ),
    )

    # Generate the initial greeting.
    if user_memory:
        name = user_memory.get("name", "")
        facts = user_memory.get("facts", {})

        greeting = (
            f"Welcome back, {name}! "
            "Greet the caller warmly and naturally mention "
            "one relevant learning fact from their saved memory. "
            "Keep the greeting short and conversational."
        )

        if facts:
            greeting += (
                " Use the saved learning information provided "
                "in your context, but do not mention the database."
            )

    else:
        greeting = (
            "Greet the caller warmly as Nexa and start "
            "a friendly conversation. "
            "Keep the greeting short and natural."
        )

    await session.generate_reply(
        instructions=greeting
    )

    # Save call analytics when the LiveKit job shuts down.
    async def save_call_analytics():
        outcome = (
            "success"
            if assistant.call_successful
            else "failed"
        )

        record_call(
            call_id=call_id,
            channel="browser",
            outcome=outcome,
        )

        logger.info(
            "Call analytics saved: call_id=%s outcome=%s",
            call_id,
            outcome,
        )

    ctx.add_shutdown_callback(save_call_analytics)


if __name__ == "__main__":
    cli.run_app(server)

