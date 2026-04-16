/**
 * Quantum Dark Template Configuration
 * reveal.js initialization with optimized settings for tech presentations
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

  // Enable for embedded presentations
  embedded: false,

  // Navigation and Controls
  controls: true,
  controlsLayout: 'bottom-right',
  controlsBackArrows: 'faded',
  progress: true,
  slideNumber: 'c/t', // Current/Total slide numbers
  showSlideNumber: 'all',

  // Hash navigation
  hash: true,
  respondToHashChanges: true,

  // Keyboard navigation
  keyboard: true,

  // Touch navigation on mobile
  touch: true,

  // Loop through slides
  loop: false,

  // Right-to-left mode
  rtl: false,

  // Navigation mode
  navigationMode: 'default', // default/linear/grid

  // Randomize slide order
  shuffle: false,

  // Transitions and Animation
  transition: 'slide', // none/fade/slide/convex/concave/zoom
  transitionSpeed: 'default', // default/fast/slow
  backgroundTransition: 'fade', // none/fade/slide/convex/concave/zoom

  // Auto-animation for matching elements
  autoAnimate: true,
  autoAnimateDuration: 1.0,
  autoAnimateEasing: 'ease',
  autoAnimateUnmatched: true,
  autoAnimateStyles: [
    'opacity',
    'color',
    'background-color',
    'padding',
    'font-size',
    'line-height',
    'letter-spacing',
    'border-width',
    'border-color',
    'border-radius',
    'outline',
    'outline-offset'
  ],

  // Fragments
  fragments: true,
  fragmentInURL: true,

  // Auto-Slide (disabled by default)
  autoSlide: 0,
  autoSlideStoppable: true,
  autoSlideMethod: null,

  // View Modes
  view: null, // Use scroll or default view

  // Scroll Progress (for scroll view)
  scrollProgress: 'auto',

  // Scroll Activation (set to null to disable scroll view)
  scrollActivationWidth: null,

  // Media
  autoPlayMedia: null, // null/true/false
  preloadIframes: null, // null/true/false

  // Presentation Features
  overview: true,
  help: true,
  pause: true,
  jumpToSlide: true,
  showNotes: false, // Set to true to show notes to audience

  // Performance
  viewDistance: 3,
  mobileViewDistance: 2,

  // Parallax Background (optional)
  // parallaxBackgroundImage: 'path/to/image.jpg',
  // parallaxBackgroundSize: '2100px 900px',
  // parallaxBackgroundHorizontal: 200,
  // parallaxBackgroundVertical: 50,

  // Spotlight Plugin (if using)
  spotlight: {
    size: 60,
    useAsPointer: false,
    toggleSpotlightOnMouseDown: false
  },

  // Math Plugin (if using)
  math: {
    mathjax: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
    config: 'TeX-AMS_HTML-full',
    TeX: {
      Macros: {
        RR: '\\mathbb{R}'
      }
    }
  },

  // PDF Export Options
  pdfMaxPagesPerSlide: 1,
  pdfSeparateFragments: true,
  pdfPageHeightOffset: -1,

  // Plugins - Load only what you need
  plugins: [
    RevealHighlight, // Syntax highlighting for code
    RevealNotes       // Speaker notes
    // RevealMarkdown, // Uncomment if using Markdown slides
    // RevealMath,     // Uncomment if using mathematical formulas
    // RevealSearch,   // Uncomment if you want search functionality
    // RevealZoom      // Uncomment for zoom capability (Alt+Click)
  ],

  // Keyboard shortcuts (customize as needed)
  keyboard: {
    // 13: 'next',     // Go to next slide when ENTER is pressed
    // 32: null,       // Disable space bar navigation
    // 39: 'next',     // Right arrow
    // 37: 'prev',     // Left arrow
    // 38: 'up',       // Up arrow
    // 40: 'down'      // Down arrow
  }
}).then(() => {
  // Presentation is ready
  console.log('🚀 Quantum Dark presentation initialized');

  // Custom initialization code can go here
  // Example: Add event listeners, custom animations, etc.

  // Listen for slide changes
  Reveal.on('slidechanged', event => {
    // event.previousSlide, event.currentSlide, event.indexh, event.indexv
    console.log(`Slide changed to: ${event.indexh}, ${event.indexv}`);
  });

  // Listen for fragment shows
  Reveal.on('fragmentshown', event => {
    // event.fragment = the fragment element
    console.log('Fragment shown:', event.fragment);
  });

  // Listen for overview mode
  Reveal.on('overviewshown', event => {
    console.log('Overview mode activated');
  });

  // Custom: Log presentation start time
  const startTime = new Date();
  console.log('Presentation started at:', startTime.toLocaleTimeString());

  // Custom: Track time spent on each slide
  let slideStartTime = Date.now();
  Reveal.on('slidechanged', () => {
    const timeSpent = (Date.now() - slideStartTime) / 1000;
    console.log(`Time spent on previous slide: ${timeSpent.toFixed(1)}s`);
    slideStartTime = Date.now();
  });
});

// Export Reveal instance for external access (optional)
window.RevealInstance = Reveal;
