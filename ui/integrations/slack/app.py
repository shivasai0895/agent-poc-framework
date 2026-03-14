"""Slack bot integration using Slack Bolt (Socket Mode).

Setup:
  1. Create a Slack app at https://api.slack.com/apps
  2. Enable Socket Mode and generate an App-Level Token (SLACK_APP_TOKEN)
  3. Add a Bot Token OAuth scope: app_mentions:read, chat:write
  4. Install the app to your workspace and copy the Bot Token (SLACK_BOT_TOKEN)
  5. Set both tokens in .env

Run:
  make slack
"""
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agents import root_agent
from agents.runner import create_runner, run_turn

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ["SLACK_BOT_TOKEN"])
runner = create_runner(root_agent)


@app.event("app_mention")
def handle_mention(event, say):
    """Respond when the bot is @mentioned in a channel."""
    user_id = event["user"]
    # Strip the bot mention from the text
    text = event.get("text", "").split(">", 1)[-1].strip()

    response = asyncio.run(
        run_turn(runner, text, user_id=user_id, session_id=f"slack-{user_id}")
    )
    say(response)


@app.message()
def handle_dm(message, say):
    """Respond to direct messages."""
    user_id = message["user"]
    text = message.get("text", "")

    response = asyncio.run(
        run_turn(runner, text, user_id=user_id, session_id=f"slack-{user_id}")
    )
    say(response)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
