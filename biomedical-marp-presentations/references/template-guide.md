# Template Usage Guide

## Overview

Templates provide starting structures for different types of biomedical presentations. All templates are located in `assets/templates/` and use MARP syntax with pre-configured themes and layouts.

## Available Templates

### 1. Basic Presentation (`basic-presentation.md`)

**Use for**:
- General biomedical topics
- Broad audience presentations
- Standard format talks
- 30-60 minute presentations

**Features**:
- Clean, professional design
- Balanced text-to-image ratio
- General medical audience assumptions
- Default biomedical theme

**Structure**:
```
- Title slide
- Learning objectives
- Introduction (3-5 slides)
- Main content (20-30 slides)
- Summary (1-2 slides)
- References (1-2 slides)
```

**Best for**: Department seminars, grand rounds, educational talks

### 2. Research Presentation (`research-presentation.md`)

**Use for**:
- Academic research presentations
- Conference talks
- Research seminars
- Lab meetings

**Features**:
- Research-focused layout
- Dark, sophisticated design (research-seminar.css theme)
- Emphasis on data visualization
- Methods and results sections
- Statistical presentation formatting

**Structure**:
```
- Title slide (with authors and affiliations)
- Background and rationale
- Research question/hypothesis
- Methods
- Results (multiple slides with figures)
- Discussion
- Limitations
- Conclusions
- Acknowledgments
- References
```

**Best for**: Scientific conferences, thesis defenses, research group meetings

### 3. Clinical Education (`clinical-education.md`)

**Use for**:
- Medical training
- Residency education
- CME courses
- Clinical case presentations

**Features**:
- Clinical education theme
- Patient-centered focus
- Clinical decision-making emphasis
- Case-based learning structure
- Practice-oriented content

**Structure**:
```
- Title slide
- Learning objectives (competency-based)
- Clinical context
- Pathophysiology
- Clinical presentation
- Diagnostic approach
- Treatment algorithms
- Clinical pearls
- Case studies
- Summary and takeaways
- References
```

**Best for**: Resident training, CME courses, clinical teaching rounds

## How to Use Templates

### Step 1: Choose Appropriate Template

**Decision matrix**:

| If your presentation is... | Use template... |
|---------------------------|----------------|
| For medical students or general audience | basic-presentation.md |
| Original research findings | research-presentation.md |
| Training residents/fellows | clinical-education.md |
| Conference abstract presentation | research-presentation.md |
| Grand rounds | basic-presentation.md or clinical-education.md |
| Journal club | research-presentation.md |

### Step 2: Copy Template Structure

Templates provide:
- YAML frontmatter configuration
- Slide type examples
- Layout patterns
- Citation formatting
- Section organization

**Do not**:
- Copy templates verbatim without customization
- Keep placeholder content
- Use template examples as actual content

**Do**:
- Use structure as guide
- Adapt layouts to your content
- Maintain formatting patterns
- Keep theme consistency

### Step 3: Customize Content

**Replace**:
- Title and author information
- Learning objectives
- All slide content
- Image sources and captions
- References

**Maintain**:
- Slide type ratios (70% concise, 30% explanatory)
- Citation format
- Image sizing conventions
- Layout patterns
- Theme directives

### Step 4: Verify Theme Application

Each template references a specific theme:

```yaml
# basic-presentation.md
theme: ./assets/themes/default-biomedical.css

# research-presentation.md
theme: ./assets/themes/research-seminar.css

# clinical-education.md
theme: ./assets/themes/clinical-education.css
```

**Path adjustment**: If your presentation file is in a different location, adjust the relative path:

```yaml
# If presentation is in outputs/
theme: ../assets/themes/default-biomedical.css

# If presentation is in skill root
theme: ./assets/themes/default-biomedical.css
```

## Template Customization

### Changing Themes

All themes work with all templates. To change:

```yaml
---
# Original
theme: ./assets/themes/default-biomedical.css

# Change to dark theme
theme: ./assets/themes/dark-scientific.css
---
```

**Theme characteristics**:
- **default-biomedical.css**: Professional, blue accents, high contrast
- **clinical-education.css**: Warm tones, education-focused, readable
- **research-seminar.css**: Dark background, sophisticated, data-focused
- **dark-scientific.css**: Modern dark theme, vibrant accents, tech-forward

### Adding Sections

Templates are starting points. Add sections as needed:

```markdown
<!-- After introduction, before main content -->

---

# Additional Section

Content here

---
```

### Removing Sections

Not all presentations need all sections:

```markdown
<!-- Can remove if not applicable -->
<!-- # Limitations -->
<!-- # Future Directions -->
```

