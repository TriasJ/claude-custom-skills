---
name: create-powerpoint-presentations
description: Create professional PowerPoint presentations using PptxGenJS with 8 templates (corporate, modern, academic, creative, minimal, neumorphic, tech, bio-sciences), infographic slides (7 patterns), master slides, HTML table conversion, smart image matching, charts, 185+ shapes, media, **AI-generated custom images** (via image-generation skill with Gemini), and stock images (via fetch-media skill). Use when creating presentations, slides, infographics, or when user mentions PowerPoint, PPTX, slide decks, data visualization, scientific presentations, or needs custom logos/artwork.
---

<objective>
Create beautiful, professional PowerPoint presentations from various sources using PptxGenJS. Supports 8 aesthetic templates (including neumorphic, modern tech, biological sciences), infographic slide creation, master slides, **automatic image retrieval via fetch-media skill** (Wikimedia Commons, NIH BioArt, Unsplash), **AI-generated custom images via image-generation skill** (Google Gemini), smart image matching, HTML table conversion, automated chart generation, robust shape handling (185+ types), and media embedding (video, audio, YouTube).

**Image Workflow**: Multi-source image strategy:
1. Automatically searches temp directory for existing stock images:
   - **Windows**: `$env:TEMP\fetch-media\`
   - **Unix/macOS**: `/tmp/fetch-media/`
2. Invokes fetch-media skill to download topic-relevant images from open-access sources
3. **Invokes image-generation skill** to create custom AI-generated images for unique concepts, logos, custom illustrations, or when stock images are insufficient
4. Intelligently matches all images to slide content using scoring algorithm
</objective>

<prerequisites>
**Required:**
- Node.js (v14 or higher): `node --version`
- npm: `npm --version`
- PptxGenJS: `npm install pptxgenjs`

If PptxGenJS not installed, guide user through:
```powershell
# Works on Windows PowerShell, macOS, and Linux
npm install pptxgenjs
```

**Optional (for AI Image Generation):**
- image-generation skill installed in user's Claude skills directory
- GEMINI_API_KEY environment variable set (get from https://aistudio.google.com/apikey)
- Python dependencies: `pip install google-genai Pillow`

To check if image-generation is available:
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
</prerequisites>

<coordinate_system>
**CRITICAL - Coordinate System and Layout:**

All PptxGenJS coordinates are **absolute values in inches**, NOT percentages or relative values.

**Default Layout - ALWAYS Use Widescreen:**
```javascript
// ALWAYS set widescreen layout at the start of every script
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';  // Widescreen: 10 inches wide × 5.625 inches tall
```

**Coordinate Ranges for Widescreen (16:9):**
- **X-axis**: 0 to 10 inches (horizontal)
- **Y-axis**: 0 to 5.625 inches (vertical)
- **Recommended content area**: x: 0.5-9.5, y: 0.5-5.1 (with margins)

**Shape Placement Rules:**
1. **Never use percentages** - Always use absolute inch values
2. **Validate bounds**: Ensure `x + w ≤ 10` and `y + h ≤ 5.625`
3. **Use margins**: Keep shapes at least 0.3 inches from edges
4. **Standard element sizes**:
   - Title: `x: 0.5, y: 0.5, w: 9, h: 0.8`
   - Content area: `x: 0.5, y: 1.5, w: 9, h: 3.6`
   - Footer: `x: 0.5, y: 5, w: 9, h: 0.3`

**Examples:**
```javascript
// ✓ CORRECT - Absolute inches, fits in widescreen
slide.addShape(pptx.ShapeType.rect, {
  x: 1,        // 1 inch from left
  y: 2,        // 2 inches from top
  w: 4,        // 4 inches wide
  h: 2         // 2 inches tall
});

// ✗ WRONG - Would overflow slide bounds
slide.addShape(pptx.ShapeType.rect, {
  x: 7,
  y: 3,
  w: 5,        // 7 + 5 = 12 inches (exceeds 10 inch width!)
  h: 4         // 3 + 4 = 7 inches (exceeds 5.625 inch height!)
});

// ✗ WRONG - Never use percentages or decimals as percentages
slide.addShape(pptx.ShapeType.rect, {
  x: 0.5,      // This is 0.5 inches, NOT 50%
  y: 0.5,      // This is 0.5 inches, NOT 50%
  w: 9,        // This is 9 inches, NOT 90%
  h: 4         // This is 4 inches, NOT 40%
});
```

**Validation Before Generation:**
- Check all x + width combinations stay within 10 inches
- Check all y + height combinations stay within 5.625 inches
- Add safety margins (0.3-0.5 inches) from slide edges
</coordinate_system>

<quick_start>
**Fast workflow for common cases:**

1. **Validate dependencies**: Check Node.js, npm, PptxGenJS installed
2. **Gather requirements**: Ask about topic, content sources, preferred style
3. **Collect content**: Read files, search web, or use provided information
4. **Gather images** (automatic multi-source):
   - Check temp directory for existing images (Glob):
     - **Windows**: `$env:TEMP\fetch-media\`
     - **Unix/macOS**: `/tmp/fetch-media/`
   - Search local directory for images (Glob)
   - **Invoke fetch-media skill** for stock images:
     - Extract key topics from presentation content
     - For scientific/medical: Use BioArt source
     - For general: Use Wikimedia Commons
     - Download to temp directory
   - **Invoke image-generation skill** for custom AI images (when available):
     - For unique concepts without good stock matches
     - For custom logos, diagrams, or illustrations
     - For creative/artistic imagery
     - Save to temp directory (generated-images subfolder)
5. **Choose template**: Corporate Blue, Modern Gradient, Academic Classic, Creative Pop, or Minimal White
6. **Generate script**: Create complete Node.js script with all features including fetch-media image paths
7. **Write & Execute**:
   - Use **Write tool** to save script as `generate-presentation.js`
   - Use **Bash tool** to run `node generate-presentation.js`
   - Verify .pptx file created
   - Report file location to user

**IMPORTANT**: The skill automatically writes and executes the script - don't just show code to the user.

**fetch-media Integration**: For scientific/medical presentations, fetch-media is **always invoked** to get high-quality BioArt illustrations. For other presentations, it's invoked when local images are insufficient.

**image-generation Integration**: When GEMINI_API_KEY is available, AI-generated images can be created for:
- Custom logos and branding elements
- Unique illustrations not available in stock libraries
- Conceptual/abstract visuals
- Personalized imagery matching exact presentation themes

**Minimal example:**
```javascript
import pptxgen from 'pptxgenjs';
const pptx = new pptxgen();

