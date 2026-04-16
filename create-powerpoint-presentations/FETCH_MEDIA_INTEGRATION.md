# fetch-media Integration Guide

**Last Updated**: 2025-11-19
**Status**: ✅ Fully Integrated

This document explains how the `create-powerpoint-presentations` skill integrates with the `fetch-media` skill to automatically retrieve high-quality, open-access images for presentations.

---

## Overview

The `create-powerpoint-presentations` skill now **automatically invokes** the `fetch-media` skill to download relevant images from:
- **Wikimedia Commons**: General topics, scientific concepts, nature, geography
- **NIH BioArt**: Medical, biological, health topics (scientific illustrations)
- **Unsplash**: Modern stock photography, lifestyle, technology (requires API key)

**Key Benefits**:
- ✅ No manual image searching required
- ✅ High-quality, properly licensed images
- ✅ Automatic attribution/citation handling
- ✅ Intelligent image-to-slide matching
- ✅ Multi-source fallback strategy

---

## How It Works

### 1. Image Gathering Workflow

When creating a presentation, the skill follows this multi-source strategy:

```
1. Check temp/fetch-media/ for existing images (from previous downloads)
   (Windows: $env:TEMP\fetch-media\  |  Unix: /tmp/fetch-media/)
   ↓
2. Search local working directory for images
   ↓
3. Extract key topics from presentation content
   ↓
4. Invoke fetch-media skill for each topic
   ↓
5. Download images to temp/fetch-media/
   ↓
6. Scan temp/fetch-media/ for all downloaded images
   ↓
7. Match images to slides using content scoring
   ↓
8. Generate presentation with matched images
```

### 2. Automatic Topic Extraction

The skill automatically extracts key topics from:
- Presentation title
- Section headers
- Slide content keywords
- Important technical terms

**Example**: For a presentation titled "CRISPR Gene Editing in Medicine"
```javascript
Extracted topics:
- "CRISPR Cas9 mechanism"
- "gene editing process"
- "DNA double helix"
- "genetic therapy"
```

### 3. Source Selection Logic

The skill intelligently selects the best image source based on content:

| Topic Type | Preferred Source | Reason |
|------------|------------------|--------|
| Medical/Biological | **BioArt** | Scientific illustrations, anatomical diagrams |
| Scientific concepts | **Wikimedia Commons** | Educational images, diagrams, photos |
| Nature/Geography | **Wikimedia Commons** | High-quality nature photography |
| Modern tech/Business | **Unsplash** | Contemporary stock photos (needs API key) |
| General topics | **Wikimedia Commons** | Broad coverage, reliable |

**Detection Keywords**:
- BioArt: `biolog`, `medic`, `health`, `cell`, `virus`, `bacteria`, `anatom`, `disease`, `gene`, `protein`
- Unsplash: `tech`, `startup`, `business`, `modern`, `lifestyle`
- Default: Wikimedia Commons

### 4. fetch-media Invocation

The skill uses the `Skill` tool to invoke fetch-media:

```javascript
// Example invocation for CRISPR presentation
Skill("fetch-media") with prompt:
  "Search for images about 'CRISPR Cas9 mechanism'
   Download mode, prefer BioArt source, limit 3 images"

// This downloads images to temp/fetch-media/:
// <temp>/fetch-media/bioart_123_CRISPR_Cas9_Complex.png
// <temp>/fetch-media/bioart_124_DNA_Editing_Process.png
```

### 5. Image Filename Parsing

fetch-media saves images with this format:
```
<source>_<id>_<title>.<ext>

Examples:
- wikimedia_789_Solar_Panel_Installation.jpg
- bioart_2_Tick_Nymph_Feeding_0-24_Hours.png
- unsplash_456_Sustainable_City.jpg
```

The skill parses these filenames to extract:
- **Source**: For attribution
- **ID**: For citation/reference
- **Title**: For keyword matching
- **Keywords**: For content scoring

### 6. Intelligent Image Matching

Each image is scored against slide content:

