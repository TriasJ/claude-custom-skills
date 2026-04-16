# User Request Formats

## Overview

Users may provide presentation requests in various formats, from simple natural language to structured JSON specifications. This guide shows how to parse and respond to different request formats.

## Format Types

### 1. Simple Natural Language

**Example**:
```
"Create a presentation on TMS for depression"
```

**Parsing**:
- **Topic**: TMS (Transcranial Magnetic Stimulation)
- **Condition**: Depression
- **Implied scope**: Treatment overview
- **Inferred duration**: 30-60 minutes (standard)
- **Audience**: General medical (assumed)

**Required follow-up questions**:
- Target audience (residents, researchers, general?)
- Specific focus (mechanism, efficacy, protocols?)
- Duration
- Image sources available

### 2. Detailed Natural Language

**Example**:
```
"Create a 1-hour presentation for psychiatry residents on TMS mechanisms and clinical protocols for treatment-resistant depression. Include evidence from recent meta-analyses and compare different coil types. Use images from PMC if possible."
```

**Parsing**:
- **Topic**: TMS mechanisms and protocols
- **Condition**: Treatment-resistant depression
- **Duration**: 1 hour (~30-40 slides)
- **Audience**: Psychiatry residents
- **Required content**:
  - Mechanisms of action
  - Clinical protocols
  - Meta-analysis evidence
  - Coil type comparisons
- **Image source**: PMC (contextual fetcher)

**Workflow**:
1. Identify subtopics: mechanisms, protocols, evidence, coil types
2. Search PubMed for meta-analyses (last 5 years)
3. Configure contextual image fetcher for each subtopic
4. Use clinical-education template
5. Structure for 60-minute delivery

### 3. Structured JSON Format

**Example**:
```json
{
  "general_instruction": "Create MARP presentation for psychiatry residency training",
  "topics": {
    "topic": "Transcranial Magnetic Stimulation",
    "subtopic": "Treatment protocols for major depressive disorder"
  },
  "operational_data": {
    "hours": 1,
    "modality": "Synchronous"
  },
  "key_points": [
    "TMS coil types and electromagnetic properties",
    "rTMS vs theta-burst stimulation protocols",
    "FDA-approved treatment parameters",
    "Clinical efficacy and response rates",
    "Safety profile and contraindications"
  ],
  "keywords": [
    "transcranial magnetic stimulation",
    "rTMS",
    "theta-burst",
    "dorsolateral prefrontal cortex",
    "treatment-resistant depression"
  ],
  "competencies": "Residents should be able to: (1) Explain TMS mechanisms, (2) Describe treatment protocols, (3) Identify appropriate candidates, (4) Counsel patients on efficacy and safety",
  "image_usage": {
    "instructions": ["Use PMC contextual image search"],
    "procedure": [
      "Search for figures showing coil types",
      "Find protocol comparison tables",
      "Include meta-analysis forest plots",
      "Show DLPFC targeting images"
    ]
  },
  "bibliography": "Recent meta-analyses and RCTs from PubMed (2020-2025)"
}
```

**Parsing**:
```yaml
Context: Residency training (formal education)
Main topic: TMS
Focus: Treatment protocols for MDD
Duration: 1 hour
Modality: Synchronous (live presentation)

Learning objectives (from competencies):
  1. Explain TMS mechanisms
  2. Describe treatment protocols
  3. Identify appropriate candidates
  4. Counsel patients

Content requirements (from key_points):
  - Coil types and physics
  - Protocol comparison (rTMS vs TBS)
  - FDA parameters
  - Evidence (efficacy, response rates)
  - Safety considerations

Image strategy (from image_usage):
  - PMC contextual search
  - Subtopics: coil types, protocols, efficacy data, targeting

PubMed search parameters (from bibliography):
  - Date range: 2020-2025
  - Publication types: meta-analysis, RCT
  - Focus on recent evidence
```

### 4. Minimal Structured Format

**Example**:
```json
{
  "topic": "CRISPR gene editing",
  "audience": "medical students",
  "duration": 45,
  "focus": ["mechanisms", "clinical applications", "ethical considerations"]
}
```

**Parsing**:
- **Topic**: CRISPR gene editing
- **Audience**: Medical students
- **Duration**: 45 minutes (~25-30 slides)
- **Sections**: Three main areas specified
- **Template**: Basic presentation (student level)
- **Image sources**: Not specified (ask or use PMC default)

