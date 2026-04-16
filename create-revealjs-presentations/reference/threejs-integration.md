# Three.js Integration with reveal.js

Complete guide to embedding Three.js 3D models and scenes in reveal.js presentations.

## Overview

Three.js enables WebGL-powered 3D graphics in reveal.js slides, perfect for:
- Product demonstrations
- Architecture/engineering models
- Scientific visualizations
- Interactive 3D data
- Educational content

## Installation

### CDN (Recommended)

```html
<!-- Three.js core -->
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>

<!-- GLTFLoader for .glb/.gltf files -->
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/loaders/GLTFLoader.js"></script>

<!-- OrbitControls for camera interaction -->
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js"></script>
```

## Basic Setup

### 1. Create Container in Slide

```html
<section>
  <h2><i class="fas fa-cube"></i> 3D Model Viewer</h2>
  <div id="three-container" style="width: 100%; height: 600px;"></div>
  <aside class="notes">
    Interactive 3D model. Drag to rotate, scroll to zoom.
  </aside>
</section>
```

### 2. Initialize Three.js Scene

```javascript
// Initialize when slide becomes active
Reveal.on('slidechanged', event => {
  const container = event.currentSlide.querySelector('#three-container');
  if (container && !container.dataset.initialized) {
    container.dataset.initialized = 'true';
    init3DScene(container);
  }
});

function init3DScene(container) {
  // Scene setup
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a0a); // Match Quantum Dark theme

  // Camera
  const camera = new THREE.PerspectiveCamera(
    75,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
  );
  camera.position.z = 5;

  // Renderer
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  container.appendChild(renderer.domElement);

  // Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0x00FFF5, 1);
  directionalLight.position.set(5, 5, 5);
  scene.add(directionalLight);

  // Controls
  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;

  // Animation loop
  function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  }
  animate();

  // Handle window resize
  window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });

  // Store references for cleanup
  container.threeScene = { scene, camera, renderer, controls };
}
```

## Loading GLB Models

### Method 1: Load from Local File

```javascript
function loadGLBModel(container, modelPath) {
  const { scene } = container.threeScene;

  const loader = new THREE.GLTFLoader();
  loader.load(
    modelPath,
    (gltf) => {
      const model = gltf.scene;

      // Center and scale model
      const box = new THREE.Box3().setFromObject(model);
      const center = box.getCenter(new THREE.Vector3());
      const size = box.getSize(new THREE.Vector3());
      const maxDim = Math.max(size.x, size.y, size.z);
      const scale = 3 / maxDim;

      model.scale.multiplyScalar(scale);
      model.position.sub(center.multiplyScalar(scale));

      scene.add(model);

      // Optional: Add animation
      if (gltf.animations && gltf.animations.length) {
        const mixer = new THREE.AnimationMixer(model);
        const action = mixer.clipAction(gltf.animations[0]);
        action.play();
        container.threeScene.mixer = mixer;
      }
    },
    (progress) => {
      console.log(`Loading: ${(progress.loaded / progress.total * 100).toFixed(2)}%`);
    },
    (error) => {
      console.error('Error loading model:', error);
    }
  );
}

// Usage
Reveal.on('slidechanged', event => {
  const container = event.currentSlide.querySelector('#three-container');
  if (container && !container.dataset.initialized) {
    container.dataset.initialized = 'true';
    init3DScene(container);
    loadGLBModel(container, 'models/your-model.glb');
  }
});
```

### Method 2: Search and Load via fetch-media Skill

The create-revealjs-presentations skill will:
1. Check working directory for GLB files
2. If not found, use fetch-media skill to search public repositories
3. Download and reference models automatically

## Advanced Techniques

### Auto-Rotating Model

```javascript
let rotationSpeed = 0.01;

function animate() {
  requestAnimationFrame(animate);

  // Auto-rotate model
  if (model) {
    model.rotation.y += rotationSpeed;
  }

  controls.update();
  renderer.render(scene, camera);
}
```

### Multiple Models on Same Slide

```html
<section>
  <h2>Product Variants</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
    <div id="model-1" class="three-container" style="height: 400px;"></div>
    <div id="model-2" class="three-container" style="height: 400px;"></div>
  </div>
</section>

<script>
Reveal.on('slidechanged', event => {
  const containers = event.currentSlide.querySelectorAll('.three-container');
  containers.forEach((container, index) => {
    if (!container.dataset.initialized) {
      container.dataset.initialized = 'true';
      init3DScene(container);
      loadGLBModel(container, `models/variant-${index + 1}.glb`);
    }
  });
});
</script>
```

### Interactive Hotspots

```javascript
// Raycaster for detecting clicks
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

// Create hotspot spheres
const hotspots = [
  { position: new THREE.Vector3(1, 1, 0), label: 'Feature A' },
  { position: new THREE.Vector3(-1, 1, 0), label: 'Feature B' }
];

hotspots.forEach(spot => {
  const geometry = new THREE.SphereGeometry(0.1, 16, 16);
  const material = new THREE.MeshBasicMaterial({ color: 0x00FFF5 });
  const sphere = new THREE.Mesh(geometry, material);
  sphere.position.copy(spot.position);
  sphere.userData = { label: spot.label };
  scene.add(sphere);
});

// Click detection
renderer.domElement.addEventListener('click', (event) => {
  const rect = renderer.domElement.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(scene.children, true);

  if (intersects.length > 0 && intersects[0].object.userData.label) {
    alert(intersects[0].object.userData.label);
  }
});
```