```javascript
Scoring algorithm:
- Exact keyword match: +3 points
- Partial keyword match: +1 point
- Related terms: +0.5 points

Example:
Slide: "How CRISPR Works: Cas9 Protein Mechanism"
Image: bioart_123_CRISPR_Cas9_Complex.png
Keywords: ["CRISPR", "Cas9", "Complex"]

Score calculation:
- "CRISPR" exact match: +3
- "Cas9" exact match: +3
- "mechanism" partial match with "Complex": +1
Total: 7 points (high match) → Image assigned to this slide
```

---

## When fetch-media is Invoked

### Always Invoked:
1. **Scientific/Medical presentations** (BioArt has excellent resources)
2. **When presentation topic is provided** but no local images available
3. **When user requests image-rich presentations**

### Optionally Invoked:
1. **General topic presentations** if local images are insufficient
2. **Marketing/business presentations** for stock photos (needs Unsplash API)

### Not Invoked:
1. **User explicitly provides image folder** with sufficient images
2. **User opts out of internet image retrieval**
3. **Presentation is text/data-heavy** (charts, tables only)

---

## Integration Points in SKILL.md

The fetch-media integration is documented in these sections:

1. **`<objective>`** (lines 6-10): Highlights automatic image retrieval
2. **`<quick_start>`** (lines 30-48): Step-by-step workflow with fetch-media
3. **`<workflow>` → `<phase name="content_gathering">`** (lines 85-111): Detailed image gathering process
4. **`<image_matching>`** (lines 289-408): Complete fetch-media integration workflow
5. **`<common_patterns>`** (lines 660-743): Examples with fetch-media
6. **`<validation>`** (lines 795-826): Pre/post checks for fetch-media
7. **`<success_criteria>`** (lines 828-856): Requirements for proper integration

---

## Example Use Cases

### Example 1: Scientific Presentation

**User Request**: "Create a presentation about the human immune system"

**Automatic fetch-media Invocations**:
```bash
1. Skill("fetch-media") query: "human immune system cells"
   → BioArt: Neutrophil, T-Cell, B-Cell images

2. Skill("fetch-media") query: "antibody structure"
   → BioArt: Antibody diagrams

3. Skill("fetch-media") query: "lymph node anatomy"
   → BioArt/Wikimedia: Anatomical illustrations
```

**Result**: 10-15 slide deck with 8-10 high-quality BioArt scientific illustrations automatically matched to content.

### Example 2: Business Presentation

**User Request**: "Create a pitch deck for a renewable energy startup"

**Automatic fetch-media Invocations**:
```bash
1. Skill("fetch-media") query: "solar panels installation"
   → Wikimedia: Solar panel photos

2. Skill("fetch-media") query: "wind turbine renewable energy"
   → Wikimedia: Wind farm images

3. Skill("fetch-media") query: "sustainable technology"
   → Wikimedia/Unsplash: Modern tech images
```

**Result**: Professional pitch deck with compelling imagery from open-access sources.

### Example 3: Educational Presentation

**User Request**: "Create slides about climate change effects"

**Automatic fetch-media Invocations**:
```bash
1. Skill("fetch-media") query: "arctic ice melting"
   → Wikimedia: Climate change photos

2. Skill("fetch-media") query: "coral reef bleaching"
   → Wikimedia: Environmental images

3. Skill("fetch-media") query: "forest deforestation"
   → Wikimedia: Deforestation imagery
```

**Result**: Educational presentation with impactful environmental imagery.

---

## File Paths and Locations

### fetch-media Skill Location:
```powershell
# Windows
$HOME\.claude\skills\fetch-media\SKILL.md

# Unix/macOS
~/.claude/skills/fetch-media/SKILL.md
```

### Image Download Directory:
```powershell
# Windows
$env:TEMP\fetch-media\

# Unix/macOS
/tmp/fetch-media/
```

### Example Downloaded Files:
```
<temp>/fetch-media/bioart_2_Tick_Nymph_Feeding_0-24_Hours.png
<temp>/fetch-media/bioart_447_Retro_Virus.png
<temp>/fetch-media/wikimedia_12345_Solar_Panel_Installation.jpg
<temp>/fetch-media/wikimedia_67890_DNA_Double_Helix.jpg
```

