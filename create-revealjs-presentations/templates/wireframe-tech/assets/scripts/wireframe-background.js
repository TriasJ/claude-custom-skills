/**
 * Wireframe Torus Background with Dynamic Transitions
 * Creates an animated 3D wireframe torus using Three.js
 * Supports slide-specific effects and transitions
 */

(function() {
  'use strict';

  // Configuration
  const CONFIG = {
    // Torus geometry parameters
    torusRadius: 2.5,
    tubeRadius: 0.8,
    radialSegments: 24,
    tubularSegments: 120,

    // Default animation speeds
    rotationX: 0.003,
    rotationY: 0.005,
    rotationZ: 0.002,

    // Camera settings
    cameraDistance: 8,
    cameraFOV: 75,

    // Colors
    wireframeColor: 0x00ffff,
    backgroundColor: 0x050510,
    pointLightColor: 0xff00ff,

    // Lighting
    ambientLightIntensity: 0.3,
    pointLightIntensity: 1.0,

    // Particles
    enableParticles: true,
    particleCount: 200,
    particleColor: 0x00ffff,
    particleSize: 0.05,

    // Transition speed
    transitionDuration: 1500 // milliseconds
  };

  let scene, camera, renderer, torus, particles;
  let mouseX = 0, mouseY = 0;
  let targetRotationX = 0, targetRotationY = 0;

  // Animation state
  let currentState = 'default';
  let transitionStartTime = 0;
  let isTransitioning = false;
  let fromState = {};
  let toState = {};

  // Camera position states
  const cameraStates = {
    default: { x: 0, y: 0, z: 8, lookAt: { x: 0, y: 0, z: 0 } },
    zoomIn: { x: 0, y: 0, z: 4, lookAt: { x: 0, y: 0, z: 0 } },
    zoomOut: { x: 0, y: 0, z: 12, lookAt: { x: 0, y: 0, z: 0 } },
    topView: { x: 0, y: 8, z: 0, lookAt: { x: 0, y: 0, z: 0 } },
    sideView: { x: 8, y: 0, z: 0, lookAt: { x: 0, y: 0, z: 0 } },
    angleView: { x: 6, y: 4, z: 6, lookAt: { x: 0, y: 0, z: 0 } },
    closeup: { x: 0, y: 0, z: 3, lookAt: { x: 0, y: 0, z: 0 } }
  };

  // Rotation speed states
  const rotationStates = {
    default: { x: 0.003, y: 0.005, z: 0.002 },
    slow: { x: 0.001, y: 0.002, z: 0.001 },
    fast: { x: 0.01, y: 0.015, z: 0.008 },
    spin: { x: 0, y: 0.03, z: 0 },
    tumble: { x: 0.02, y: 0.015, z: 0.01 },
    freeze: { x: 0, y: 0, z: 0 }
  };

  /**
   * Initialize Three.js scene
   */
  function init() {
    const canvas = document.getElementById('wireframe-canvas');
    if (!canvas) {
      console.error('Wireframe canvas not found');
      return;
    }

    // Create scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(CONFIG.backgroundColor);

    // Create camera
    camera = new THREE.PerspectiveCamera(
      CONFIG.cameraFOV,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    camera.position.z = CONFIG.cameraDistance;

    // Create renderer
    renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      alpha: false
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Create wireframe torus
    createTorus();

    // Add lighting
    createLights();

    // Create particles (optional)
    if (CONFIG.enableParticles) {
      createParticles();
    }

    // Event listeners
    window.addEventListener('resize', onWindowResize);
    document.addEventListener('mousemove', onMouseMove);

    // Listen for reveal.js slide changes
    if (window.Reveal) {
      Reveal.on('slidechanged', onSlideChanged);
    }

    // Start animation loop
    animate();

    console.log('✨ Wireframe torus background initialized with dynamic transitions');
  }

  /**
   * Create the wireframe torus geometry
   */
  function createTorus() {
    const geometry = new THREE.TorusGeometry(
      CONFIG.torusRadius,
      CONFIG.tubeRadius,
      CONFIG.radialSegments,
      CONFIG.tubularSegments
    );

    const material = new THREE.MeshBasicMaterial({
      color: CONFIG.wireframeColor,
      wireframe: true,
      transparent: true,
      opacity: 0.6
    });

    torus = new THREE.Mesh(geometry, material);
    torus.userData = { baseOpacity: 0.6 }; // Store base opacity
    scene.add(torus);

    // Add second torus for depth
    const geometry2 = new THREE.TorusGeometry(
      CONFIG.torusRadius * 0.7,
      CONFIG.tubeRadius * 0.5,
      CONFIG.radialSegments,
      CONFIG.tubularSegments
    );

    const material2 = new THREE.MeshBasicMaterial({
      color: CONFIG.pointLightColor,
      wireframe: true,
      transparent: true,
      opacity: 0.3
    });

    const torus2 = new THREE.Mesh(geometry2, material2);
    torus2.rotation.x = Math.PI / 4;
    torus2.rotation.y = Math.PI / 6;
    torus2.userData = { baseOpacity: 0.3 };
    scene.add(torus2);

    torus.innerTorus = torus2;
  }

  /**
   * Create lighting for the scene
   */
  function createLights() {
    const ambientLight = new THREE.AmbientLight(0xffffff, CONFIG.ambientLightIntensity);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(CONFIG.pointLightColor, CONFIG.pointLightIntensity, 100);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);

    const pointLight2 = new THREE.PointLight(CONFIG.wireframeColor, CONFIG.pointLightIntensity * 0.5, 100);
    pointLight2.position.set(-5, -5, -5);
    scene.add(pointLight2);
  }

  /**
   * Create particle field
   */
  function createParticles() {
    const geometry = new THREE.BufferGeometry();
    const positions = [];

    for (let i = 0; i < CONFIG.particleCount; i++) {
      const x = (Math.random() - 0.5) * 20;
      const y = (Math.random() - 0.5) * 20;
      const z = (Math.random() - 0.5) * 20;
      positions.push(x, y, z);
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
      color: CONFIG.particleColor,
      size: CONFIG.particleSize,
      transparent: true,
      opacity: 0.6,
      blending: THREE.AdditiveBlending
    });

    particles = new THREE.Points(geometry, material);
    scene.add(particles);
  }

  /**
   * Handle slide change events from reveal.js
   */
  function onSlideChanged(event) {
    const slide = event.currentSlide;

    // Get effect attributes from slide
    const effect = slide.dataset.torusEffect || 'default';
    const cameraView = slide.dataset.torusCamera || 'default';
    const rotation = slide.dataset.torusRotation || 'default';
    const color = slide.dataset.torusColor;
    const glow = slide.dataset.torusGlow === 'true';
    const particleEffect = slide.dataset.torusParticles;

    console.log(`🌀 Slide changed - Effect: ${effect}, Camera: ${cameraView}, Rotation: ${rotation}`);

    // Apply effects
    applyEffect(effect);
    setCameraView(cameraView);
    setRotationSpeed(rotation);

    if (color) {
      setColor(parseInt(color, 16));
    }

    if (glow) {
      applyGlowEffect();
    }

    if (particleEffect === 'burst') {
      triggerParticleBurst();
    } else if (particleEffect === 'hide') {
      if (particles) particles.visible = false;
    } else if (particleEffect === 'show') {
      if (particles) particles.visible = true;
    }
  }

  /**
   * Apply visual effects
   */
  function applyEffect(effect) {
    switch(effect) {
      case 'pulse':
        pulseTorus();
        break;
      case 'fade':
        fadeTorus(0.2);
        break;
      case 'bright':
        fadeTorus(1.0);
        break;
      case 'halo':
        applyHaloEffect();
        break;
      case 'reset':
        resetTorus();
        break;
    }
  }

  /**
   * Set camera view with smooth transition
   */
  function setCameraView(viewName) {
    const targetView = cameraStates[viewName] || cameraStates.default;

    if (!isTransitioning) {
      fromState.camera = {
        x: camera.position.x,
        y: camera.position.y,
        z: camera.position.z
      };
      toState.camera = targetView;
      startTransition();
    }
  }

  /**
   * Set rotation speed
   */
  function setRotationSpeed(speedName) {
    const speeds = rotationStates[speedName] || rotationStates.default;
    CONFIG.rotationX = speeds.x;
    CONFIG.rotationY = speeds.y;
    CONFIG.rotationZ = speeds.z;
  }

  /**
   * Pulse effect - scale in and out
   */
  function pulseTorus() {
    if (torus) {
      const startScale = torus.scale.x;
      const targetScale = 1.3;
      const duration = 1000;
      const startTime = Date.now();

      function pulse() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = easeInOutCubic(progress);

        const scale = startScale + (targetScale - startScale) * Math.sin(eased * Math.PI);
        torus.scale.set(scale, scale, scale);

        if (torus.innerTorus) {
          torus.innerTorus.scale.set(scale, scale, scale);
        }

        if (progress < 1) {
          requestAnimationFrame(pulse);
        }
      }

      pulse();
    }
  }

  /**
   * Fade torus to target opacity
   */
  function fadeTorus(targetOpacity) {
    if (torus) {
      const startOpacity = torus.material.opacity;
      const duration = 800;
      const startTime = Date.now();

      function fade() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = easeInOutCubic(progress);

        torus.material.opacity = startOpacity + (targetOpacity - startOpacity) * eased;

        if (torus.innerTorus) {
          const innerStart = torus.innerTorus.material.opacity;
          const innerTarget = targetOpacity * 0.5;
          torus.innerTorus.material.opacity = innerStart + (innerTarget - innerStart) * eased;
        }

        if (progress < 1) {
          requestAnimationFrame(fade);
        }
      }

      fade();
    }
  }

  /**
   * Apply halo glow effect
   */
  function applyHaloEffect() {
    if (torus) {
      // Add bloom-like glow by increasing opacity and adding emissive material temporarily
      const duration = 2000;
      const startTime = Date.now();

      function glow() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const intensity = Math.sin(progress * Math.PI * 2) * 0.3 + 0.7;

        torus.material.opacity = intensity;

        if (progress < 1) {
          requestAnimationFrame(glow);
        } else {
          torus.material.opacity = torus.userData.baseOpacity;
        }
      }

      glow();
    }
  }

  /**
   * Apply continuous glow effect
   */
  function applyGlowEffect() {
    if (torus) {
      torus.material.opacity = 0.9;
      if (torus.innerTorus) {
        torus.innerTorus.material.opacity = 0.6;
      }
    }
  }

  /**
   * Reset torus to default state
   */
  function resetTorus() {
    if (torus) {
      torus.scale.set(1, 1, 1);
      torus.material.opacity = torus.userData.baseOpacity;

      if (torus.innerTorus) {
        torus.innerTorus.scale.set(1, 1, 1);
        torus.innerTorus.material.opacity = torus.innerTorus.userData.baseOpacity;
      }
    }
  }

  /**
   * Trigger particle burst effect
   */
  function triggerParticleBurst() {
    if (!particles) return;

    const positions = particles.geometry.attributes.position.array;
    const velocities = [];

    // Create random velocities for particles
    for (let i = 0; i < positions.length; i += 3) {
      velocities.push(
        (Math.random() - 0.5) * 0.2,
        (Math.random() - 0.5) * 0.2,
        (Math.random() - 0.5) * 0.2
      );
    }

    const duration = 2000;
    const startTime = Date.now();
    const originalPositions = [...positions];

    function burst() {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);

      for (let i = 0; i < positions.length; i += 3) {
        positions[i] = originalPositions[i] + velocities[i] * progress * 10;
        positions[i + 1] = originalPositions[i + 1] + velocities[i + 1] * progress * 10;
        positions[i + 2] = originalPositions[i + 2] + velocities[i + 2] * progress * 10;
      }

      particles.geometry.attributes.position.needsUpdate = true;

      if (progress < 1) {
        requestAnimationFrame(burst);
      } else {
        // Reset to original positions
        for (let i = 0; i < positions.length; i++) {
          positions[i] = originalPositions[i];
        }
        particles.geometry.attributes.position.needsUpdate = true;
      }
    }

    burst();
  }

  /**
   * Start camera/object transition
   */
  function startTransition() {
    isTransitioning = true;
    transitionStartTime = Date.now();
  }

  /**
   * Update transitions
   */
  function updateTransitions() {
    if (!isTransitioning) return;

    const elapsed = Date.now() - transitionStartTime;
    const progress = Math.min(elapsed / CONFIG.transitionDuration, 1);
    const eased = easeInOutCubic(progress);

    // Animate camera position
    if (toState.camera) {
      camera.position.x = fromState.camera.x + (toState.camera.x - fromState.camera.x) * eased;
      camera.position.y = fromState.camera.y + (toState.camera.y - fromState.camera.y) * eased;
      camera.position.z = fromState.camera.z + (toState.camera.z - fromState.camera.z) * eased;
      camera.lookAt(toState.camera.lookAt.x, toState.camera.lookAt.y, toState.camera.lookAt.z);
    }

    if (progress >= 1) {
      isTransitioning = false;
    }
  }

  /**
   * Easing function for smooth transitions
   */
  function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  /**
   * Animation loop
   */
  function animate() {
    requestAnimationFrame(animate);

    // Update transitions
    updateTransitions();

    // Rotate main torus
    if (torus) {
      torus.rotation.x += CONFIG.rotationX;
      torus.rotation.y += CONFIG.rotationY;
      torus.rotation.z += CONFIG.rotationZ;

      // Rotate inner torus at different speed
      if (torus.innerTorus) {
        torus.innerTorus.rotation.x += CONFIG.rotationX * 1.5;
        torus.innerTorus.rotation.y += CONFIG.rotationY * 0.8;
        torus.innerTorus.rotation.z -= CONFIG.rotationZ * 0.5;
      }
    }

    // Subtle mouse interaction (only when not transitioning)
    if (torus && !isTransitioning) {
      targetRotationX = mouseY * 0.0005;
      targetRotationY = mouseX * 0.0005;

      torus.rotation.x += (targetRotationX - torus.rotation.x) * 0.05;
      torus.rotation.y += (targetRotationY - torus.rotation.y) * 0.05;
    }

    // Rotate particles slowly
    if (particles) {
      particles.rotation.y += 0.0005;
    }

    // Render scene
    renderer.render(scene, camera);
  }

  /**
   * Handle window resize
   */
  function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  }

  /**
   * Handle mouse movement
   */
  function onMouseMove(event) {
    mouseX = (event.clientX - window.innerWidth / 2);
    mouseY = (event.clientY - window.innerHeight / 2);
  }

  /**
   * Public API for customization
   */
  window.WireframeBackground = {
    setColor: function(color) {
      if (torus) {
        torus.material.color.setHex(color);
      }
    },

    setRotationSpeed: function(x, y, z) {
      CONFIG.rotationX = x;
      CONFIG.rotationY = y;
      CONFIG.rotationZ = z;
    },

    toggleParticles: function() {
      if (particles) {
        particles.visible = !particles.visible;
      }
    },

    setCameraView: function(viewName) {
      setCameraView(viewName);
    },

    applyEffect: function(effectName) {
      applyEffect(effectName);
    },

    getConfig: function() {
      return CONFIG;
    }
  };

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
