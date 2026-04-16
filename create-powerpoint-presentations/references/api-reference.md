# PptxGenJS API Reference - Verified Code Snippets

Complete, verified code snippets from Context7 documentation for generating correct PptxGenJS scripts.

## Initialization & Setup

**Create Presentation:**
```javascript
import pptxgen from 'pptxgenjs';

// Create new presentation
const pptx = new pptxgen();

// Set metadata
pptx.author = 'John Smith';
pptx.company = 'Acme Corporation';
pptx.title = 'Q4 Financial Results';
pptx.subject = 'Quarterly Business Review';
pptx.revision = '2';

// ALWAYS set widescreen layout (REQUIRED)
pptx.layout = 'LAYOUT_16x9';  // Widescreen: 10" wide × 5.625" tall (16:9 aspect ratio)

// Other layout options (USE ONLY IF EXPLICITLY REQUESTED):
// 'LAYOUT_4x3' - Standard 4:3 (10" × 7.5") - DO NOT USE unless user specifically requests 4:3
// 'LAYOUT_16x10' - Widescreen 16:10 (10" × 6.25")
// 'LAYOUT_WIDE' - Ultra-wide (13.33" × 7.5")

// Custom layout (rare - only for special paper sizes)
// pptx.defineLayout({ name: 'A4', width: 8.27, height: 11.69 });
// pptx.layout = 'A4';
```

**CRITICAL COORDINATE SYSTEM NOTES:**
- All coordinates (x, y, w, h) are in **INCHES**, not percentages
- For LAYOUT_16x9: x range is 0-10 inches, y range is 0-5.625 inches
- Always validate: `x + w ≤ 10` and `y + h ≤ 5.625`
- Use content margins: typically start content at x: 0.5, y: 0.5
```

**Add Slides:**
```javascript
// Basic slide
const slide = pptx.addSlide();

// Slide with master
const slideWithMaster = pptx.addSlide({ masterName: 'CORPORATE_MASTER' });

// Slide with section
const slideInSection = pptx.addSlide({ sectionTitle: 'Introduction' });
```

**Save Presentation:**
```javascript
// Save to file (Node.js - returns Promise)
pptx.writeFile({ fileName: 'presentation.pptx' })
  .then(fileName => {
    console.log(`Created: ${fileName}`);
  })
  .catch(err => {
    console.error('Error:', err);
  });

// Alternative: async/await
await pptx.writeFile({ fileName: 'presentation.pptx' });

// Export as base64 string
const base64Data = await pptx.write({ outputType: 'base64' });

// Export as buffer (Node.js)
const buffer = await pptx.stream();
```

## Text Methods

**Basic Text:**
```javascript
// Simple text
slide.addText('Hello World', {
  x: 1,
  y: 1,
  fontSize: 24,
  color: '363636'
});

// Text with all options
slide.addText('Styled Text Box', {
  x: 1,
  y: 1.5,
  w: 8,
  h: 1,
  fontSize: 20,
  fontFace: 'Arial',
  color: '0088CC',
  bold: true,
  italic: false,
  underline: false,
  strike: false,
  align: 'center',      // 'left', 'center', 'right', 'justify'
  valign: 'middle',     // 'top', 'middle', 'bottom'
  fill: { color: 'F1F1F1' },
  line: { color: '0088CC', width: 2 },
  margin: 0.1,
  rotate: 0,
  transparency: 0       // 0-100
});
```

**Lists:**
```javascript
// Bulleted list
slide.addText([
  { text: 'First bullet point', options: { bullet: true } },
  { text: 'Second bullet point', options: { bullet: true } },
  { text: 'Third bullet point', options: { bullet: true } }
], { x: 1, y: 3, w: 5, h: 2, fontSize: 14 });

// Numbered list
slide.addText([
  { text: 'Step one', options: { bullet: { type: 'number' } } },
  { text: 'Step two', options: { bullet: { type: 'number' } } },
  { text: 'Step three', options: { bullet: { type: 'number' } } }
], { x: 1, y: 5.5, w: 5, h: 1.5, fontSize: 14 });

