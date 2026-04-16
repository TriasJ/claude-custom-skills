# Wireframe Torus Dynamic Effects Guide

The Wireframe Tech template supports **dynamic background transitions** that respond to slide changes!

## 🎯 How It Works

Add `data-` attributes to your `<section>` tags to control the wireframe torus background for that specific slide.

## 📐 Camera Views

Control the camera angle and zoom with `data-torus-camera`:

```html
<!-- Default view (medium distance) -->
<section data-torus-camera="default">

<!-- Zoom in close -->
<section data-torus-camera="zoomIn">

<!-- Zoom out far -->
<section data-torus-camera="zoomOut">

<!-- Very close up -->
<section data-torus-camera="closeup">

<!-- Top-down view -->
<section data-torus-camera="topView">

<!-- Side view -->
<section data-torus-camera="sideView">

<!-- Angled perspective -->
<section data-torus-camera="angleView">
```

## 🌀 Rotation Speeds

Control how fast the torus spins with `data-torus-rotation`:

```html
<!-- Normal rotation -->
<section data-torus-rotation="default">

<!-- Slow gentle rotation -->
<section data-torus-rotation="slow">

<!-- Fast spinning -->
<section data-torus-rotation="fast">

<!-- Rapid Y-axis spin -->
<section data-torus-rotation="spin">

<!-- Chaotic tumbling -->
<section data-torus-rotation="tumble">

<!-- Freeze (no rotation) -->
<section data-torus-rotation="freeze">
```

## ✨ Visual Effects

Apply visual effects with `data-torus-effect`:

```html
<!-- Pulse effect (scale in/out) -->
<section data-torus-effect="pulse">

<!-- Fade to subtle -->
<section data-torus-effect="fade">

<!-- Bright and prominent -->
<section data-torus-effect="bright">

<!-- Halo glow effect -->
<section data-torus-effect="halo">

<!-- Reset to defaults -->
<section data-torus-effect="reset">
```

## 🎨 Color Changes

