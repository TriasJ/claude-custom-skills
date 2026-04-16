# XML Conversion Guide for Reference Files

## Overview

This guide shows how to convert reference files from markdown headings to pure XML structure, following the best practices established in the SKILL.md conversion.

## Conversion Pattern

### Rule: Remove All Markdown Headings

**Before** (Markdown headings):
```markdown
# Main Title

## Section Name

### Subsection Name

Content here...

### Another Subsection

More content...
```

**After** (Pure XML):
```markdown
# Main Title

<section_name>
<subsection_name>
Content here...
</subsection_name>

<another_subsection>
More content...
</another_subsection>
</section_name>
```

### Key Principles

1. **Keep the H1 title** (`# Main Title`) - This helps with file identification
2. **Convert ## headings to XML tags** - Use semantic names
3. **Convert ### headings to nested XML tags** - Proper hierarchy
4. **Use underscores for multi-word tags** - e.g., `<image_sourcing>` not `<image sourcing>`
5. **Close all tags properly** - Every `<tag>` needs `</tag>`
6. **Keep markdown formatting within content** - Bold, italic, lists, code blocks all stay

## Semantic Tag Naming

Choose meaningful tag names based on content function:

| Content Type | Good Tag Name | Avoid |
|--------------|---------------|-------|
| Step-by-step process | `<workflow>`, `<process>` | `<steps>` |
| Configuration info | `<configuration>`, `<setup>` | `<config>` |
| Examples | `<examples>`, `<use_cases>` | `<ex>` |
| Best practices | `<best_practices>`, `<guidelines>` | `<tips>` |
| Common issues | `<troubleshooting>`, `<common_issues>` | `<problems>` |
| Technical details | `<technical_details>`, `<specifications>` | `<tech>` |

## Conversion Examples

### Example 1: Simple Section

**Before**:
```markdown
## Quick Start

Follow these steps to get started:
1. Install dependencies
2. Configure settings
3. Run the script
```

**After**:
```markdown
<quick_start>
Follow these steps to get started:
1. Install dependencies
2. Configure settings
3. Run the script
</quick_start>
```

### Example 2: Nested Sections

**Before**:
```markdown
## Image Sourcing

### Option A: Contextual Search

Use the contextual fetcher for best results.

### Option B: Keyword Search

Use simple keyword matching when needed.
```

**After**:
```markdown
<image_sourcing>
<option_a_contextual>
Use the contextual fetcher for best results.
</option_a_contextual>

<option_b_keyword>
Use simple keyword matching when needed.
</option_b_keyword>
</image_sourcing>
```

### Example 3: Multiple Nested Levels

**Before**:
```markdown
## Configuration

### Basic Setup

#### Required Fields

These fields are mandatory:
- Field 1
- Field 2

#### Optional Fields

These fields are optional:
- Field 3
- Field 4

### Advanced Setup

More complex configuration...
```

**After**:
```markdown
<configuration>
<basic_setup>
<required_fields>
These fields are mandatory:
- Field 1
- Field 2
</required_fields>

<optional_fields>
These fields are optional:
- Field 3
- Field 4
</optional_fields>
</basic_setup>

<advanced_setup>
More complex configuration...
</advanced_setup>
</configuration>
```

### Example 4: Preserving Code and Lists

**Before**:
```markdown
## Usage Examples

### Python Script

Run the script like this:

```bash
python script.py --arg value
```

### Common Options

- `--help`: Show help
- `--verbose`: Enable verbose output
```

**After**:
```markdown
<usage_examples>
<python_script>
Run the script like this:

```bash
python script.py --arg value
```
</python_script>

<common_options>
- `--help`: Show help
- `--verbose`: Enable verbose output
</common_options>
</usage_examples>
```

## Files Needing Conversion

### 1. openi-advanced-search.md (505 lines)

**Current structure** (first 100 lines):
```
# Advanced Open-i Biomedical Image Search
## Overview
## What is Open-i?
## Enhanced Features
## Usage
### Basic Search
### Search with Modality Filter
```

**Suggested XML structure**:
```xml
<overview>...</overview>
<what_is_openi>...</what_is_openi>
<enhanced_features>...</enhanced_features>
<usage>
  <basic_search>...</basic_search>
  <modality_filter>...</modality_filter>
  <multiple_filters>...</multiple_filters>
</usage>
<available_filters>...</available_filters>
```

### 2. contextual-image-retrieval.md (412 lines)

**Suggested XML structure**:
```xml
<overview>...</overview>
<problem_with_keywords>...</problem_with_keywords>
<solution_contextual_matching>...</solution_contextual_matching>
<how_it_works>
  <step_1_define>...</step_1_define>
  <step_2_search>...</step_2_search>
  <step_3_extract>...</step_3_extract>
</how_it_works>
<usage_in_skill>...</usage_in_skill>
<advantages>...</advantages>
<best_practices>...</best_practices>
```

