# image-generation Integration Guide

**Last Updated**: 2025-12-15
**Status**: Fully Integrated

This document explains how the `create-powerpoint-presentations` skill integrates with the `image-generation` skill to create custom AI-generated images for presentations using Google Gemini.

---

## Overview

The `create-powerpoint-presentations` skill can **optionally invoke** the `image-generation` skill to generate custom images using Google's Gemini API when:
- Stock images from fetch-media don't meet specific needs
- User needs custom logos, branding, or unique artwork
- Specific artistic styles are required (kawaii, isometric, minimalist, etc.)
- Abstract concepts need visual representation

**Key Benefits**:
- Custom logos and branding elements on-demand
- Unique illustrations matching exact presentation themes
- Style-specific artwork (photorealistic, illustration, kawaii, etc.)
- Text rendering in images (Gemini excels at this)
- No copyright concerns for generated images

---

## Prerequisites

### Required for AI Image Generation

1. **GEMINI_API_KEY environment variable**:
   ```powershell
   # Windows PowerShell
   $env:GEMINI_API_KEY = "your_key_here"
   ```
   ```bash
   # Unix/macOS
   export GEMINI_API_KEY=your_key_here
   ```
   Get your key from: https://aistudio.google.com/apikey

2. **image-generation skill installed**:
   ```powershell
   # Windows
   $HOME\.claude\skills\image-generation\SKILL.md

   # Unix/macOS
   ~/.claude/skills/image-generation/SKILL.md
   ```

3. **Python dependencies**:
   ```powershell
   pip install google-genai Pillow
   ```

### Checking Availability

```powershell
# Windows PowerShell
Test-Path "$HOME\.claude\skills\image-generation\SKILL.md"
$env:GEMINI_API_KEY
```
```bash
# Unix/macOS
ls ~/.claude/skills/image-generation/SKILL.md
echo $GEMINI_API_KEY
```

---

## How It Works

### 1. Decision Flow: Stock vs AI-Generated Images

```
Presentation Content Analysis
           │
           ▼
┌─────────────────────────────────────────┐
│  Does slide need custom imagery?        │
│  - Custom logo/branding?                │
│  - Unique concept not in stock?         │
│  - Specific artistic style?             │
│  - Text in image required?              │
└─────────────────────────────────────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
   YES           NO
    │             │
    ▼             ▼
image-generation  fetch-media
(AI custom)      (stock images)
    │             │
    ▼             ▼
temp/generated-   temp/fetch-media/
images/
    │             │
    └──────┬──────┘
           ▼
   Match to slides
           │
           ▼
   Generate presentation
```

### 2. When to Use image-generation vs fetch-media

| Use Case | Recommended Source | Reason |
|----------|-------------------|--------|
| Scientific diagrams | fetch-media (BioArt) | High-quality scientific illustrations |
| Stock photography | fetch-media (Wikimedia/Unsplash) | Real-world images |
| Custom logo | **image-generation** | Unique branding |
| Abstract concepts | **image-generation** | No stock equivalent |
| Specific text in image | **image-generation** | Gemini handles text well |
| Kawaii/artistic style | **image-generation** | Style-specific generation |
| Nature photography | fetch-media | Real photos better |
| Future/imaginary scenes | **image-generation** | Doesn't exist in stock |

### 3. Image Generation Workflow

```javascript
// Step 1: Identify slides needing custom images
const slidesNeedingCustomImages = slides.filter(slide =>
  slide.needsLogo ||
  slide.needsCustomGraphic ||
  slide.type === 'title' && !matchedStockImage ||
  slide.visualConcept && !stockImageMatch
);

// Step 2: Generate prompts based on slide content
function generateImagePrompt(slide, template) {
  const baseStyle = template.style;
  const colors = template.colors;

  let prompt = `${slide.visualConcept || slide.title}`;

  // Add style guidance
  if (slide.needsLogo) {
    prompt += `, clean modern logo design, white background`;
  } else {
    prompt += `, ${baseStyle} style illustration`;
  }

  // Add color matching
  prompt += `, colors matching ${colors.primary}`;

  // Add aspect ratio
  prompt += `, 16:9 aspect ratio for presentation`;

  return prompt;
}

// Step 3: Invoke image-generation skill
// Skill("image-generation") with the generated prompt
// Image saved to temp/generated-images/ (cross-platform)

// Step 4: Load generated images (cross-platform)
function loadGeneratedImages() {
  const os = require('os');
  const path = require('path');
  const generatedDir = path.join(os.tmpdir(), 'generated-images');
  // Glob with platform-appropriate path
  return generatedFiles.map(parseGeneratedFilename);
}
```

---

## Prompt Strategies

### Logo Generation

```
Clean modern logo with text 'CompanyName', [icon type],
[color palette], white background, minimalist style
```

