---
name: notebooklm-studio
description: Create NotebookLM studio artifacts (audio, video, slides, infographics, reports, quizzes, flashcards, mind maps, data tables) using MCP tools. Full lifecycle from notebook creation through source ingestion, research, artifact generation, and download. Use when user wants to create podcasts, presentations, study materials, or any NotebookLM media content.
---

<objective>
Orchestrate the NotebookLM MCP server tools (`mcp__notebooklm-mcp__*`) to create studio artifacts end-to-end. This skill does NOT use browser automation or Python scripts — it drives the MCP tools directly through a guided multi-step workflow.

Supports all 9 artifact types: audio overviews, video overviews, slide decks, infographics, reports, quizzes, flashcards, mind maps, and data tables.

This skill is a companion to the existing `notebooklm` skill (browser-based querying). Use this skill for **creating media**; use the other for **querying notebook content**.
</objective>

<context>
<mcp_tools>
All tools use the `mcp__notebooklm-mcp__` prefix. Key tools by stage:

**Notebooks**: `notebook_list`, `notebook_create`, `notebook_get`, `notebook_describe`, `notebook_rename`
**Sources**: `source_add` (unified: url|text|file|drive), `source_describe`, `source_get_content`
**Research**: `research_start`, `research_status`, `research_import`
**Studio**: `studio_create` (unified: all 9 types), `studio_status`, `studio_delete`
**Download**: `download_artifact` (unified: all types)
**Auth**: `refresh_auth`, `save_auth_tokens`
</mcp_tools>

<critical_rules>
- `studio_create` and all delete operations require `confirm=True` — ALWAYS get user confirmation first
- After `studio_create`, you MUST poll `studio_status` until status is "completed" or "failed"
- After "completed", you MUST call `download_artifact` to save the file
- If "failed", retry ONCE with the same parameters. If second attempt fails, report the error
- All downloads go to `~/Downloads/notebooklm/{notebook-name}/{type}-{date}.{ext}`
- Default language is English. User can override with BCP-47 codes (es, fr, de, ja, etc.)
</critical_rules>
</context>

<quick_start>
**Fastest path — create a podcast from URLs:**

1. Create notebook:
   `mcp__notebooklm-mcp__notebook_create(title="My Research")`

2. Add sources (repeat for each URL):
   `mcp__notebooklm-mcp__source_add(notebook_id="ID", source_type="url", url="https://...", wait=True)`

3. Generate audio:
   `mcp__notebooklm-mcp__studio_create(notebook_id="ID", artifact_type="audio", audio_format="deep_dive", audio_length="default", confirm=True)`

4. Poll until complete, then download:
   `mcp__notebooklm-mcp__studio_status(notebook_id="ID")`
   `mcp__notebooklm-mcp__download_artifact(notebook_id="ID", artifact_type="audio", output_path="~/Downloads/notebooklm/my-research/audio-2026-02-23.mp3")`
</quick_start>

<workflow>
<stage_1 name="Notebook Setup">
**Goal**: Select an existing notebook or create a new one.

1. **List notebooks**: `notebook_list(max_results=100)`
2. Present notebooks to user with names, source counts
3. For context on a notebook: `notebook_describe(notebook_id="ID")` — shows AI summary + suggested topics
4. User picks existing OR requests new: `notebook_create(title="Name")`

**If user provides a notebook name/ID directly**, skip the listing.
</stage_1>

<stage_2 name="Source Management">
**Goal**: Ensure the notebook has sources to generate from.

Check current sources: `notebook_get(notebook_id="ID")` — shows existing sources.

**Add sources** using `source_add` with `wait=True` (waits for processing):