// ALWAYS set widescreen layout
pptx.layout = 'LAYOUT_16x9';  // 10" × 5.625" widescreen

// Add slide with text (coordinates in inches)
const slide = pptx.addSlide();
slide.addText('Hello World', {
  x: 1,          // 1 inch from left
  y: 2,          // 2 inches from top
  fontSize: 44,
  bold: true
});

// Write file
pptx.writeFile({ fileName: 'presentation.pptx' });
```
</quick_start>

<workflow>
<phase name="discovery">
**Ask user about:**
- Topic/purpose of presentation
- Target audience
- Content sources available:
  - Local files (markdown, CSV, JSON, images, videos)
  - Web content (URLs to fetch, topics to research)
  - User-provided information
- Preferred visual style (or offer 5 templates)
- Special requirements (branding, logo, specific colors)

**Use AskUserQuestion for style selection** if not specified.
</phase>

<phase name="content_gathering">
**Text content:**
- Read local files: Use Read tool for .md, .txt, .html, .csv, .json
- Research topics: Use WebSearch for trends, statistics, facts
- Fetch URLs: Use WebFetch for specific web pages
- Parse and organize into logical sections

**Data for charts:**
- Read CSV/JSON: Parse tabular and numerical data
- Detect chart types automatically:
  - Date/time series → Line chart
  - Comparisons → Bar chart
  - Parts of whole (≤8 items) → Pie chart
  - Multiple series → Grouped bar or multi-line
- Format data for PptxGenJS chart API

**Images (Automatic Multi-Source):**
1. **Check temp directory first**: Use Glob to find existing images from previous fetch-media downloads
   ```powershell
   # Cross-platform: Use os.tmpdir() in Node.js or platform-specific paths
   # Windows: Glob $env:TEMP\fetch-media\**\*.{png,jpg,jpeg,gif,svg}
   # Unix/macOS: Glob /tmp/fetch-media/**/*.{png,jpg,jpeg,gif,svg}
   ```
2. **Search local folders**: `Glob **/*.{png,jpg,jpeg,gif,bmp,svg}` in working directory
3. **Parse filenames for keywords**:
   - `logo.*` → Header/title slides
   - `background.*` → Slide backgrounds
   - `bioart_*`, `wikimedia_*` → Content images from fetch-media
   - Other keywords → Match to slide content via scoring algorithm
4. **Proactively invoke fetch-media** for topic-relevant images:
   - Extract key topics from presentation content (title, section headings, slide keywords)
   - For each major topic/section, invoke fetch-media skill:
     ```javascript
     // Example: Presentation about "Climate Change and Renewable Energy"
     // Invoke fetch-media for each major topic:
     // - Skill("fetch-media") with query "climate change effects"
     // - Skill("fetch-media") with query "solar panels renewable energy"
     // - Skill("fetch-media") with query "wind turbines"
     ```
   - Download mode for presentation use, URL mode for citation gathering
   - Prefer:
     - **Wikimedia Commons**: General topics, scientific concepts, nature, geography
     - **NIH BioArt**: Medical/biological/health topics (requires BioArt index)
     - **Unsplash**: Modern stock photography, lifestyle, technology (requires API key)
5. **Invoke image-generation skill** for custom AI-generated images (when GEMINI_API_KEY available):
   - Identify slides that need unique/custom imagery:
     - Custom logos or branding elements
     - Abstract/conceptual illustrations
     - Specific scenes not found in stock libraries
     - Creative/artistic visuals
   - Generate images using Gemini API:
     ```javascript
     // Example: Create a custom logo for the presentation
     // Skill("image-generation") with prompt:
     // "Clean modern logo with text 'EcoTech', leaf icon, green gradient, white background"

     // Example: Generate unique illustration
     // Skill("image-generation") with prompt:
     // "Stylized illustration of futuristic solar farm, isometric view, soft colors"
     ```
   - Save generated images to temp directory (generated-images subfolder)
   - Filename format: `generated_<timestamp>_<prompt_slug>.png`
6. **Apply content analysis with scoring** to match all images (local + fetch-media + AI-generated) to slides

**Media files:**
- Videos: `Glob **/*.{mp4,mov,avi,webm}`
- Audio: `Glob **/*.{mp3,wav,ogg,m4a}`
- YouTube links: Extract from content or ask user
</phase>

<phase name="design_selection">
**8 Pre-made Templates:**

See [references/templates.md](references/templates.md) for complete definitions.

Quick reference:
1. **Corporate Blue**: Professional, business-ready (Navy/Light blue/White/Gray)
2. **Modern Gradient**: Contemporary, eye-catching (Purple/Pink gradient)
3. **Academic Classic**: Traditional, scholarly (Burgundy/Gold/Cream)
4. **Creative Pop**: Bold, colorful (Orange/Teal/Yellow/Purple)
5. **Minimal White**: Clean, simple (White/Black/Gray/Accent)
6. **Neumorphic Soft UI**: Modern 3D with soft shadows (Soft Gray/Blue, tactile feel)
7. **Modern Tech**: Dark mode with neon accents (Dark Navy/Neon Blue/Purple, futuristic)
8. **Biological Sciences**: Natural, scientific (Deep Green/Teal/Blue, academic)

Each template includes master slides for: Title, Section Header, Content, Two-Column, Image, Closing.

**Template selection**: Use AskUserQuestion if user hasn't specified preference.
</phase>

<phase name="generation">
**Generate Node.js script with:**

1. **Imports and setup**
   - Import pptxgenjs
   - **Set widescreen layout**: `pptx.layout = 'LAYOUT_16x9';` (REQUIRED)
2. **Template definitions**: Master slides from selected template
   - All coordinates in inches for widescreen (10" × 5.625")
3. **Helper functions**:
   - Image matching
   - Chart generation
   - Shape placement with bounds validation
   - **Coordinate validator** (ensure x+w ≤ 10, y+h ≤ 5.625)
4. **Content slides**: Convert gathered content to slides with appropriate elements
   - Validate all shape coordinates before adding
   - Use safe margins (0.5" from edges)
5. **Write file**: Save .pptx

**Two generation modes:**

**Complete Script** (for quick execution):
```javascript
import pptxgen from 'pptxgenjs';

const pptx = new pptxgen();

// CRITICAL: Always set widescreen layout first
pptx.layout = 'LAYOUT_16x9';  // 10" × 5.625" (16:9 widescreen)

// Master slide definitions (coordinates for widescreen)
pptx.defineSlideMaster({ title: 'TEMPLATE_TITLE', ... });
pptx.defineSlideMaster({ title: 'TEMPLATE_CONTENT', ... });

// Helper functions
function addChartSlide(data) { ... }
function matchImages(slides, images) { ... }

// Generate slides
const titleSlide = pptx.addSlide({ masterName: 'TEMPLATE_TITLE' });
titleSlide.addText('Presentation Title', ...);

// ... more slides ...

pptx.writeFile({ fileName: 'presentation.pptx' });
```

**Modular Snippets** (for customization):
Provide reusable functions user can combine:
- `createMasterSlides(pptx, template)`
- `addTitleSlide(pptx, title, subtitle)`
- `addContentSlide(pptx, title, content)`
- `addChartSlide(pptx, data, chartType)`
- `addTableSlide(pptx, tableData)`
- `matchImagesToContent(slides, images)`
</phase>

<phase name="execution">
**Automatically execute the generation process:**

1. **Write script**: Use Write tool to create `generate-presentation.js` with the generated code
2. **Execute script**: Use Bash tool to run `node generate-presentation.js`
3. **Verify output**: Check that .pptx file was created successfully
4. **Report results**: Inform user of file location and size
5. **Offer refinements**:
   - Adjust colors/fonts
   - Reorder slides
   - Change chart types
   - Update images
   - Modify content

**IMPORTANT**: Do not just show the code to the user - actually write the file and execute it to generate the presentation.

**Error handling:**
- If Node.js not found: Guide user to install Node.js
- If PptxGenJS not found: Run `npm install pptxgenjs`
- If script fails: Show error and debug

**Example execution:**
```powershell
# Write the script
# (Use Write tool with generated JavaScript code)

# Execute it
node generate-presentation.js

# Verify (Windows PowerShell)
Get-Item presentation.pptx | Select-Object Name, Length
```
```bash
# Verify (Unix/macOS)
ls -lh presentation.pptx
```
</phase>
</workflow>

<image_matching>
**Smart Image Matching Algorithm** (content analysis with scoring):

```javascript
// Parse filename for keywords
function parseImageFilename(filename) {
  const name = filename.toLowerCase()
    .replace(/\.(png|jpg|jpeg|gif|bmp|svg)$/i, '');

  // Special types
  if (/logo/i.test(name)) return { type: 'logo', keywords: [] };
  if (/background|bg/i.test(name)) return { type: 'background', keywords: [] };

  // Extract keywords: split by hyphens, underscores, camelCase
  const keywords = name
    .split(/[-_]/)
    .flatMap(word => word.match(/[A-Z][a-z]+|[a-z]+/g) || [word]);

  return { type: 'content', keywords };
}

// Score image relevance to slide content
function scoreImageMatch(slideContent, imageKeywords) {
  const slideWords = slideContent.toLowerCase()
    .split(/\s+/)
    .filter(w => w.length > 3); // Filter short words

  let score = 0;

  imageKeywords.forEach(keyword => {
    const kw = keyword.toLowerCase();

    // Exact match: +3 points
    if (slideWords.includes(kw)) score += 3;

    // Partial match: +1 point
    if (slideWords.some(w => w.includes(kw) || kw.includes(w))) score += 1;
  });

  return score;
}

// Match images to slides
function matchImagesToSlides(slides, images) {
  const matches = [];

  images.forEach(img => {
    const { type, keywords } = parseImageFilename(img.path);

    if (type === 'logo') {
      // Add to all title/header slides
      matches.push({ image: img, slideTypes: ['title', 'section'] });
    } else if (type === 'background') {
      // Set as background for all slides or specific template
      matches.push({ image: img, slideTypes: ['background'] });
    } else {
      // Score against each slide
      slides.forEach(slide => {
        const score = scoreImageMatch(slide.content, keywords);
        if (score > 0) {
          matches.push({ image: img, slide: slide.id, score });
        }
      });
    }
  });

  // Sort by score, take best matches
  return matches.sort((a, b) => (b.score || 0) - (a.score || 0));
}
```

**fetch-media Integration:**

Proactive workflow for automatic image retrieval:

```javascript
// Step 1: Extract topics from presentation content
function extractKeyTopics(presentationData) {
  const topics = [];

  // Extract from title
  topics.push(presentationData.title);

  // Extract from section headers
  presentationData.sections.forEach(section => {
    topics.push(section.title);
  });

  // Extract significant keywords from slide content
  presentationData.slides.forEach(slide => {
    // Extract nouns, technical terms, domain-specific keywords
    const keywords = extractImportantKeywords(slide.content);
    topics.push(...keywords);
  });

  // Remove duplicates and short terms
  return [...new Set(topics)].filter(t => t.split(' ').length >= 2 || t.length > 5);
}

// Step 2: Invoke fetch-media for each topic
async function fetchImagesForTopics(topics, presentationType) {
  const images = [];

  for (const topic of topics) {
    // Determine best source based on topic and presentation type
    let source = 'wikimedia'; // default

    if (/biolog|medic|health|cell|virus|bacteria|anatom|disease/i.test(topic)) {
      source = 'bioart'; // Medical/biological topics
    } else if (/tech|startup|business|modern|lifestyle/i.test(presentationType)) {
      source = 'unsplash'; // Modern stock photography
    }

    // Invoke fetch-media skill via Skill tool
    // This will download images to temp directory (fetch-media subfolder)
    // Windows: $env:TEMP\fetch-media\  |  Unix: /tmp/fetch-media/
    console.log(`Fetching images for "${topic}" from ${source}...`);
    // Use: Skill("fetch-media") with appropriate query
  }

  return images;
}

// Step 3: Scan temp directory for all downloaded images (cross-platform)
function loadFetchMediaImages() {
  // Cross-platform temp directory detection:
  const os = require('os');
  const fetchMediaDir = path.join(os.tmpdir(), 'fetch-media');
  // Use Glob tool with platform-appropriate path
  const fetchMediaFiles = []; // populated by Glob results

  return fetchMediaFiles.map(filePath => {
    // Parse fetch-media filename format:
    // wikimedia_<id>_<title>.jpg
    // bioart_<id>_<title>.png
    // unsplash_<id>_<title>.jpg

    const basename = path.basename(filePath);
    const match = basename.match(/^(wikimedia|bioart|unsplash)_(\d+)_(.+)\.(png|jpg|jpeg|gif|svg)$/);

    if (match) {
      const [, source, id, titleSlug, ext] = match;
      const title = titleSlug.replace(/_/g, ' ');

      return {
        path: filePath,
        source,
        id,
        title,
        keywords: title.toLowerCase().split(' '),
        type: 'content'
      };
    }

    return {
      path: filePath,
      keywords: parseImageFilename(basename).keywords,
      type: 'content'
    };
  });
}

// Step 4: Load AI-generated images (cross-platform)
function loadGeneratedImages() {
  // Cross-platform temp directory detection:
  const os = require('os');
  const generatedImagesDir = path.join(os.tmpdir(), 'generated-images');
  // Use Glob tool with platform-appropriate path
  const generatedFiles = []; // populated by Glob results

  return generatedFiles.map(filePath => {
    const basename = path.basename(filePath);
    // Parse generated filename format: generated_<timestamp>_<prompt_slug>.<ext>
    const match = basename.match(/^generated_(\d+)_(.+)\.(png|jpg|jpeg)$/);

    if (match) {
      const [, timestamp, promptSlug, ext] = match;
      const title = promptSlug.replace(/_/g, ' ');

      return {
        path: filePath,
        source: 'ai-generated',
        timestamp,
        title,
        keywords: title.toLowerCase().split(' '),
        type: 'content'
      };
    }

    return {
      path: filePath,
      source: 'ai-generated',
      keywords: parseImageFilename(basename).keywords,
      type: 'content'
    };
  });
}

// Step 5: Combine all image sources (cross-platform)
function gatherAllImages() {
  const os = require('os');
  const images = [];

  // Priority 1: Check temp/fetch-media/ for fetch-media downloads
  images.push(...loadFetchMediaImages());

  // Priority 2: Check temp/generated-images/ for AI-generated images
  images.push(...loadGeneratedImages());

  // Priority 3: Local working directory images
  // Use Glob: **/*.{png,jpg,jpeg,gif,bmp,svg}
  images.push(...loadLocalImages());

  return images;
}

