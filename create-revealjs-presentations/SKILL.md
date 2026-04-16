---
name: create-revealjs-presentations
description: Creates professional HTML presentations using reveal.js with 8 templates, automatic media fetching (via fetch-media skill), **AI-generated custom images** (via image-generation skill with Gemini), D3.js/Three.js/P5.js visualizations, speaker notes, and single-file deployment. Use when creating presentations, slide decks, HTML presentations, interactive slides, or when user needs custom logos/artwork.
---

<objective>
Create stunning, interactive HTML presentations using reveal.js with professional templates, automatic media embedding, and advanced features like D3.js visualizations, Three.js 3D models, video backgrounds, and speaker notes. Outputs presentation as both multi-file structure and single standalone HTML file for easy deployment.

**Image Workflow**: Multi-source image strategy:
1. Use **fetch-media skill** to download topic-relevant stock images from open-access sources
2. Use **image-generation skill** to create custom AI-generated images for unique concepts, logos, custom illustrations, or when stock images are insufficient
3. Encode all images as BASE64 for single-file deployment
</objective>

<quick_start>
<basic_workflow>
1. **Gather requirements**: Ask about presentation topic, desired template style, and key slides
2. **Select or customize template**: Choose from 8 built-in templates (see [templates directory](templates/))
3. **Fetch media automatically**: Use fetch-media skill to search and download relevant images
4. **Build presentation**: Generate HTML with widescreen format (1280x720)
5. **Add speaker notes**: Prompt user for presenter notes on each slide
6. **Create deployment package**: Generate both multi-file and single-file BASE64-encoded versions
7. **Create launcher script**: Generate Node.js script for local server + presenter view
</basic_workflow>

<example>
**User request**: "Create a presentation about quantum computing"

**Your workflow**:
1. Ask about target audience and preferred template style
2. Use AskUserQuestion to confirm slide patterns (title+bullets, comparison, etc.)
3. Use fetch-media skill: "quantum computer chip", "quantum circuit", "qubit diagram"
4. Generate reveal.js HTML with quantum-dark template (black bg, teal accents)
5. Embed fetched images as BASE64
6. Create present.js launcher script
7. Output: quantum-computing.html (single file) + source folder
</example>
</quick_start>

<workflow>
<step_1>
**Requirements gathering**: Use AskUserQuestion to gather:
- Presentation topic and target audience
- Preferred template style (creative/professional/modern)
- Number of slides and general structure
- Whether to use pre-built slide patterns (see [patterns/](patterns/))
</step_1>

<step_2>
**Template selection**: Present 8 template options with previews:

**Creative Templates** (3):
- `neon-glow` - Vibrant gradients, animated backgrounds, bold typography
- `paper-craft` - 3D paper textures, shadow effects, organic feel
- `liquid-motion` - Fluid animations, morphing shapes, dynamic colors

**Professional Templates** (2):
- `corporate-blue` - Clean lines, corporate blue palette, professional spacing
- `executive-minimal` - Ultra-minimal, high contrast, serif typography

**Modern Templates** (3):
- `quantum-dark` - Black background, teal/blue accents, tech-forward
- `glass-morphism` - Frosted glass effects, soft shadows, modern UI
- `cyber-grid` - Grid patterns, neon accents, futuristic aesthetic

See [templates/README.md](templates/README.md) for full template specifications.
</step_2>

<step_3>
**Media acquisition**: Multi-source image strategy

**Stock images via fetch-media skill:**
- Analyze slide content to identify needed imagery
- Search for relevant, high-quality images automatically
- Download and prepare for BASE64 encoding
- Maintain citation metadata for all fetched media

