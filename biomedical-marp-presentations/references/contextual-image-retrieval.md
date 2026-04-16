# Contextual Image Retrieval for Biomedical Presentations

## Overview

Contextual image retrieval is an advanced method for finding scientifically relevant figures that match the specific content and context of each presentation subtopic, rather than just matching keywords.

## The Problem with Keyword Matching

Traditional keyword-based image search has limitations:
- ❌ May miss relevant figures with different terminology
- ❌ Returns false positives with keyword matches but wrong context
- ❌ Doesn't understand semantic relationships
- ❌ Ignores the narrative flow of the presentation

## The Solution: Contextual Matching with fig_desc

**Contextual matching** uses the rich descriptions from PMC figures (`fig_desc`) to find images that truly match your subtopic's context:

✅ **Semantic Understanding**: Matches meaning, not just words
✅ **Context-Aware**: Considers the full subtopic description
✅ **Relevance Ranking**: Scores figures by how well they fit
✅ **Subtopic-Specific**: Finds best figures for each section

## How It Works

### Step 1: Define Subtopics

For each presentation subtopic, define:

```json
{
  "subtopic_name": "TMS Coil Types",
  "keywords": ["figure-8 coil", "H-coil", "circular coil"],
  "context_description": "Overview of different TMS coil designs, their geometry, and physical characteristics",
  "pmc_query": "transcranial magnetic stimulation AND coil design",
  "max_figures": 3
}
```

**Fields Explained**:
- `subtopic_name`: The slide section or topic
- `keywords`: Important terms (for fallback matching)
- `context_description`: What this subtopic covers (for semantic matching)
- `pmc_query`: PubMed search to find relevant articles
- `max_figures`: How many figures to retrieve

### Step 2: Search PMC

The system searches PMC for articles matching your query:

```
Query: "transcranial magnetic stimulation AND coil design"
  ↓
Returns: Recent open-access articles about TMS coils
```

### Step 3: Extract Figure Descriptions

For each article, extract:
- `fig_desc`: Full figure caption/description (the key!)
- `fig_title`: Figure title
- `fig_label`: "Figure 1", "Fig. 2A", etc.
- `image_url`: Where to download the image
- Article metadata

**Example fig_desc**:
> "Comparison of figure-8, circular, and H-coil configurations showing penetration depth and focality characteristics. The figure-8 coil provides superior focality (FWHM=2.5cm) while the H-coil achieves greater depth penetration (>6cm)."

### Step 4: Calculate Relevance Scores

Two methods (automatic fallback):

#### Method A: TF-IDF Cosine Similarity (Preferred)

Uses machine learning to understand semantic similarity:

```python
# Combine subtopic context
context = "Overview of different TMS coil designs, their geometry, 
           and physical characteristics figure-8 coil H-coil circular coil"

# Compare to fig_desc using TF-IDF
similarity = cosine_similarity(context, fig_desc)
# Returns: 0.0 to 1.0 (higher = more relevant)
```

**Advantages**:
- Understands word importance
- Captures semantic relationships
- Weighs terms appropriately

#### Method B: Keyword Matching (Fallback)

Simple matching when sklearn unavailable:

```python
keywords = ["figure-8 coil", "H-coil", "circular coil"]
matches = count(keyword in fig_desc for keyword in keywords)
score = matches / len(keywords)
```

### Step 5: Rank and Select

Figures are ranked by relevance score:

```
TMS Coil Types:
  1. Score: 0.847 - Figure 2 (Coil comparison diagram)
  2. Score: 0.723 - Figure 3A (Field distribution)
  3. Score: 0.681 - Figure 1 (Coil geometries)
```

Top N figures are downloaded for each subtopic.

### Step 6: Create Image Library

All matched figures are saved to `image_library.json`:

```json
{
  "image_id": "PMC12345_Fig2",
  "filename": "PMC12345_Fig2.jpg",
  "path": "/full/path/to/image.jpg",
  "caption": "Comparison of figure-8, circular...",
  "section": "TMS Coil Types",
  "relevance_score": 0.847,
  "subtopic": "TMS Coil Types"
}
```

