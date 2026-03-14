#!/usr/bin/env python3
"""Scaffold a new sub-agent.

Usage:
    python scripts/new_agent.py <agent_name>
    make new-agent name=<agent_name>

Creates:
    agents/sub_agents/<name>/
    ├── __init__.py
    ├── agent.py
    └── tools/
        └── __init__.py
"""
import argparse
import sys
from pathlib import Path

AGENT_PY = '''\
"""{name} sub-agent."""
import os

from google.adk.agents import Agent

from .tools import tools

agent = Agent(
    name="{name}",
    model=os.getenv("ADK_MODEL", "gemini-2.5-flash"),
    instruction="You are a specialist agent responsible for ...",
    description="Describe what this agent does so the orchestrator knows when to route here.",
    tools=tools,
)
'''

INIT_PY = '''\
from .agent import agent

__all__ = ["agent"]
'''

TOOLS_INIT_PY = '''\
"""Tools for the {name} agent.

Define plain Python functions here — ADK wraps them automatically.
Type hints and docstrings are used by the model to understand when and how to call each tool.
"""


def placeholder_tool(input: str) -> str:
    """Placeholder tool. Replace with real logic.

    Args:
        input: The input to process.

    Returns:
        Result string.
    """
    return f"Result: {{input}}"


tools = [placeholder_tool]
'''


def scaffold(name: str) -> None:
    root = Path(__file__).parent.parent
    base = root / "agents" / "sub_agents" / name

    if base.exists():
        print(f"Error: {base} already exists.")
        sys.exit(1)

    (base / "tools").mkdir(parents=True)
    (base / "__init__.py").write_text(INIT_PY)
    (base / "agent.py").write_text(AGENT_PY.format(name=name))
    (base / "tools" / "__init__.py").write_text(TOOLS_INIT_PY.format(name=name))

    print(f"Created agents/sub_agents/{name}/")
    print(f"  ├── __init__.py")
    print(f"  ├── agent.py")
    print(f"  └── tools/__init__.py")
    print()
    print(f"Next: register {name} in agents/agent.py")
    print(f"  from .sub_agents.{name} import agent as {name}_agent")
    print(f"  sub_agents=[..., {name}_agent]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new sub-agent.")
    parser.add_argument("name", help="Agent name in snake_case (e.g. data_analyst)")
    args = parser.parse_args()
    scaffold(args.name)