// Example complete workflow:
// 1. Extract topics: ["Climate Change", "Renewable Energy", "Solar Power"]
// 2. Invoke fetch-media for each topic (downloads to temp/fetch-media/)
// 3. Identify slides needing custom imagery → Invoke image-generation skill
// 4. Scan temp/fetch-media/ and temp/generated-images/ for all images
// 5. Match images to slides using scoring algorithm
// 6. Generate presentation with matched images
```

**When to invoke fetch-media:**
- **Always** for scientific/medical presentations (BioArt has excellent illustrations)
- **Always** when presentation topic is provided but no local images available
- **Optionally** for general topics if user wants high-quality stock photos
- **Skip** if user explicitly provides image folder or doesn't want internet images

**fetch-media Query Strategy:**
- Keep queries focused and specific (2-4 words)
- Use technical terms for scientific presentations
- Use descriptive phrases for general topics
- Example good queries: "solar panel installation", "human immune system", "DNA replication", "renewable energy turbine"

**When to invoke image-generation (requires GEMINI_API_KEY):**
- **Custom branding**: Logos, icons, branded graphics specific to the presentation
- **Unique concepts**: Abstract ideas, future scenarios, imaginary scenes not in stock libraries
- **Text in images**: When specific text needs to appear in the image itself
- **Style-specific artwork**: Particular artistic styles (isometric, kawaii, minimalist, etc.)
- **Gap-filling**: After fetch-media, when specific slides still lack suitable imagery
- **User request**: When user explicitly asks for AI-generated/custom images
- **Skip** if GEMINI_API_KEY not available, or user prefers only stock images

**image-generation Prompt Strategy:**
- Be descriptive and specific about the desired output
- Include style keywords: photorealistic, illustration, minimalist, isometric, etc.
- Specify aspect ratio when needed (16:9 for slide backgrounds, 1:1 for icons)
- Include color preferences if matching template theme
- Example good prompts:
  - "Clean modern logo with text 'TechCorp', blue gradient, white background, minimalist"
  - "Isometric illustration of smart city with solar panels and wind turbines, soft pastel colors"
  - "Abstract representation of data flow, blue and purple network nodes, dark background"
  - "Kawaii style mascot character, friendly robot, waving, simple background"

**image-generation Workflow:**
```javascript
// Step 1: Check if image-generation is available (cross-platform)
const os = require('os');
const imageGenAvailable = process.env.GEMINI_API_KEY &&
  fs.existsSync(path.join(os.homedir(), '.claude', 'skills', 'image-generation', 'SKILL.md'));

