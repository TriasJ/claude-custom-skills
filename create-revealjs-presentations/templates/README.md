# reveal.js Presentation Templates

This directory contains 9 professionally designed reveal.js templates categorized by style.

## Template Categories

### Creative Templates (3)

#### 1. Neon Glow
**Style**: Vibrant gradients, animated backgrounds, bold typography
**Best for**: Tech launches, creative showcases, design presentations
**Colors**: Electric blue (#00D9FF), hot pink (#FF0080), purple (#9D00FF)
**Features**:
- Animated gradient backgrounds
- Neon text effects with glow
- Smooth color transitions
- Modern sans-serif typography (Inter)

#### 2. Paper Craft
**Style**: 3D paper textures, shadow effects, organic feel
**Best for**: Educational content, workshops, storytelling
**Colors**: Warm beige (#F5E6D3), terracotta (#D4754E), forest green (#4A7C59)
**Features**:
- Layered paper textures
- Drop shadow depth effects
- Organic shapes and rounded corners
- Handwriting-style accents (Caveat font)

#### 3. Liquid Motion
**Style**: Fluid animations, morphing shapes, dynamic colors
**Best for**: Brand presentations, product launches, creative pitches
**Colors**: Ocean blue (#0066CC), turquoise (#00C9B7), coral (#FF6B6B)
**Features**:
- SVG blob animations
- Smooth morphing transitions
- Glassmorphism effects
- Circular element patterns

### Professional Templates (2)

#### 4. Corporate Blue
**Style**: Clean lines, corporate blue palette, professional spacing
**Best for**: Business meetings, corporate reports, client presentations
**Colors**: Navy (#003d7a), light blue (#4A90E2), silver (#F5F7FA)
**Features**:
- Clean grid layouts
- Professional iconography
- Data visualization friendly
- Sans-serif typography (Roboto)

#### 5. Executive Minimal
**Style**: Ultra-minimal, high contrast, serif typography
**Best for**: Executive briefings, strategy presentations, board meetings
**Colors**: Charcoal (#2C2C2C), white (#FFFFFF), gold accent (#D4AF37)
**Features**:
- Maximum whitespace
- High contrast ratios
- Elegant serif fonts (Playfair Display)
- Subtle animations only

### Modern Templates (4)

#### 6. Quantum Dark 🌟
**Style**: Black background, teal/blue accents, tech-forward
**Best for**: Tech presentations, developer talks, scientific content
**Colors**: Deep black (#0a0a0a), electric teal (#00FFF5), cyber blue (#0080FF)
**Features**:
- Dark mode optimized
- Code syntax highlighting
- Tech-inspired grid patterns
- Monospace accents (Fira Code)

#### 7. Wireframe Tech 🌀
**Style**: Animated 3D wireframe torus background, cyberpunk aesthetic
**Best for**: Futuristic demos, tech conferences, creative showcases
**Colors**: Deep navy (#050510), electric cyan (#00ffff), vibrant magenta (#ff00ff)
**Features**:
- Three.js powered 3D wireframe torus animation
- Dual-torus design with depth effect
- Optional particle field
- Mouse parallax interaction
- Hardware-accelerated WebGL (60fps)
- Glitch text effects
- Orbitron futuristic font

#### 8. Glass Morphism
**Style**: Frosted glass effects, soft shadows, modern UI
**Best for**: UI/UX presentations, modern product showcases, design systems
**Colors**: Soft purple (#A78BFA), pink (#F472B6), blue (#60A5FA)
**Features**:
- Frosted glass blur effects
- Soft gradient overlays
- Rounded modern shapes
- Light/airy feel

#### 9. Cyber Grid
**Style**: Grid patterns, neon accents, futuristic aesthetic
**Best for**: Tech conferences, cybersecurity, gaming, sci-fi themes
**Colors**: Matrix green (#00FF41), cyber purple (#B026FF), electric blue (#00D9FF)
**Features**:
- Animated grid backgrounds
- Glitch text effects
- Neon line accents
- Futuristic UI elements

## Template Structure

Each template directory contains:

```
template-name/
├── index.html          # Full presentation template
├── theme.css           # Custom theme styles
├── config.js           # Reveal.js configuration
├── README.md           # Template documentation
└── assets/            # Template-specific assets
    ├── fonts/         # Custom fonts
    ├── images/        # Background patterns, icons
    └── scripts/       # Template-specific JavaScript
```

## Customization

All templates support customization via CSS variables:

```css
:root {
  --primary-color: #your-color;
  --secondary-color: #your-color;
  --accent-color: #your-color;
  --heading-font: 'Your Font', sans-serif;
  --body-font: 'Your Font', sans-serif;
  --slide-padding: 60px;
  --transition-speed: 0.3s;
}
```

## Usage in Skill

When creating presentations, the skill will:

1. Ask user for preferred template style (creative/professional/modern)
2. Present 2-3 options from that category
3. Generate presentation using selected template
4. Offer customization options (colors, fonts)
5. Apply template-specific animations and styles

## Adding New Templates

To add a new template:

1. Create directory: `templates/your-template-name/`
2. Copy structure from existing template
3. Customize `theme.css` with your styles
4. Update `config.js` with template-specific settings
5. Add example slides in `index.html`
6. Document in template's README.md
7. Update this README with template description

## CDN Resources

All templates use these CDN resources for zero-dependency deployment:

- **reveal.js**: `https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/`
- **Font Awesome**: `https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.1/`
- **Google Fonts**: `https://fonts.googleapis.com/`
- **Three.js** (Wireframe Tech only): `https://cdn.jsdelivr.net/npm/three@0.160.0/`

For single-file deployment, the skill automatically inlines all CDN resources as BASE64.