### 3. troubleshooting.md (314 lines)

**Suggested XML structure**:
```xml
<common_issues>
  <images_not_displaying>
    <symptom>...</symptom>
    <solutions>...</solutions>
  </images_not_displaying>
  <citations_missing>...</citations_missing>
  <theme_not_applying>...</theme_not_applying>
</common_issues>
<getting_help>...</getting_help>
```

### 4. template-guide.md (453 lines)

**Suggested XML structure**:
```xml
<overview>...</overview>
<available_templates>
  <basic_presentation>...</basic_presentation>
  <research_presentation>...</research_presentation>
  <clinical_education>...</clinical_education>
</available_templates>
<how_to_use>...</how_to_use>
<customization>...</customization>
<best_practices>...</best_practices>
```

### 5. request-formats.md (485 lines)

**Suggested XML structure**:
```xml
<overview>...</overview>
<format_types>
  <natural_language>...</natural_language>
  <structured_json>...</structured_json>
  <minimal_format>...</minimal_format>
</format_types>
<parsing_workflow>...</parsing_workflow>
<special_request_types>...</special_request_types>
<examples>...</examples>
```

### 6. advanced-features.md (782 lines)

**Suggested XML structure**:
```xml
<overview>...</overview>
<custom_slide_classes>...</custom_slide_classes>
<background_images>...</background_images>
<speaker_notes>...</speaker_notes>
<pagination_footers>...</pagination_footers>
<advanced_layouts>...</advanced_layouts>
<image_techniques>...</image_techniques>
<best_practices>...</best_practices>
```

## Step-by-Step Conversion Process

### Step 1: Read the File
```bash
# Open the file in your editor
code /home/eleonora/.claude/skills/biomedical-marp-presentations/references/openi-advanced-search.md
```

### Step 2: Identify Structure
- Note all `##` headings (main sections)
- Note all `###` headings (subsections)
- Plan the XML tag hierarchy

### Step 3: Convert Headings
- Replace each `##` heading with `<semantic_tag_name>`
- Add closing `</semantic_tag_name>` before next section
- Nest `###` tags inside their parent `##` tags

### Step 4: Verify Structure
- Ensure all tags are properly closed
- Check nesting is logical
- Verify no markdown headings remain (except H1)

### Step 5: Test
- The file should still be readable
- Code blocks should remain intact
- Lists should remain intact
- Only structural headings replaced with XML

## Quick Conversion Checklist

For each reference file:

- [ ] Keep H1 title (`# Title`)
- [ ] Convert all `##` to `<semantic_tag>`
- [ ] Convert all `###` to nested `<tags>`
- [ ] Use underscores in multi-word tags
- [ ] Close all tags properly
- [ ] Preserve markdown formatting (bold, italic, lists, code)
- [ ] Remove any remaining `##` or `###` headings
- [ ] Verify proper XML nesting

## Validation

After conversion, check:

1. **No markdown headings in body** (except H1)
   ```bash
   grep "^##" filename.md
   # Should return nothing (or only show in code blocks)
   ```

2. **Balanced XML tags**
   - Every `<tag>` has matching `</tag>`
   - Proper nesting (no overlapping tags)

3. **Readability preserved**
   - Content still makes sense
   - Code examples intact
   - Lists and formatting preserved

## Benefits of XML Structure

After conversion, reference files will have:

✅ **Consistent parsing** - Claude reliably understands section boundaries
✅ **Clear hierarchy** - Nesting shows relationships
✅ **Semantic meaning** - Tag names indicate content purpose
✅ **Token efficiency** - More efficient for LLM processing
✅ **Unambiguous structure** - No confusion about sections

## Example: Complete File Conversion

**Before** (troubleshooting.md excerpt):
```markdown
# Troubleshooting Guide

## Common Issues and Solutions

### Images Not Displaying

**Symptom**: Images don't appear in the rendered presentation

**Causes and Solutions**:
- Path mismatch: Verify exact path from JSON
- File extension error: Check extensions are correct
```

**After**:
```markdown
# Troubleshooting Guide

<common_issues>
<images_not_displaying>
<symptom>
Images don't appear in the rendered presentation
</symptom>

<solutions>
- Path mismatch: Verify exact path from JSON
- File extension error: Check extensions are correct
</solutions>
</images_not_displaying>
</common_issues>
```

## Tools for Conversion

You can use Claude Code to convert each file:

```prompt
Convert the file references/openi-advanced-search.md to pure XML structure:
1. Keep the H1 title
2. Replace all ## headings with semantic XML tags
3. Replace all ### headings with nested XML tags
4. Close all tags properly
5. Preserve all markdown formatting within content
6. Use underscore_case for multi-word tag names
```

Or manually edit following the patterns shown above.

## Final Note

The SKILL.md scored 87/100 after XML conversion (up from 37/100). Converting these reference files will bring the entire skill to best-practice compliance with consistent, unambiguous structure throughout.
