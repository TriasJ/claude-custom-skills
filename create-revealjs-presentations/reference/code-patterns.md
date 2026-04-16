<table_of_contents>
- basic_presentation: Complete HTML structure with reveal.js setup
- image_base64: Converting images to BASE64 data URIs
- d3_embed: D3.js visualization embedding pattern
- threejs_embed: Three.js 3D model embedding pattern
- video_background: Video background slide pattern
- fragment_animations: Fragment reveal animations
- two_column_layout: Side-by-side content layout
</table_of_contents>

<basic_presentation>
Complete reveal.js HTML structure with widescreen configuration

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Presentation</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/dist/theme/black.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/plugin/highlight/monokai.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <section>
        <h1>Title Slide</h1>
        <p>Subtitle or description</p>
        <aside class="notes">
          Welcome everyone. Today we'll discuss...
        </aside>
      </section>

      <section data-background-color="#0a4d68">
        <h2>Slide with Color Background</h2>
        <ul>
          <li class="fragment">Point 1</li>
          <li class="fragment">Point 2</li>
          <li class="fragment">Point 3</li>
        </ul>
        <aside class="notes">
          Remember to pause between points.
        </aside>
      </section>

      <section data-background-image="data:image/jpeg;base64,...">
        <h2 style="color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">
          Slide with Image Background
        </h2>
        <aside class="notes">
          Image: "Landscape" from Wikimedia Commons
        </aside>
      </section>

      <section data-background-video="video.mp4" data-background-video-loop>
        <h2>Slide with Video Background</h2>
      </section>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/plugin/notes/notes.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/plugin/highlight/highlight.js"></script>
  <script>
    Reveal.initialize({
      width: 1280,
      height: 720,
      margin: 0.04,
      minScale: 0.2,
      maxScale: 2.0,
      center: true,
      hash: true,
      transition: 'slide',
      transitionSpeed: 'default',
      plugins: [RevealNotes, RevealHighlight]
    });
  </script>
</body>
</html>
```
</basic_presentation>

<image_base64>
Converting images to BASE64 for single-file deployment

```javascript
// Node.js: Convert image to BASE64
const fs = require('fs');
const path = require('path');

function imageToBase64(imagePath) {
  const imageBuffer = fs.readFileSync(imagePath);
  const base64Image = imageBuffer.toString('base64');

  // Determine MIME type from extension
  const ext = path.extname(imagePath).toLowerCase();
  const mimeTypes = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.webp': 'image/webp'
  };

  const mimeType = mimeTypes[ext] || 'application/octet-stream';
  return `data:${mimeType};base64,${base64Image}`;
}

// Usage
const dataUri = imageToBase64('./images/photo.jpg');
// Result: data:image/jpeg;base64,/9j/4AAQSkZJRg...

// In HTML:
// <img src="data:image/jpeg;base64,/9j/4AAQSkZJRg..." alt="Description">
// or as background:
// <section data-background-image="data:image/jpeg;base64,...">
```
</image_base64>

<d3_embed>
D3.js visualization embedding with reveald3 plugin

```html
<!-- Include reveald3 plugin in head -->
<script src="https://cdn.jsdelivr.net/npm/reveald3@1.5.5/reveald3.js"></script>

<!-- D3.js visualization slide -->
<section>
  <h2>Interactive Chart</h2>
  <div class="fig-container"
       data-file="visualizations/chart.html"
       style="height: 600px;">
  </div>
  <aside class="notes">
    This chart shows the data trend over time.
    Click on legend items to toggle series.
  </aside>
</section>

<!-- Initialize with reveald3 plugin -->
<script>
  Reveal.initialize({
    width: 1280,
    height: 720,
    plugins: [RevealNotes, Reveald3]
  });
</script>
```

Separate chart.html file structure:

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    svg { font-family: sans-serif; }
    .bar { fill: steelblue; }
    .bar:hover { fill: orange; }
  </style>
</head>
<body>
  <script>
    const data = [30, 86, 168, 281, 303, 365];

    const svg = d3.select("body").append("svg")
      .attr("width", 800)
      .attr("height", 400);

    svg.selectAll("rect")
      .data(data)
      .enter()
      .append("rect")
      .attr("class", "bar")
      .attr("x", (d, i) => i * 120 + 50)
      .attr("y", d => 400 - d)
      .attr("width", 100)
      .attr("height", d => d);
  </script>
</body>
</html>
```
</d3_embed>

