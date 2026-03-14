.PHONY: install run streamlit slack teams deploy new-agent

# ── Setup ─────────────────────────────────────────────────────────────────────
install:
	pip install -r requirements.txt

# ── Local dev ─────────────────────────────────────────────────────────────────
run:
	adk web

streamlit:
	streamlit run ui/streamlit/app.py

slack:
	python ui/integrations/slack/app.py

teams:
	python ui/integrations/teams/app.py

# ── Scaffold ──────────────────────────────────────────────────────────────────
# Usage: make new-agent name=my_agent
new-agent:
	python scripts/new_agent.py $(name)

# ── Deploy ────────────────────────────────────────────────────────────────────
# Requires PROJECT_ID and REGION to be set, e.g.:
#   make deploy PROJECT_ID=my-project REGION=us-central1
deploy:
	docker build -t gcr.io/$(PROJECT_ID)/agent:latest -f docker/Dockerfile .
	docker push gcr.io/$(PROJECT_ID)/agent:latest
	gcloud run deploy agent \
		--image gcr.io/$(PROJECT_ID)/agent:latest \
		--region $(REGION) \
		--platform managed \
		--set-env-vars GOOGLE_CLOUD_PROJECT=$(PROJECT_ID)