// Custom bullet
slide.addText([
  { text: 'Custom bullet', options: { bullet: { code: '2713' } } }  // ✓
], { x: 1, y: 3, w: 5, fontSize: 14 });
```

**Mixed Formatting:**
```javascript
// Multiple styles in one text block
slide.addText([
  { text: 'This is ', options: { fontSize: 14 } },
  { text: 'bold', options: { fontSize: 14, bold: true } },
  { text: ' and this is ', options: { fontSize: 14 } },
  { text: 'italic', options: { fontSize: 14, italic: true, color: 'FF0000' } }
], { x: 1, y: 3, w: 8, h: 1 });
```

**Text with Shape Background:**
```javascript
// Text inside a shape
slide.addText('Shape Text', {
  x: 3.5,
  y: 6.5,
  w: 3,
  h: 0.75,
  shape: pptx.ShapeType.roundRect,
  fill: { color: '4472C4' },
  color: 'FFFFFF',
  fontSize: 16,
  bold: true,
  align: 'center',
  valign: 'middle'
});
```

## Table Methods

**Basic Table:**
```javascript
// Simple string array
const rows = [
  ['Header 1', 'Header 2', 'Header 3'],
  ['Row 1, Cell 1', 'Row 1, Cell 2', 'Row 1, Cell 3'],
  ['Row 2, Cell 1', 'Row 2, Cell 2', 'Row 2, Cell 3']
];

slide.addTable(rows, {
  x: 1,
  y: 1,
  w: 8,
  colW: [2.5, 2.5, 3],
  rowH: 0.5,
  fontSize: 12,
  border: { type: 'solid', pt: 1, color: '000000' },
  align: 'left',
  valign: 'middle',
  margin: 0.1
});
```

**Advanced Table with Cell Formatting:**
```javascript
// Cell objects with individual styling
const advancedRows = [
  [
    {
      text: 'Product',
      options: {
        bold: true,
        fill: { color: '4472C4' },
        color: 'FFFFFF',
        align: 'center'
      }
    },
    {
      text: 'Q1 Sales',
      options: {
        bold: true,
        fill: { color: '4472C4' },
        color: 'FFFFFF',
        align: 'center'
      }
    },
    {
      text: 'Q2 Sales',
      options: {
        bold: true,
        fill: { color: '4472C4' },
        color: 'FFFFFF',
        align: 'center'
      }
    }
  ],
  [
    { text: 'Widget A', options: { fill: { color: 'E7E6E6' } } },
    { text: '$12,500', options: { align: 'right' } },
    { text: '$15,750', options: { align: 'right', color: '00AA00', bold: true } }
  ],
  [
    { text: 'Widget B', options: { fill: { color: 'E7E6E6' } } },
    { text: '$8,200', options: { align: 'right' } },
    { text: '$9,100', options: { align: 'right', color: '00AA00', bold: true } }
  ]
];

slide.addTable(advancedRows, {
  x: 0.5,
  y: 3.5,
  w: 9,
  colW: [3, 3, 3],
  rowH: 0.5,
  fontSize: 12,
  border: { type: 'solid', pt: 1, color: '366092' },
  align: 'left',
  valign: 'middle'
});
```

**Table with Merged Cells:**
```javascript
// Colspan example
const mergedRows = [
  [
    {
      text: 'Merged Header',
      options: {
        colspan: 2,
        bold: true,
        align: 'center',
        fill: { color: 'FFD966' }
      }
    }
  ],
  ['Cell 1', 'Cell 2']
];

slide.addTable(mergedRows, {
  x: 2,
  y: 2,
  w: 6,
  colW: [3, 3]
});

// Rowspan example
const rowspanRows = [
  [
    { text: 'Spans 2 Rows', options: { rowspan: 2, valign: 'middle' } },
    { text: 'Cell 1' }
  ],
  [
    { text: 'Cell 2' }
  ]
];

slide.addTable(rowspanRows, { x: 1, y: 1, w: 6 });
```

**Auto-Paging Tables:**
```javascript
// Large table that splits across multiple slides
const tableData = [
  [
    { text: 'ID', options: { bold: true, fill: { color: '4472C4' }, color: 'FFFFFF' } },
    { text: 'Name', options: { bold: true, fill: { color: '4472C4' }, color: 'FFFFFF' } },
    { text: 'Department', options: { bold: true, fill: { color: '4472C4' }, color: 'FFFFFF' } },
    { text: 'Status', options: { bold: true, fill: { color: '4472C4' }, color: 'FFFFFF' } }
  ]
];