### Attribution Format:
```
BioArt images:
  NIAID Visual & Medical Arts, BioArt Source, https://bioart.niaid.nih.gov/bioart/{id}

Wikimedia images:
  {Title}, {Author/Creator}, {License}, https://commons.wikimedia.org/wiki/File:{filename}

Unsplash images:
  Photo by {Photographer} on Unsplash, https://unsplash.com/photos/{id}
```

---

## Technical Implementation Details

### 1. Checking for fetch-media Availability

Before using fetch-media, verify it's installed:

```javascript
// Cross-platform check using Node.js
const os = require('os');
const path = require('path');
const fs = require('fs');

const skillPath = path.join(os.homedir(), '.claude', 'skills', 'fetch-media', 'SKILL.md');
const fetchMediaAvailable = fs.existsSync(skillPath);

// If found: fetch-media available
// If not found: Skip fetch-media, use local images only
```

### 2. Scanning temp/fetch-media/ (Cross-Platform)

```javascript
// Cross-platform directory scanning
const os = require('os');
const path = require('path');

const fetchMediaDir = path.join(os.tmpdir(), 'fetch-media');
// Use Glob with platform-appropriate path

// Returns array of file paths:
[
  "<temp>/fetch-media/bioart_2_Tick_Nymph_Feeding_0-24_Hours.png",
  "<temp>/fetch-media/bioart_447_Retro_Virus.png",
  "<temp>/fetch-media/wikimedia_12345_Solar_Panel.jpg"
]
```

### 3. Parsing Filenames

```javascript
const path = require('path');

function parseFetchMediaFilename(filePath) {
  const basename = path.basename(filePath);  // Cross-platform
  const match = basename.match(/^(wikimedia|bioart|unsplash)_(\d+)_(.+)\.(png|jpg|jpeg|gif|svg)$/);

  if (match) {
    const [, source, id, titleSlug, ext] = match;
    return {
      source,
      id,
      title: titleSlug.replace(/_/g, ' '),
      keywords: titleSlug.toLowerCase().split('_'),
      path,
      ext
    };
  }

  return null;
}

// Example:
parseFetchMediaFilename("<temp>/fetch-media/bioart_447_Retro_Virus.png")
// Returns:
{
  source: "bioart",
  id: "447",
  title: "Retro Virus",
  keywords: ["retro", "virus"],
  path: "<temp>/fetch-media/bioart_447_Retro_Virus.png",
  ext: "png"
}
```

### 4. Adding Images to Slides (PptxGenJS)

```javascript
// After matching images to slides (cross-platform path)
const os = require('os');
const path = require('path');
const imagePath = path.join(os.tmpdir(), 'fetch-media', 'bioart_447_Retro_Virus.png');

slide.addImage({
  path: imagePath,
  x: 1,
  y: 2,
  w: 4,
  h: 3,
  altText: 'Retro Virus illustration from NIH BioArt'
});

// Add attribution in speaker notes
slide.addNotes('Image: Retro Virus, NIAID BioArt, https://bioart.niaid.nih.gov/bioart/447');
```

---

## Query Strategies

### Good fetch-media Queries:
- ✅ "CRISPR Cas9 mechanism" (specific, technical)
- ✅ "solar panel installation" (descriptive, focused)
- ✅ "human immune system cells" (clear, educational)
- ✅ "DNA double helix structure" (precise)

### Poor fetch-media Queries:
- ❌ "biology" (too broad)
- ❌ "science stuff" (vague)
- ❌ "pictures of things" (unclear)
- ❌ "a b c" (too short)

### Query Optimization Tips:
1. **Use 2-4 words** for specificity
2. **Include technical terms** for scientific topics
3. **Add descriptive adjectives** for clarity
4. **Avoid stop words** ("the", "a", "of")
5. **Use domain-specific vocabulary**

---

## Troubleshooting

### Issue 1: No images downloaded from fetch-media

