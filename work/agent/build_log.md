# FlyRank Study Coach — Build Log

## Goal

Build a narrow personal AI agent that answers FlyRank internship
and Machine Learning study questions using the project's provided
files as its data source.

## Platform

Python scripted agent.

## MVP Scope

The first version will:

1. Accept one study question.
2. Search relevant FlyRank project files.
3. Retrieve relevant material.
4. Generate a grounded answer.
5. Identify the source used.

The MVP will not modify, delete, commit, or submit project files.

## Iteration 1 — Initial setup

### What worked

The FlyRank repository and required project folders are available.

A dedicated `work/agent/` directory has been created for the agent.

### What broke

Nothing yet.

### What I changed

Created a dedicated location for the agent and its build log.

### What I cut from the original specification

For the MVP, I am not implementing:

- quiz generation
- automatic file modification
- GitHub commits
- automatic submission
- external actions

### Why

These features are outside the narrowest core job. I want to get the
question → relevant files → grounded answer loop working first.

## Iteration 2 — File retrieval MVP

### Status

Successful.

### What I tried

Ran:

`python work/agent/agent.py`

and tested the question:

"Why did I use client grouped train test splitting in my Week 5 model?"

### What worked

The agent successfully loaded 3 FlyRank knowledge documents and
retrieved relevant evidence from:

- `skills/flyrank/flyrank-data/SKILL.md`
- `skills/flyrank/flyrank-context/SKILL.md`
- `skills/training-honest-models/SKILL.md`

The most relevant evidence confirmed that `client_id` should be used
for grouped train/test splits.

### What broke

The retrieval layer worked, but the agent does not yet generate a
natural-language answer from the retrieved evidence.

### What I changed

Created a keyword-based retrieval layer that searches the configured
FlyRank knowledge files and displays matching evidence.

### Next step

Connect the retrieved evidence to an LLM so the agent can answer the
user's question using the retrieved project material.

## Iteration 3 — LLM connection attempt

### Status

Retrieval succeeded, but LLM generation failed because the OpenAI
API account had no remaining credits.

### What I tried

Connected the retrieved FlyRank evidence to the OpenAI API and tested
the Week-5 client-grouped train/test question.

### What worked

The agent successfully:
- loaded the FlyRank knowledge files;
- retrieved 3 relevant sources;
- reached the LLM call.

### What broke

The OpenAI API returned:

`429 insufficient_quota / credit_balance_exhausted`

The account has no remaining API credits.

### What I changed

I decided not to add paid API credits for the MVP.

### Why

The assignment allows a scripted agent, and the core job can be
implemented using the project's local knowledge files without adding
an unnecessary paid dependency.

### Next step

Build a local grounded response layer that uses retrieved evidence
and refuses to answer when supporting evidence is unavailable.