// Add many rows
for (let i = 1; i <= 100; i++) {
  tableData.push([
    `${i}`,
    `Employee ${i}`,
    i % 3 === 0 ? 'Sales' : i % 3 === 1 ? 'Engineering' : 'Marketing',
    i % 2 === 0 ? 'Active' : 'On Leave'
  ]);
}

slide.addTable(tableData, {
  x: 0.5,
  y: 1,
  w: 9,
  colW: [0.8, 2.5, 2.5, 1.5],
  fontSize: 11,
  border: { type: 'solid', pt: 1, color: '366092' },
  autoPage: true,                    // Enable auto-paging
  autoPageRepeatHeader: true,        // Repeat header on each new slide
  autoPageHeaderRows: 1,             // Number of header rows
  autoPageSlideStartY: 0.5,          // Y position on subsequent slides
  autoPageCharWeight: 0,             // Adjust character wrapping (-1.0 to 1.0)
  autoPageLineWeight: 0,             // Adjust line spacing (-1.0 to 1.0)
  margin: 0.05,
  valign: 'middle'
});

// Access auto-generated slides
if (slide.newAutoPagedSlides && slide.newAutoPagedSlides.length > 0) {
  console.log(`Table created ${slide.newAutoPagedSlides.length + 1} slides`);

  // Add page numbers to each auto-generated slide
  slide.newAutoPagedSlides.forEach((autoSlide, idx) => {
    autoSlide.addText(`Page ${idx + 2}`, {
      x: 9,
      y: 7,
      w: 0.5,
      h: 0.3,
      fontSize: 10,
      color: '666666',
      align: 'right'
    });
  });
}
```

## Image Methods

**Add Images:**
```javascript
// Image from local path (Node.js)
slide.addImage({
  path: './images/photo.jpg',
  x: 1,
  y: 1,
  w: 4,
  h: 3
});

// Image from URL
slide.addImage({
  path: 'https://example.com/logo.png',
  x: 5,
  y: 1,
  w: 3,
  h: 2
});

// Image from base64 data
slide.addImage({
  data: 'image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA...',
  x: 1,
  y: 4,
  w: 2,
  h: 1.5
});
```

**Image with Advanced Options:**
```javascript
slide.addImage({
  path: './images/chart.png',
  x: 1,
  y: 1,
  w: 8,
  h: 4,
  sizing: {
    type: 'contain',  // 'contain', 'cover', 'crop'
    w: 8,
    h: 4
  },
  hyperlink: {
    url: 'https://example.com',
    tooltip: 'Click for details'
  },
  rounding: true,
  shadow: {
    type: 'outer',
    color: '000000',
    opacity: 0.5,
    blur: 10,
    offset: 5,
    angle: 45
  },
  transparency: 0,    // 0-100
  rotate: 0,          // Degrees
  flipH: false,
  flipV: false,
  altText: 'Bar chart showing quarterly sales data for 2024'  // Accessibility
});
```

## Chart Methods

**Chart Types:**
```javascript
// Available chart types
pptx.ChartType.area
pptx.ChartType.bar
pptx.ChartType.bar3D
pptx.ChartType.bubble
pptx.ChartType.doughnut
pptx.ChartType.line
pptx.ChartType.pie
pptx.ChartType.radar
pptx.ChartType.scatter
```

**Bar Chart:**
```javascript
const barChartData = [
  {
    name: 'Product A',
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    values: [12000, 15000, 18000, 21000]
  },
  {
    name: 'Product B',
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    values: [8000, 9500, 11000, 13000]
  }
];

slide.addChart(pptx.ChartType.bar, barChartData, {
  x: 1,
  y: 1.5,
  w: 8,
  h: 4,
  showTitle: true,
  title: 'Sales by Quarter',
  titleFontSize: 16,
  titleColor: '000000',
  showLegend: true,
  legendPos: 'r',        // 't', 'b', 'l', 'r'
  legendFontSize: 11,
  showValue: true,
  dataLabelFontSize: 10,
  dataLabelColor: '000000',
  chartColors: ['4472C4', 'ED7D31'],
  barDir: 'col',         // 'col' (vertical), 'bar' (horizontal)
  barGrouping: 'clustered',  // 'clustered', 'stacked', 'percentStacked'
  catAxisLabelFontSize: 11,
  catAxisLabelColor: '000000',
  valAxisMaxVal: 25000,
  valAxisMinVal: 0,
  valGridLine: { style: 'solid', color: 'D9D9D9', size: 1 },
  catGridLine: { style: 'none' }
});
```

**Pie Chart:**
```javascript
const pieChartData = [
  {
    name: 'Market Share',
    labels: ['Company A', 'Company B', 'Company C', 'Company D', 'Others'],
    values: [35, 28, 18, 12, 7]
  }
];