## Usage in Skill Workflow

### Option 1: Manual Configuration File

1. **Create subtopics config**:

```bash
# Generate example
python scripts/pmc_contextual_fetcher.py --example-config

# Edit subtopics_example.json with your topics
```

2. **Run contextual fetcher**:

```bash
python scripts/pmc_contextual_fetcher.py \
  --config subtopics.json \
  --output ./images \
  --create-library
```

3. **Use in presentation**:
Images are automatically organized by subtopic in the library.

### Option 2: Automatic (Skill-Driven)

When Claude creates a presentation, it can:

1. **Parse presentation structure** into subtopics
2. **Generate config automatically** from key points and keywords
3. **Run contextual fetcher** for each subtopic
4. **Insert matched figures** in appropriate slides

**Example automated workflow**:

```
User Request:
  "Create presentation on TMS coil types and stimulation patterns"

Claude:
  1. Identifies subtopics:
     - TMS Coil Types
     - Penetration Depth
     - Stimulation Patterns
  
  2. Generates config:
     {
       "subtopic_name": "TMS Coil Types",
       "keywords": ["figure-8", "H-coil", "circular"],
       "context_description": "Different coil designs and geometry",
       "pmc_query": "TMS AND coil design"
     }
  
  3. Runs pmc_contextual_fetcher.py
  
  4. Inserts top-scored figures in relevant slides
```

## Configuration Examples

### Example 1: Mechanism Slides

```json
{
  "subtopic_name": "NMDA Receptor Signaling",
  "keywords": ["NMDA receptor", "calcium", "CaMKII", "LTP"],
  "context_description": "Molecular signaling cascade from NMDA receptor activation to long-term potentiation, including calcium influx and downstream kinases",
  "pmc_query": "NMDA receptor AND signaling AND (long-term potentiation OR LTP)",
  "max_figures": 2
}
```

### Example 2: Clinical Evidence

```json
{
  "subtopic_name": "TMS Efficacy in Depression",
  "keywords": ["depression", "efficacy", "response rate", "meta-analysis"],
  "context_description": "Clinical trial data showing treatment response rates and effect sizes for TMS in major depressive disorder",
  "pmc_query": "(transcranial magnetic stimulation OR TMS) AND depression AND (efficacy OR response rate) AND meta-analysis[PT]",
  "max_figures": 3
}
```

### Example 3: Anatomical/Imaging

```json
{
  "subtopic_name": "Prefrontal Cortex Targeting",
  "keywords": ["DLPFC", "prefrontal cortex", "targeting", "neuroimaging"],
  "context_description": "Neuroanatomical targeting of dorsolateral prefrontal cortex with TMS, including imaging guidance and localization methods",
  "pmc_query": "TMS AND (DLPFC OR dorsolateral prefrontal cortex) AND (targeting OR localization)",
  "max_figures": 2
}
```

## Advantages Over Simple Search

| Feature | Keyword Search | Contextual Matching |
|---------|----------------|---------------------|
| Semantic understanding | ❌ | ✅ |
| Context awareness | ❌ | ✅ |
| Relevance ranking | Basic | Advanced (TF-IDF) |
| False positives | High | Low |
| Subtopic specificity | Low | High |
| Narrative coherence | No | Yes |

## Best Practices

### 1. Write Good Context Descriptions

❌ **Bad**: "Coils"
✅ **Good**: "Overview of different TMS coil designs, their geometry, physical characteristics, and electromagnetic properties"

The richer your context description, the better the matching.

### 2. Use Specific PMC Queries

Include:
- Main topic terms
- Publication type filters: `meta-analysis[PT]`, `review[PT]`
- MeSH terms when appropriate
- Date ranges if needed: `AND 2020:2025[pdat]`

### 3. Set Appropriate max_figures