**Custom images via image-generation skill** (when GEMINI_API_KEY available):
- Generate custom logos and branding elements
- Create unique illustrations not available in stock libraries
- Generate style-specific artwork (isometric, kawaii, minimalist, etc.)
- Fill gaps when fetch-media doesn't find suitable matches
- Save generated images to temp directory:
  - **Windows**: `$env:TEMP\generated-images\`
  - **Unix/macOS**: `/tmp/generated-images/`

**3D models:** Check working directory first, then use fetch-media for public repositories
</step_3>

<step_4>
**Speaker notes**: After generating each slide, prompt user:
"Would you like to add speaker notes for this slide? (These appear in presenter view)"
- Add notes as `<aside class="notes">` elements
- Support markdown formatting within notes
- Notes visible only in presenter view (press 'S' key)
</step_4>

<step_5>
**Widescreen configuration**: ALWAYS use 16:9 widescreen format
```javascript
Reveal.initialize({
  width: 1280,
  height: 720,
  margin: 0.04,
  minScale: 0.2,
  maxScale: 2.0,
  // ... other config
});
```
</step_5>

<step_6>
**Multimedia embedding**: Support for:
- **D3.js visualizations**: Use reveald3 plugin pattern (see [reference/d3-integration.md](reference/d3-integration.md))
- **Three.js 3D models**: Load GLB files with Three.js loader (see [reference/threejs-integration.md](reference/threejs-integration.md))
- **P5.js sketches**: Embed p5 canvas in slides (see [reference/p5js-integration.md](reference/p5js-integration.md))
- **SVG animations**: Inline SVG with CSS animations (see [reference/svg-animations.md](reference/svg-animations.md))
- **Video backgrounds**: `data-background-video` attribute
- **Animated media**: GIFs, APNGs, embedded videos
</step_6>

<step_7>
**Single-file deployment**: Generate standalone HTML
- Encode all images as BASE64 data URIs
- Inline all CSS (including reveal.js core and theme)
- Inline all JavaScript (including reveal.js and plugins)
- Result: One HTML file that works anywhere, no server required
- Ask user: "Generate single-file version with all assets embedded?"
</step_7>

<step_8>
**Presenter view script**: Create `present.js` Node.js launcher
```javascript
// Auto-opens presentation and presenter view
// Starts local server on port 8000
// Handles file serving and CORS
```
User runs: `node present.js` to launch presentation + speaker view
</step_8>
</workflow>

<slide_patterns>
When user opts for patterns, offer these pre-built structures (see [patterns/](patterns/)):

**Content Patterns**:
- `title-bullets` - Title with bullet points
- `image-caption` - Large image with caption
- `two-column` - Side-by-side content
- `comparison` - Side-by-side comparison with pros/cons
- `quote` - Large centered quote with attribution

**Data Patterns**:
- `infographic` - Visual data representation with icons and stats
- `timeline` - Horizontal or vertical timeline
- `chart` - Embedded Chart.js or D3.js visualization
- `data-grid` - Grid of statistics or metrics

**Special Patterns**:
- `team-intro` - Team member cards with photos
- `process-flow` - Step-by-step process diagram
- `full-background` - Full-slide background image with text overlay
- `video-background` - Full-slide video background

Each pattern includes responsive CSS and animation presets.
</slide_patterns>

<templates>
<template_structure>
Each template includes:
- **Base HTML structure**: reveal.js wrapper with proper nesting
- **Custom CSS theme**: Colors, fonts, spacing, animations
- **JavaScript config**: Reveal.js initialization with template-specific settings
- **Example slides**: 3-5 sample slides showing template features
- **Asset requirements**: Fonts, icons, background patterns

Templates are in `templates/{template-name}/` with:
- `index.html` - Full presentation template
- `theme.css` - Custom theme styles
- `config.js` - Reveal.js configuration
- `README.md` - Template documentation and customization guide
</template_structure>

<customization>
Allow users to customize templates:
- **Colors**: Primary, secondary, accent colors
- **Fonts**: Heading and body font families
- **Spacing**: Slide padding and margins
- **Animations**: Transition effects and timing
- **Background**: Solid color, gradient, image, or video

Use AskUserQuestion to offer customization after selecting base template.
</customization>
</templates>

<advanced_features>
**Full documentation in reference directory**:

- **D3.js integration**: [reference/d3-integration.md](reference/d3-integration.md)
  - Using reveald3 plugin for animated visualizations
  - Fragment transitions with D3 charts
  - Embedding external D3 HTML files

- **Three.js integration**: [reference/threejs-integration.md](reference/threejs-integration.md)
  - Loading and displaying GLB models
  - Interactive 3D controls
  - Animation and lighting
  - Camera positioning per slide

- **P5.js integration**: [reference/p5js-integration.md](reference/p5js-integration.md)
  - Embedding p5 sketches in slides
  - Controlling sketch lifecycle with reveal.js events
  - Per-slide sketch instances

- **SVG animations**: [reference/svg-animations.md](reference/svg-animations.md)
  - Line drawing animations with stroke-dasharray
  - Fragment reveal for SVG layers
  - CSS-based SVG animations

- **Theme customization**: [reference/theme-customization.md](reference/theme-customization.md)
  - Creating custom themes from scratch
  - Sass variables and mixins
  - CSS custom properties
  - Responsive design patterns

- **Speaker notes best practices**: [reference/speaker-notes.md](reference/speaker-notes.md)
  - Writing effective presenter notes
  - Timing information
  - Slide navigation tips
  - Multi-device setup (laptop + projector)

- **Deployment options**: [reference/deployment.md](reference/deployment.md)
  - Single-file HTML with BASE64
  - GitHub Pages hosting
  - Static site hosting (Netlify, Vercel)
  - PDF export
</advanced_features>

<fetch_media_integration>
**CRITICAL**: ALWAYS use the fetch-media skill for image acquisition

<automatic_process>
1. **Analyze slide content**: Identify slides needing visual support
2. **Generate search queries**: Create specific search terms for each slide
3. **Use Skill tool**: `Skill({skill: "fetch-media"})`
4. **Pass search query**: E.g., "search for quantum computer chip high resolution"
5. **Download images**: fetch-media handles search and download
6. **Get file paths**: Receive local paths to downloaded images
7. **Encode BASE64**: Read image files and convert to data URIs
8. **Embed in HTML**: Insert as `<img src="data:image/...">` or backgrounds
</automatic_process>

<example_usage>
For a slide about climate change:
```
Skill({skill: "fetch-media"})
Search query: "climate change effects melting glacier"
→ Downloads: glacier-melting.jpg
→ Convert to BASE64
→ Embed: <img src="data:image/jpeg;base64,/9j/4AAQ...">
```
</example_usage>

<citations>
Include image citations in speaker notes:
```html
<aside class="notes">
  Image: "Melting Glacier" from Wikimedia Commons (CC BY 4.0)
  Source: fetch-media skill search results
