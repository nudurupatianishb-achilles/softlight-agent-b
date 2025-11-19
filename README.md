# Softlight Agent B – UI State Capture System

This repo implements **Agent B** for the Softlight take-home: a system that
takes a natural language request like:

> "How do I create a project in Linear?"  
> "How do I filter a database in Notion?"

and then:

1. Plans a sequence of generic UI actions (open URL, click, fill, wait).
2. Drives a real browser (via Playwright) to execute those actions.
3. Captures screenshots of each important UI state (including non-URL states
   like modals and forms).
4. Writes a dataset of images + metadata grouped by app and task.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install
```

## Running

Linear demo:

```bash
python main.py \
  --app linear \
  --request "How do I create a project in Linear?" \
  --task-id linear_create_project_demo
```

Notion example (adjust workspace URL in `agent/planner.py`):

```bash
python main.py \
  --app notion \
  --request "How do I filter a database in Notion?" \
  --task-id notion_filter_demo
```

Output structure:

```text
dataset/
  <app>/
    <task_id>/
      meta.json
      steps/
        01_*.png
        02_*.png
        ...
```