// Step 2: Identify slides needing custom images
function identifySlidesNeedingCustomImages(slides, matchedImages) {
  return slides.filter(slide => {
    // No matched image or low match score
    const matchedImage = matchedImages.find(m => m.slideId === slide.id);
    if (!matchedImage || matchedImage.score < 3) {
      // Check if slide needs custom content
      return slide.type === 'title' ||           // Title slides often need custom imagery
             slide.needsLogo ||                   // Logo requirement
             slide.content.includes('logo') ||
             slide.content.includes('concept') ||
             slide.content.includes('future');
    }
    return false;
  });
}

// Step 3: Generate prompts for each slide
function generateImagePrompt(slide, template) {
  const baseStyle = template.style; // e.g., "modern tech", "corporate", "creative"
  const colors = template.colors;    // e.g., { primary: "#1E3A8A", accent: "#60A5FA" }

  // Construct prompt based on slide content and template
  let prompt = `${slide.visualConcept || slide.title}, `;
  prompt += `${baseStyle} style, `;
  prompt += `colors matching ${colors.primary} and ${colors.accent}, `;
  prompt += `16:9 aspect ratio for presentation slide`;

  return prompt;
}

// Step 4: Invoke image-generation skill
// Use Skill("image-generation") with the generated prompt
// Save result to temp/generated-images/generated_<timestamp>_<prompt_slug>.png
// (Uses os.tmpdir() for cross-platform compatibility)
```
</image_matching>

<infographic_creation>
**Create data-rich, visually compelling infographic slides** using shape compositions.

See [references/infographics.md](references/infographics.md) for complete patterns and examples.

**7 Infographic Layout Patterns:**

1. **Timeline/Process Flow**: Sequential steps with arrows and numbered circles
2. **Statistics Grid**: Multiple KPIs in organized grid with icons
3. **Comparison Chart**: Side-by-side comparison of two options
4. **Pyramid/Hierarchy**: Show hierarchical relationships or priorities
5. **Circle/Radial Layout**: Interconnected concepts or cyclical processes
6. **Funnel/Conversion**: Progressive narrowing for conversion stages
7. **Icon Grid**: Features or benefits with icon representations

**Auto-select pattern based on content type:**
```javascript
function selectInfographicPattern(contentType, dataStructure) {
  // Process/timeline → timeline pattern
  // Metrics → statistics grid
  // Comparison → side-by-side comparison
  // Hierarchy → pyramid
  // Relationships → radial
  // Conversion → funnel
  // Features → icon grid
}
```

**Integration**: When user requests infographic slides, identify content type, select appropriate pattern, extract data, and generate using shape compositions.
</infographic_creation>

<shape_handling>
**185+ Shape Types** organized by category. See [references/shapes.md](references/shapes.md) for complete catalog.

**Coordinate Validation (CRITICAL - Use this helper):**

```javascript
// Validate shape coordinates fit within widescreen slide (10" × 5.625")
function validateCoordinates(shape, layoutWidth = 10, layoutHeight = 5.625) {
  const errors = [];

  if (shape.x < 0) errors.push(`x (${shape.x}) is negative`);
  if (shape.y < 0) errors.push(`y (${shape.y}) is negative`);
  if (shape.x + shape.w > layoutWidth) {
    errors.push(`x + w (${shape.x} + ${shape.w} = ${shape.x + shape.w}) exceeds layout width (${layoutWidth})`);
  }
  if (shape.y + shape.h > layoutHeight) {
    errors.push(`y + h (${shape.y} + ${shape.h} = ${shape.y + shape.h}) exceeds layout height (${layoutHeight})`);
  }

  if (errors.length > 0) {
    console.warn('Shape coordinate validation failed:', errors.join('; '));
    // Auto-fix: constrain to layout bounds with margin
    shape.x = Math.max(0.5, Math.min(shape.x, layoutWidth - shape.w - 0.5));
    shape.y = Math.max(0.5, Math.min(shape.y, layoutHeight - shape.h - 0.5));
    shape.w = Math.min(shape.w, layoutWidth - shape.x - 0.5);
    shape.h = Math.min(shape.h, layoutHeight - shape.y - 0.5);
  }

  return shape;
}