slide.addChart(pptx.ChartType.pie, pieChartData, {
  x: 2,
  y: 1.5,
  w: 6,
  h: 4.5,
  showPercent: true,
  showValue: false,
  showLegend: true,
  legendPos: 'b',
  dataLabelFontSize: 11,
  chartColors: ['4472C4', 'ED7D31', 'A5A5A5', 'FFC000', '5B9BD5'],
  holeSize: 0            // 0 for pie, >0 for doughnut (70 recommended)
});
```

**Line Chart:**
```javascript
const lineChartData = [
  {
    name: '2023',
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    values: [50, 55, 62, 58, 65, 70]
  },
  {
    name: '2024',
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    values: [55, 60, 68, 72, 78, 85]
  }
];

slide.addChart(pptx.ChartType.line, lineChartData, {
  x: 1,
  y: 1.5,
  w: 8,
  h: 4,
  showTitle: true,
  title: 'Revenue Growth',
  showLegend: true,
  legendPos: 'r',
  showValue: false,
  lineSize: 3,
  lineSmooth: true,           // Smooth curves
  lineDataSymbol: 'circle',   // 'circle', 'dash', 'diamond', 'dot', 'none', 'square', 'triangle'
  lineDataSymbolSize: 6,
  lineDataSymbolLineSize: 1,
  chartColors: ['0088CC', 'FF6600'],
  valAxisMaxVal: 100,
  valAxisMinVal: 0,
  catAxisLabelFontSize: 11,
  valGridLine: { style: 'solid', color: 'D9D9D9' }
});
```

## Shape Methods

**Add Shapes:**
```javascript
// Rectangle
slide.addShape(pptx.ShapeType.rect, {
  x: 1,
  y: 1,
  w: 2,
  h: 1.5,
  fill: { color: '0088CC' },
  line: { color: '000000', width: 2 }
});

// Rounded Rectangle
slide.addShape(pptx.ShapeType.roundRect, {
  x: 1,
  y: 1,
  w: 2,
  h: 1.5,
  fill: { color: '00AA00' },
  rectRadius: 0.2
});

// Ellipse/Circle
slide.addShape(pptx.ShapeType.ellipse, {
  x: 4,
  y: 1,
  w: 2,
  h: 2,
  fill: { color: 'FF6600' },
  line: { color: '000000', width: 1 }
});

// Triangle
slide.addShape(pptx.ShapeType.triangle, {
  x: 1,
  y: 3.5,
  w: 2,
  h: 2,
  fill: { color: 'FFD700' },
  line: { color: '000000', width: 2 },
  rotate: 180
});

// Arrow
slide.addShape(pptx.ShapeType.rightArrow, {
  x: 4,
  y: 3.5,
  w: 3,
  h: 1,
  fill: { color: 'FF0000' },
  line: { color: '000000', width: 1 }
});

// Line
slide.addShape(pptx.ShapeType.line, {
  x: 1,
  y: 6,
  w: 8,
  h: 0,
  line: {
    color: '333333',
    width: 3,
    beginArrowType: 'arrow',  // 'arrow', 'diamond', 'oval', 'stealth', 'triangle'
    endArrowType: 'arrow',
    dashType: 'solid'         // 'solid', 'dash', 'dashDot', 'lgDash', 'lgDashDot', 'sysDash'
  }
});
```

**Shape with Fill Options:**
```javascript
// Gradient fill
slide.addShape(pptx.ShapeType.rect, {
  x: 1,
  y: 1,
  w: 3,
  h: 2,
  fill: {
    type: 'solid',
    color: '4472C4',
    transparency: 50  // 0-100
  },
  line: { color: '000000', width: 1 }
});

// Shadow
slide.addShape(pptx.ShapeType.roundRect, {
  x: 5,
  y: 1,
  w: 3,
  h: 2,
  fill: { color: 'FFFFFF' },
  shadow: {
    type: 'outer',
    color: '000000',
    opacity: 0.5,
    blur: 10,
    offset: 5,
    angle: 45
  }
});
```

## Media Methods

**Add Video:**
```javascript
// Local video file
slide.addMedia({
  type: 'video',
  path: './videos/demo.mp4',
  x: 1,
  y: 1.5,
  w: 8,
  h: 4.5
});