- **Complex topics**: 3-4 figures
- **Simple concepts**: 1-2 figures
- **Comparison slides**: 2-3 figures

### 4. Keywords as Safety Net

Even with contextual matching, include key terms as fallback:
- Specific terminology
- Abbreviations
- Important concepts
- Technical terms

### 5. Iterate and Refine

After first run:
1. Check relevance scores (>0.5 is good)
2. Adjust context descriptions if scores are low
3. Refine PMC queries if few articles found
4. Update keywords for better fallback

## Troubleshooting

### Low Relevance Scores (<0.3)

**Problem**: Figures don't match well

**Solutions**:
- Make context description more specific
- Add more relevant keywords
- Broaden PMC query to get more articles
- Check if topic is too narrow

### No Figures Found

**Problem**: No articles or figures retrieved

**Solutions**:
- Simplify PMC query
- Check for typos in medical terms
- Broaden date range
- Try alternative terminology

### Wrong Figures Retrieved

**Problem**: High scores but irrelevant content

**Solutions**:
- Add negative keywords to context
- Make context description more specific
- Filter PMC query with publication type
- Manually review and curate results

## Integration with Presentation Workflow

### In SKILL.md Workflow

```markdown
5. Source Images

  5.1 Analyze presentation structure
      - Identify subtopics
      - Extract keywords and key points
      - Determine context for each section
  
  5.2 Generate contextual config
      - Create subtopics.json automatically
      - Use user's key points as context
      - Formulate PMC queries
  
  5.3 Run contextual fetcher
      - Execute pmc_contextual_fetcher.py
      - Download matched figures
      - Create image_library.json
  
  5.4 Insert figures in slides
      - Match subtopic to slide section
      - Use top-ranked figures
      - Include proper citations and captions
```

### When to Use Contextual Fetcher vs. Simple Search

**Use Contextual Fetcher**:
- ✅ Multiple subtopics in presentation
- ✅ Need best match for specific content
- ✅ Important to have narrative coherence
- ✅ Creating comprehensive presentations

**Use Simple Search**:
- ✅ Single general topic
- ✅ Quick presentations
- ✅ User provides specific PMIDs/images
- ✅ Broad overview without depth

## Technical Requirements

```bash
# Required
pip install requests --break-system-packages

# Recommended (for TF-IDF matching)
pip install scikit-learn --break-system-packages

# Optional (for data handling)
pip install polars --break-system-packages
```

Without sklearn: Falls back to keyword matching (still functional)

## Example Complete Workflow

```bash
# 1. Create config
cat > tms_subtopics.json << EOF
[
  {
    "subtopic_name": "TMS Coil Geometry",
    "keywords": ["figure-8", "H-coil", "coil design"],
    "context_description": "Physical design and electromagnetic properties of different TMS coil types",
    "pmc_query": "transcranial magnetic stimulation AND coil AND (design OR geometry)",
    "max_figures": 3
  },
  {
    "subtopic_name": "Clinical Protocols",
    "keywords": ["rTMS", "theta burst", "protocol"],
    "context_description": "Treatment protocols including frequency, intensity, and duration parameters",
    "pmc_query": "repetitive transcranial magnetic stimulation AND protocol",
    "max_figures": 2
  }
]
EOF

# 2. Run fetcher
python scripts/pmc_contextual_fetcher.py \
  --config tms_subtopics.json \
  --output ./tms_images \
  --create-library

# 3. Use in presentation
# The image_library.json now has figures organized by subtopic
# with relevance scores for optimal selection
```

## Summary

Contextual image retrieval transforms how biomedical presentations find and use figures:

1. **Define** subtopics with context descriptions
2. **Search** PMC for relevant open-access articles
3. **Extract** figures with rich descriptions (fig_desc)
4. **Match** using TF-IDF semantic similarity
5. **Rank** by relevance score
6. **Select** top figures for each subtopic

This ensures every figure is not just keyword-relevant, but **contextually appropriate** for its specific slide and narrative purpose.
