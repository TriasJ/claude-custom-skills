# Artifact Options Reference

Complete parameter reference for `mcp__notebooklm-mcp__studio_create`.

## Common Parameters (All Types)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `notebook_id` | string | *required* | Notebook UUID |
| `artifact_type` | string | *required* | One of: audio, video, slide_deck, infographic, report, quiz, flashcards, data_table, mind_map |
| `confirm` | boolean | false | **Must be True** — always set after user confirmation |
| `source_ids` | string[] | null (all) | Specific source UUIDs. Default uses all sources |
| `language` | string | "en" | BCP-47 language code |
| `focus_prompt` | string | "" | Focus the artifact on specific aspects |

---

## Audio Overview

Podcast-style audio content generated from notebook sources.

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `audio_format` | `deep_dive`, `brief`, `critique`, `debate` | `deep_dive` | Conversation style |
| `audio_length` | `short`, `default`, `long` | `default` | Duration |

**Output**: MP4/MP3 file

**Format descriptions**:
- `deep_dive`: Two hosts explore the topic in depth, conversational style
- `brief`: Quick summary overview, shorter format
- `critique`: Critical analysis, examines strengths and weaknesses
- `debate`: Two opposing viewpoints discuss the topic

---

## Video Overview

Animated video with narration and visuals.

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `video_format` | `explainer`, `brief` | `explainer` | Video style |
| `visual_style` | `auto_select`, `classic`, `whiteboard`, `kawaii`, `anime`, `watercolor`, `retro_print`, `heritage`, `paper_craft` | `auto_select` | Visual aesthetic |

**Output**: MP4 file

**Visual style descriptions**:
- `auto_select`: AI picks the best style for the content
- `classic`: Clean, professional animation
- `whiteboard`: Hand-drawn whiteboard sketches
- `kawaii`: Cute, colorful Japanese style
- `anime`: Japanese anime art style
- `watercolor`: Artistic watercolor paintings
- `retro_print`: Vintage print/letterpress aesthetic
- `heritage`: Traditional, historical art style
- `paper_craft`: Paper cutout / craft aesthetic

---

## Slide Deck

Presentation slides exported as PDF.

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `slide_format` | `detailed_deck`, `presenter_slides` | `detailed_deck` | Slide density |
| `slide_length` | `short`, `default` | `default` | Number of slides |

**Output**: PDF file

**Format descriptions**:
- `detailed_deck`: Full slides with text and visuals, ready to present
- `presenter_slides`: Condensed slides with speaker notes emphasis

---

## Infographic

Visual summary as a single image.

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `orientation` | `landscape`, `portrait`, `square` | `landscape` | Image orientation |
| `detail_level` | `concise`, `standard`, `detailed` | `standard` | Information density |

**Output**: PNG file

---

## Report

Text-based document in markdown format.

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `report_format` | `Briefing Doc`, `Study Guide`, `Blog Post`, `Create Your Own` | `Briefing Doc` | Document style |
| `custom_prompt` | string (max 10000 chars) | "" | Required when report_format is "Create Your Own" |

**Output**: Markdown file

**Format descriptions**:
- `Briefing Doc`: Executive summary with key findings and recommendations
- `Study Guide`: Educational format with questions, summaries, key concepts
- `Blog Post`: Casual, accessible writing style for blog publication
- `Create Your Own`: Fully custom format defined by `custom_prompt`

---

## Quiz

Multiple-choice questions.

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `question_count` | integer | 2 | Number of questions |
| `difficulty` | `easy`, `medium`, `hard` | `medium` | Question difficulty |

**Output**: JSON file (default), or Markdown/HTML via `download_artifact(output_format="markdown|html")`

---

## Flashcards

Study flashcards with front/back content.

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `difficulty` | `easy`, `medium`, `hard` | `medium` | Content complexity |

**Output**: JSON file (default), or Markdown/HTML via `download_artifact(output_format="markdown|html")`

---

## Mind Map

Visual mind map of concepts and relationships.

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `title` | string | "Mind Map" | Title for the mind map |

**Output**: JSON file

---

## Data Table

Structured data extracted from sources.

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `description` | string | "" | **Required** — describes what data to extract |

**Output**: CSV file

**Important**: The `description` parameter is required for data tables. It tells NotebookLM what data to structure. Example: "Extract all mentioned gene names, their functions, and associated diseases."

---

## Download Format Reference

| Artifact Type | File Extension | MIME Type |
|--------------|---------------|-----------|
| Audio | .mp3 | audio/mpeg |
| Video | .mp4 | video/mp4 |
| Slide Deck | .pdf | application/pdf |
| Infographic | .png | image/png |
| Report | .md | text/markdown |
| Quiz | .json / .md / .html | application/json |
| Flashcards | .json / .md / .html | application/json |
| Mind Map | .json | application/json |
| Data Table | .csv | text/csv |
