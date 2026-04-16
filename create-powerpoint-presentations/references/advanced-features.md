# Advanced PowerPoint Features

Additional PptxGenJS capabilities for professional presentations.

## Speaker Notes

Add presenter guidance and talking points to slides.

**Basic Usage:**
```javascript
slide.addNotes('Key talking points:\n' +
  '- Emphasize 25% growth in Q2\n' +
  '- Address questions about market conditions\n' +
  '- Mention upcoming product launch\n' +
  '- Estimated time: 3 minutes');
```

**Detailed Notes Example:**
```javascript
const titleSlide = pptx.addSlide({ masterName: 'TITLE' });
titleSlide.addText('Annual Report 2024', { ...});

titleSlide.addNotes(
  'INTRODUCTION (2 min)\n\n' +
  'Welcome everyone to the 2024 annual report presentation.\n\n' +
  'Key Points to Cover:\n' +
  '- Thank board and stakeholders\n' +
  '- Brief overview of agenda\n' +
  '- Set positive, confident tone\n\n' +
  'Transition: "Let\'s start with our financial highlights..."'
);

const resultsSlide = pptx.addSlide({ masterName: 'CONTENT' });
resultsSlide.addText('Financial Results', { ... });

resultsSlide.addNotes(
  'FINANCIAL RESULTS (5 min)\n\n' +
  'Talking Points:\n' +
  '1. Revenue grew 25% YoY to $50M\n' +
  '2. EBITDA margin improved from 15% to 22%\n' +
  '3. Cash flow positive for 4 consecutive quarters\n\n' +
  'Be prepared for questions about:\n' +
  '- Geographic breakdown (NA 60%, EMEA 30%, APAC 10%)\n' +
  '- Customer concentration (top 10 clients = 45% revenue)\n' +
  '- Seasonal variations (Q4 typically strongest)\n\n' +
  'Transition: "Now let\'s look at our market position..."'
);
```

**Best Practices:**
- Include estimated time for each slide
- Add transition phrases
- Anticipate likely questions
- Note pronunciation of difficult terms
- Include statistics not on slides
- Mark slides where audience interaction expected

## Presentation Sections

Organize large presentations into logical groups.

**Creating Sections:**
```javascript
// Add sections in presentation order
pptx.addSection({ title: 'Introduction' });
pptx.addSection({ title: 'Market Analysis' });
pptx.addSection({ title: 'Product Updates' });
pptx.addSection({ title: 'Financial Results' });
pptx.addSection({ title: 'Q&A' });

// Add slides to sections
const slide1 = pptx.addSlide({ sectionTitle: 'Introduction' });
slide1.addText('Welcome', { ... });

const slide2 = pptx.addSlide({ sectionTitle: 'Introduction' });
slide2.addText('Agenda', { ... });

const slide3 = pptx.addSlide({ sectionTitle: 'Market Analysis' });
slide3.addText('Market Trends', { ... });
```

**Section at Specific Position:**
```javascript
// Add appendix at end regardless of when defined
pptx.addSection({ title: 'Appendix', order: 100 });
```

**Section Best Practices:**
- 3-7 sections ideal for most presentations
- Each section = 3-10 slides
- Use section headers (master slides) to mark divisions
- Common sections:
  - Introduction/Agenda
  - Problem Statement
  - Solution/Approach
  - Results/Impact
  - Next Steps/Conclusion
  - Q&A
  - Appendix/References

## Custom Layouts and Dimensions

Create presentations for different output formats.

**Standard Layouts:**
```javascript
// 16:9 Widescreen (default)
pptx.layout = 'LAYOUT_16x9'; // 10" x 5.625"

// 4:3 Standard
pptx.layout = 'LAYOUT_4x3'; // 10" x 7.5"

// Custom dimensions
pptx.defineLayout({ name: 'A4', width: 8.27, height: 11.69 });
pptx.layout = 'A4';

// Square format (social media)
pptx.defineLayout({ name: 'SQUARE', width: 8, height: 8 });
pptx.layout = 'SQUARE';

// Ultra-wide
pptx.defineLayout({ name: 'ULTRAWIDE', width: 12, height: 5 });
pptx.layout = 'ULTRAWIDE';
```

