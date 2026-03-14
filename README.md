# agent-poc-framework

A reusable starting point for building Google ADK (Agent Development Kit) proof-of-concept agents on GCP. Clone this repo for each new client engagement.

## What's included

| Section | What it does |
|---------|-------------|
| `infra/` | Terraform modules for GCP services + gcloud fallback scripts |
| `agents/` | Multi-agent ADK setup — orchestrator + sub-agents |
| `ui/` | Streamlit demo UI and Slack/Teams chat integrations |
| `scripts/` | Scaffold tool to generate new sub-agents |
| `docker/` | Dockerfile for Cloud Run deployment |

## Prerequisites

- Python 3.11+
- [Google ADK](https://google.github.io/adk-docs/) — `pip install google-adk`
- A GCP project with billing enabled, or a [Google AI Studio API key](https://aistudio.google.com/app/apikey) for local dev without GCP
- Terraform (optional — only needed for infra provisioning)

## Getting started

**1. Clone for a new client**
```bash
git clone https://github.com/shivasai0895/agent-poc-framework.git client-name
cd client-name
```

**2. Install dependencies**
```bash
make install
```

**3. Configure environment**
```bash
cp .env.example .env
# Fill in GOOGLE_API_KEY (AI Studio) or GOOGLE_CLOUD_PROJECT (Vertex AI)
```

**4. Run the agent**
```bash
make run        # ADK web UI — good for development and debugging
make streamlit  # Streamlit demo UI — good for client walkthroughs
```

## Project structure

```
agent-poc-framework/
│
├── infra/
│   ├── terraform/
│   │   ├── main.tf              # Uncomment modules as needed per client
│   │   ├── variables.tf
│   │   └── modules/
│   │       ├── vertex_ai/       # Always required
│   │       ├── cloud_run/
│   │       ├── bigquery/
│   │       ├── cloud_sql/
│   │       ├── cloud_storage/
│   │       └── pubsub/
│   └── scripts/
│       └── enable_apis.sh       # Manual fallback if Terraform isn't available
│
├── agents/
│   ├── __init__.py              # Exposes root_agent (required by ADK)
│   ├── agent.py                 # Orchestrator — routes to sub-agents
│   ├── runner.py                # Shared runner imported by all UIs
│   ├── prompts/                 # System prompts
│   ├── shared_tools/            # Tools available to any agent (BigQuery, GCS)
│   └── sub_agents/
│       └── example/             # Template sub-agent
│           ├── agent.py
│           └── tools/
│
├── docker/
│   └── Dockerfile               # Cloud Run container
│
├── scripts/
│   └── new_agent.py             # Sub-agent scaffolding tool
│
└── ui/
    ├── streamlit/               # Demo UI
    └── integrations/
        ├── slack/               # Slack bot (Socket Mode)
        └── teams/               # Microsoft Teams bot
```

## Adding a sub-agent

```bash
make new-agent name=data_analyst
```

This creates `agents/sub_agents/data_analyst/` with all the boilerplate. Then register it in `agents/agent.py`:

```python
from .sub_agents.data_analyst import agent as data_analyst_agent

root_agent = Agent(
    ...
    sub_agents=[data_analyst_agent],
)
```

## GCP infrastructure

Vertex AI is always provisioned. Everything else is optional — open `infra/terraform/main.tf` and uncomment the modules this client needs:

```hcl
module "bigquery" {
  source     = "./modules/bigquery"
  project_id = var.project_id
  region     = var.region
  dataset_id = var.bigquery_dataset_id
}
```

Then:
```bash
cd infra/terraform
terraform init
terraform apply -var="project_id=YOUR_PROJECT"
```

If Terraform isn't available:
```bash
PROJECT_ID=your-project bash infra/scripts/enable_apis.sh
```

## Chat integrations

**Slack** — uncomment `slack-bolt` in `requirements.txt`, add tokens to `.env`, then:
```bash
make slack
```

**Teams** — uncomment `botbuilder-core` and `flask` in `requirements.txt`, add app credentials to `.env`, then:
```bash
make teams
```

## Deploying to Cloud Run

```bash
make deploy PROJECT_ID=your-project REGION=us-central1
```

This builds the container, pushes to Google Container Registry, and deploys to Cloud Run.
