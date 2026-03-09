---
# Fill in the fields below to create a basic custom agent for your repository.
# The Copilot CLI can be used for local testing: https://gh.io/customagents/cli
# To make this agent available, merge this file into the default repository branch.
# For format details, see: https://gh.io/customagents/config

name:
description:
---

# My Agent

agent:
  name: triage-bot
  purpose: "Label new issues, detect duplicates, and request missing info"
  model: gpt-4o-mini
  temperature: 0.2
  context:
    include:
      - README.md
      - docs/**
      - issues: last_50
  triggers:
    - github.event: issues.opened
    - command: "/triage"
  permissions:
    repo: read
    issues: write
    pull_requests: comment
  tools:
    - name: similarity_search
      provider: local
    - name: jira
      provider: api
  guardrails:
    - "Never close issues automatically"
    - "Escalate to @maintainers on low confidence"