// Video with custom thumbnail
slide.addMedia({
  type: 'video',
  path: './videos/tutorial.mp4',
  cover: './images/video-thumbnail.jpg',
  x: 1,
  y: 1,
  w: 8,
  h: 4.5
});

// Video from URL
slide.addMedia({
  type: 'video',
  path: 'https://example.com/videos/demo.mp4',
  extn: 'mp4',  // Specify extension if not in URL
  x: 1,
  y: 1,
  w: 8,
  h: 4.5
});
```

**Add Audio:**
```javascript
// Local audio file
slide.addMedia({
  type: 'audio',
  path: './audio/background.mp3',
  x: 3,
  y: 3,
  w: 2,
  h: 0.5
});

// Audio from URL
slide.addMedia({
  type: 'audio',
  path: 'https://example.com/audio/podcast.mp3',
  x: 3,
  y: 3,
  w: 2,
  h: 0.5
});
```

**YouTube Video:**
```javascript
// Embed YouTube video
slide.addMedia({
  type: 'online',
  link: 'https://www.youtube.com/embed/VIDEO_ID',
  x: 1.5,
  y: 1.5,
  w: 7,
  h: 4
});
```

## Master Slide Methods

**Define Master Slide:**
```javascript
pptx.defineSlideMaster({
  title: 'CORPORATE_MASTER',
  background: { color: 'FFFFFF' },
  margin: [0.5, 0.5, 0.5, 0.5],  // [top, right, bottom, left]
  objects: [
    // Logo
    {
      image: {
        path: './images/logo.png',
        x: 0.5,
        y: 0.3,
        w: 1.5,
        h: 0.5
      }
    },
    // Title placeholder
    {
      placeholder: {
        options: {
          name: 'title',
          type: 'title',
          x: 0.5,
          y: 1.2,
          w: 9,
          h: 0.75,
          fontSize: 28,
          bold: true,
          color: '0088CC'
        },
        text: 'Click to add title'
      }
    },
    // Body placeholder
    {
      placeholder: {
        options: {
          name: 'body',
          type: 'body',
          x: 0.5,
          y: 2.2,
          w: 9,
          h: 4,
          fontSize: 14
        },
        text: 'Click to add content'
      }
    },
    // Footer line
    {
      line: {
        x: 0.5,
        y: 6.8,
        w: 9,
        h: 0,
        line: { color: '0088CC', width: 2 }
      }
    },
    // Footer text
    {
      text: {
        text: '© 2024 Company Name',
        options: {
          x: 0.5,
          y: 7,
          w: 9,
          h: 0.3,
          fontSize: 10,
          color: '666666',
          align: 'center'
        }
      }
    }
  ],
  slideNumber: {
    x: 9,
    y: 7,
    fontSize: 10,
    color: '666666'
  }
});

// Use the master slide
const slide = pptx.addSlide({ masterName: 'CORPORATE_MASTER' });
```

## Additional Features

**Sections:**
```javascript
// Add sections for organization
pptx.addSection({ title: 'Introduction' });
pptx.addSection({ title: 'Main Content' });
pptx.addSection({ title: 'Conclusion' });

// Add slides to sections
const slide1 = pptx.addSlide({ sectionTitle: 'Introduction' });
const slide2 = pptx.addSlide({ sectionTitle: 'Main Content' });
```

**Speaker Notes:**
```javascript
slide.addNotes(
  'Key talking points:\n' +
  '- Emphasize 25% growth in Q2\n' +
  '- Address questions about market conditions\n' +
  '- Estimated time: 3 minutes'
);
```

**Slide Background:**
```javascript
// Color background
slide.background = { color: 'E8F4FF' };

// Image background
slide.background = { path: './images/background.jpg' };

