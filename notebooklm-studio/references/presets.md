# Preset Definitions

## Unified Tiers

Three tiers apply across all artifact types. Use tier name as shorthand (e.g., "quick audio", "detailed slides").

### Quick Tier
Fast, minimal output. Good for previews and quick checks.

| Type | Parameters |
|------|-----------|
| **Audio** | `audio_format="brief"`, `audio_length="short"` |
| **Video** | `video_format="brief"`, `visual_style="auto_select"` |
| **Slides** | `slide_format="presenter_slides"`, `slide_length="short"` |
| **Infographic** | `detail_level="concise"`, `orientation="square"` |
| **Report** | `report_format="Blog Post"` |
| **Quiz** | `question_count=5`, `difficulty="easy"` |
| **Flashcards** | `difficulty="easy"` |
| **Mind Map** | *(no tier-specific params)* |
| **Data Table** | *(no tier-specific params, description required)* |

### Standard Tier (Default)
Balanced defaults. Use when user doesn't specify a preference.

| Type | Parameters |
|------|-----------|
| **Audio** | `audio_format="deep_dive"`, `audio_length="default"` |
| **Video** | `video_format="explainer"`, `visual_style="auto_select"` |
| **Slides** | `slide_format="detailed_deck"`, `slide_length="default"` |
| **Infographic** | `detail_level="standard"`, `orientation="landscape"` |
| **Report** | `report_format="Briefing Doc"` |
| **Quiz** | `question_count=10`, `difficulty="medium"` |
| **Flashcards** | `difficulty="medium"` |
| **Mind Map** | *(no tier-specific params)* |
| **Data Table** | *(no tier-specific params, description required)* |

### Detailed Tier
Maximum depth and length. For thorough analysis and comprehensive outputs.

| Type | Parameters |
|------|-----------|
| **Audio** | `audio_format="debate"`, `audio_length="long"` |
| **Video** | `video_format="explainer"`, `visual_style="whiteboard"` |
| **Slides** | `slide_format="detailed_deck"`, `slide_length="default"` |
| **Infographic** | `detail_level="detailed"`, `orientation="landscape"` |
| **Report** | `report_format="Study Guide"` |
| **Quiz** | `question_count=20`, `difficulty="hard"` |
| **Flashcards** | `difficulty="hard"` |
| **Mind Map** | *(no tier-specific params)* |
| **Data Table** | *(no tier-specific params, description required)* |

---

## Type-Specific Named Presets

### Audio Presets

| Preset | audio_format | audio_length | Description |
|--------|-------------|-------------|-------------|
| `podcast` | deep_dive | default | Deep conversational exploration of the topic |
| `briefing` | brief | short | Quick summary overview |
| `critique` | critique | default | Critical analysis with counterarguments |
| `debate` | debate | long | Two-sided debate format |

### Video Presets

| Preset | video_format | visual_style | Description |
|--------|-------------|-------------|-------------|
| `explainer` | explainer | auto_select | Standard animated explainer video |
| `whiteboard` | explainer | whiteboard | Hand-drawn whiteboard style |
| `anime` | explainer | anime | Japanese anime visual style |
| `watercolor` | explainer | watercolor | Artistic watercolor style |

Additional visual styles available for custom override:
`classic`, `kawaii`, `retro_print`, `heritage`, `paper_craft`

### Slide Presets

| Preset | slide_format | slide_length | Description |
|--------|-------------|-------------|-------------|
| `presentation` | detailed_deck | default | Full presentation with detail |
| `quick-deck` | presenter_slides | short | Compact presenter notes format |

### Infographic Presets

| Preset | orientation | detail_level | Description |
|--------|-----------|-------------|-------------|
| `landscape` | landscape | standard | Wide format, balanced detail |
| `portrait` | portrait | standard | Tall format, balanced detail |
| `poster` | landscape | detailed | Dense, information-rich poster |
| `summary` | square | concise | Compact square overview |

### Report Presets

| Preset | report_format | Description |
|--------|--------------|-------------|
| `briefing` | Briefing Doc | Executive summary format |
| `study-guide` | Study Guide | Educational study format |
| `blog` | Blog Post | Casual, readable blog format |
| `custom` | Create Your Own | Requires `custom_prompt` parameter |

---

## Override Examples

Override any preset parameter:

```
# Use podcast preset but make it short
"Create a podcast" -> podcast preset (deep_dive, default)
"Make it short" -> override: audio_length="short"
Result: audio_format="deep_dive", audio_length="short"

# Use standard tier for slides but in portrait
"Standard slides" -> standard tier (detailed_deck, default)
"Portrait orientation" -> N/A for slides, ignore

# Use detailed tier for infographic but concise
"Detailed infographic" -> detailed tier (detailed, landscape)
"Keep it concise" -> override: detail_level="concise"
Result: detail_level="concise", orientation="landscape"
```

## Language Override

Any preset can be combined with a language override:
- `language="en"` (default)
- `language="es"` (Spanish)
- `language="fr"` (French)
- `language="de"` (German)
- `language="ja"` (Japanese)
- Any valid BCP-47 code
