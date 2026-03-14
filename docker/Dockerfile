FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agents/ ./agents/
COPY ui/ ./ui/
COPY .env.example .env

ENV PORT=8080
EXPOSE 8080

# Default: run the ADK API server (REST endpoint for the agent)
# To serve Streamlit instead, override CMD:
#   CMD ["streamlit", "run", "ui/streamlit/app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
# To run the Slack integration:
#   CMD ["python", "ui/integrations/slack/app.py"]
CMD ["adk", "api_server", "--port", "8080", "agents"]