**Responsive Positioning:**
```javascript
// Position elements based on layout
function getResponsivePosition(layout) {
  const positions = {
    'LAYOUT_16x9': { titleY: 1, contentY: 2, contentH: 4 },
    'LAYOUT_4x3': { titleY: 0.8, contentY: 1.8, contentH: 5 },
    'SQUARE': { titleY: 1, contentY: 2, contentH: 5 }
  };

  return positions[layout] || positions['LAYOUT_16x9'];
}

const pos = getResponsivePosition(pptx.layout);
slide.addText('Title', { x: 1, y: pos.titleY, ... });
```

## Slide Numbering

Add page numbers to presentations.

**Via Master Slide:**
```javascript
pptx.defineSlideMaster({
  title: 'CONTENT_MASTER',
  slideNumber: {
    x: 9,           // X position
    y: 7,           // Y position
    fontSize: 10,
    color: '666666',
    bold: false,
    italic: false
  },
  objects: [ ... ]
});
```

**Manual Slide Numbers:**
```javascript
// Add to each slide individually
const slideNum = 1;
slide.addText(`${slideNum}`, {
  x: 9,
  y: 7,
  w: 0.5,
  h: 0.3,
  fontSize: 10,
  color: '666666',
  align: 'right'
});
```

**Custom Numbering:**
```javascript
// "Page X of Y" format
function addPageNumbers(slides, totalSlides) {
  slides.forEach((slide, idx) => {
    slide.addText(`${idx + 1} / ${totalSlides}`, {
      x: 8.5,
      y: 7,
      w: 1,
      h: 0.3,
      fontSize: 9,
      color: '999999',
      align: 'center'
    });
  });
}
```

## Accessibility Features

Make presentations accessible to all users.

**Alt Text for Images:**
```javascript
slide.addImage({
  path: './chart.png',
  x: 1,
  y: 2,
  w: 8,
  h: 4,
  altText: 'Bar chart showing quarterly revenue from Q1 to Q4 2024. ' +
           'Revenue increased from $10M in Q1 to $15M in Q4, ' +
           'representing 50% growth over the year.'
});
```

**Readable Fonts and Sizes:**
```javascript
// Minimum font sizes
const fontSizes = {
  title: 28,      // Slide titles
  heading: 24,    // Section headings
  body: 18,       // Body text
  caption: 14,    // Image captions, notes
  footer: 10      // Footer text, disclaimers
};

// Readable fonts
const accessibleFonts = [
  'Arial',
  'Helvetica',
  'Calibri',
  'Verdana',
  'Tahoma'
];
```

**Color Contrast (WCAG AA Compliance):**
```javascript
// Color contrast checker
function meetsContrastRequirements(foreground, background) {
  // Calculate relative luminance
  const getLuminance = (hex) => {
    const rgb = parseInt(hex, 16);
    const r = ((rgb >> 16) & 0xff) / 255;
    const g = ((rgb >> 8) & 0xff) / 255;
    const b = (rgb & 0xff) / 255;

    const [rs, gs, bs] = [r, g, b].map(c =>
      c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)
    );

    return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
  };

  const l1 = getLuminance(foreground);
  const l2 = getLuminance(background);
  const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);

  return {
    ratio: ratio.toFixed(2),
    meetsAA: ratio >= 4.5,      // Normal text
    meetsAALarge: ratio >= 3,   // Large text (18pt+ or 14pt+ bold)
    meetsAAA: ratio >= 7
  };
}

// Example usage
const contrast = meetsContrastRequirements('000000', 'FFFFFF');
console.log(`Contrast ratio: ${contrast.ratio}:1`);
console.log(`Meets WCAG AA: ${contrast.meetsAA}`);
```

**Accessible Color Palettes:**
```javascript
// High contrast combinations
const accessiblePalettes = {
  corporate: {
    dark: '003366',
    light: '4472C4',
    background: 'FFFFFF',
    text: '000000'
  },
  warm: {
    dark: '8B4513',
    light: 'FF6B35',
    background: 'FFF8DC',
    text: '2F2F2F'
  },
  cool: {
    dark: '003D5C',
    light: '00A9CE',
    background: 'F0F8FF',
    text: '1A1A1A'
  }
};
```

**Logical Reading Order:**
- Structure content hierarchically
- Use headings appropriately
- Place content in logical flow (top to bottom, left to right)
- Group related items
- Avoid relying solely on color to convey information