// Use before adding shapes:
const shapeParams = validateCoordinates({ x: 7, y: 3, w: 4, h: 2 });
slide.addShape(pptx.ShapeType.rect, shapeParams);
```

**Contextual Shape Selection:**

```javascript
// Select shapes based on slide purpose
function selectShapeForContext(slideContext) {
  const context = slideContext.toLowerCase();

  // Process flows
  if (/process|workflow|steps/i.test(context)) {
    return ['rightArrow', 'flowChartProcess', 'flowChartDecision'];
  }

  // Highlights/Important
  if (/important|highlight|key/i.test(context)) {
    return ['star5', 'star6', 'cloudCallout'];
  }

  // Warnings/Alerts
  if (/warning|alert|caution/i.test(context)) {
    return ['triangle', 'hexagon', 'borderCallout1'];
  }

  // Data/Numbers
  if (/data|metric|number/i.test(context)) {
    return ['rect', 'roundRect', 'frame'];
  }

  return ['rect']; // Default
}

// Position shapes intelligently
function addContextualShape(slide, shapeType, content, position) {
  const template = getCurrentTemplate();

  slide.addShape(pptx.ShapeType[shapeType], {
    x: position.x,
    y: position.y,
    w: position.w,
    h: position.h,
    fill: { color: template.accentColor },
    line: { color: template.lineColor, width: 2 }
  });

  // Add text inside shape if content provided
  if (content) {
    slide.addText(content, {
      x: position.x,
      y: position.y,
      w: position.w,
      h: position.h,
      fontSize: 14,
      color: template.textColor,
      align: 'center',
      valign: 'middle'
    });
  }
}
```

**Common Shape Patterns:**

- **Process arrows**: Link steps with rightArrow, bentArrow
- **Callout boxes**: Emphasize points with cloudCallout, wedgeRectCallout
- **Flowcharts**: Use flowChartProcess, flowChartDecision, flowChartDocument
- **Highlights**: Draw attention with star shapes, hexagons
- **Decorative**: Gears, hearts, moons for thematic touches
</shape_handling>

<html_table_conversion>
**Convert HTML tables to slides** with auto-pagination:

```javascript
// From HTML table element (browser)
pptx.tableToSlides('tableElementId', {
  x: 0.5,
  y: 1,
  w: 9,
  autoPage: true,                   // Split across multiple slides
  autoPageRepeatHeader: true,       // Repeat headers on each slide
  autoPageHeaderRows: 1,            // Number of header rows
  autoPageSlideStartY: 0.5,         // Y position on subsequent slides
  border: { type: 'solid', pt: 1, color: '366092' },
  fontSize: 11
});

// From data array (Node.js)
const tableData = [
  [
    { text: 'Header 1', options: { bold: true, fill: { color: '4472C4' }, color: 'FFFFFF' } },
    { text: 'Header 2', options: { bold: true, fill: { color: '4472C4' }, color: 'FFFFFF' } }
  ],
  ['Row 1, Cell 1', 'Row 1, Cell 2'],
  ['Row 2, Cell 1', 'Row 2, Cell 2']
];