## Parsing Workflow

### Step 1: Extract Core Requirements

Always identify:
```yaml
REQUIRED:
  - Topic/subject matter
  - General scope

INFER IF MISSING:
  - Audience (default: general medical)
  - Duration (default: 60 minutes)
  - Structure (from template selection)

ASK IF CRITICAL:
  - Image sources (if specific library provided)
  - Specific constraints or requirements
  - Special formatting needs
```

### Step 2: Map to Skill Parameters

**Topic → PubMed queries**:
```
"TMS for depression" →
  Queries:
    - "(transcranial magnetic stimulation OR TMS) AND depression"
    - "TMS AND depression AND meta-analysis[PT]"
    - "repetitive TMS AND major depressive disorder"
```

**Audience → Template selection**:
```
"residents" → clinical-education.md
"researchers" → research-presentation.md
"medical students" → basic-presentation.md
```

**Key points → Subtopics for image search**:
```
"TMS coil types" → Subtopic config:
  {
    "subtopic_name": "TMS Coil Types",
    "keywords": ["figure-8 coil", "H-coil"],
    "context_description": "Electromagnetic coil designs for TMS",
    "pmc_query": "TMS AND coil design"
  }
```

**Duration → Slide count**:
```
30 minutes → 15-20 slides
45 minutes → 25-30 slides
60 minutes → 30-40 slides
90 minutes → 50-60 slides
```

### Step 3: Generate Subtopic Configuration

From structured or unstructured requests, extract subtopics:

**From key_points**:
```json
"key_points": [
  "TMS mechanisms",
  "Clinical protocols",
  "Safety considerations"
]

→ Subtopics:
[
  {
    "subtopic_name": "TMS Mechanisms",
    "keywords": ["electromagnetic induction", "cortical excitability"],
    "context_description": "Biophysical mechanisms of TMS including electromagnetic induction and cortical modulation",
    "pmc_query": "TMS AND mechanism AND (electromagnetic OR cortical excitability)"
  },
  ...
]
```

**From natural language**:
```
"Compare different coil types"

→ Subtopic:
{
  "subtopic_name": "TMS Coil Comparison",
  "keywords": ["figure-8", "H-coil", "circular coil"],
  "context_description": "Comparative analysis of TMS coil geometries, field characteristics, and clinical applications",
  "pmc_query": "TMS AND coil AND (comparison OR design)"
}
```

### Step 4: Validate and Clarify

Before proceeding, verify:

**Critical items**:
- [ ] Topic is clear and scoped appropriately
- [ ] Audience knowledge level is understood
- [ ] Duration is realistic for content depth
- [ ] Image sources are specified or can be inferred

**Ask if unclear**:
```markdown
When to ask questions:
- Ambiguous scope: "Should this cover X or focus only on Y?"
- Missing audience: "Who is the target audience?"
- Unrealistic duration: "This topic typically requires X hours. Should we narrow the scope?"
- Conflicting requirements: "You've requested both basic overview and detailed mechanisms. Which should we prioritize?"
```

## Special Request Types

### CME/Continuing Medical Education

**Indicators**:
- "CME course"
- "continuing education"
- "accredited presentation"

**Special requirements**:
- Learning objectives must be measurable
- Evidence-based content required
- Cite primary sources
- Include disclosure slides
- May need pre/post assessment

**Template**: clinical-education.md

### Conference Abstract Presentation

**Indicators**:
- "present at conference"
- "abstract accepted"
- "10-minute talk"

**Special requirements**:
- Very focused (one main finding)
- Short duration (10-15 minutes)
- Heavy on data visualization
- Conclusions front-loaded
- Minimal background

**Template**: research-presentation.md (abbreviated)

### Grand Rounds

**Indicators**:
- "grand rounds"
- "department presentation"
- "case-based"

**Special requirements**:
- Case presentation format
- Clinical reasoning emphasis
- Literature review component
- Practice implications
- Q&A time allocated

**Template**: clinical-education.md or basic-presentation.md

### Journal Club

**Indicators**:
- "journal club"
- "article discussion"
- "paper review"

**Special requirements**:
- Critical appraisal focus
- Methods detail
- Statistics explanation
- Limitations discussion
- Clinical applicability