</aside>
```
</citations>
</fetch_media_integration>

<image_generation_integration>
**Use image-generation skill for custom AI-generated images**

<when_to_use>
Invoke image-generation skill when:
- **Custom branding**: Logos, icons, branded graphics specific to the presentation
- **Unique concepts**: Abstract ideas, future scenarios, imaginary scenes not in stock libraries
- **Text in images**: When specific text needs to appear in the image itself (Gemini excels at this)
- **Style-specific artwork**: Particular artistic styles (isometric, kawaii, minimalist, neon, etc.)
- **Gap-filling**: After fetch-media, when specific slides still lack suitable imagery
- **User request**: When user explicitly asks for AI-generated/custom images
</when_to_use>

<prerequisites>
- image-generation skill installed in user's Claude skills directory
- GEMINI_API_KEY in `.env` file or environment variable
- Python dependencies: `pip install google-genai Pillow python-dotenv`

Check availability:
```powershell
# Windows PowerShell
Test-Path "$HOME\.claude\skills\image-generation\SKILL.md"
Get-Content "$HOME\.claude\skills\image-generation\.env" | Select-String "GEMINI"
```
```bash
# Unix/macOS
ls ~/.claude/skills/image-generation/SKILL.md
cat ~/.claude/skills/image-generation/.env | grep GEMINI
```
</prerequisites>

<workflow>
1. **Identify slides needing custom imagery**: Title slides, branded content, unique concepts
2. **Generate descriptive prompts**: Include style, colors, composition details
3. **Invoke skill**: `Skill({skill: "image-generation"})`
4. **Pass prompt**: E.g., "Create a modern minimalist logo with text 'TechCon 2025', blue gradient"
5. **Receive image path**: Generated image saved to temp directory (platform-specific)
6. **Encode BASE64**: Read image and convert to data URI
7. **Embed in HTML**: Insert as `<img src="data:image/png;base64,...">` or background
</workflow>

<prompt_examples>
**Logo generation:**
```
Skill({skill: "image-generation"})
Prompt: "Clean modern logo with text 'EcoSummit', leaf icon integrated into text, green gradient on white background, minimalist sans-serif font"
→ Saves to: <temp-dir>/generated-images/generated_<timestamp>_ecosummit_logo.png
```

**Presentation slide background:**
```
Skill({skill: "image-generation"})
Prompt: "Abstract technology background, dark blue with glowing network nodes, subtle grid pattern, 16:9 aspect ratio for presentation slide"
→ Saves to: <temp-dir>/generated-images/generated_<timestamp>_tech_background.png
```

**Conceptual illustration:**
```
Skill({skill: "image-generation"})
Prompt: "Isometric illustration of smart city with solar panels on buildings, electric vehicles, green spaces, soft pastel colors, clean lines"
→ Saves to: <temp-dir>/generated-images/generated_<timestamp>_smart_city.png
```

**Stylized diagram:**
```
Skill({skill: "image-generation"})
Prompt: "Professional presentation slide showing 3-step process: Research → Design → Launch, modern flat icons, blue and orange color scheme, dark background"
→ Saves to: <temp-dir>/generated-images/generated_<timestamp>_process_diagram.png
```

**Note**: `<temp-dir>` is `$env:TEMP` on Windows or `/tmp` on Unix/macOS
</prompt_examples>

<integration_with_base64>
After generating images, encode for single-file deployment:
```javascript
// In Node.js generation script (cross-platform)
const fs = require('fs');
const path = require('path');
const os = require('os');