Change torus color with `data-torus-color` (hex value without #):

```html
<!-- Red torus -->
<section data-torus-color="ff0000">

<!-- Green torus -->
<section data-torus-color="00ff00">

<!-- Gold torus -->
<section data-torus-color="ffd700">

<!-- Purple torus -->
<section data-torus-color="9d00ff">
```

## 💫 Particle Effects

Control particles with `data-torus-particles`:

```html
<!-- Particle burst explosion -->
<section data-torus-particles="burst">

<!-- Hide particles -->
<section data-torus-particles="hide">

<!-- Show particles -->
<section data-torus-particles="show">
```

## 🌟 Glow Effect

Add a continuous glow with `data-torus-glow`:

```html
<!-- Enable glow -->
<section data-torus-glow="true">
```

## 🎭 Combining Effects

You can combine multiple attributes on the same slide!

```html
<!-- Zoom in + fast spin + red color + glow -->
<section
  data-torus-camera="zoomIn"
  data-torus-rotation="fast"
  data-torus-color="ff0000"
  data-torus-glow="true">

  <h2>Dramatic Entrance!</h2>
  <p>The torus zooms in, spins fast, turns red, and glows!</p>
</section>
```

## 📋 Complete Example

```html
<!doctype html>
<html lang="en">
<head>
  <title>Dynamic Torus Demo</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/dist/reveal.css">
  <link rel="stylesheet" href="theme.css">
  <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
</head>
<body>
  <canvas id="wireframe-canvas"></canvas>

  <div class="reveal">
    <div class="slides">

      <!-- Slide 1: Default -->
      <section>
        <h1>Welcome</h1>
        <p>Default torus view</p>
      </section>

      <!-- Slide 2: Zoom in close with fast spin -->
      <section
        data-torus-camera="zoomIn"
        data-torus-rotation="fast">
        <h2>Getting Started</h2>
        <p>Watch the torus zoom in and spin faster!</p>
      </section>

      <!-- Slide 3: Top view with pulse -->
      <section
        data-torus-camera="topView"
        data-torus-effect="pulse">
        <h2>Overview</h2>
        <p>Top-down view with pulsing effect</p>
      </section>

      <!-- Slide 4: Closeup + frozen + red -->
      <section
        data-torus-camera="closeup"
        data-torus-rotation="freeze"
        data-torus-color="ff0000">
        <h2>Important!</h2>
        <p>Frozen close-up in red for emphasis</p>
      </section>

      <!-- Slide 5: Particle burst + glow -->
      <section
        data-torus-particles="burst"
        data-torus-glow="true">
        <h2>Finale!</h2>
        <p>Particle explosion with glow!</p>
      </section>

      <!-- Slide 6: Reset everything -->
      <section
        data-torus-camera="default"
        data-torus-rotation="default"
        data-torus-effect="reset">
        <h2>Thank You</h2>
        <p>Back to normal</p>
      </section>

    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/dist/reveal.js"></script>
  <script src="assets/scripts/wireframe-background.js"></script>
  <script src="config.js"></script>
</body>
</html>
```

## 🎬 Effect Combinations for Different Moods

### Dramatic Entrance
```html
<section
  data-torus-camera="zoomIn"
  data-torus-rotation="fast"
  data-torus-effect="bright"
  data-torus-glow="true">
```

### Calm and Focused
```html
<section
  data-torus-camera="default"
  data-torus-rotation="slow"
  data-torus-effect="fade">
```

### Exciting Highlight
```html
<section
  data-torus-camera="angleView"
  data-torus-rotation="spin"
  data-torus-color="ffd700"
  data-torus-particles="burst">
```

### Serious and Important
```html
<section
  data-torus-camera="closeup"
  data-torus-rotation="freeze"
  data-torus-color="ff0000"
  data-torus-effect="halo">
```

### Subtle Background
```html
<section
  data-torus-camera="zoomOut"
  data-torus-rotation="slow"
  data-torus-effect="fade"
  data-torus-particles="hide">
```

### Dynamic Action
```html
<section
  data-torus-camera="sideView"
  data-torus-rotation="tumble"
  data-torus-effect="bright">
```

## 💡 Tips

1. **Smooth Transitions**: All changes animate smoothly (1.5 second transition)
2. **Performance**: Effects are hardware-accelerated via WebGL
3. **Browser Console**: Check console for effect confirmations: `🌀 Slide changed - Effect: pulse, Camera: zoomIn, Rotation: fast`
4. **Testing**: Use arrow keys to navigate and see effects in action
5. **Defaults**: Omit attributes to use default settings
6. **Layering**: Combine effects for maximum impact
7. **Reset**: Use `data-torus-effect="reset"` to restore defaults

## 🎮 Manual Control via Console

You can also trigger effects manually via the browser console:

```javascript
// Change camera view
WireframeBackground.setCameraView('zoomIn');

// Change color
WireframeBackground.setColor(0xff0000);

// Apply effect
WireframeBackground.applyEffect('pulse');

// Change rotation speed
WireframeBackground.setRotationSpeed(0.02, 0.03, 0.01);

// Toggle particles
WireframeBackground.toggleParticles();
```

## 🔧 Customization

Want to add your own camera positions or effects? Edit `wireframe-background.js`:

```javascript
// Add new camera state
const cameraStates = {
  // ... existing states
  myView: { x: 10, y: 5, z: 3, lookAt: { x: 0, y: 0, z: 0 } }
};

// Add new rotation state
const rotationStates = {
  // ... existing states
  mySpeed: { x: 0.005, y: 0.01, z: 0.003 }
};
```

Then use: `data-torus-camera="myView"` or `data-torus-rotation="mySpeed"`

---

**Enjoy creating dynamic, engaging presentations with the Wireframe Tech template!** 🌀✨