**Template**: research-presentation.md

## Example Parsing Scenarios

### Scenario 1: Minimal Request

**Input**:
```
"Make a presentation about ketamine for depression"
```

**Parsed**:
```yaml
topic: Ketamine for depression
audience: UNKNOWN → Ask or assume general medical
duration: UNKNOWN → Assume 60 minutes
scope: UNKNOWN → Broad overview
images: UNKNOWN → Use PMC contextual
```

**Response**:
```
I'll create a presentation on ketamine for depression. Let me clarify a few things:
- Target audience: Residents, researchers, or general medical audience?
- Duration: 30, 60, or 90 minutes?
- Focus: Mechanisms, clinical protocols, or both?
```

### Scenario 2: Well-Specified Request

**Input**:
```json
{
  "general_instruction": "Create presentation for neuroscience conference",
  "topics": {
    "topic": "Ketamine",
    "subtopic": "Rapid antidepressant mechanisms"
  },
  "operational_data": {
    "hours": 0.25,
    "modality": "Synchronous"
  },
  "key_points": [
    "NMDA receptor antagonism",
    "mTOR pathway activation",
    "Synaptic plasticity changes",
    "Clinical time course"
  ]
}
```

**Parsed**:
```yaml
topic: Ketamine antidepressant mechanisms
audience: Neuroscience researchers (inferred from conference)
duration: 15 minutes (0.25 hours)
scope: Focused on mechanisms
key_sections:
  - NMDA antagonism
  - mTOR pathway
  - Synaptic plasticity
  - Time course
template: research-presentation.md
slide_count: 10-12 slides
images: Molecular pathways, clinical data
pubmed_focus: Mechanistic studies, recent reviews
```

**No questions needed** - proceed directly to creation.

### Scenario 3: Conflicting Requirements

**Input**:
```
"Create a comprehensive deep dive into the neurobiology of depression including monoamine theory, neuroplasticity, neuroinflammation, and HPA axis dysregulation. Keep it to 20 minutes for medical students."
```

**Analysis**:
```
CONFLICT: Comprehensive deep dive (90+ minutes) vs 20 minutes
CONFLICT: Deep neurobiology vs medical student level
```

**Response**:
```
This topic requires choosing between depth and breadth. For 20 minutes with medical students, I'd recommend either:

Option A: High-level overview of all four areas (5 minutes each)
Option B: Deep dive into one area (e.g., neuroplasticity)

Which approach would you prefer?
```

## JSON Schema Reference

For structured requests, this is the expected schema:

```json
{
  "general_instruction": "string (context/setting)",
  "topics": {
    "topic": "string (main subject)",
    "subtopic": "string (optional specific focus)"
  },
  "operational_data": {
    "hours": number,
    "modality": "string (Synchronous/Asynchronous)"
  },
  "key_points": ["array", "of", "strings"],
  "keywords": ["array", "of", "medical", "terms"],
  "competencies": "string (learning objectives)",
  "image_usage": {
    "instructions": ["array", "of", "image", "strategies"],
    "procedure": ["array", "of", "specific", "image", "requirements"]
  },
  "bibliography": "string (source requirements)"
}
```

All fields are optional. Minimum viable request:
```json
{
  "topics": {
    "topic": "Subject matter"
  }
}
```

## Best Practices

### For Skill Implementation

1. **Be flexible**: Handle any format gracefully
2. **Extract intelligently**: Infer obvious details
3. **Ask sparingly**: Only when truly ambiguous
4. **Confirm understanding**: Summarize parsed requirements
5. **Provide options**: When scope needs clarification

### For Users

1. **Specify audience**: Changes depth and language
2. **State duration**: Affects slide count and detail
3. **List key points**: Ensures coverage of priorities
4. **Indicate image preferences**: Especially if using custom library
5. **Mention constraints**: Special requirements, format needs

## Summary

The skill should handle requests ranging from:
- **Minimal**: "Present on X"
- **Natural**: "Create 1-hour talk on X for Y audience covering Z"
- **Structured**: Complete JSON specification

In all cases:
1. Extract what's provided
2. Infer what's reasonable
3. Ask about what's critical
4. Proceed confidently

This flexibility ensures the skill works for users with varying levels of specificity in their requests.