### Adjusting Slide Counts

**For shorter presentations (30 minutes)**:
- Title (1)
- Objectives (1)
- Introduction (2-3)
- Main content (10-15)
- Summary (1)
- References (1)
Total: ~20 slides

**For longer presentations (90 minutes)**:
- Title (1)
- Objectives (1-2)
- Introduction (5-7)
- Main content (40-50)
- Clinical applications (3-5)
- Summary (2-3)
- References (1-2)
Total: ~60 slides

## Layout Patterns in Templates

### Two-Column Comparisons

```markdown
<div class="columns">
<div>

**Option A**
- Feature 1
- Feature 2

</div>
<div>

**Option B**
- Feature 1
- Feature 2

</div>
</div>
```

### Text + Image Layout

```markdown
<div class="columns">
<div>

# Key Points

- Point 1
- Point 2
- Point 3

</div>
<div>

![w:500px](image.jpg)

</div>
</div>
```

### Full-Width Image with Caption

```markdown
# Slide Title

![w:800px](image.jpg)

<div style="font-size: 16px; text-align: center; color: #666; margin-top: 10px;">

**Figure 1**. Descriptive caption here.
*Source*: Author et al. Journal. 2024.<sup>1</sup>

</div>
```

### Explanatory Slide

```markdown
<!-- _class: explanatory -->

# Deep Dive: Topic Name

First paragraph with detailed explanation of mechanism, theory, or concept...

Second paragraph providing clinical context, evidence, and practical implications...

**Key Takeaway**: One-sentence summary of the essential point.

<div style="font-size: 16px; color: #666; margin-top: 30px;">

**References**: 3. Author et al. Journal. 2024.

</div>
```

## Template Best Practices

### 1. Maintain Consistency

Once you choose a template structure:
- Keep the same section naming
- Use consistent formatting
- Maintain image sizing standards
- Follow citation patterns

### 2. Adapt, Don't Copy

Templates show *how* to structure content, not *what* content to include:
- Replace all placeholder content
- Customize for your specific topic
- Adjust depth based on audience
- Add domain-specific sections

### 3. Preserve Layout Patterns

Templates demonstrate effective layouts:
- Two-column for comparisons
- Full-width for impactful images
- Explanatory slides for complex topics
- Bullet lists for key points

Use these patterns consistently throughout your presentation.

### 4. Reference Template Files

When creating presentations, refer to templates for:
- YAML frontmatter syntax
- Slide directive usage (`<!-- _class: -->`)
- Image sizing conventions
- Caption formatting
- Citation placement

## Creating Custom Templates

To create a new template:

### 1. Start with Existing Template

Copy the template that most closely matches your needs:

```bash
cp assets/templates/basic-presentation.md assets/templates/my-custom-template.md
```

### 2. Define Purpose

Document what makes this template unique:
- Target audience
- Use cases
- Special features
- Required sections

### 3. Customize Structure

Modify:
- Section order
- Slide types
- Layout patterns
- Theme selection

### 4. Add Template Header

Include usage instructions at the top:

```markdown
<!--
Template: Custom Template Name
Purpose: Specific use case
Audience: Target audience
Duration: Recommended length
Theme: Recommended theme
-->
```

### 5. Document in This Guide

Add your template to the "Available Templates" section above with:
- Name and filename
- Use cases
- Key features
- Best practices

## Template File Locations

```
assets/templates/
├── basic-presentation.md       # General biomedical presentations
├── research-presentation.md    # Research and academic talks
└── clinical-education.md       # Medical training and education
```

## Integration with Skill Workflow

When creating presentations with this skill:

1. **Skill selects template** based on user's request:
   - Request mentions "research" → research-presentation.md
   - Request mentions "residents" or "training" → clinical-education.md
   - General request → basic-presentation.md

2. **Extract structure** from template:
   - Section organization
   - Slide count guidelines
   - Layout patterns

3. **Populate with content**:
   - Replace placeholders with actual content
   - Add PubMed-cited information
   - Insert contextually-matched images
   - Format citations

4. **Maintain template conventions**:
   - Keep slide type ratios
   - Use template layouts
   - Follow formatting patterns

## Summary

Templates accelerate presentation creation while maintaining quality:

- **Choose** the appropriate template for your presentation type
- **Copy** the structure and formatting patterns
- **Customize** all content for your specific topic
- **Maintain** consistency with template conventions
- **Adapt** layouts and sections as needed for your content

Templates are guides, not constraints. Use them to ensure professional structure while adapting content to your unique needs.