<threejs_embed>
Three.js 3D model embedding pattern

```html
<!-- Three.js slide -->
<section>
  <h2>3D Model Viewer</h2>
  <div id="threejs-container" style="width: 100%; height: 600px;"></div>
  <aside class="notes">
    Rotate the model with mouse drag.
    Scroll to zoom in/out.
  </aside>
</section>

<!-- Include Three.js libraries -->
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/loaders/GLTFLoader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js"></script>

<script>
  let scene, camera, renderer, controls;

  Reveal.on('slidechanged', event => {
    const container = event.currentSlide.querySelector('#threejs-container');
    if (container && !container.hasChildNodes()) {
      initThreeJS(container);
    }
  });

  function initThreeJS(container) {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);

    // Camera
    camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.z = 5;

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    // Controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);

    // Load GLB model
    const loader = new THREE.GLTFLoader();
    loader.load('models/model.glb', (gltf) => {
      scene.add(gltf.scene);
      animate();
    });

    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }
  }
</script>
```
</threejs_embed>

<video_background>
Video background slide patterns

```html
<!-- Autoplay looping video background -->
<section data-background-video="video.mp4"
         data-background-video-loop
         data-background-video-muted>
  <h2 style="color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">
    Video Background
  </h2>
</section>

<!-- YouTube embed as background (requires plugin) -->
<section data-background-iframe="https://www.youtube.com/embed/VIDEO_ID?autoplay=1&mute=1&controls=0&loop=1"
         data-background-interactive>
  <h2>YouTube Background</h2>
</section>

<!-- Video with BASE64 encoding (for single-file) -->
<section data-background-video="data:video/mp4;base64,...">
  <h2>Embedded Video</h2>
</section>
```
</video_background>

<fragment_animations>
Fragment reveal animations for progressive disclosure

```html
<section>
  <h2>Progressive Reveal</h2>

  <!-- Basic fragments (appear on click) -->
  <ul>
    <li class="fragment">First point</li>
    <li class="fragment">Second point</li>
    <li class="fragment">Third point</li>
  </ul>

  <!-- Ordered fragments -->
  <p class="fragment" data-fragment-index="1">Appears first</p>
  <p class="fragment" data-fragment-index="3">Appears third</p>
  <p class="fragment" data-fragment-index="2">Appears second</p>

  <!-- Fragment animations -->
  <p class="fragment fade-in">Fade in</p>
  <p class="fragment fade-out">Fade out</p>
  <p class="fragment fade-up">Fade up</p>
  <p class="fragment fade-down">Fade down</p>
  <p class="fragment fade-left">Fade left</p>
  <p class="fragment fade-right">Fade right</p>
  <p class="fragment grow">Grow</p>
  <p class="fragment shrink">Shrink</p>
  <p class="fragment strike">Strike through</p>
  <p class="fragment highlight-red">Highlight red</p>
  <p class="fragment highlight-green">Highlight green</p>
  <p class="fragment highlight-blue">Highlight blue</p>
  <p class="fragment highlight-current-red">Current red</p>

  <!-- Nested fragments -->
  <div class="fragment fade-in">
    <span class="fragment highlight-red">Nested</span>
    <span class="fragment highlight-blue">fragments</span>
  </div>
</section>
```
</fragment_animations>

<two_column_layout>
Side-by-side content layout

```html
<section>
  <h2>Two Column Layout</h2>
  <div style="display: flex; gap: 2em;">
    <div style="flex: 1;">
      <h3>Left Column</h3>
      <ul>
        <li>Point A</li>
        <li>Point B</li>
        <li>Point C</li>
      </ul>
    </div>
    <div style="flex: 1;">
      <h3>Right Column</h3>
      <img src="data:image/jpeg;base64,..." alt="Image" style="max-width: 100%;">
    </div>
  </div>
</section>

<!-- With CSS classes (add to theme.css) -->
<style>
  .columns {
    display: flex;
    gap: 2em;
  }
  .column {
    flex: 1;
  }
  .column-left { flex: 1; }
  .column-right { flex: 1; }
  .column-narrow { flex: 0.5; }
  .column-wide { flex: 1.5; }
</style>

<section>
  <h2>Styled Columns</h2>
  <div class="columns">
    <div class="column-narrow">
      <p>Narrow left</p>
    </div>
    <div class="column-wide">
      <p>Wide right with more content</p>
    </div>
  </div>
</section>
```
</two_column_layout>