### Material and Lighting Effects

```javascript
// Metallic material with Quantum Dark colors
const material = new THREE.MeshStandardMaterial({
  color: 0x00FFF5,
  metalness: 0.8,
  roughness: 0.2,
  emissive: 0x0080FF,
  emissiveIntensity: 0.3
});

// Dynamic lighting
const spotLight = new THREE.SpotLight(0x00FFF5);
spotLight.position.set(5, 5, 5);
spotLight.intensity = 1.5;
spotLight.angle = Math.PI / 6;
scene.add(spotLight);

// Animated light movement
function animate() {
  const time = Date.now() * 0.001;
  spotLight.position.x = Math.sin(time) * 5;
  spotLight.position.z = Math.cos(time) * 5;
  // ... rest of animation loop
}
```

## Fragment Integration

Show/hide 3D objects with reveal.js fragments:

```javascript
// Define object groups
const layers = [
  scene.getObjectByName('base-layer'),
  scene.getObjectByName('detail-layer'),
  scene.getObjectByName('annotation-layer')
];

// Initially hide all layers
layers.forEach(layer => layer.visible = false);

// Show on fragment reveal
Reveal.on('fragmentshown', event => {
  const index = event.fragment.dataset.layer;
  if (index && layers[index]) {
    layers[index].visible = true;
  }
});

Reveal.on('fragmenthidden', event => {
  const index = event.fragment.dataset.layer;
  if (index && layers[index]) {
    layers[index].visible = false;
  }
});
```

```html
<section>
  <div id="three-container" style="height: 600px;"></div>
  <ul>
    <li class="fragment" data-layer="0">Base structure</li>
    <li class="fragment" data-layer="1">Internal details</li>
    <li class="fragment" data-layer="2">Annotations</li>
  </ul>
</section>
```

## Performance Optimization

### 1. Dispose of Resources

```javascript
// Clean up when leaving slide
Reveal.on('slidechanged', event => {
  // Clean up previous slide's Three.js scene
  const prevSlides = document.querySelectorAll('.slides section:not(.present)');
  prevSlides.forEach(slide => {
    const container = slide.querySelector('[data-initialized]');
    if (container && container.threeScene) {
      const { scene, renderer, controls } = container.threeScene;

      // Dispose geometries and materials
      scene.traverse(object => {
        if (object.geometry) object.geometry.dispose();
        if (object.material) {
          if (Array.isArray(object.material)) {
            object.material.forEach(m => m.dispose());
          } else {
            object.material.dispose();
          }
        }
      });

      renderer.dispose();
      controls.dispose();
      container.innerHTML = '';
      delete container.threeScene;
      delete container.dataset.initialized;
    }
  });
});
```

### 2. Use Lower Poly Models

- Aim for < 50,000 polygons for presentations
- Use compressed GLB format, not OBJ or FBX
- Optimize textures (max 2048x2048)

### 3. Limit Active Scenes

Only render Three.js on visible slides:

```javascript
let activeContainer = null;

Reveal.on('slidechanged', event => {
  // Pause previous animation
  if (activeContainer && activeContainer.threeScene) {
    activeContainer.threeScene.paused = true;
  }

  // Resume current animation
  activeContainer = event.currentSlide.querySelector('[data-initialized]');
  if (activeContainer && activeContainer.threeScene) {
    activeContainer.threeScene.paused = false;
  }
});
```

## Common Use Cases

### Product Showcase

- 360° product views
- Exploded assembly views
- Color/material variants
- Interactive annotations

### Architecture

- Building walkthroughs
- Floor plan overlays
- Material samples
- Construction phases

### Scientific Visualization

- Molecular structures
- Anatomical models
- Geological formations
- Physical simulations

### Education

- Geometric concepts
- Engineering principles
- Historical artifacts
- Interactive diagrams

## Troubleshooting

### Model not loading
- Check file path and format (.glb or .gltf)
- Verify Three.js and GLTFLoader are loaded
- Check browser console for CORS errors
- Use local server (required for file loading)

### Performance issues
- Reduce polygon count
- Lower texture resolution
- Disable shadows if not needed
- Limit number of lights

### Controls not working
- Ensure OrbitControls is loaded
- Check that controls are created after renderer
- Verify container has sufficient height

## Resources

- [Three.js Documentation](https://threejs.org/docs/)
- [Three.js Examples](https://threejs.org/examples/)
- [Sketchfab](https://sketchfab.com/) - Free 3D models
- [Three.js Journey](https://threejs-journey.com/) - Tutorials
- [GLB Model Viewer](https://gltf-viewer.donmccurdy.com/) - Test models

## Complete Example

See [examples/threejs-presentation/](../examples/threejs-presentation/) for a complete working example.
