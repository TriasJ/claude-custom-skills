/**
 * Wireframe Tech Template Configuration
 * reveal.js initialization with 3D wireframe background
 */

Reveal.initialize({
  // Display and Layout - Widescreen 16:9
  width: 1280,
  height: 720,
  margin: 0.04,
  minScale: 0.2,
  maxScale: 2.0,

  // Center slides vertically
  center: true,

  // Navigation and Controls
  controls: true,
  controlsLayout: 'bottom-right',
  controlsBackArrows: 'faded',
  progress: true,
  slideNumber: 'c/t',
  showSlideNumber: 'all',

  // Hash navigation
  hash: true,
  respondToHashChanges: true,

  // Keyboard navigation
  keyboard: true,

  // Touch navigation
  touch: true,

  // Loop through slides
  loop: false,

  // Navigation mode
  navigationMode: 'default',

  // Transitions and Animation
  transition: 'fade', // fade works best with 3D background
  transitionSpeed: 'default',
  backgroundTransition: 'fade',

  // Auto-animation
  autoAnimate: true,
  autoAnimateDuration: 1.0,
  autoAnimateEasing: 'ease',

  // Fragments
  fragments: true,
  fragmentInURL: true,

  // Auto-Slide (disabled)
  autoSlide: 0,

  // Media
  autoPlayMedia: null,
  preloadIframes: null,

  // Features
  overview: true,
  help: true,
  pause: true,
  showNotes: false,

  // Performance
  viewDistance: 3,
  mobileViewDistance: 2,

  // Plugins
  plugins: [
    RevealHighlight,
    RevealNotes
  ]

}).then(() => {
  console.log('🚀 Wireframe Tech presentation initialized');

  // Optional: Customize wireframe based on slide
  Reveal.on('slidechanged', event => {
    // Example: Change torus color based on slide data attribute
    const slideColor = event.currentSlide.dataset.torusColor;
    if (slideColor && window.WireframeBackground) {
      window.WireframeBackground.setColor(parseInt(slideColor, 16));
    }
  });

  // Optional: Log slide timing
  let slideStartTime = Date.now();
  Reveal.on('slidechanged', () => {
    const timeSpent = (Date.now() - slideStartTime) / 1000;
    console.log(`Time on slide: ${timeSpent.toFixed(1)}s`);
    slideStartTime = Date.now();
  });
});

// Export Reveal for external access
window.RevealInstance = Reveal;
