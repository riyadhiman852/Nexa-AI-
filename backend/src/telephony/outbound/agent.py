import asyncio
import json
import logging
import os

from dotenv import load_dotenv
from livekit import api, rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    RunContext,
    cli,
    function_tool,
    room_io,
    tokenize,
)
from livekit.plugins import deepgram, google, murf, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("nexa-outbound-agent")

load_dotenv(".env.local")

OUTBOUND_TRUNK_ID = os.getenv("LIVEKIT_SIP_OUTBOUND_TRUNK_ID")

CALLEE_IDENTITY = "phone-user"

SYSTEM_PROMPT = """
You are Nexa, a friendly AI study assistant calling a student for their
daily practice session.

This is an unexpected outbound call, so be brief, respectful, and
conversational.

Your purpose is to help the student complete a short daily learning
practice session.

When the call starts, briefly introduce yourself, explain that you are
calling for the student's daily practice session, and tell them they can
ask you to stop if they do not want future calls.

Then ask whether they would like today's practice question.

If they agree, ask one or two simple programming or study-related questions
and respond naturally to their answers.

If they are busy, respect that and end the call politely.

If they say they do not want these calls or ask you not to call again,
respect their request immediately and end the call.

Never ask for passwords, OTPs, PINs, banking information, or other sensitive
personal information.

Keep responses short because this is a phone call.

When the conversation is finished, use the end_call tool.
"""

GREETING = (
    "Hi, this is Nexa, your AI study assistant. "
    "I'm calling for your daily practice session. "
    "If you'd rather not receive these calls, just tell me and I won't call again. "
    "Would you like today's practice question?"
)


class OutboundAgent(Agent):
    def __init__(self, ctx: JobContext) -> None:
        super().__init__(instructions=SYSTEM_PROMPT)
        self.ctx = ctx

    @function_tool
    async def end_call(self, context: RunContext) -> str:
        """End the outbound call politely."""
        await context.session.generate_reply(
            instructions="Thank them for their time and say a very short goodbye."
        )

        logger.info("ending call")
        await self._hangup()
        return "Call ended."

    @function_tool
    async def opt_out(self, context: RunContext) -> str:
        """Respect a request to stop receiving outbound calls."""
        await context.session.generate_reply(
            instructions=(
                "Apologize briefly, confirm that you will not call again, "
                "and say goodbye."
            )
        )

        logger.info("caller requested no further calls")
        await self._hangup()
        return "Call ended because the caller opted out."

    async def _hangup(self) -> None:
        await self.ctx.api.room.delete_room(
            api.DeleteRoomRequest(room=self.ctx.room.name)
        )


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


def phone_number_from_metadata(ctx: JobContext) -> str | None:
    """Read the destination phone/SIP number from dispatch metadata."""
    metadata = ctx.job.metadata

    if not metadata:
        return None

    try:
        return json.loads(metadata).get("phone_number")
    except json.JSONDecodeError:
        return metadata.strip() or None


@server.rtc_session(agent_name="outbound-agent")
async def outbound_agent(ctx: JobContext):
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    phone_number = phone_number_from_metadata(ctx)

    if not phone_number:
        logger.error("No phone number found in job metadata.")
        ctx.shutdown()
        return

    if not OUTBOUND_TRUNK_ID:
        logger.error(
            "LIVEKIT_SIP_OUTBOUND_TRUNK_ID is not set."
        )
        ctx.shutdown()
        return

    await ctx.connect()

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(
            model="gemini-flash-latest",
        ),
        tts=murf.TTS(
            voice="Anisha",
            tokenizer=tokenize.basic.SentenceTokenizer(
                min_sentence_len=2
            ),
            text_pacing=True,
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    session_started = asyncio.create_task(
        session.start(
            agent=OutboundAgent(ctx),
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
    )

    logger.info("Dialing %s", phone_number)

    try:
        await ctx.api.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                room_name=ctx.room.name,
                sip_trunk_id=OUTBOUND_TRUNK_ID,
                sip_call_to=phone_number,
                participant_identity=CALLEE_IDENTITY,
                participant_name="Phone user",
                wait_until_answered=False,
            )
        )

    except api.TwirpError as e:
        logger.error(
            "Call to %s was not answered: %s (%s)",
            phone_number,
            e.message,
            e.metadata.get("sip_status"),
        )
        session_started.cancel()
        ctx.shutdown()
        return

    await session_started

    await session.say(
        GREETING,
        allow_interruptions=True,
    )


if __name__ == "__main__":
    cli.run_app(server)