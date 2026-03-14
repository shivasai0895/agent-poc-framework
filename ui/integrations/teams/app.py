"""Microsoft Teams bot integration using Bot Framework SDK + Flask.

Setup:
  1. Register a bot at https://dev.botframework.com (or Azure Bot Service)
  2. Note the App ID and App Password → set in .env
  3. Set the messaging endpoint to: https://<your-cloud-run-url>/api/messages
  4. Install the bot into your Teams tenant

Run:
  make teams
"""
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, Response, request

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agents import root_agent
from agents.runner import create_runner, run_turn

from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

app = Flask(__name__)
runner = create_runner(root_agent)

adapter = BotFrameworkAdapter(
    BotFrameworkAdapterSettings(
        app_id=os.environ.get("MICROSOFT_APP_ID", ""),
        app_password=os.environ.get("MICROSOFT_APP_PASSWORD", ""),
    )
)


async def _handle_turn(turn_context: TurnContext) -> None:
    if turn_context.activity.type != "message":
        return

    user_id = turn_context.activity.from_property.id
    text = turn_context.activity.text or ""

    response = await run_turn(
        runner, text, user_id=user_id, session_id=f"teams-{user_id}"
    )
    await turn_context.send_activity(response)


@app.route("/api/messages", methods=["POST"])
def messages():
    activity = Activity().deserialize(request.json)
    auth_header = request.headers.get("Authorization", "")

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(
            adapter.process_activity(activity, auth_header, _handle_turn)
        )
    finally:
        loop.close()

    return Response(status=200)


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 3978)))