// Background with transparency
slide.background = {
  path: './images/watermark.png',
  transparency: 50  // 50% transparent
};
```

**Hyperlinks:**
```javascript
// Text with hyperlink
slide.addText('Visit Website', {
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

// Link to specific slide
slide.addText('Go to Summary', {
  x: 8,
  y: 7,
  w: 1.5,
  h: 0.4,
  hyperlink: { slide: 15 }  // Slide number
});

// Previous/Next navigation
slide.addShape(pptx.ShapeType.actionButtonForwardNext, {
  x: 9,
  y: 6.5,
  w: 0.5,
  h: 0.5,
  hyperlink: { slide: 'next' }  // or 'prev', 'first', 'last'
});
```

## Complete Working Example

```javascript
import pptxgen from 'pptxgenjs';

// Initialize
const pptx = new pptxgen();
pptx.author = 'John Doe';
pptx.company = 'Acme Corp';
pptx.title = 'Sales Report Q4 2024';
pptx.layout = 'LAYOUT_16x9';

// Define master slide
pptx.defineSlideMaster({
  title: 'MASTER',
  background: { color: 'FFFFFF' },
  objects: [
    {
      text: {
        text: 'Acme Corp',
        options: {
          x: 0.5,
          y: 7,
          fontSize: 10,
          color: '666666'
        }
      }
    }
  ],
  slideNumber: { x: 9, y: 7, fontSize: 10, color: '666666' }
});

// Title Slide
const titleSlide = pptx.addSlide({ masterName: 'MASTER' });
titleSlide.addText('Q4 Sales Report', {
  x: 1,
  y: 2.5,
  w: 8,
  h: 1.5,
  fontSize: 44,
  bold: true,
  align: 'center',
  color: '003366'
});
titleSlide.addText('Year End Review 2024', {
  x: 1,
  y: 4.2,
  w: 8,
  fontSize: 20,
  align: 'center',
  color: '666666'
});

// Data Slide with Chart
const chartSlide = pptx.addSlide({ masterName: 'MASTER' });
chartSlide.addText('Revenue by Quarter', {
  x: 0.5,
  y: 0.5,
  fontSize: 24,
  bold: true,
  color: '003366'
});

const chartData = [
  {
    name: 'Revenue',
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    values: [12000, 15000, 18000, 21000]
  }
];

chartSlide.addChart(pptx.ChartType.bar, chartData, {
  x: 1,
  y: 1.5,
  w: 8,
  h: 4.5,
  showTitle: false,
  showLegend: true,
  chartColors: ['4472C4']
});

// Table Slide
const tableSlide = pptx.addSlide({ masterName: 'MASTER' });
tableSlide.addText('Regional Performance', {
  x: 0.5,
  y: 0.5,
  fontSize: 24,
  bold: true,
  color: '003366'
});

const tableData = [
  [
    { text: 'Region', options: { bold: true, fill: { color: '4472C4' }, color: 'FFFFFF' } },
    { text: 'Revenue', options: { bold: true, fill: { color: '4472C4' }, color: 'FFFFFF' } },
    { text: 'Growth', options: { bold: true, fill: { color: '4472C4' }, color: 'FFFFFF' } }
  ],
  ['North America', '$45M', '+25%'],
  ['Europe', '$32M', '+18%'],
  ['Asia Pacific', '$28M', '+32%']
];

tableSlide.addTable(tableData, {
  x: 1,
  y: 1.5,
  w: 8,
  colW: [3, 2.5, 2.5],
  fontSize: 14,
  border: { type: 'solid', pt: 1, color: '366092' }
});

// Save
pptx.writeFile({ fileName: 'Sales-Report-Q4.pptx' })
  .then(fileName => console.log(`Created: ${fileName}`))
  .catch(err => console.error('Error:', err));
```

## Error Handling

```javascript
// Proper error handling
try {
  const pptx = new pptxgen();

  // Check file exists before adding
  const fs = require('fs');
  if (fs.existsSync('./logo.png')) {
    slide.addImage({ path: './logo.png', x: 0.5, y: 0.5, w: 2, h: 1 });
  } else {
    console.warn('Logo not found, skipping...');
  }

  // Validate data before charts
  if (chartData && chartData.length > 0) {
    slide.addChart(pptx.ChartType.bar, chartData, { x: 1, y: 1, w: 8, h: 4 });
  } else {
    console.warn('No chart data available');
  }

  await pptx.writeFile({ fileName: 'presentation.pptx' });
  console.log('Success!');

} catch (error) {
  console.error('Error generating presentation:', error.message);

  if (error.message.includes('ENOENT')) {
    console.error('File not found. Check file paths.');
  } else if (error.message.includes('memory')) {
    console.error('Out of memory. Reduce image sizes or slide count.');
  }
}
```
