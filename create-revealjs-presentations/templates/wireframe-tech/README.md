# Wireframe Tech Template

A cutting-edge reveal.js presentation template featuring an animated 3D wireframe torus background powered by Three.js.

## Overview

**Category**: Modern/Creative
**Style**: Animated 3D wireframe background with cyan/magenta accents
**Best For**: Tech presentations, futuristic demos, developer conferences, creative showcases

## Features

- 🌀 **Animated 3D Wireframe Torus** - Continuously rotating in the background
- ✨ **Particle Effects** - Optional floating particles for atmosphere
- 🎨 **Dual-torus Design** - Two concentric toruses for depth
- 🖱️ **Mouse Parallax** - Subtle interaction following mouse movement
- 🎯 **Hardware Accelerated** - WebGL-powered for smooth 60fps animation
- 🎭 **Glitch Text Effect** - Cyberpunk-style text animations
- 💫 **Gradient Buttons** - Cyan-to-magenta gradient accents
- 📱 **Fully Responsive** - 3D background adapts to all screen sizes
- 🌐 **16:9 Widescreen** - Optimized for modern displays (1280x720)

## Color Palette

```css
--background-color: #050510 (Deep Navy)
--text-color: #e0e0e0 (Light Gray)
--heading-color: #ffffff (White)
--cyan-accent: #00ffff (Electric Cyan)
--magenta-accent: #ff00ff (Vibrant Magenta)
--blue-accent: #0066ff (Bright Blue)
--green-accent: #00ff88 (Neon Green)
```

## Typography

- **Headings**: Orbitron (Futuristic, geometric sans-serif)
- **Body**: Rajdhani (Modern, technical sans-serif)
- **Code**: Fira Code (Monospace with programming ligatures)

## File Structure

```
wireframe-tech/
├── index.html              # Main template with example slides
├── theme.css               # Custom theme styles
├── config.js               # reveal.js configuration
├── README.md              # This file
└── assets/
    └── scripts/
        └── wireframe-background.js  # 3D torus animation logic
```

## Customization

### Changing Torus Colors

Edit `assets/scripts/wireframe-background.js`:

```javascript
const CONFIG = {
  wireframeColor: 0x00ffff,  // Main torus color (hex)
  pointLightColor: 0xff00ff, // Secondary torus color (hex)
  // ...
};
```

Or dynamically via JavaScript:

```javascript
// Change color on specific slide
WireframeBackground.setColor(0xff0000); // Red torus
```

### Adjusting Animation Speed

In `wireframe-background.js`:

```javascript
const CONFIG = {
  rotationX: 0.003,  // Faster/slower X rotation
  rotationY: 0.005,  // Faster/slower Y rotation
  rotationZ: 0.002,  // Faster/slower Z rotation
  // ...
};
```

Or dynamically:

```javascript
WireframeBackground.setRotationSpeed(0.01, 0.01, 0.01); // Faster
WireframeBackground.setRotationSpeed(0.001, 0.001, 0.001); // Slower
```

### Toggling Particles

```javascript
WireframeBackground.toggleParticles(); // Show/hide particle effects
```

### Changing Torus Geometry

In `wireframe-background.js`:

```javascript
const CONFIG = {
  torusRadius: 2.5,        // Main radius (larger = bigger torus)
  tubeRadius: 0.8,         // Tube thickness
  radialSegments: 24,      // Detail level (lower = more angular)
  tubularSegments: 120,    // Smoothness (higher = rounder)
  // ...
};
```

### Per-Slide Color Changes

Add `data-torus-color` attribute to slides:

```html
<section data-torus-color="ff0000">
  <h2>This slide has a red torus!</h2>
</section>
```

### Disabling 3D Background

If you want to use the theme without the 3D background:

1. Remove the canvas: `<canvas id="wireframe-canvas"></canvas>`
2. Remove the script: `<script src="assets/scripts/wireframe-background.js"></script>`
3. Update CSS: Change `.reveal .slides section` background to solid color

## Performance Tips

### High Performance (Default)
- 60fps on modern hardware
- ~5% CPU usage
- Hardware-accelerated WebGL

### Lower-End Devices

Reduce complexity in `wireframe-background.js`:

```javascript
const CONFIG = {
  radialSegments: 16,      // Lower = better performance
  tubularSegments: 80,     // Lower = better performance
  enableParticles: false,  // Disable particles
  particleCount: 100,      // Fewer particles if enabled
  // ...
};
```

### Mobile Optimization

The template automatically reduces quality on smaller screens. You can further optimize:

