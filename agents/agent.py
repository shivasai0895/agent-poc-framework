"""Orchestrator — root agent that delegates to sub-agents."""
import os
from pathlib import Path

from google.adk.agents import Agent

from .sub_agents.example import agent as example_agent

_prompt = (Path(__file__).parent / "prompts" / "orchestrator.txt").read_text()

root_agent = Agent(
    name="orchestrator",
    model=os.getenv("ADK_MODEL", "gemini-2.5-flash"),
    instruction=_prompt,
    description="Orchestrator that routes requests to specialist sub-agents.",
    sub_agents=[example_agent],
)
