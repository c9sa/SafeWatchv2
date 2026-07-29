# SafeWatch

SafeWatch listens to Singapore subreddits for unreported crimes. Our AI Agents classifies the incidents, evaluates whether the report is authentic, and stores full agent traces for debugging, auditability, and demo explainability.

# Current Status

This project is being rebuilt from a hackathon prototype into a more structured, scalable, and observable AI agent system.

## System Architecture

```text
Crawler
  ↓
Raw Post Storage
  ↓
Cleaner Agent
  ↓
Classifier Agent
  ↓
Decision Agent
  ↓
Retry Loop, if needed
  ↓
Published Incident / Rejected Incident
  ↓
Dashboard + Agent Trace Logs
```

## Project Structure

```text
SAFEWATCHV2/
  agents/
    classifier.py
    cleaner.py
    crawler.py
    decision.py

  app/
    main.py

  clients/
    openai_client.py

  config/
    settings.py

  graph/
    routing.py
    workflow.py

  prompts/
    classifier_prompt.py
    crawler_prompt.py
    decision_prompt.py

  schemas/
    messages.py
    outputs.py
    state.py

  scripts/
    run_mock_pipeline.py

  services/
    observability.py

  .env
  .gitignore
  README.md
```

## Overview

SafeWatch is designed to solve a common problem in community safety reporting: online posts may contain useful public safety information, but they are often unstructured, vague, duplicated, exaggerated, or unrelated to actual local incidents.

The system uses an agentic workflow to process each report through multiple stages:

1. Crawl source posts from public platforms
2. Store the untouched raw post
3. Clean and extract incident details
4. Classify the incident category, authenticity, and severity
5. Decide whether to publish, reject, or retry classification
6. Log every agent step for observability
7. Publish approved incidents to a public-facing table or dashboard

## Core Features

* Public post ingestion from Reddit or mock data
* Structured incident extraction
* AI-based incident classification
* Publish / reject / retry decision workflow
* Agent-to-agent feedback loop
* Full trace logging for observability
* Separate raw, processed, and published incident records
* Designed for Singapore-specific public safety use cases


## Agent Workflow

### 1. Crawler

The crawler collects public posts and stores the original source content.

Responsibilities:

* Fetch posts from Reddit or another public source
* Store raw title, body, URL, source ID, author, and timestamp
* Avoid duplicate ingestion using source platform and source post ID

### 2. Cleaner Agent

The cleaner converts messy post content into structured incident fields.

Responsibilities:

* Clean raw text
* Extract location
* Extract action
* Extract time if available
* Identify whether the post is relevant to Singapore public safety
* Prepare cleaner output for the classifier

### 3. Classifier Agent

The classifier assigns incident labels.

Responsibilities:

* Choose a valid category
* Assign authenticity level
* Assign severity level
* Explain the classification
* Reconsider output if feedback is provided by the Decision Agent

### 4. Decision Agent

The decision agent decides whether the incident should be published.

Possible decisions:

* `publish`
* `reject`
* `needs_retry`

Responsibilities:

* Apply publishing rules
* Check whether the classification is reasonable
* Send structured feedback to the classifier if retry is needed
* Prevent infinite retry loops

### 5. Optional Verifier Agent

The verifier agent can be added later to check external evidence such as links, images, documents, or official sources.

Responsibilities:

* Check whether attachments support the claim
* Validate source credibility
* Flag unsupported or misleading claims
* Improve public safety reliability

## Incident Categories

Recommended starting categories:

```text
theft
burglary
robbery
assault
violent_crime
vandalism
scam_fraud
identity_document_fraud
harassment_threat
sexual_offense
suspicious_activity
public_disorder
regulatory_offence
drug_offence
traffic_transport_offence
other
```

Use `other` for:

* General news
* Business or legal commentary
* Political posts
* Overseas incidents with no Singapore relevance
* Lost item posts without evidence of theft
* Vague discussions that are not concrete incidents

## Database Design

Under review

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=safewatch-bot
```

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

For Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Requirements

```text
openai
langgraph
langchain
python-dotenv
pydantic
supabase
praw
requests
pytest
```

## Running the Mock Pipeline

```bash
python scripts/run_mock_pipeline.py
```

## Running the Reddit Pipeline

```bash
python scripts/run_reddit_pipeline.py --subreddit singapore --limit 25
```

Optional flags:

```bash
--pretty
--backfill
--limit 50
```

## Observability Goals

Every agent step should log:

```text
trace_id
incident_id
agent_name
attempt_number
input_json
output_json
model
latency_ms
token_usage
status
error_message
created_at
```

This makes the system easier to debug, evaluate, and explain during demos.

## Testing Strategy

Recommended tests:

* Cleaner extracts correct fields
* Classifier only returns valid categories
* Decision Agent publishes clear incidents
* Decision Agent rejects unrelated posts
* Retry loop stops after maximum attempts
* Agent traces are saved correctly
* Duplicate raw posts are not inserted twice

Example test cases:

```text
Clear theft report → publish
Vague rumor → reject or needs_retry
Overseas crime news → reject
Singapore scam report → publish
Lost item without theft evidence → reject
Wrong initial category → needs_retry → corrected classification
```

## Roadmap

### Version 1

* Structured code and database
* Cleaner, classifier, and decision agents
* Retry loop
* Agent trace logging
* Mock post runner

### Version 2

* Reddit crawler integration
* Supabase dashboard
* Published incident map
* Better evaluation dataset
* Human review queue

### Version 3

* Multimodal verifier agent
* Source credibility scoring
* Duplicate incident detection
* Official source cross-checking
* Alerting and notification system
