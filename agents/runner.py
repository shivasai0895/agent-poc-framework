"""Shared runner — imported by all UI layers."""
import os

from dotenv import load_dotenv
from google.adk.agents import BaseAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()


def create_runner(agent: BaseAgent) -> Runner:
    """Create a Runner with an in-memory session service (local dev default).

    For Vertex AI session persistence, swap InMemorySessionService for
    VertexAiSessionService and pass project/location/agent_engine_id.
    """
    session_service = InMemorySessionService()
    return Runner(
        agent=agent,
        app_name=agent.name,
        session_service=session_service,
    )


async def run_turn(
    runner: Runner,
    user_input: str,
    user_id: str = "user",
    session_id: str = "default",
) -> str:
    """Send one message and return the agent's final text response."""
    session = await runner.session_service.get_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id,
    )
    if session is None:
        session = await runner.session_service.create_session(
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id,
        )

    message = types.Content(
        role="user",
        parts=[types.Part(text=user_input)],
    )

    final_response = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if part.text:
                    final_response += part.text

    return final_response