// Get temp directory (works on Windows, macOS, Linux)
const tempDir = os.tmpdir();
const generatedImagesDir = path.join(tempDir, 'generated-images');

function encodeGeneratedImage(imagePath) {
  const imageBuffer = fs.readFileSync(imagePath);
  const base64 = imageBuffer.toString('base64');
  const ext = path.extname(imagePath).slice(1);
  return `data:image/${ext};base64,${base64}`;
}

// Usage (cross-platform path)
const logoPath = path.join(generatedImagesDir, 'generated_123_logo.png');
const logoDataUri = encodeGeneratedImage(logoPath);
// Insert into HTML: <img src="${logoDataUri}" alt="Presentation Logo">
```
</integration_with_base64>

<citations>
Note AI-generated images in speaker notes:
```html
<aside class="notes">
  Logo: AI-generated via image-generation skill (Gemini)
  Prompt: "Clean modern logo with text 'TechCon 2025'..."
</aside>
```
</citations>
</image_generation_integration>

<presenter_view_setup>
**Local server required for presenter view**

<script_generation>
Copy the launcher script from [scripts/present.js](scripts/present.js) to the presentation root directory.

The script provides:
- HTTP server on configurable port (default: 8000)
- MIME type handling for all media formats
- Auto-opens browser with presentation
- Cross-platform support (Windows, macOS, Linux)

**Launch presentation:**
```powershell
# Windows PowerShell
node present.js [port] [filename]
```
```bash
# Unix/macOS
chmod +x present.js  # Make executable (first time only)
node present.js [port] [filename]
```
</script_generation>

<keyboard_shortcuts>
- `S` - Open speaker view (put on laptop, main presentation on projector)
- `F` - Fullscreen
- `O` - Overview mode
- `Arrow keys` - Navigate slides
- `ESC` - Exit fullscreen/overview
</keyboard_shortcuts>

<single_file_note>
Single-file standalone HTML works without server but speaker view requires `present.js` server.
</single_file_note>
</presenter_view_setup>

<validation>
<checklist>
Before delivering presentation to user, verify:

- [ ] reveal.js properly initialized with widescreen config (1280x720)
- [ ] Selected template applied with custom CSS loaded
- [ ] **Stock images fetched via fetch-media skill and embedded**
- [ ] **Custom images generated via image-generation skill** (for logos, branding, unique concepts)
- [ ] Images encoded as BASE64 in single-file version
- [ ] Speaker notes added to slides (if user provided)
- [ ] D3/Three.js/P5.js/SVG embeds working (if applicable)
- [ ] Video backgrounds autoplay correctly (if applicable)
- [ ] `present.js` launcher script created and tested
- [ ] README with launch instructions included
- [ ] Both multi-file and single-file versions generated
- [ ] All slide transitions smooth and working
- [ ] Responsive design works at different screen sizes
- [ ] No console errors when opening presentation
- [ ] Speaker view opens with 'S' key
- [ ] **Citations included for fetch-media images**
- [ ] **AI-generation noted for image-generation images**
</checklist>

<testing_procedure>
1. **Open presentation**: Run `node present.js`
2. **Test navigation**: Arrow keys work, slide transitions smooth
3. **Test speaker view**: Press 'S', verify notes and timer appear
4. **Test single-file**: Open standalone HTML, verify all assets load
5. **Test interactivity**: D3/Three.js/P5.js elements interactive
6. **Test responsive**: Resize browser, verify layout adapts
7. **Test on different browsers**: Chrome, Firefox, Safari
</testing_procedure>
</validation>

<anti_patterns>
**Avoid these common mistakes**:

❌ Using external image URLs without BASE64 encoding (breaks offline use)
✅ Always fetch images and encode as BASE64 data URIs

❌ Hardcoding file:// paths (won't work in single-file version)
✅ Use relative paths or data URIs

❌ Forgetting to prompt for speaker notes
✅ Always ask user for presenter notes after generating slides

❌ Using default 960x700 resolution (not widescreen)
✅ Always configure 1280x720 for 16:9 aspect ratio

❌ Skipping fetch-media skill and manually adding images
✅ ALWAYS use fetch-media skill for automatic image acquisition

❌ Not testing presenter view before delivery
✅ Always test with `present.js` and verify speaker view works

❌ Forgetting platform-specific setup
✅ On Unix/macOS: Include `chmod +x present.js` in README
✅ On Windows: Just run `node present.js` directly (no chmod needed)

❌ Using complex D3/Three.js without fallbacks
✅ Test on lower-powered devices, provide static alternatives

❌ Adding too much content per slide (causes overflow)
✅ Limit to 5-6 bullet points, keep images under 500px height, use concise text

❌ Using excessively large fonts or headings
✅ Templates use optimized sizes (28px base, 1.8-2.8em headings) with scrolling fallback

❌ Using generic stock images when custom branding is needed
✅ Use image-generation skill for logos, branded graphics, and unique concepts

❌ Skipping image-generation when user requests custom artwork
✅ Check GEMINI_API_KEY availability and invoke image-generation for custom visuals
</anti_patterns>

<common_patterns>
See [reference/code-patterns.md](reference/code-patterns.md) for complete code examples including:
- **basic_presentation**: Full HTML structure with reveal.js widescreen setup
- **image_base64**: Converting images to BASE64 data URIs
- **d3_embed**: D3.js visualization with reveald3 plugin
- **threejs_embed**: Three.js 3D model loading and display
- **video_background**: Video background slide patterns
- **fragment_animations**: Progressive reveal animations
- **two_column_layout**: Side-by-side content layout

Quick reference for widescreen initialization:
```javascript
Reveal.initialize({
  width: 1280,
  height: 720,
  margin: 0.04,
  plugins: [RevealNotes, RevealHighlight]
});
```
</common_patterns>

<success_criteria>
A successful reveal.js presentation includes:

✅ **Professional appearance**: Clean template with consistent styling
✅ **Widescreen format**: 1280x720 (16:9 aspect ratio)
✅ **Rich media from multiple sources**:
   - Stock images via fetch-media skill
   - **Custom AI-generated images via image-generation skill** (logos, branding, unique visuals)
✅ **Speaker notes**: Presenter notes on all key slides
✅ **Interactive elements**: D3/Three.js/P5.js visualizations (if applicable)
✅ **Smooth transitions**: Tested slide animations and fragment reveals
✅ **Deployment ready**: Both multi-file and single-file versions
✅ **Easy to present**: `present.js` script for one-command launch
✅ **Well documented**: README with instructions and shortcuts
✅ **Accessible**: Works offline, no external dependencies in standalone version
✅ **Responsive**: Adapts to different screen sizes
✅ **Cross-browser**: Tested in Chrome, Firefox, Safari
✅ **Proper attribution**: Stock image citations + AI-generation notes in speaker notes
</success_criteria>

<reference_guides>
For detailed information, see reference directory:

- [templates/README.md](templates/README.md) - Template gallery and customization
- [patterns/README.md](patterns/README.md) - Pre-built slide patterns
- [reference/code-patterns.md](reference/code-patterns.md) - HTML/JS code examples
- [reference/d3-integration.md](reference/d3-integration.md) - D3.js embedding guide
- [reference/threejs-integration.md](reference/threejs-integration.md) - Three.js 3D models
- [reference/p5js-integration.md](reference/p5js-integration.md) - P5.js sketches
- [reference/svg-animations.md](reference/svg-animations.md) - SVG animation techniques
- [reference/theme-customization.md](reference/theme-customization.md) - Creating custom themes
- [reference/speaker-notes.md](reference/speaker-notes.md) - Writing effective notes
- [reference/deployment.md](reference/deployment.md) - Publishing presentations
- [scripts/present.js](scripts/present.js) - Presentation launcher script
- [examples/](examples/) - Complete example presentations

**External resources**:
- [reveal.js Official Documentation](https://revealjs.com/)
- [reveal.js GitHub Repository](https://github.com/hakimel/reveal.js)
- [reveald3 Plugin](https://github.com/gcalmettes/reveal.js-d3)

**Related skills**:
- **fetch-media skill**: `Skill({skill: "fetch-media"})` - Stock image search and download
- **image-generation skill**: `Skill({skill: "image-generation"})` - AI-generated custom images (requires GEMINI_API_KEY)
</reference_guides>