**Possible Causes**:
- BioArt index not built (for BioArt queries)
- Network connectivity issues
- Query too specific/no matches found

**Solutions**:
- Build BioArt index:
  - Windows: `cd $HOME\.claude\skills\fetch-media; python scripts\bioart_crawler.py --mode full`
  - Unix: `cd ~/.claude/skills/fetch-media && python3 scripts/bioart_crawler.py --mode full`
- Check network connection
- Try broader queries
- Use Wikimedia Commons as fallback

### Issue 2: Images not matching slides well

**Possible Causes**:
- Query terms don't match slide content
- Filenames lack descriptive keywords
- Scoring threshold too high

**Solutions**:
- Adjust queries to match slide keywords
- Use multiple queries per topic
- Lower matching score threshold
- Manually specify image-to-slide mapping

### Issue 3: temp/fetch-media/ images not found

**Possible Causes**:
- Temp directory cleaned by OS
- Incorrect Glob pattern
- fetch-media download failed

**Solutions**:
- Re-invoke fetch-media to re-download
- Verify Glob pattern uses correct temp directory:
  - Windows: `$env:TEMP\fetch-media\**\*.{png,jpg,jpeg,gif,svg}`
  - Unix: `/tmp/fetch-media/**/*.{png,jpg,jpeg,gif,svg}`
- Check fetch-media skill output for errors

---

## Best Practices

### 1. Image Quality
- Prefer **BioArt** for scientific presentations (high-quality illustrations)
- Use **Wikimedia Commons** for educational content (reliable, well-documented)
- Reserve **Unsplash** for modern marketing presentations

### 2. Attribution
- Always include attributions in speaker notes or final slide
- Use fetch-media's provided attribution strings
- Link back to original sources

### 3. Performance
- Limit fetch-media queries to 3-5 per presentation (avoid over-fetching)
- Check temp/fetch-media/ before invoking fetch-media (reuse existing)
- Use `limit` parameter to control download count

### 4. Content Matching
- Extract clear, specific keywords from slides
- Use scoring threshold of 5+ for good matches
- Manually review critical slides (title, conclusion)

---

## Future Enhancements

Potential improvements to the integration:

1. **Caching Strategy**: Cache fetch-media results per presentation topic
2. **Smart Retry**: Retry failed fetch-media queries with broader terms
3. **User Preferences**: Allow users to specify preferred sources
4. **Batch Downloads**: Invoke fetch-media once with multiple queries
5. **Image Quality Filtering**: Prefer high-resolution images (>1200px)
6. **Duplicate Detection**: Avoid downloading duplicate images

---

## Testing the Integration

To test the fetch-media integration:

```powershell
# Test 1: Scientific presentation
# Prompt: "Create a presentation about CRISPR gene editing"
# Expected: fetch-media invoked for BioArt images

# Test 2: Business presentation
# Prompt: "Create a pitch deck for renewable energy startup"
# Expected: fetch-media invoked for Wikimedia/Unsplash images

# Test 3: With existing images
# First, download some images
# Windows:
cd $HOME\.claude\skills\fetch-media
python scripts\search_media.py --query "solar energy" --mode download --limit 5

# Unix/macOS:
cd ~/.claude/skills/fetch-media
python3 scripts/search_media.py --query "solar energy" --mode download --limit 5

# Then create presentation
# Prompt: "Create slides about solar energy"
# Expected: Uses images from temp/fetch-media/ without re-downloading
```

---

## Conclusion

The fetch-media integration makes `create-powerpoint-presentations` a **fully autonomous presentation creator** that:
- ✅ Automatically sources high-quality images
- ✅ Intelligently matches images to content
- ✅ Handles attribution and licensing
- ✅ Supports multiple image sources
- ✅ Requires zero manual image searching

This integration is **production-ready** and follows best practices for skill composition in Claude Code.

---

**Questions?** See:
- `$HOME/.claude/skills/fetch-media/SKILL.md` for fetch-media documentation
- `$HOME/.claude/skills/create-powerpoint-presentations/SKILL.md` for presentation skill documentation
