# Usage Guide: create-revealjs-presentations Skill

Quick guide to creating stunning reveal.js presentations with this skill.

## Quick Start

### Method 1: Using Slash Command (Easiest)

```
/create-revealjs-presentation Create a presentation about quantum computing
```

### Method 2: Direct Skill Invocation

In your conversation with Claude:
```
Create a presentation about artificial intelligence using reveal.js
```

Claude will automatically invoke this skill if you mention:
- "presentation"
- "slides"
- "reveal.js"
- "HTML presentation"

## What Happens Next

The skill will guide you through:

1. **Template Selection**
   - Choose from 8 professionally designed templates
   - Options: Creative, Professional, or Modern styles

2. **Slide Structure**
   - Confirm number of slides
   - Select pre-built patterns (optional)

3. **Media Fetching**
   - Automatically searches for relevant images
   - Downloads and embeds as BASE64

4. **Speaker Notes**
   - Prompted to add notes for each slide
   - Appears only in presenter view

5. **Final Output**
   - Multi-file version (with assets folder)
   - Single-file standalone HTML
   - `present.js` launcher script
   - README with instructions

## Example Workflows

### Example 1: Tech Presentation

**Input:**
```
Create a 10-slide presentation about blockchain technology for developers.
Use a modern template with dark background.
```

**Skill Actions:**
1. Selects Quantum Dark template (black bg, teal/blue accents)
2. Generates 10 slides covering blockchain basics
3. Uses fetch-media to find blockchain diagrams
4. Prompts for speaker notes on each slide
5. Creates final package with:
   - `blockchain-presentation.html` (single file)
   - `blockchain-presentation/` (source folder)
   - `present.js` (launcher)
   - `README.md` (instructions)

**To Present:**
```powershell
# Windows PowerShell
cd blockchain-presentation
node present.js
# Press 'S' in browser to open speaker view
```
```bash
# Unix/macOS
cd blockchain-presentation
node present.js
# Press 'S' in browser to open speaker view
```

### Example 2: Business Pitch

**Input:**
```
Create a business pitch presentation with:
- Executive minimal template
- 8 slides total
- Include statistics, team intro, and roadmap
```

**Skill Actions:**
1. Selects Executive Minimal template
2. Uses pre-built patterns:
   - Infographic for statistics
   - Team Intro for team slide
   - Timeline for roadmap
3. Fetches professional images
4. Generates polished business presentation

### Example 3: Data Visualization

**Input:**
```
Create a presentation showing Q4 sales data with interactive charts.
Include D3.js visualizations.
```

**Skill Actions:**
1. Selects appropriate template
2. Generates D3.js chart HTML files
3. Embeds charts with reveald3 plugin
4. Creates interactive, animated visualizations
5. Adds fragment transitions for progressive disclosure

### Example 4: 3D Product Showcase

**Input:**
```
Create a product presentation with 3D model viewer.
I have product.glb in my working directory.
```

**Skill Actions:**
1. Detects GLB file in directory
2. Generates Three.js scene setup
3. Creates interactive 3D viewer slide
4. Adds orbit controls (drag to rotate, scroll to zoom)
5. Includes lighting and materials optimized for product display

## Customization After Generation

### Changing Colors

Edit the CSS variables in your presentation:

```css
:root {
  --teal-accent: #YOUR_COLOR;
  --blue-accent: #YOUR_COLOR;
  --background-color: #YOUR_COLOR;
}
```

### Adding More Slides

Copy existing slide section and modify:

```html
<section>
  <h2>Your New Slide</h2>
  <p>Your content here</p>
  <aside class="notes">
    Your speaker notes here
  </aside>
</section>
```

### Changing Template

The skill can regenerate with a different template:
```
Regenerate this presentation using the Neon Glow template instead
```

## Features You Get Automatically

✅ **Widescreen 16:9** (1280x720) - Perfect for modern displays
✅ **Speaker Notes** - Press 'S' to open presenter view
✅ **Auto-embedded Media** - All images as BASE64
✅ **Single-file Option** - Works anywhere, no server needed
✅ **Responsive Design** - Works on all screen sizes
✅ **Fragment Animations** - Progressive content reveal
✅ **Interactive Elements** - D3/Three.js/P5.js support
✅ **Video Backgrounds** - Dynamic video slides
✅ **Code Highlighting** - Syntax-highlighted code blocks
✅ **Custom Icons** - Font Awesome integration
✅ **Presenter Script** - One-command launch

## Keyboard Shortcuts (While Presenting)

- `S` - Open speaker view
- `F` - Fullscreen mode
- `O` - Overview mode (slide grid)
- `Arrow Keys` - Navigate slides
- `ESC` - Exit fullscreen/overview
- `?` - Show all shortcuts
- `B` or `.` - Pause (black screen)
- `Alt+Click` - Zoom in on element (requires Zoom plugin)

## Tips for Best Presentations

1. **Keep it concise**: Max 5-6 points per slide
2. **Use fragments**: Reveal content progressively
3. **High-quality images**: Use fetch-media for professional photos
4. **Practice with timer**: Speaker view shows elapsed time
5. **Test beforehand**: Run through once before presenting
6. **Backup plan**: Have single-file HTML ready
7. **Check projector**: Test resolution before event
8. **Use speaker notes**: Don't memorize, use notes effectively

## Troubleshooting

### "Cannot read property 'initialize' of undefined"
**Solution**: Ensure reveal.js CDN is accessible. Check internet connection or use offline version.

### Speaker view not opening
**Solution**: Must use local server (`node present.js`). File protocol (file://) doesn't support speaker view.

### Images not showing in single-file version
**Solution**: Skill automatically encodes as BASE64. If manual images, ensure they're properly encoded.

### 3D model not loading
**Solution**:
- Check file path is correct
- Ensure model is .glb format
- Use local server (required for file loading)
- Check console for CORS errors

### Presentation looks small on projector
**Solution**: Press 'F' for fullscreen. Presentation auto-scales to fit display.

## Getting Help

1. **Check README.md** in your presentation folder
2. **Consult reference docs** in skill's reference/ directory
3. **Ask Claude**: "How do I [specific task] in my reveal.js presentation?"
4. **reveal.js Docs**: https://revealjs.com/
5. **GitHub Issues**: https://github.com/hakimel/reveal.js/issues

## Advanced Usage

### Custom D3 Visualizations

```
Add an interactive D3 force-directed graph showing our team relationships
```

### Custom Three.js Scenes

```
Create a Three.js slide showing our product exploding into components
```

### Video Backgrounds

```
Add a looping video background to the intro slide using this URL: [url]
```

### Custom Animations

```
Add a slide transition animation that uses a circular wipe effect
```

## What's Included in Output

When the skill finishes, you'll receive:

```
your-presentation/
├── index.html                  # Multi-file version
├── presentation-standalone.html # Single-file version
├── present.js                  # Launcher script
├── README.md                   # Usage instructions
├── assets/                     # Media files
│   ├── images/
│   └── videos/
├── visualizations/             # D3 charts (if applicable)
└── models/                     # 3D models (if applicable)
```

## Next Steps

After receiving your presentation:

1. **Review content**: Check all slides for accuracy
2. **Test locally**: Run `node present.js`
3. **Practice delivery**: Use speaker notes and timer
4. **Share single-file**: Email `presentation-standalone.html` to others
5. **Publish online**: Upload to GitHub Pages, Netlify, or Vercel
6. **Export PDF**: Use browser print with CSS media

---

**Happy Presenting! 🎉**

Created with the create-revealjs-presentations skill for Claude Code.
