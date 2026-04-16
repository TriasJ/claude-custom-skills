# Quantum Dark Template

A modern, tech-focused reveal.js presentation template with dark background and vibrant teal/blue accents.

## Overview

**Category**: Modern
**Style**: Dark background with electric teal (#00FFF5) and cyber blue (#0080FF) accents
**Best For**: Tech presentations, developer talks, scientific content, product launches

## Features

- ✨ Animated tech grid background
- 🎨 Vibrant teal and blue color scheme
- 💻 Optimized code syntax highlighting (Monokai theme)
- 📊 Statistics grid with animated cards
- 🎯 Process flow diagrams
- 🎬 Video background support
- 📝 Clean typography with Inter font
- 🔤 Monospace code font (Fira Code)
- 📱 Fully responsive design
- 🌐 16:9 widescreen format (1280x720)

## Color Palette

```css
--background-color: #0a0a0a (Deep Black)
--text-color: #e0e0e0 (Light Gray)
--heading-color: #ffffff (White)
--teal-accent: #00FFF5 (Electric Teal)
--blue-accent: #0080FF (Cyber Blue)
--purple-accent: #B026FF (Neon Purple)
--success-color: #00FF41 (Matrix Green)
```

## Typography

- **Headings**: Inter (Sans-serif, weight 600-700)
- **Body**: Inter (Sans-serif, weight 300-400)
- **Code**: Fira Code (Monospace with ligatures)

## Customization

### Changing Colors

Edit the CSS variables in `theme.css`:

```css
:root {
  --teal-accent: #YOUR_COLOR;
  --blue-accent: #YOUR_COLOR;
}
```

### Changing Fonts

Update the Google Fonts link and CSS variables:

```html
<link href="https://fonts.googleapis.com/css2?family=YourFont" rel="stylesheet">
```

```css
:root {
  --heading-font: 'YourFont', sans-serif;
  --body-font: 'YourFont', sans-serif;
}
```

### Adding Custom Animations

The template includes a `glow-pulse` animation. Add your own:

```css
@keyframes your-animation {
  from { /* start state */ }
  to { /* end state */ }
}

.your-class {
  animation: your-animation 2s ease-in-out infinite;
}
```

## Available Slide Patterns

### Title Slide
- Large glowing heading
- Subtitle with teal accent
- Author info with icon
- Tech grid background

### Content Slide
- Heading with icon
- Bullet points with custom markers
- Two-column layout option

### Code Slide
- Syntax highlighting (Monokai theme)
- Line number highlighting
- Support for multiple languages

### Statistics Grid
- 2x2 or 4-column grid
- Icon + Number + Label pattern
- Hover animations
- Fragment reveals

### Quote Slide
- Centered large quote
- Attribution
- Minimal distractions

### Image Slide
- Full-width or contained images
- Border with teal accent
- Caption support
- Overlay text option

### Process Flow
- Horizontal step-by-step layout
- Numbered circles
- Arrow connectors
- Fragment animations

### Video Background
- Full-slide video loops
- Overlay content container
- Blur backdrop effect

### Call to Action
- Centered content
- Button group (primary/secondary)
- Gradient button effects

## Usage in Skill

The create-revealjs-presentations skill will:

1. Use this template when user selects "modern" style
2. Generate slides using the pre-built patterns
3. Fetch and embed relevant tech imagery
4. Add speaker notes
5. Create single-file version with BASE64 assets
6. Generate `present.js` launcher script

## File Structure

```
quantum-dark/
├── index.html          # Main template with example slides
├── theme.css           # Custom theme styles
├── config.js           # reveal.js configuration
├── README.md          # This file
└── assets/            # Template assets
    ├── fonts/         # (Optional) Custom fonts
    ├── images/        # (Optional) Template images
    └── scripts/       # (Optional) Custom JavaScript
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Dependencies

All dependencies loaded via CDN (no local installation required):

- reveal.js 5.0.4
- Font Awesome 6.5.1
- Google Fonts (Inter, Fira Code)

## License

This template is part of the create-revealjs-presentations skill.
Free to use and customize for your presentations.

## Tips for Best Results

1. **Images**: Use high-resolution tech/abstract imagery
2. **Code**: Keep code blocks concise (< 15 lines visible)
3. **Animations**: Use fragments sparingly for impact
4. **Colors**: Stick to the teal/blue palette for consistency
5. **Content**: Maximum 5-6 bullet points per slide
6. **Videos**: Keep background videos short and looped
7. **Speaker Notes**: Add detailed notes for all slides

## Keyboard Shortcuts

- `S` - Open speaker view
- `F` - Fullscreen
- `O` - Overview mode
- `Arrow keys` - Navigate
- `ESC` - Exit fullscreen/overview
- `?` - Show keyboard shortcuts help

## Presenting

1. Run `node present.js` to start local server
2. Presentation opens automatically
3. Press `S` to open speaker view
4. Put speaker view on laptop, presentation on projector
5. Navigate with arrow keys or remote clicker

---

Created with ❤️ for the reveal.js community
