# ADK Framework

Template repo for spinning up Google ADK proof-of-concept agents on GCP.
**Clone this repo for each new client engagement — one repo per client.**

## Structure

| Path | Purpose |
|------|---------|
| `infra/terraform/` | GCP infrastructure. Each module is optional — uncomment in `main.tf` as needed |
| `infra/scripts/` | gcloud fallback commands for clients where Terraform isn't available |
| `agents/` | ADK agent package. `__init__.py` exposes `root_agent` (required by ADK CLI) |
| `agents/agent.py` | Orchestrator (root agent) — delegates to sub-agents |
| `agents/runner.py` | Shared runner — both Streamlit and chat integrations import this |
| `agents/shared_tools/` | Tools available to any agent (BigQuery, GCS, etc.) |
| `agents/sub_agents/` | One folder per capability/domain |
| `docker/Dockerfile` | Container for Cloud Run deployment |
| `ui/streamlit/` | Demo UI for PoC walkthroughs |
| `ui/integrations/slack/` | Slack bot integration |
| `ui/integrations/teams/` | Microsoft Teams bot integration |
| `scripts/new_agent.py` | Scaffolds a new sub-agent |

## Conventions

- Each sub-agent lives in `agents/sub_agents/<name>/` with `__init__.py` exposing `agent`
- The orchestrator imports sub-agents and passes them to `sub_agents=[]`
- Tools specific to a sub-agent live in `agents/sub_agents/<name>/tools/`
- Tools shared across agents live in `agents/shared_tools/`
- Model is set via `ADK_MODEL` env var, defaults to `gemini-2.5-flash`

## Common commands

```bash
make install          # install dependencies
make run              # launch ADK web UI (agent dev/debug)
make streamlit        # launch Streamlit demo UI
make new-agent name=my_agent   # scaffold a new sub-agent
make deploy           # build and deploy to Cloud Run
```

## Adding a new sub-agent

```bash
make new-agent name=my_agent
```

Then register it in `agents/agent.py`:

```python
from .sub_agents.my_agent import agent as my_agent

root_agent = Agent(
    ...
    sub_agents=[existing_agent, my_agent],
)
```

## Environment setup

Copy `.env.example` to `.env` and fill in values before running anything.
For Vertex AI, run `gcloud auth application-default login` instead of setting `GOOGLE_APPLICATION_CREDENTIALS`.