slide.addTable(tableData, {
  x: 0.5,
  y: 1.5,
  w: 9,
  colW: [4.5, 4.5],
  autoPage: true,
  autoPageRepeatHeader: true
});
```

**Handle colspan/rowspan:**
PptxGenJS automatically handles HTML table colspan and rowspan attributes.
</html_table_conversion>

<chart_generation>
**Automatic Chart Type Detection:**

```javascript
function detectChartType(data) {
  // Date/time series → Line chart
  if (data.labels && data.labels.some(isDateLike)) {
    return 'line';
  }

  // Single series, few items → Pie chart
  if (!data.series && data.values.length <= 8) {
    return 'pie';
  }

  // Multiple series → Bar chart
  if (data.series && data.series.length > 1) {
    return 'bar';
  }

  return 'bar'; // Default
}

// Generate chart
function addChart(slide, chartData, options) {
  const chartType = detectChartType(chartData);
  const template = getCurrentTemplate();

  slide.addChart(pptx.ChartType[chartType], chartData, {
    x: options.x || 1,
    y: options.y || 1.5,
    w: options.w || 8,
    h: options.h || 4,
    showTitle: true,
    title: options.title,
    showLegend: true,
    legendPos: 'r',
    showValue: chartType === 'pie',
    chartColors: template.chartColors,
    ...options
  });
}
```

**Chart Types:**
- Line: Trends over time
- Bar: Comparisons between categories
- Pie: Parts of a whole
- Scatter: Relationships between variables
- Area: Cumulative trends
- Doughnut: Alternative to pie with center space
</chart_generation>

<media_embedding>
**Video, Audio, YouTube:**

```javascript
// Local video file
slide.addMedia({
  type: 'video',
  path: './videos/demo.mp4',
  x: 1,
  y: 1.5,
  w: 8,
  h: 4.5
});

// Local audio file
slide.addMedia({
  type: 'audio',
  path: './audio/background.mp3',
  x: 3,
  y: 3,
  w: 2,
  h: 0.5
});

// YouTube video (online)
slide.addMedia({
  type: 'online',
  link: 'https://www.youtube.com/embed/VIDEO_ID',
  x: 1.5,
  y: 1.5,
  w: 7,
  h: 4
});

// Video with custom thumbnail
slide.addMedia({
  type: 'video',
  path: 'https://example.com/video.mp4',
  cover: './images/video-thumbnail.jpg',
  x: 1,
  y: 1,
  w: 8,
  h: 4.5
});
```

**Supported Formats:**
- Video: MP4, MOV, AVI, WebM
- Audio: MP3, WAV, OGG, M4A
- Online: YouTube embed URLs
</media_embedding>

<common_patterns>
**Pattern 1: Research Presentation from Topic (with automatic fetch-media)**

User provides topic → WebSearch for content → **Invoke fetch-media for images** → Generate slides

**Example: "Create a presentation about CRISPR gene editing"**

```javascript
// Step 1: Gather content via WebSearch
// - Search for "CRISPR gene editing mechanism"
// - Search for "CRISPR applications medicine"
// - Organize into sections: Introduction, Mechanism, Applications, Ethics

// Step 2: Extract key topics for images
const topics = [
  "CRISPR Cas9 mechanism",
  "DNA editing process",
  "gene therapy",
  "bacteria immune system"
];

// Step 3: Invoke fetch-media for each topic
// Use Skill("fetch-media") with query "CRISPR Cas9 mechanism" → downloads to temp/fetch-media/
// Use Skill("fetch-media") with query "DNA editing process" → downloads to temp/fetch-media/
// Prefers BioArt source for biological topics

// Step 4: Scan temp/fetch-media/ for downloaded images (cross-platform)
// Use Glob with os.tmpdir() for platform-appropriate path
// Example files found:
// - <temp>/fetch-media/bioart_123_CRISPR_Cas9_Complex.png
// - <temp>/fetch-media/wikimedia_456_DNA_Double_Helix.jpg

// Step 5: Match images to slides using content scoring
// Slide about "How CRISPR Works" → matches bioart_123_CRISPR_Cas9_Complex.png (score: 8)

// Step 6: Apply Academic Classic template
// Step 7: Generate 10-15 slide deck with matched images
```

**Pattern 2: Data Report from CSV**

User provides CSV → Parse data → Generate charts → Create table slides

```javascript
// 1. Read CSV with numerical data
// 2. Detect chart opportunities
// 3. Generate bar/line/pie charts
// 4. Create auto-paginated table with full data
// 5. Apply Corporate Blue template
```

**Pattern 3: Marketing Pitch with Media (with fetch-media stock photos)**

User provides concept → **fetch-media for stock photos** → Create compelling story → Modern design

**Example: "Create a pitch deck for a renewable energy startup"**

```javascript
// Step 1: Structure narrative (problem, solution, benefits, CTA)
const sections = [
  { title: "The Problem", content: "Climate change and fossil fuel dependency" },
  { title: "Our Solution", content: "Affordable solar energy for homes" },
  { title: "Market Opportunity", content: "$500B renewable energy market" },
  { title: "Call to Action", content: "Join us in transforming energy" }
];

// Step 2: Invoke fetch-media for compelling imagery
// Use Skill("fetch-media") with query "solar panels home installation" (source: wikimedia/unsplash)
// Use Skill("fetch-media") with query "wind turbine renewable energy" (source: wikimedia)
// Use Skill("fetch-media") with query "sustainable technology" (source: wikimedia)

// Step 3: Check temp/fetch-media/ for downloaded images (cross-platform)
// - <temp>/fetch-media/wikimedia_789_Solar_Panel_Installation.jpg
// - <temp>/fetch-media/wikimedia_790_Wind_Turbine_Farm.jpg
// - <temp>/fetch-media/unsplash_123_Sustainable_City.jpg (if API key configured)

// Step 4: Match images to slides
// "The Problem" slide → Climate-related image
// "Our Solution" slide → Solar panel image
// "Market Opportunity" slide → Modern tech/business image