**Screen Reader Considerations:**
```javascript
// Add meaningful titles to slides
slide.addText('Introduction to Machine Learning', {
  placeholder: 'title',
  ...
});

// Provide text alternatives for charts
slide.addNotes(
  'Chart Description: Line graph showing model accuracy improving from ' +
  '65% to 95% over 10 training epochs. Accuracy increases rapidly in ' +
  'epochs 1-5, then plateaus around 93-95% in epochs 6-10.'
);

// Describe complex visuals
slide.addImage({
  path: './diagram.png',
  altText: 'System architecture diagram showing three layers: ' +
           'Frontend (React), API Gateway (Node.js), and Backend (PostgreSQL). ' +
           'Arrows indicate data flow from frontend through API to database.'
});
```

## Presentation Metadata

Set properties for the presentation file.

**Basic Metadata:**
```javascript
pptx.author = 'John Doe';
pptx.company = 'Acme Corporation';
pptx.title = 'Quarterly Business Review - Q4 2024';
pptx.subject = 'Financial results and strategic initiatives';
pptx.revision = '2';
```

**Extended Properties:**
```javascript
// Set multiple properties
Object.assign(pptx, {
  author: 'Jane Smith',
  company: 'Tech Innovations Inc.',
  title: 'Product Launch Presentation',
  subject: 'New AI-Powered Analytics Platform',
  keywords: 'AI, analytics, machine learning, data visualization',
  category: 'Product Marketing',
  revision: '5',
  status: 'Final'
});
```

## Background Images and Watermarks

Add full-slide backgrounds or watermarks.

**Full Background Image:**
```javascript
slide.background = {
  path: './images/background.jpg'
};

// With transparency
slide.background = {
  path: './images/watermark.png',
  transparency: 50  // 50% transparent
};

// Solid color background
slide.background = { color: 'E8F4FF' };

// Gradient background (via shape)
slide.addShape(pptx.ShapeType.rect, {
  x: 0,
  y: 0,
  w: 10,
  h: 7.5,
  fill: {
    type: 'solid',
    color: '4472C4',
    transparency: 80
  }
});
```

**Watermark:**
```javascript
function addWatermark(slide, text, options = {}) {
  slide.addText(text, {
    x: options.x || 2,
    y: options.y || 3,
    w: options.w || 6,
    h: options.h || 1.5,
    fontSize: options.fontSize || 60,
    color: options.color || 'CCCCCC',
    transparency: options.transparency || 70,
    rotate: options.rotate || -30,
    align: 'center',
    valign: 'middle',
    bold: true
  });
}

// Usage
addWatermark(slide, 'CONFIDENTIAL');
addWatermark(slide, 'DRAFT', { color: 'FF0000', transparency: 50 });
```

## Hyperlinks

Add clickable links to slides.

**Text Hyperlinks:**
```javascript
slide.addText('Visit our website', {
  x: 1,
  y: 5,
  w: 3,
  h: 0.5,
  fontSize: 14,
  color: '0088CC',
  underline: { style: 'sng' },
  hyperlink: {
    url: 'https://example.com',
    tooltip: 'Click to visit example.com'
  }
});
```

**Image Hyperlinks:**
```javascript
slide.addImage({
  path: './logo.png',
  x: 0.5,
  y: 0.5,
  w: 2,
  h: 0.8,
  hyperlink: {
    url: 'https://company.com',
    tooltip: 'Visit our homepage'
  }
});
```

**Slide Navigation:**
```javascript
// Link to specific slide
slide.addText('Go to Summary', {
  x: 8,
  y: 7,
  w: 1.5,
  h: 0.4,
  hyperlink: { slide: 15 }  // Slide number
});

// Previous/Next slide
slide.addShape(pptx.ShapeType.actionButtonForwardNext, {
  x: 9,
  y: 6.5,
  w: 0.5,
  h: 0.5,
  hyperlink: { slide: 'next' }
});

slide.addShape(pptx.ShapeType.actionButtonBackPrevious, {
  x: 0.4,
  y: 6.5,
  w: 0.5,
  h: 0.5,
  hyperlink: { slide: 'prev' }
});
```

## Animations and Transitions

*Note: PptxGenJS has limited animation support. For advanced animations, consider post-processing in PowerPoint or using alternative libraries.*

**Slide Transitions:**
```javascript
// Basic transition support
slide.transition = {
  type: 'fade',
  duration: 0.5
};

// Available transitions (limited):
// - fade
// - push
// - wipe
// - split
// - cover
```

