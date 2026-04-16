# Troubleshooting Guide

## Authentication Errors

| Symptom | Cause | Solution |
|---------|-------|----------|
| 401/403 from any MCP tool | Expired auth tokens | Run `refresh_auth()`. If fails, run `nlm login` in terminal |
| "Missing required cookies" | Never authenticated | Run `nlm login` in terminal for first-time setup |
| Auth works then stops | Token rotation | Run `nlm login` to refresh cookies |
| Chrome profile errors | Browser state corrupted | Run `nlm login --manual` for manual cookie extraction |

**Auth Recovery Workflow**:
1. `mcp__notebooklm-mcp__refresh_auth()` — try automatic refresh first
2. If fails: instruct user to run `nlm login` in their terminal
3. If `nlm login` auto mode fails: try `nlm login --manual`
4. After re-auth: retry the failed operation

---

## Generation Failures

| Symptom | Cause | Solution |
|---------|-------|----------|
| `studio_status` shows "failed" | Server-side generation error | Retry once with same parameters |
| Second retry also fails | Content too complex or sources incompatible | Try: fewer sources, different format, simpler focus_prompt |
| Generation stuck "in_progress" | Processing delay | Continue polling (increase `max_wait`). Audio/video can take 5+ min |
| "No sources" error | Empty notebook | Add sources before generating |
| Data table fails | Missing description | `description` parameter is required for data_table type |

**Retry Protocol**:
1. If first `studio_create` results in "failed" status:
   - Call `studio_create` again with identical parameters
   - Poll `studio_status` again
2. If second attempt also fails:
   - Report the error to user
   - Suggest: "Try with fewer sources, a different artifact type, or remove the focus_prompt"

---

## Source Processing Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| `source_add` times out | Large file or slow URL | Increase `wait_timeout=300` |
| Source shows 0 content | URL blocked or empty page | Try different URL or use `source_type="text"` with pasted content |
| YouTube source fails | Private/age-restricted video | Only public YouTube videos are supported |
| File upload fails | Unsupported format | Supported: PDF, text, audio files. Convert other formats first |
| Drive source stale | Document updated after import | Use `source_sync_drive` to refresh |

**Source Processing Tips**:
- Always use `wait=True` with `source_add` to ensure processing completes before generation
- Default `wait_timeout` is 120 seconds — increase for large PDFs or slow URLs
- Check source was processed: `source_describe(source_id="ID")` should return a summary
- Maximum sources per notebook: check via `notebook_get` before adding more

---

## Research Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Research returns no results | Query too specific | Broaden search terms |
| Deep research times out | >5 min processing | Increase `max_wait=600` in `research_status` |
| Research stuck | Server-side issue | Use `task_id` in `research_status` to check specific task |
| Import fails | Research not completed | Always check `research_status` shows "completed" before `research_import` |

---

## Download Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Download returns empty file | Artifact not yet complete | Check `studio_status` shows "completed" first |
| Wrong file format | Incorrect `artifact_type` | Match `artifact_type` to what was generated |
| Path doesn't exist | Parent directory missing | Ensure `~/Downloads/notebooklm/{notebook-name}/` exists |
| Quiz/flashcards format wrong | Default is JSON | Use `output_format="markdown"` or `output_format="html"` for readable formats |

---

## Polling Best Practices

- **Audio**: 1-3 minutes typical. Poll every 30 seconds.
- **Video**: 2-5 minutes typical. Poll every 30 seconds.
- **Slides**: 30-90 seconds typical. Poll every 15 seconds.
- **Infographic**: 30-90 seconds typical. Poll every 15 seconds.
- **Report**: 15-60 seconds typical. Poll every 15 seconds.
- **Quiz/Flashcards**: 15-30 seconds typical. Poll every 10 seconds.
- **Mind Map**: 15-30 seconds typical. Poll every 10 seconds.
- **Data Table**: 15-60 seconds typical. Poll every 15 seconds.

For batch mode: poll `studio_status` once to see ALL artifact statuses simultaneously.

---

## Common MCP Tool Errors

| Error | Tool | Solution |
|-------|------|----------|
| "confirm must be True" | studio_create, *_delete | Always set `confirm=True` after user confirms |
| "notebook_id required" | most tools | Pass the notebook UUID, not the name |
| "Invalid source_type" | source_add | Must be one of: url, text, file, drive |
| "description required" | studio_create (data_table) | Provide `description` parameter for data tables |
| "rate limit" | any tool | Wait a few minutes and retry |