// Step 5: Embed product demo video (local file)
// Step 6: Use shapes for emphasis (stars for highlights, arrows for process)
// Step 7: Apply Modern Gradient or Creative Pop template
```

**Pattern 4: Convert Existing Document**

User provides .md/.html document → Parse structure → Generate slides

```javascript
// 1. Read document, parse headings as slide titles
// 2. Convert tables to presentation tables
// 3. Extract lists as bullet points
// 4. Find referenced images
// 5. Apply appropriate template based on content tone
```

**Pattern 5: Branded Presentation with AI-Generated Images**

User provides concept + branding requirements → **image-generation for custom logos/graphics** → fetch-media for stock photos → Generate polished deck

**Example: "Create a branded pitch deck for 'NeuraTech AI' startup"**

```javascript
// Step 1: Structure presentation content
const sections = [
  { title: "Introducing NeuraTech AI", type: "title", needsLogo: true },
  { title: "The Problem", content: "AI is complex and inaccessible" },
  { title: "Our Solution", content: "AI-powered automation platform", needsCustomGraphic: true },
  { title: "How It Works", content: "Simple 3-step process" },
  { title: "Market Opportunity", content: "$50B AI market by 2030" },
  { title: "Team", content: "Industry experts" },
  { title: "Join Us", type: "closing", needsLogo: true }
];

// Step 2: Generate custom logo using image-generation skill
// Use Skill("image-generation") with prompt:
// "Clean modern logo with text 'NeuraTech AI', neural network icon,
//  blue and purple gradient, white background, minimalist tech style"
// → Saves to <temp>/generated-images/generated_1234567890_neuratech_ai_logo.png

// Step 3: Generate custom illustration for "Our Solution" slide
// Use Skill("image-generation") with prompt:
// "Isometric illustration of AI automation workflow, connected nodes,
//  data flowing between systems, blue and purple colors, soft shadows"
// → Saves to <temp>/generated-images/generated_1234567891_ai_automation_workflow.png

// Step 4: Invoke fetch-media for stock photos
// Use Skill("fetch-media") with query "artificial intelligence technology"
// Use Skill("fetch-media") with query "business team meeting"
// → Downloads to <temp>/fetch-media/

// Step 5: Gather all images from all sources (cross-platform paths)
// - <temp>/generated-images/generated_*_neuratech_ai_logo.png (AI-generated logo)
// - <temp>/generated-images/generated_*_ai_automation_workflow.png (AI-generated illustration)
// - <temp>/fetch-media/wikimedia_123_AI_Neural_Network.jpg (stock photo)
// - <temp>/fetch-media/unsplash_456_Business_Team.jpg (stock photo)

// Step 6: Match images to slides
// Title slide → AI-generated logo
// "Our Solution" slide → AI-generated workflow illustration
// "Team" slide → Stock photo of business team
// Other slides → Stock photos of AI/technology

// Step 7: Apply Modern Tech template (dark mode with neon accents)
// Step 8: Generate branded presentation with custom + stock imagery
```

**Pattern 6: Creative Presentation with Style-Specific AI Art**

User requests artistic/creative style → **image-generation for custom artwork** → Generate visually unique presentation

**Example: "Create a fun presentation about our company culture in kawaii style"**

```javascript
// Step 1: Plan visual theme
const visualStyle = "kawaii, cute, pastel colors, simple shapes, friendly characters";

// Step 2: Generate custom mascot/character using image-generation
// Use Skill("image-generation") with prompt:
// "Kawaii style mascot character, friendly smiling robot, round shape,
//  pastel blue color, simple eyes, waving hand, white background"
// → Saves to /tmp/generated-images/generated_*_kawaii_robot_mascot.png

// Step 3: Generate themed illustrations for each section
// "Our Values" slide:
// Use Skill("image-generation") with prompt:
// "Kawaii style illustration of teamwork, cute characters holding hands,
//  pastel colors, simple shapes, cheerful atmosphere"

// "Work-Life Balance" slide:
// Use Skill("image-generation") with prompt:
// "Kawaii style illustration of coffee cup and laptop, cute face on cup,
//  pastel pink and blue, cozy atmosphere"

// "Join Our Team" slide:
// Use Skill("image-generation") with prompt:
// "Kawaii style group of diverse cute characters, waving, happy faces,
//  pastel rainbow colors, welcoming gesture"