```javascript
// Detect mobile and adjust settings
if (window.innerWidth < 768) {
  CONFIG.radialSegments = 12;
  CONFIG.tubularSegments = 60;
  CONFIG.enableParticles = false;
}
```

## Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest - with WebGL support)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)
- ⚠️ Older browsers may not support WebGL (fallback to solid background)

## Dependencies

All loaded via CDN (no local installation):

- **reveal.js** 5.0.4
- **Three.js** 0.160.0
- **Font Awesome** 6.5.1
- **Google Fonts** (Orbitron, Rajdhani)

## Usage in Skill

When the create-revealjs-presentations skill uses this template:

1. Automatically includes 3D wireframe background
2. Generates slides with cyberpunk/tech aesthetic
3. Fetches relevant tech imagery via fetch-media
4. Optimizes for widescreen presentation
5. Creates single-file version (3D works in standalone HTML)
6. Generates launcher script for presenter view

## Advanced Customization

### Custom Geometry

Replace torus with other shapes in `wireframe-background.js`:

```javascript
// Sphere instead of torus
const geometry = new THREE.SphereGeometry(3, 32, 32);

// Icosahedron (20-sided polygon)
const geometry = new THREE.IcosahedronGeometry(3, 1);

// Knot (complex twisted shape)
const geometry = new THREE.TorusKnotGeometry(2, 0.5, 100, 16);

// Custom shape from vertices
const geometry = new THREE.BufferGeometry();
// ... define vertices
```

### Multiple Shapes

Add more objects to the scene:

```javascript
// Add a sphere
const sphereGeometry = new THREE.SphereGeometry(1, 32, 32);
const sphereMaterial = new THREE.MeshBasicMaterial({
  color: 0x00ff88,
  wireframe: true
});
const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
sphere.position.x = 4;
scene.add(sphere);
```

### Pulsing Effect

Add breathing animation:

```javascript
function animate() {
  requestAnimationFrame(animate);

  // Pulsing effect
  const time = Date.now() * 0.001;
  const scale = 1 + Math.sin(time) * 0.1;
  torus.scale.set(scale, scale, scale);

  // ... rest of animation code
}
```

### Camera Movement

Animate camera for dramatic effect:

```javascript
function animate() {
  requestAnimationFrame(animate);

  // Orbital camera movement
  const time = Date.now() * 0.0001;
  camera.position.x = Math.sin(time) * 10;
  camera.position.z = Math.cos(time) * 10;
  camera.lookAt(scene.position);

  // ... rest of animation code
}
```

## Troubleshooting

### Canvas not appearing
- Ensure Three.js CDN is loaded before wireframe-background.js
- Check browser console for WebGL errors
- Verify browser supports WebGL (chrome://gpu/)

### Low frame rate
- Reduce geometry complexity (lower segment counts)
- Disable particles
- Check GPU usage in browser dev tools

### Torus disappears on some slides
- Ensure canvas has z-index: -1 in CSS
- Check that slide backgrounds aren't covering canvas
- Verify canvas is positioned fixed

### Mobile issues
- Reduce complexity for mobile devices
- Test on actual device, not just browser resize
- Check mobile GPU support

## Examples

### Tech Conference Talk
Perfect for developer conferences, tech demos, and futuristic product launches.

### Creative Portfolio
Showcase creative work with engaging 3D background.

### Data Visualization
Present data with tech-forward aesthetic that emphasizes innovation.

### Educational Content
Teach technical concepts with visually engaging presentations.

## Tips for Best Results

1. **Keep content concise**: The 3D background is eye-catching, so less text is more
2. **High contrast**: Use bright text on the semi-transparent slides
3. **Limit animations**: The background provides motion; avoid too many slide animations
4. **Test on target hardware**: Ensure smooth performance on presentation device
5. **Dark rooms work best**: The glowing wireframe is most impressive in darker environments
6. **Use fragments sparingly**: Progressive reveal works well, but don't overdo it
7. **Color coordination**: Stick to cyan/magenta palette for consistency

## Keyboard Shortcuts

Standard reveal.js shortcuts apply:

- `S` - Open speaker view
- `F` - Fullscreen
- `O` - Overview mode
- `Arrow keys` - Navigate
- `ESC` - Exit fullscreen/overview
- `?` - Show help

## Credits

- **reveal.js**: Hakim El Hattab
- **Three.js**: Ricardo Cabello (mrdoob)
- **Template Design**: Claude Code create-revealjs-presentations skill
- **Fonts**: Orbitron by Matt McInerney, Rajdhani by Indian Type Foundry

---

**Enjoy your futuristic presentations! 🚀**

Created with the create-revealjs-presentations skill.