## Export Options

Control presentation file output.

**File Name and Compression:**
```javascript
// Basic export
pptx.writeFile({ fileName: 'presentation.pptx' });

// With compression
pptx.writeFile({
  fileName: 'presentation.pptx',
  compression: true  // Smaller file size
});
```

**Export as Base64 (for web apps):**
```javascript
// Get base64 string
pptx.write('base64').then(data => {
  console.log('Base64 data:', data);
  // Can be used to download via browser
});
```

**Streaming Output (Node.js):**
```javascript
const fs = require('fs');

pptx.write('nodebuffer').then(data => {
  fs.writeFileSync('presentation.pptx', data);
  console.log('Presentation saved!');
});
```

## Performance Optimization

Best practices for large presentations.

**Image Optimization:**
```javascript
// Use appropriately sized images
// - Width: 1920px for full-slide images
// - Width: 1024px for content images
// - Width: 512px for icons/logos

// Compress images before adding
// - JPEG quality: 85-90% for photos
// - PNG: Use optimization tools like pngquant
// - SVG: Consider converting to PNG for compatibility
```

**Lazy Loading:**
```javascript
// For very large presentations, generate slides in batches
async function generateLargePresentation(data) {
  const pptx = new pptxgen();

  // Process in batches
  const batchSize = 20;
  for (let i = 0; i < data.length; i += batchSize) {
    const batch = data.slice(i, i + batchSize);

    batch.forEach(item => {
      const slide = pptx.addSlide();
      // Add content...
    });

    console.log(`Processed slides ${i + 1} to ${Math.min(i + batchSize, data.length)}`);
  }

  await pptx.writeFile({ fileName: 'large-presentation.pptx' });
}
```

**Memory Management:**
```javascript
// Clear unused data
let imageData = loadLargeImage();
slide.addImage({ data: imageData, ... });
imageData = null; // Free memory

// Limit media file sizes
// - Video: < 100MB per file
// - Audio: < 10MB per file
// - Total presentation: < 500MB recommended
```

## Testing and Validation

Ensure presentation quality.

**Automated Checks:**
```javascript
function validatePresentation(pptx) {
  const issues = [];

  // Check slide count
  if (pptx.slides.length === 0) {
    issues.push('No slides in presentation');
  } else if (pptx.slides.length > 100) {
    issues.push('Very large presentation (>100 slides), consider splitting');
  }

  // Check for missing metadata
  if (!pptx.title) issues.push('Missing presentation title');
  if (!pptx.author) issues.push('Missing author');

  // Check each slide
  pptx.slides.forEach((slide, idx) => {
    if (!slide.hasContent) {
      issues.push(`Slide ${idx + 1} appears to be empty`);
    }

    // Check for accessibility
    const images = slide.getImages();
    images.forEach(img => {
      if (!img.altText) {
        issues.push(`Image on slide ${idx + 1} missing alt text`);
      }
    });
  });

  return issues;
}

// Usage
const issues = validatePresentation(pptx);
if (issues.length > 0) {
  console.warn('Presentation issues:', issues);
} else {
  console.log('Presentation validated successfully');
}
```

**Cross-Platform Testing:**
- Test on PowerPoint (Windows/Mac)
- Test on Google Slides
- Test on LibreOffice Impress
- Check on different screen sizes
- Verify media playback
- Confirm fonts render correctly

## Error Handling

Handle common issues gracefully.

```javascript
try {
  const pptx = new pptxgen();

  // Validate file exists before adding
  if (fs.existsSync('./logo.png')) {
    slide.addImage({ path: './logo.png', ... });
  } else {
    console.warn('Logo not found, skipping...');
  }

  // Validate data before charts
  if (chartData && chartData.length > 0) {
    slide.addChart(pptx.ChartType.bar, chartData, ...);
  } else {
    console.warn('No chart data available');
    slide.addText('Data not available', { ... });
  }

  await pptx.writeFile({ fileName: 'presentation.pptx' });
  console.log('Success!');

} catch (error) {
  console.error('Error generating presentation:', error);

  // Provide helpful error messages
  if (error.message.includes('ENOENT')) {
    console.error('File not found. Check file paths.');
  } else if (error.message.includes('memory')) {
    console.error('Out of memory. Try reducing image sizes or slide count.');
  }
}
```