**Examples**:
- "Clean modern logo with text 'TechCorp', circuit board icon, blue gradient, white background, minimalist"
- "Elegant logo with text 'Bloom Wellness', leaf icon, green and gold, transparent background"

### Illustrations

```
[Style] illustration of [subject], [visual details],
[color palette], [mood/atmosphere]
```

**Examples**:
- "Isometric illustration of smart city with solar panels, soft pastel colors, clean lines"
- "Flat design illustration of team collaboration, diverse characters, corporate blue palette"

### Abstract/Conceptual

```
Abstract representation of [concept], [visual metaphor],
[color scheme], [style keywords]
```

**Examples**:
- "Abstract representation of data flow, flowing blue particles, dark background, futuristic"
- "Visual metaphor for innovation, lightbulb with gears, gradient purple to orange"

### Style-Specific Art

| Style | Prompt Keywords |
|-------|----------------|
| Kawaii | "kawaii style, cute, pastel colors, simple shapes, friendly faces" |
| Isometric | "isometric view, 3D illustration, clean lines, soft shadows" |
| Minimalist | "minimalist, simple shapes, limited color palette, clean design" |
| Photorealistic | "photorealistic, detailed, natural lighting, high resolution" |
| Flat Design | "flat design, bold colors, no gradients, simple shapes" |
| Watercolor | "watercolor style, soft edges, blended colors, artistic" |

---

## File Management

### Generated Image Location

```powershell
# Windows: $env:TEMP\generated-images\
# Unix/macOS: /tmp/generated-images/

<temp>/generated-images/
├── generated_1702656000_company_logo.png
├── generated_1702656001_workflow_illustration.png
├── generated_1702656002_abstract_data_flow.png
└── generated_1702656003_team_mascot.png
```

### Filename Format

```
generated_<unix_timestamp>_<prompt_slug>.png
```

- **timestamp**: Unix timestamp of generation
- **prompt_slug**: Sanitized version of the prompt (underscores, lowercase)

### Parsing Filenames

```javascript
function parseGeneratedFilename(filePath) {
  const basename = path.basename(filePath);
  const match = basename.match(/^generated_(\d+)_(.+)\.(png|jpg|jpeg)$/);

  if (match) {
    const [, timestamp, promptSlug, ext] = match;
    return {
      path: filePath,
      source: 'ai-generated',
      timestamp: parseInt(timestamp),
      title: promptSlug.replace(/_/g, ' '),
      keywords: promptSlug.toLowerCase().split('_'),
      type: 'content'
    };
  }
  return null;
}
```

---

## Integration with fetch-media

The image-generation skill works alongside fetch-media in a **complementary** manner:

### Combined Workflow

```javascript
const os = require('os');
const path = require('path');

async function gatherAllImages(presentationContent) {
  const images = [];
  const tempDir = os.tmpdir();  // Cross-platform temp directory

  // 1. Check existing fetch-media downloads
  const fetchMediaDir = path.join(tempDir, 'fetch-media');
  const existingStockImages = await glob(path.join(fetchMediaDir, '**/*.{png,jpg,jpeg,gif,svg}'));
  images.push(...existingStockImages.map(parseFetchMediaFilename));

  // 2. Check existing AI-generated images
  const generatedDir = path.join(tempDir, 'generated-images');
  const existingGeneratedImages = await glob(path.join(generatedDir, '**/*.{png,jpg,jpeg}'));
  images.push(...existingGeneratedImages.map(parseGeneratedFilename));

  // 3. Analyze which slides need images
  const slidesNeedingImages = analyzeImageNeeds(presentationContent, images);

  // 4. For slides needing stock photos
  for (const slide of slidesNeedingImages.filter(s => s.needsStockPhoto)) {
    // Invoke fetch-media skill
    await invokeFetchMedia(slide.topic);
  }

  // 5. For slides needing custom images (if GEMINI_API_KEY available)
  if (process.env.GEMINI_API_KEY) {
    for (const slide of slidesNeedingImages.filter(s => s.needsCustomImage)) {
      // Invoke image-generation skill
      await invokeImageGeneration(slide.prompt);
    }
  }

  // 6. Re-scan directories for new images
  const allImages = await gatherAllImagesFromDirectories();

  // 7. Match images to slides
  return matchImagesToSlides(presentationContent.slides, allImages);
}
```

### Priority Order for Image Sources

1. **User-provided images** (local directory)
2. **Previously downloaded stock images** (temp/fetch-media/)
3. **Previously generated AI images** (temp/generated-images/)
4. **New fetch-media downloads** (for stock photo needs)
5. **New AI generations** (for custom image needs)

---

## Example Use Cases

### Example 1: Branded Startup Pitch

**Request**: "Create a pitch deck for 'GreenLeaf Technologies' renewable energy startup"