// Step 4: Apply Creative Pop template with pastel color overrides
// Step 5: Generate playful, visually consistent presentation
```
</common_patterns>

<advanced_features>
**Speaker Notes:**
```javascript
slide.addNotes('Key talking points:\n- Emphasize Q2 growth\n- Address market concerns\n- Transition to next section');
```

**Sections:**
Organize large presentations:
```javascript
pptx.addSection({ title: 'Introduction' });
pptx.addSection({ title: 'Analysis' });
pptx.addSection({ title: 'Conclusion' });
```

**Custom Layouts:**
```javascript
pptx.defineLayout({ name: 'A4', width: 8.27, height: 11.69 });
pptx.layout = 'A4';
```

**Slide Numbers:**
```javascript
pptx.defineSlideMaster({
  title: 'MASTER_NAME',
  slideNumber: { x: 9, y: 7, fontSize: 10, color: '666666' }
});
```

**Accessibility:**
- Alt text for images: `slide.addImage({ ..., altText: 'Description' })`
- Readable font sizes (minimum 14pt body, 24pt titles)
- Color contrast compliance (WCAG AA)
- Logical reading order

See [references/advanced-features.md](references/advanced-features.md) for more details.
</advanced_features>

<validation>
**Pre-generation checks:**
- [ ] Node.js and npm installed
- [ ] PptxGenJS installed (`npm list pptxgenjs`)
- [ ] **Widescreen layout will be set**: `pptx.layout = 'LAYOUT_16x9';` (MANDATORY)
- [ ] Content sources accessible (files exist, URLs reachable)
- [ ] **fetch-media skill available** (check skill exists in user's Claude skills directory)
- [ ] **Check temp/fetch-media/ for existing images** before invoking fetch-media
- [ ] Image sources prioritized:
  - [ ] temp/fetch-media/ images (from previous/current fetch-media downloads)
  - [ ] temp/generated-images/ images (from AI generation)
  - [ ] Local working directory images
  - [ ] Invoke fetch-media for missing topics
  - [ ] Invoke image-generation for custom/unique imagery (if GEMINI_API_KEY available)
- [ ] **image-generation availability** (optional): Check GEMINI_API_KEY and skill exists
- [ ] Data for charts properly formatted
- [ ] Media files accessible
- [ ] **Coordinate validation**: All shapes have x+w ≤ 10 and y+h ≤ 5.625

**During image gathering:**
- [ ] Extract key topics from presentation content (title, sections, keywords)
- [ ] For scientific/medical presentations: **Always invoke fetch-media** with BioArt source
- [ ] For general presentations: Invoke fetch-media only if local images insufficient
- [ ] Use focused queries (2-4 words) for fetch-media
- [ ] Wait for fetch-media downloads to complete before scanning temp/fetch-media/
- [ ] Parse fetch-media filename format: `<source>_<id>_<title>.<ext>`
- [ ] **For custom imagery** (logos, branding, unique concepts): Invoke image-generation skill
- [ ] **For style-specific artwork** (kawaii, isometric, etc.): Use image-generation with style prompts
- [ ] Wait for image-generation to complete before scanning temp/generated-images/
- [ ] Parse AI-generated filename format: `generated_<timestamp>_<prompt_slug>.<ext>`

**Post-generation checks:**
- [ ] **Script includes**: `pptx.layout = 'LAYOUT_16x9';` at the top
- [ ] **All coordinates validated**: No shapes exceed 10" width or 5.625" height
- [ ] Script syntax valid (no errors)
- [ ] .pptx file created
- [ ] File size reasonable (< 50MB for performance)
- [ ] Slides render correctly when opened
- [ ] **All shapes fit within slide bounds** - no clipping or overflow
- [ ] **Images from temp/fetch-media/ embedded properly**
- [ ] **Images from temp/generated-images/ embedded properly** (if AI-generated)
- [ ] Image attributions included in notes or final slide (if using fetch-media)
- [ ] AI-generated images noted in speaker notes (if using image-generation)
- [ ] Charts show data accurately
- [ ] Media plays (if embedded)
</validation>

<success_criteria>
**The skill must accomplish all of the following:**

- ✅ PptxGenJS properly installed and validated (or installed automatically)
- ✅ **Widescreen (16:9) layout set in every generated script**: `pptx.layout = 'LAYOUT_16x9';`
- ✅ **All coordinates use absolute inch values** (not percentages or relative values)
- ✅ **All shapes fit within widescreen bounds** (x+w ≤ 10, y+h ≤ 5.625)
- ✅ Content successfully gathered from all specified sources
- ✅ **Images obtained through multi-source strategy:**
  - ✅ temp/fetch-media/ checked for existing stock images (cross-platform)
  - ✅ temp/generated-images/ checked for existing AI-generated images (cross-platform)
  - ✅ Local working directory searched for images
  - ✅ **fetch-media skill invoked** for missing/insufficient stock images (especially for scientific/medical topics)
  - ✅ **image-generation skill invoked** (when available) for custom logos, branding, unique illustrations
  - ✅ Image attributions preserved from fetch-media downloads
  - ✅ AI-generated image prompts documented in speaker notes
- ✅ Images matched intelligently to slide content using scoring algorithm
- ✅ Template applied with consistent branding and colors
- ✅ Complete, executable Node.js script generated
- ✅ **Script written to file using Write tool** (e.g., `generate-presentation.js`)
- ✅ **Script executed using Bash tool** (`node generate-presentation.js`)
- ✅ **.pptx file created and verified to exist**
- ✅ File location reported to user (with size)
- ✅ Presentation opens in PowerPoint/LibreOffice/Google Slides
- ✅ All elements (text, images from fetch-media, AI-generated images, charts, shapes, media) display correctly
- ✅ User satisfied with design and ready to present or refine further

**The skill should NOT:**
- ❌ Just show JavaScript code to user without executing it
- ❌ Ask user to manually run the script
- ❌ Leave user to figure out Node.js installation
- ❌ Ignore temp/fetch-media/ images when they exist
- ❌ Ignore temp/generated-images/ AI-generated images when they exist
- ❌ Skip fetch-media for scientific/medical presentations (BioArt has excellent resources)
- ❌ Skip image-generation when user explicitly requests custom logos/artwork (and GEMINI_API_KEY available)
- ❌ Hardcode image paths that assume specific user directory structure (use os.tmpdir() and os.homedir())
</success_criteria>

<anti_patterns>
**Avoid:**
- **Using percentages or relative coordinates** - Always use absolute inch values (x: 1.5 means 1.5 inches, NOT 1.5%)
- **Forgetting to set widescreen layout** - ALWAYS include `pptx.layout = 'LAYOUT_16x9';`
- **Not validating coordinate bounds** - Shapes must fit: x+w ≤ 10, y+h ≤ 5.625
- **Alternating between 4:3 and 16:9 layouts** - ONLY use widescreen unless explicitly requested
- **Shapes exceeding slide boundaries** - Validate all coordinates before generating script
- Generating scripts without validating dependencies first
- Overloading slides with too much text (max 5-7 bullet points)
- Using low-resolution images (< 800px width)
- Inconsistent fonts or colors within presentation
- Missing alt text on images (accessibility)
- Charts with more than 7 data series (too cluttered)
- Video files > 100MB (performance issues)
- Assuming file paths exist without checking
- Hardcoding paths that won't work on user's system
- Generating 50+ slides without pagination strategy
</anti_patterns>

<reference_guides>
**Detailed documentation:**
- [references/templates.md](references/templates.md) - Complete template definitions with code (8 templates including neumorphic, modern tech, biological sciences)
- [references/infographics.md](references/infographics.md) - Infographic slide patterns with shape compositions (7 layout patterns)
- [references/shapes.md](references/shapes.md) - All 185+ shapes with usage examples
- [references/advanced-features.md](references/advanced-features.md) - Charts, media, sections, accessibility
- [references/api-reference.md](references/api-reference.md) - PptxGenJS API quick reference

**External resources:**
- PptxGenJS via Context7: `/gitbrent/pptxgenjs`
- fetch-media skill: Use Skill tool with "fetch-media"
- image-generation skill: Use Skill tool with "image-generation" (requires GEMINI_API_KEY)
</reference_guides>