- **URL/webpage**: `source_add(notebook_id="ID", source_type="url", url="https://...", wait=True)`
- **YouTube video**: `source_add(notebook_id="ID", source_type="url", url="https://youtube.com/...", wait=True)`
- **Pasted text**: `source_add(notebook_id="ID", source_type="text", text="...", title="Name", wait=True)`
- **Local file** (PDF, text, audio): `source_add(notebook_id="ID", source_type="file", file_path="/path/to/file", wait=True)`
- **Google Drive**: `source_add(notebook_id="ID", source_type="drive", document_id="DOC_ID", doc_type="doc|slides|sheets|pdf", wait=True)`

After adding, confirm: "Notebook has N sources. Ready to proceed?"

**If notebook already has sufficient sources**, skip to Stage 3 or 4.
</stage_2>

<stage_3 name="Research (Optional)">
**Goal**: Discover and import new sources via web or Drive search.

Only run this stage if user requests research (e.g., "research X and make a podcast").

1. **Start research**:
   `research_start(query="search terms", source="web", mode="fast|deep", notebook_id="ID")`
   - `fast`: ~30 seconds, ~10 sources
   - `deep`: ~5 minutes, ~40+ sources (web only)

2. **Poll progress**:
   `research_status(notebook_id="ID", poll_interval=30, max_wait=300)`
   Wait for `status="completed"`.

3. **Import sources**:
   `research_import(notebook_id="ID", task_id="TASK_ID")`
   Imports all discovered sources (or specify `source_indices` for selective import).

Present research results summary to user before proceeding.
</stage_3>

<stage_4 name="Artifact Configuration">
**Goal**: Determine what to create and with what settings.

Present available artifact types:
1. **Audio Overview** — podcast-style (deep_dive, brief, critique, debate)
2. **Video Overview** — animated video (explainer, brief; 9 visual styles)
3. **Slide Deck** — presentation PDF (detailed_deck, presenter_slides)
4. **Infographic** — visual PNG (landscape, portrait, square)
5. **Report** — text document (Briefing Doc, Study Guide, Blog Post, Custom)
6. **Quiz** — multiple choice (configurable count + difficulty)
7. **Flashcards** — study cards (easy, medium, hard)
8. **Mind Map** — visual diagram (JSON)
9. **Data Table** — structured data (CSV, requires description)

<preset_system>
**Unified Tiers** (apply to all types):
- **quick** — fast, minimal: brief formats, short lengths, concise detail
- **standard** — balanced defaults: deep_dive/explainer, default length, standard detail
- **detailed** — maximum depth: debate/detailed formats, long lengths, high detail

**Type-Specific Named Presets** (power users):
- Audio: `podcast`, `briefing`, `critique`, `debate`
- Video: `explainer`, `whiteboard`, `anime`, `watercolor`
- Slides: `presentation`, `quick-deck`
- Infographic: `landscape`, `portrait`, `poster`, `summary`
- Report: `briefing`, `study-guide`, `blog`, `custom`

See [references/presets.md](references/presets.md) for complete definitions.

**Override**: User can always specify individual parameters to override any preset.
</preset_system>

**Optional parameters** (apply to all types):
- `focus_prompt`: Focus the artifact on specific aspects (e.g., "focus on methodology")
- `language`: BCP-47 code (default: "en"). Example: "es" for Spanish, "ja" for Japanese
- `source_ids`: Generate from specific sources only (default: all)

**Ask the user**: "What type of artifact? Which preset or custom settings? Any focus prompt?"
</stage_4>

<stage_5 name="Generation + Polling">
**Goal**: Create the artifact and wait for completion.

1. **Confirm with user**: "Ready to generate [type] with [settings]. Proceed?"
2. **Create**: `studio_create(notebook_id="ID", artifact_type="TYPE", confirm=True, ...params)`
3. **Poll**: `studio_status(notebook_id="ID")` — repeat until artifact status is "completed" or "failed"
   - Report progress to user while polling
4. **On failure**: Retry ONCE with identical parameters. If second attempt fails, report error with details.

<batch_mode>
**Batch Mode** — for creating multiple artifacts at once:

1. User requests multiple types (e.g., "podcast, slides, and infographic")
2. Present all configurations for confirmation:
   ```
   Queuing 3 artifacts:
    1. Audio (deep_dive, default)
    2. Slide deck (detailed_deck, default)
    3. Infographic (landscape, standard)
   Confirm generation of all 3?
   ```
3. Call `studio_create` for each (sequentially — each needs confirm=True)
4. Poll `studio_status` — it shows ALL artifacts with their statuses
5. Download each as they complete
</batch_mode>
</stage_5>

<stage_6 name="Download">
**Goal**: Save completed artifacts to disk.

**Download path pattern**: `~/Downloads/notebooklm/{notebook-name}/{type}-{date}.{ext}`

Sanitize notebook name: lowercase, replace spaces with hyphens, remove special characters.

**File extensions by type**:
| Type | Extension |
|------|-----------|
| Audio | .mp3 |
| Video | .mp4 |
| Slide Deck | .pdf |
| Infographic | .png |
| Report | .md |
| Quiz | .json (or .md/.html via output_format) |
| Flashcards | .json (or .md/.html via output_format) |
| Mind Map | .json |
| Data Table | .csv |

**Download call**:
`download_artifact(notebook_id="ID", artifact_type="TYPE", output_path="PATH", artifact_id="ARTIFACT_ID")`

If `artifact_id` is omitted, downloads the latest artifact of that type.

After download, confirm: "Saved to [path]. Would you like to create another artifact or are we done?"
</stage_6>
</workflow>

<error_handling>
<auth_errors>
If any MCP tool returns 401/403 or auth-related error:
1. Run `refresh_auth()` to attempt token refresh
2. If refresh fails, instruct user: "Run `nlm login` in your terminal to re-authenticate"
3. After re-auth, retry the failed operation
</auth_errors>

<generation_failures>
If `studio_status` shows "failed":
1. Retry ONCE with identical parameters (same artifact_type, same options)
2. If second attempt also fails, report:
   - Artifact type and settings used
   - Error details from studio_status
   - Suggestion: try with fewer sources, different format, or simpler focus_prompt
</generation_failures>

<timeout_handling>
- `source_add` with `wait=True`: default timeout 120s. If source processing is slow, increase `wait_timeout`
- `research_status`: default max_wait 300s. Deep research may need `max_wait=600`
- `studio_status`: poll every 30 seconds. Audio/video may take 2-5 minutes
</timeout_handling>
</error_handling>

<anti_patterns>
**Never do these**:
- Call `studio_create` without `confirm=True` — it will fail
- Skip polling `studio_status` after `studio_create` — orphaned generation
- Download without checking status is "completed" — incomplete artifacts
- Use `source_type="url"` for local files — use `source_type="file"` instead
- Pass `source_type="text"` without a `title` — makes sources hard to identify
- Forget to `wait=True` on `source_add` — source may not be ready for generation
- Use `research_import` without checking `research_status` is "completed"
- Create a data_table without the required `description` parameter
</anti_patterns>

<success_criteria>
A successful run means:
- Notebook exists with sources loaded and processed
- `studio_create` returned successfully with `confirm=True`
- `studio_status` shows artifact status as "completed"
- `download_artifact` saved file to `~/Downloads/notebooklm/{notebook-name}/{type}-{date}.{ext}`
- User confirmed the artifact meets their needs
- For batch mode: all requested artifacts are downloaded
</success_criteria>

<reference_guides>
**Complete preset definitions**: [references/presets.md](references/presets.md)
- Unified tiers mapped to all 9 types
- Type-specific named presets with exact parameter values
- Override examples

**Full parameter reference**: [references/artifact-options.md](references/artifact-options.md)
- Every parameter for each artifact type
- Valid values and defaults
- Common parameters (language, focus_prompt, source_ids)

**Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md)
- Auth errors and recovery
- Generation failures
- Source processing issues
- Timeout handling
</reference_guides>
