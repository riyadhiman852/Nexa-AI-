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


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
IDENTITY

You are Nexa, a friendly AI voice assistant for students.

You help students with:
- study planning
- programming
- coding
- AI
- productivity
- academic guidance


============================================================
IMPORTANT CODING ROUTING RULE
============================================================

CODING REQUESTS MUST BE HANDED OFF.

Whenever the student asks for ANY programming or coding help,
you MUST use the transfer_to_coding_specialist tool.

Do NOT solve the coding problem yourself.

Do NOT ask unnecessary follow-up questions before transferring.

Examples:

Student:
"Help me with a Java coding problem."

Action:
Immediately call transfer_to_coding_specialist.

Student:
"My Python code has an error."

Action:
Immediately call transfer_to_coding_specialist.

Student:
"Explain arrays in Java."

Action:
Immediately call transfer_to_coding_specialist.

Student:
"I have a DSA problem."

Action:
Immediately call transfer_to_coding_specialist.

Student:
"Help with JavaScript."

Action:
Immediately call transfer_to_coding_specialist.

Student:
"Debug this code."

Action:
Immediately call transfer_to_coding_specialist.

Student:
"Help me solve a programming problem."

Action:
Immediately call transfer_to_coding_specialist.


CODING TOPICS INCLUDE:

- Python
- Java
- JavaScript
- C
- C++
- SQL
- DSA
- algorithms
- debugging
- programming errors
- coding interview questions
- code explanation
- programming concepts
- data structures
- competitive programming


Before the transfer, say only a short sentence such as:

"I'll connect you with our Coding Specialist."

Then immediately use the transfer_to_coding_specialist tool.

After transfer, the Coding Specialist continues the conversation.

Do NOT give the coding answer before transfer.


============================================================
GENERAL OBJECTIVES
============================================================

1. Help students create effective study plans.
2. Explain academic concepts in simple language.
3. Help with productivity and learning.
4. Remember useful educational information only with permission.
5. End conversations with a useful next step.


============================================================
MEMORY
============================================================

Caller memory is loaded automatically.

Use only memory information provided in your context.

Never claim to remember information that is not available.

Before saving new learning information, ask:

"Would you like me to remember that for our future conversations?"

Only save after clear permission.

Never save:
- passwords
- OTPs
- PINs
- bank details
- account numbers
- sensitive personal information

Useful information may include:
- learning level
- programming languages
- topics being studied
- learning difficulties
- educational goals
- language preference


============================================================
LANGUAGE
============================================================

Reply in the same language as the user.

English -> English.

Hindi -> Hindi using Devanagari.

Hinglish -> natural Hinglish.

Keep voice responses short and natural.


============================================================
EXERCISES
============================================================

Use get_next_exercise when the student asks for:

- practice question
- quiz
- exercise
- coding practice question
- question at a particular difficulty level

Do not read JSON aloud.

Convert the tool result into a natural response.

Do not invent exercise data.


============================================================
SUCCESS TRACKING
============================================================

Use mark_call_success only when:

- the student successfully completes a learning exercise, OR
- the student clearly achieves the learning goal.

Do NOT mark success merely because:
- a question was asked
- an explanation was given
- an exercise was provided
- the call ended


============================================================
ESCALATION
============================================================

Create a human-help request only when:

1. The student is clearly upset/frustrated/overwhelmed and needs human support.
2. The student explicitly asks for a teacher or human.

Before create_escalation:
- explain what will be shared
- ask for permission

Only call create_escalation after clear permission.

Never include:
- passwords
- OTPs
- PINs
- bank details
- unnecessary private information


============================================================
STYLE
============================================================

Be:
- friendly
- calm
- encouraging
- concise

Keep responses natural for voice conversations.

Never claim to be human.

Never claim to have real-time internet access unless actually available.
"""


# ============================================================
# LOCAL EDUCATIONAL DATA
# ============================================================

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


# ============================================================
# CODING SPECIALIST
# ============================================================

class CodingSpecialist(Agent):

    def __init__(self) -> None:
        super().__init__(
            instructions="""
You are Nexa's Coding Specialist.

You specialize in:

- Java
- Python
- JavaScript
- C
- C++
- SQL
- DSA
- algorithms
- debugging
- programming concepts
- coding interviews

IMPORTANT:

You are receiving the conversation after Nexa transferred
the student to you.

Do NOT restart the conversation.

Continue naturally from the student's request.

If the student said:

"Help me with a Java coding problem"

respond naturally, for example:

"Sure, send me the Java problem or your code, and I'll help
you solve it."

If the student provides code:
- analyze it carefully
- identify the likely issue
- explain the fix
- provide corrected code when appropriate

If the student asks a conceptual question:
- explain it simply
- use a small example

Keep responses concise because this is a voice conversation.

LANGUAGE:

English -> English.

Hindi -> Hindi in Devanagari.

Hinglish -> natural Hinglish.

Do not restart the conversation unnecessarily.
"""
        )


# ============================================================
# MAIN ASSISTANT
# ============================================================

class Assistant(Agent):

    @function_tool
    async def transfer_to_coding_specialist(
        self,
        context: RunContext,
    ):
        """
        Transfer programming and coding requests to the
        Coding Specialist.
        """

        logger.info(
            "CODING HANDOFF STARTED | user_id=%s",
            self.user_id,
        )

        return (
            CodingSpecialist(),
            "I'll connect you with our Coding Specialist."
        )

    def __init__(
        self,
        user_id: str,
        user_memory=None,
    ) -> None:

        self.user_id = user_id
        self.returning_user = user_memory is not None
        self.user_memory = user_memory

        # Day 8 analytics
        self.call_successful = False

        memory_context = self._build_memory_context()

        super().__init__(
            instructions=SYSTEM_PROMPT + memory_context
        )

    # --------------------------------------------------------
    # MEMORY CONTEXT
    # --------------------------------------------------------

    def _build_memory_context(self) -> str:

        if not self.user_memory:
            return """

