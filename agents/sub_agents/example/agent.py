"""Example sub-agent — replace with your domain-specific agent."""
import os

from google.adk.agents import Agent

from .tools import tools

agent = Agent(
    name="example",
    model=os.getenv("ADK_MODEL", "gemini-2.5-flash"),
    instruction="You are a specialist agent. Handle requests related to your domain and use your tools to get real data.",
    description="Example specialist agent — describes what this agent does so the orchestrator knows when to route here.",
    tools=tools,
)