**image-generation Invocations**:
```
1. Logo: "Clean modern logo with text 'GreenLeaf Technologies',
   leaf with solar panel design, green gradient, white background"

2. Hero image: "Isometric illustration of sustainable smart city,
   solar panels, wind turbines, green spaces, soft colors"
```

**fetch-media Invocations**:
```
1. "solar panel installation residential"
2. "wind turbine farm"
3. "renewable energy statistics graph"
```

**Result**: Professional pitch deck with custom logo and hero image + relevant stock photos.

### Example 2: Fun Company Culture Presentation

**Request**: "Create a playful presentation about our team culture in kawaii style"

**image-generation Invocations**:
```
1. Mascot: "Kawaii style mascot, friendly smiling laptop character,
   pastel blue, simple eyes, waving"

2. Values slide: "Kawaii style illustration of teamwork, cute characters
   holding hands in circle, pastel rainbow colors"

3. Work-life balance: "Kawaii style coffee cup and plant, cute faces,
   cozy office desk, pastel pink and green"
```

**Result**: Visually cohesive presentation with consistent kawaii art style throughout.

### Example 3: Technical Product Demo

**Request**: "Create slides for our AI-powered analytics platform"

**image-generation Invocations**:
```
1. Logo: "Minimalist logo with text 'DataFlow AI', flowing data streams icon,
   blue and purple gradient, white background"

2. Architecture diagram: "Abstract representation of AI pipeline,
   connected nodes, data flowing, dark background with neon blue accents"
```

**fetch-media Invocations**:
```
1. "data analytics dashboard"
2. "machine learning neural network"
3. "cloud computing infrastructure"
```

**Result**: Tech-focused presentation with custom branding and stock technical imagery.

---

## Best Practices

### 1. Prompt Quality

- **Be specific**: Include colors, style, mood, composition
- **Match template**: Reference template colors in prompts
- **Specify aspect ratio**: Use "16:9" for slide backgrounds, "1:1" for icons
- **Include text carefully**: Gemini handles text well, but keep it short

### 2. Image Consistency

- Use consistent style keywords across all prompts
- Reference the same color palette
- Maintain visual coherence with stock images

### 3. Performance

- Limit AI generations to 3-5 per presentation (API calls take time)
- Use cached images when available
- Batch similar style generations together

### 4. Fallback Strategy

- Always have fetch-media as backup
- If AI generation fails, use stock alternatives
- Don't block presentation creation on AI failures

---

## Troubleshooting

### Issue 1: GEMINI_API_KEY not set

**Symptoms**: AI image generation skipped, only stock images used

**Solution**:
```bash
export GEMINI_API_KEY=your_api_key_here
```

### Issue 2: Rate limiting

**Symptoms**: "Rate limit exceeded" errors

**Solution**:
- Wait 60 seconds between requests
- Reduce number of generated images
- Use fetch-media for some images instead

### Issue 3: Image quality issues

**Symptoms**: Generated images don't match expectations

**Solution**:
- Refine prompts with more specific details
- Add style keywords (photorealistic, illustration, etc.)
- Specify aspect ratio explicitly

### Issue 4: temp/generated-images/ not found

**Symptoms**: Generated images not saved

**Solution**:
```powershell
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "$env:TEMP\generated-images"
```
```bash
# Unix/macOS
mkdir -p /tmp/generated-images
```

---

## Comparison: fetch-media vs image-generation

| Aspect | fetch-media | image-generation |
|--------|-------------|------------------|
| Source | Stock libraries (Wikimedia, BioArt, Unsplash) | AI-generated (Gemini) |
| Cost | Free (open-access) | API costs (GEMINI_API_KEY) |
| Speed | Fast (download) | Slower (generation) |
| Uniqueness | Shared images | Unique images |
| Customization | Limited | Full control |
| Text rendering | Not available | Excellent |
| Realism | Excellent (photos) | Variable |
| Scientific accuracy | Excellent (BioArt) | May have inaccuracies |
| Licensing | Attribution required | No attribution needed |

---

## Conclusion

The image-generation integration transforms `create-powerpoint-presentations` into a **fully creative presentation tool** that can:

- Generate unique, branded imagery on-demand
- Create consistent visual themes across all slides
- Produce custom logos without external design tools
- Match any artistic style requested by the user

Combined with fetch-media for stock imagery, the skill now offers a **complete image solution** for any presentation need.

---

**Questions?** See:
- `$HOME/.claude/skills/image-generation/SKILL.md` for image-generation documentation
- `$HOME/.claude/skills/create-powerpoint-presentations/SKILL.md` for presentation skill documentation
- `$HOME/.claude/skills/create-powerpoint-presentations/FETCH_MEDIA_INTEGRATION.md` for fetch-media integration
