---
description: Create NotebookLM studio artifacts (podcasts, videos, slides, infographics, reports, quizzes, flashcards, mind maps, data tables)
argument-hint: [what to create, e.g., "podcast from my CRISPR notebook" or "debate + slides from these URLs"]
allowed-tools: Skill(notebooklm-studio)
---

<objective>
Delegate NotebookLM studio artifact creation to the notebooklm-studio skill for: $ARGUMENTS

This routes to the specialized skill containing MCP tool workflows, preset definitions, and guided multi-step artifact generation.
</objective>

<process>
1. Use Skill tool to invoke notebooklm-studio skill
2. Pass user's request: $ARGUMENTS
3. Let skill handle the full lifecycle: notebook setup, sources, research, generation, polling, download
</process>

<success_criteria>
- Skill successfully invoked
- Arguments passed correctly to skill
- Artifact generated and downloaded to ~/Downloads/notebooklm/
</success_criteria>