CALLER MEMORY

No saved memory is available.

Do not claim to remember previous conversations.
"""

        return f"""

CALLER MEMORY

Previously saved information:

{json.dumps(
    self.user_memory,
    ensure_ascii=False,
    indent=2
)}

Use this information naturally when relevant.

Do not mention the database.
Do not invent information.
"""

    # --------------------------------------------------------
    # EXERCISE TOOL
    # --------------------------------------------------------

    @function_tool
    async def get_next_exercise(
        self,
        context: RunContext,
        topic: str,
        level: str,
    ) -> str:

        logger.info(
            "Fetching exercise topic=%s level=%s",
            topic,
            level,
        )

        try:

            topic_key = topic.strip().lower()
            level_key = level.strip().lower()

            topic_data = EXERCISES.get(topic_key)

            if not topic_data:
                return (
                    f"I don't currently have a practice exercise "
                    f"for {topic}. Please try Python, JavaScript, or AI."
                )

            exercises = topic_data.get(level_key)

            if not exercises:
                return (
                    f"I don't currently have a {level} exercise "
                    f"for {topic}. Please try another difficulty level."
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

            logger.exception(
                "Exercise lookup failed"
            )

            return (
                "I couldn't access the exercise data right now. "
                "Please try again in a moment."
            )

    # --------------------------------------------------------
    # SUCCESS TOOL
    # --------------------------------------------------------

    @function_tool
    async def mark_call_success(
        self,
        context: RunContext,
    ) -> str:

        self.call_successful = True

        logger.info(
            "CALL MARKED SUCCESSFUL | user_id=%s",
            self.user_id,
        )

        return (
            "The learning call has been marked as successful."
        )

    # --------------------------------------------------------
    # MEMORY TOOL
    # --------------------------------------------------------

    @function_tool
    async def save_user_memory(
        self,
        context: RunContext,
        name: str,
        language_preference: str,
        facts: str,
    ) -> str:

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

    # --------------------------------------------------------
    # HUMAN ESCALATION
    # --------------------------------------------------------

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

        logger.info(
            "Creating escalation user_id=%s reason=%s urgency=%s",
            self.user_id,
            reason,
            urgency,
        )

        escalation_id = (
            f"ESC-{uuid.uuid4().hex[:6].upper()}"
        )

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

            with open(
                "escalations.json",
                "r",
                encoding="utf-8"
            ) as f:

                escalations = json.load(f)

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):

            escalations = []

        escalations.append(escalation)

        with open(
            "escalations.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                escalations,
                f,
                ensure_ascii=False,
                indent=2,
            )

        logger.info(
            "Human-help request created: %s",
            escalation_id,
        )

        return json.dumps(
            {
                "success": True,
                "reference_id": escalation_id,
                "status": "open",
                "message": (
                    "Human-help request created successfully."
                ),
            },
            ensure_ascii=False,
        )


# ============================================================
# SERVER
# ============================================================

server = AgentServer()


def prewarm(proc: JobProcess):

    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


# ============================================================
# LIVEKIT SESSION
# ============================================================

@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: JobContext):

    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Day 8 analytics
    init_analytics_db()

    await ctx.connect()

    # Wait for browser participant
    participant = await ctx.wait_for_participant()

    user_id = participant.identity

    # Unique call ID
    call_id = (
        f"CALL-{uuid.uuid4().hex[:8].upper()}"
    )

    logger.info(
        "CALL CONNECTED | identity=%s | room=%s | call_id=%s",
        user_id,
        ctx.room.name,
        call_id,
    )

    # Load memory
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

    # ========================================================
    # AGENT SESSION
    # ========================================================

    session = AgentSession(

        stt=deepgram.STT(
            model="nova-3",
            language="multi",
        ),

        # Keep current Gemini configuration
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

    # Create assistant
    assistant = Assistant(
        user_id=user_id,
        user_memory=user_memory,
    )

    # Start session
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

    # ========================================================
    # INITIAL GREETING
    # ========================================================

    if user_memory:

        name = user_memory.get(
            "name",
            ""
        )

        facts = user_memory.get(
            "facts",
            {}
        )

        greeting = (
            f"Welcome back, {name}! "
            "Greet the caller warmly and naturally. "
            "Mention one relevant learning fact from memory "
            "if available. Keep it short."
        )

        if facts:

            greeting += (
                " Use the saved learning information "
                "naturally without mentioning the database."
            )

    else:

        greeting = (
            "Greet the caller warmly as Nexa. "
            "Start a friendly conversation. "
            "Keep the greeting short and natural."
        )

    await session.generate_reply(
        instructions=greeting
    )

    # ========================================================
    # ANALYTICS ON SHUTDOWN
    # ========================================================

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
            "CALL ANALYTICS SAVED | call_id=%s | outcome=%s",
            call_id,
            outcome,
        )

    ctx.add_shutdown_callback(
        save_call_analytics
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    cli.run_app(server)