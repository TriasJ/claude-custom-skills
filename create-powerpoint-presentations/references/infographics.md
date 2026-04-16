# Infographic Slide Creation with Shapes

Complete guide for creating data-rich, visually compelling infographic slides using PptxGenJS shapes.

## CRITICAL - Coordinate System

**All coordinates in this file are for WIDESCREEN (16:9) layout:**
- Layout dimensions: **10 inches wide × 5.625 inches tall**
- All values (x, y, w, h) are in **INCHES**, NOT percentages
- Ensure all shapes fit: `x + w ≤ 10` and `y + h ≤ 5.625`
- Use margins: Keep shapes at least 0.3-0.5 inches from edges

## What are Infographic Slides?

Infographic slides combine text, shapes, icons, and data visualization to tell a visual story. They transform complex information into easily digestible, memorable visual narratives.

## Core Principles

1. **Visual Hierarchy**: Most important information should be largest/most prominent
2. **Logical Flow**: Information should progress top-down or left-right
3. **Color Coding**: Use consistent colors to group related information
4. **White Space**: Don't overcrowd - balance content with breathing room
5. **Icon + Text**: Combine shapes/icons with concise text labels

## Infographic Layout Patterns

### 1. Timeline/Process Flow

Perfect for showing sequential steps, historical progression, or workflows.

```javascript
function createTimelineInfographic(slide, steps) {
  const startX = 0.5;
  const startY = 2.5;
  const stepWidth = 1.5;
  const spacing = 0.3;

  steps.forEach((step, idx) => {
    const x = startX + (idx * (stepWidth + spacing));

    // Circle for step number
    slide.addShape(pptx.ShapeType.ellipse, {
      x: x + 0.4,
      y: startY - 0.7,
      w: 0.7,
      h: 0.7,
      fill: { color: '4472C4' },
      line: { color: '2E5396', width: 2 }
    });

    // Step number
    slide.addText(`${idx + 1}`, {
      x: x + 0.4,
      y: startY - 0.7,
      w: 0.7,
      h: 0.7,
      fontSize: 18,
      bold: true,
      color: 'FFFFFF',
      align: 'center',
      valign: 'middle'
    });

    // Rectangle for content
    slide.addShape(pptx.ShapeType.roundRect, {
      x: x,
      y: startY,
      w: stepWidth,
      h: 1.5,
      fill: { color: 'E7F0FF' },
      line: { color: '4472C4', width: 1 }
    });

    // Step title
    slide.addText(step.title, {
      x: x,
      y: startY + 0.1,
      w: stepWidth,
      h: 0.4,
      fontSize: 14,
      bold: true,
      color: '1F3864',
      align: 'center'
    });

    // Step description
    slide.addText(step.description, {
      x: x + 0.1,
      y: startY + 0.6,
      w: stepWidth - 0.2,
      h: 0.8,
      fontSize: 11,
      color: '333333',
      align: 'left',
      valign: 'top'
    });

    // Arrow between steps (except last)
    if (idx < steps.length - 1) {
      slide.addShape(pptx.ShapeType.rightArrow, {
        x: x + stepWidth + 0.05,
        y: startY + 0.6,
        w: spacing - 0.1,
        h: 0.3,
        fill: { color: '4472C4' },
        line: { color: '2E5396', width: 1 }
      });
    }
  });
}

// Usage
const steps = [
  { title: 'Research', description: 'Gather requirements and analyze user needs' },
  { title: 'Design', description: 'Create wireframes and prototypes' },
  { title: 'Develop', description: 'Build and test the solution' },
  { title: 'Deploy', description: 'Launch and monitor performance' }
];
createTimelineInfographic(slide, steps);
```

### 2. Statistics Grid

Show multiple metrics or KPIs in an organized grid layout.

```javascript
function createStatisticsGrid(slide, metrics) {
  const cols = 3;
  const rows = Math.ceil(metrics.length / cols);
  const cellW = 2.8;
  const cellH = 1.5;
  const marginX = 0.8;
  const marginY = 1.5;
  const spacing = 0.3;

  metrics.forEach((metric, idx) => {
    const col = idx % cols;
    const row = Math.floor(idx / cols);
    const x = marginX + (col * (cellW + spacing));
    const y = marginY + (row * (cellH + spacing));

    // Background card
    slide.addShape(pptx.ShapeType.roundRect, {
      x: x,
      y: y,
      w: cellW,
      h: cellH,
      fill: {
        type: 'solid',
        color: metric.color || 'F0F0F0'
      },
      line: { color: metric.borderColor || 'CCCCCC', width: 1 }
    });

    // Icon shape (top)
    const iconShape = metric.icon || 'ellipse';
    slide.addShape(pptx.ShapeType[iconShape], {
      x: x + (cellW / 2) - 0.3,
      y: y + 0.15,
      w: 0.6,
      h: 0.6,
      fill: { color: metric.iconColor || '4472C4' },
      line: { color: metric.iconBorder || '2E5396', width: 1 }
    });

    // Large number
    slide.addText(metric.value, {
      x: x,
      y: y + 0.8,
      w: cellW,
      h: 0.4,
      fontSize: 32,
      bold: true,
      color: metric.valueColor || '333333',
      align: 'center'
    });

    // Label
    slide.addText(metric.label, {
      x: x + 0.1,
      y: y + 1.2,
      w: cellW - 0.2,
      h: 0.25,
      fontSize: 12,
      color: '666666',
      align: 'center'
    });
  });
}

// Usage
const metrics = [
  { value: '98%', label: 'Customer Satisfaction', icon: 'star5', color: 'E7F0FF', iconColor: 'FFD700' },
  { value: '2.5M', label: 'Active Users', icon: 'pentagon', color: 'FFE7F0', iconColor: 'FF1493' },
  { value: '$4.2B', label: 'Revenue Growth', icon: 'rightArrow', color: 'E7FFE7', iconColor: '00A86B' },
  { value: '156', label: 'Countries Served', icon: 'hexagon', color: 'FFF4E7', iconColor: 'FF8C00' },
  { value: '24/7', label: 'Support Available', icon: 'rect', color: 'F0E7FF', iconColor: '9370DB' },
  { value: '99.9%', label: 'Uptime Guarantee', icon: 'diamond', color: 'E7FFFF', iconColor: '20B2AA' }
];
createStatisticsGrid(slide, metrics);
```

### 3. Comparison Chart

Side-by-side comparison of two options, products, or approaches.

```javascript
function createComparisonInfographic(slide, option1, option2) {
  const centerX = 5;
  const colWidth = 3.5;

  // Left column (Option 1)
  const leftX = centerX - colWidth - 0.25;

  // Header
  slide.addShape(pptx.ShapeType.roundRect, {
    x: leftX,
    y: 1.2,
    w: colWidth,
    h: 0.8,
    fill: { color: option1.color || '4472C4' },
    line: { color: '2E5396', width: 2 }
  });

  slide.addText(option1.title, {
    x: leftX,
    y: 1.2,
    w: colWidth,
    h: 0.8,
    fontSize: 20,
    bold: true,
    color: 'FFFFFF',
    align: 'center',
    valign: 'middle'
  });

  // Features list
  option1.features.forEach((feature, idx) => {
    const y = 2.3 + (idx * 0.6);

    // Checkmark or icon
    slide.addShape(pptx.ShapeType.ellipse, {
      x: leftX + 0.2,
      y: y,
      w: 0.4,
      h: 0.4,
      fill: { color: '00A86B' },
      line: { color: '008855', width: 1 }
    });

    // Feature text
    slide.addText(feature, {
      x: leftX + 0.8,
      y: y,
      w: colWidth - 1,
      h: 0.4,
      fontSize: 12,
      color: '333333',
      align: 'left',
      valign: 'middle'
    });
  });

  // Right column (Option 2)
  const rightX = centerX + 0.25;

  // Header
  slide.addShape(pptx.ShapeType.roundRect, {
    x: rightX,
    y: 1.2,
    w: colWidth,
    h: 0.8,
    fill: { color: option2.color || 'ED7D31' },
    line: { color: 'CC6600', width: 2 }
  });

  slide.addText(option2.title, {
    x: rightX,
    y: 1.2,
    w: colWidth,
    h: 0.8,
    fontSize: 20,
    bold: true,
    color: 'FFFFFF',
    align: 'center',
    valign: 'middle'
  });

  // Features list
  option2.features.forEach((feature, idx) => {
    const y = 2.3 + (idx * 0.6);

    // Checkmark or icon
    slide.addShape(pptx.ShapeType.ellipse, {
      x: rightX + 0.2,
      y: y,
      w: 0.4,
      h: 0.4,
      fill: { color: '00A86B' },
      line: { color: '008855', width: 1 }
    });

    // Feature text
    slide.addText(feature, {
      x: rightX + 0.8,
      y: y,
      w: colWidth - 1,
      h: 0.4,
      fontSize: 12,
      color: '333333',
      align: 'left',
      valign: 'middle'
    });
  });

  // VS separator
  slide.addShape(pptx.ShapeType.ellipse, {
    x: centerX - 0.3,
    y: 3.2,
    w: 0.6,
    h: 0.6,
    fill: { color: '666666' },
    line: { color: '333333', width: 2 }
  });

  slide.addText('VS', {
    x: centerX - 0.3,
    y: 3.2,
    w: 0.6,
    h: 0.6,
    fontSize: 16,
    bold: true,
    color: 'FFFFFF',
    align: 'center',
    valign: 'middle'
  });
}

// Usage
const option1 = {
  title: 'Cloud Solution',
  color: '4472C4',
  features: [
    'Scalable infrastructure',
    'Automatic updates',
    'Global availability',
    'Pay-as-you-go pricing',
    '99.9% uptime SLA'
  ]
};

const option2 = {
  title: 'On-Premise',
  color: 'ED7D31',
  features: [
    'Full data control',
    'Customizable setup',
    'No internet dependency',
    'One-time licensing',
    'Dedicated support'
  ]
};

createComparisonInfographic(slide, option1, option2);
```

### 4. Pyramid/Hierarchy

Show hierarchical relationships, priorities, or stages.

```javascript
function createPyramidInfographic(slide, levels) {
  const centerX = 5;
  const topY = 1.5;
  const maxWidth = 8;
  const levelHeight = 0.9;

  levels.forEach((level, idx) => {
    const ratio = (idx + 1) / levels.length;
    const width = maxWidth * ratio;
    const x = centerX - (width / 2);
    const y = topY + (idx * levelHeight);

    // Trapezoid shape (simulate with parallelogram)
    slide.addShape(pptx.ShapeType.trapezoid, {
      x: x,
      y: y,
      w: width,
      h: levelHeight,
      fill: { color: level.color || `4472C${9 - idx}` },
      line: { color: '2E5396', width: 2 }
    });

    // Level label
    slide.addText(level.label, {
      x: x,
      y: y + 0.1,
      w: width,
      h: 0.3,
      fontSize: 14,
      bold: true,
      color: 'FFFFFF',
      align: 'center',
      valign: 'top'
    });

    // Description
    slide.addText(level.description, {
      x: x + 0.2,
      y: y + 0.45,
      w: width - 0.4,
      h: 0.4,
      fontSize: 11,
      color: 'FFFFFF',
      align: 'center',
      valign: 'top'
    });
  });
}

// Usage - Maslow's Hierarchy
const levels = [
  {
    label: 'Self-Actualization',
    description: 'Personal growth, creativity',
    color: 'FFD700'
  },
  {
    label: 'Esteem',
    description: 'Achievement, recognition, respect',
    color: 'FF8C00'
  },
  {
    label: 'Social Belonging',
    description: 'Relationships, community, love',
    color: 'FF6347'
  },
  {
    label: 'Safety',
    description: 'Security, health, employment',
    color: 'DC143C'
  },
  {
    label: 'Physiological',
    description: 'Food, water, shelter, sleep',
    color: '8B0000'
  }
];

createPyramidInfographic(slide, levels);
```

### 5. Circle/Radial Layout

Perfect for showing interconnected concepts or cyclical processes.

```javascript
function createRadialInfographic(slide, items) {
  const centerX = 5;
  const centerY = 3.5;
  const radius = 2.2;
  const itemRadius = 0.8;

  // Center circle
  slide.addShape(pptx.ShapeType.ellipse, {
    x: centerX - 0.6,
    y: centerY - 0.6,
    w: 1.2,
    h: 1.2,
    fill: { color: '4472C4' },
    line: { color: '2E5396', width: 3 }
  });

  slide.addText('Core\nConcept', {
    x: centerX - 0.6,
    y: centerY - 0.6,
    w: 1.2,
    h: 1.2,
    fontSize: 14,
    bold: true,
    color: 'FFFFFF',
    align: 'center',
    valign: 'middle'
  });

  // Surrounding items
  items.forEach((item, idx) => {
    const angle = (idx * 2 * Math.PI) / items.length - (Math.PI / 2);
    const x = centerX + (radius * Math.cos(angle)) - (itemRadius / 2);
    const y = centerY + (radius * Math.sin(angle)) - (itemRadius / 2);

    // Connecting line
    slide.addShape(pptx.ShapeType.line, {
      x: centerX,
      y: centerY,
      w: radius * Math.cos(angle),
      h: radius * Math.sin(angle),
      line: { color: 'CCCCCC', width: 2, dashType: 'dash' }
    });

    // Item circle
    slide.addShape(pptx.ShapeType.ellipse, {
      x: x,
      y: y,
      w: itemRadius,
      h: itemRadius,
      fill: { color: item.color || 'E7F0FF' },
      line: { color: '4472C4', width: 2 }
    });

    // Item text
    slide.addText(item.label, {
      x: x,
      y: y,
      w: itemRadius,
      h: itemRadius,
      fontSize: 10,
      bold: true,
      color: '1F3864',
      align: 'center',
      valign: 'middle'
    });
  });
}

// Usage
const items = [
  { label: 'Research', color: 'FFE7E7' },
  { label: 'Design', color: 'E7FFE7' },
  { label: 'Develop', color: 'E7E7FF' },
  { label: 'Test', color: 'FFE7FF' },
  { label: 'Deploy', color: 'FFFFE7' },
  { label: 'Monitor', color: 'E7FFFF' }
];

createRadialInfographic(slide, items);
```

### 6. Funnel/Conversion

Show progressive narrowing, conversion stages, or filtering processes.

```javascript
function createFunnelInfographic(slide, stages) {
  const centerX = 5;
  const topY = 1.5;
  const topWidth = 7;
  const bottomWidth = 3;
  const stageHeight = 0.8;
  const gap = 0.1;

  stages.forEach((stage, idx) => {
    // Calculate width based on linear interpolation
    const ratio = idx / (stages.length - 1);
    const width = topWidth - ((topWidth - bottomWidth) * ratio);
    const x = centerX - (width / 2);
    const y = topY + (idx * (stageHeight + gap));

    // Funnel segment (trapezoid)
    slide.addShape(pptx.ShapeType.trapezoid, {
      x: x,
      y: y,
      w: width,
      h: stageHeight,
      fill: { color: stage.color || '4472C4' },
      line: { color: '2E5396', width: 2 }
    });

    // Stage label
    slide.addText(stage.label, {
      x: x + 0.2,
      y: y + 0.1,
      w: width - 0.4,
      h: 0.3,
      fontSize: 13,
      bold: true,
      color: 'FFFFFF',
      align: 'left',
      valign: 'top'
    });

    // Metric
    slide.addText(stage.value, {
      x: x + width - 1.2,
      y: y + 0.1,
      w: 1,
      h: 0.3,
      fontSize: 16,
      bold: true,
      color: 'FFFFFF',
      align: 'right',
      valign: 'top'
    });

    // Percentage/conversion rate (if not first stage)
    if (idx > 0 && stage.conversionRate) {
      slide.addText(`${stage.conversionRate}%`, {
        x: x + (width / 2) - 0.5,
        y: y + 0.5,
        w: 1,
        h: 0.2,
        fontSize: 11,
        color: 'FFFFFF',
        align: 'center'
      });
    }
  });
}

// Usage - Sales Funnel
const stages = [
  { label: 'Website Visitors', value: '100K', color: '4472C4' },
  { label: 'Sign-ups', value: '25K', conversionRate: 25, color: '5883D3' },
  { label: 'Active Users', value: '10K', conversionRate: 40, color: '6C94E2' },
  { label: 'Paying Customers', value: '2.5K', conversionRate: 25, color: '80A5F1' },
  { label: 'Loyal Advocates', value: '500', conversionRate: 20, color: '94B6FF' }
];

createFunnelInfographic(slide, stages);
```

### 7. Icon Grid with Text

Display multiple features, services, or benefits with icon representations.

```javascript
function createIconGridInfographic(slide, items) {
  const cols = 3;
  const rows = Math.ceil(items.length / cols);
  const cellW = 3;
  const cellH = 1.8;
  const marginX = 0.5;
  const marginY = 1.5;
  const iconSize = 0.7;

  items.forEach((item, idx) => {
    const col = idx % cols;
    const row = Math.floor(idx / cols);
    const x = marginX + (col * cellW);
    const y = marginY + (row * cellH);

    // Icon shape
    const shapeType = item.icon || 'rect';
    slide.addShape(pptx.ShapeType[shapeType], {
      x: x + (cellW / 2) - (iconSize / 2),
      y: y,
      w: iconSize,
      h: iconSize,
      fill: { color: item.iconColor || '4472C4' },
      line: { color: item.iconBorder || '2E5396', width: 2 }
    });

    // Title
    slide.addText(item.title, {
      x: x,
      y: y + iconSize + 0.15,
      w: cellW,
      h: 0.3,
      fontSize: 13,
      bold: true,
      color: '1F3864',
      align: 'center'
    });

    // Description
    slide.addText(item.description, {
      x: x + 0.15,
      y: y + iconSize + 0.5,
      w: cellW - 0.3,
      h: 0.8,
      fontSize: 10,
      color: '666666',
      align: 'center',
      valign: 'top'
    });
  });
}

// Usage
const items = [
  {
    title: 'Fast Performance',
    description: 'Lightning-fast load times under 2 seconds',
    icon: 'lightningBolt',
    iconColor: 'FFD700'
  },
  {
    title: 'Secure',
    description: 'Bank-grade encryption protects your data',
    icon: 'pentagon',
    iconColor: '00A86B'
  },
  {
    title: 'Scalable',
    description: 'Grows with your business needs',
    icon: 'rightArrowCallout',
    iconColor: '4472C4'
  },
  {
    title: 'User-Friendly',
    description: 'Intuitive interface, minimal learning curve',
    icon: 'star5',
    iconColor: 'FF8C00'
  },
  {
    title: '24/7 Support',
    description: 'Expert help whenever you need it',
    icon: 'ellipse',
    iconColor: 'DC143C'
  },
  {
    title: 'Analytics',
    description: 'Real-time insights and reporting',
    icon: 'hexagon',
    iconColor: '9370DB'
  }
];

createIconGridInfographic(slide, items);
```

## Best Practices

### Color Schemes
```javascript
// Monochromatic (shades of one color)
const monoBlue = ['1F3864', '2E5396', '4472C4', '6C94E2', '94B6FF'];

// Analogous (adjacent colors)
const analogous = ['FF6B6B', 'FFA07A', 'FFD700', 'F0E68C', 'E6F7FF'];

// Complementary (opposite colors)
const complementary = ['4472C4', 'FF8C00'];

// Triadic (evenly spaced)
const triadic = ['FF6B6B', '4472C4', 'FFD700'];
```

### Typography Hierarchy
```javascript
const typography = {
  mainTitle: { fontSize: 36, bold: true, color: '1F3864' },
  sectionHeader: { fontSize: 24, bold: true, color: '2E5396' },
  bodyText: { fontSize: 14, color: '333333' },
  caption: { fontSize: 11, color: '666666' },
  emphasis: { fontSize: 18, bold: true, color: '4472C4' }
};
```

### Spacing Standards
```javascript
const spacing = {
  titleMargin: 0.5,      // Space above main title
  sectionGap: 0.4,       // Between sections
  elementPadding: 0.2,   // Inside containers
  iconTextGap: 0.15,     // Between icon and label
  columnGutter: 0.3      // Between columns
};
```

## Quick Recipe Generator

Automatically select the best infographic pattern based on content type:

```javascript
function selectInfographicPattern(contentType, dataStructure) {
  // Sequential/Process data
  if (contentType === 'process' || contentType === 'timeline') {
    return 'timeline';
  }

  // Metrics/KPIs
  if (contentType === 'metrics' && dataStructure === 'grid') {
    return 'statisticsGrid';
  }

  // Comparison
  if (contentType === 'comparison' && dataStructure === 'twoColumn') {
    return 'comparison';
  }

  // Hierarchy
  if (contentType === 'hierarchy' || contentType === 'priorities') {
    return 'pyramid';
  }

  // Interconnected concepts
  if (contentType === 'cycle' || contentType === 'relationships') {
    return 'radial';
  }

  // Conversion/filtering
  if (contentType === 'funnel' || contentType === 'conversion') {
    return 'funnel';
  }

  // Multiple items with descriptions
  if (contentType === 'features' || contentType === 'benefits') {
    return 'iconGrid';
  }

  // Default to grid
  return 'statisticsGrid';
}
```

## Integration with Main Skill

When the user requests infographic slides:

1. **Identify content type**: Process, metrics, comparison, hierarchy, etc.
2. **Select pattern**: Use `selectInfographicPattern()` helper
3. **Extract data**: Parse content into structured format
4. **Apply color scheme**: Choose template-appropriate colors
5. **Generate infographic**: Use appropriate creation function
6. **Add to presentation**: Insert as regular slides

Example workflow:
```javascript
// User requests: "Create an infographic showing our product features"
const contentType = 'features';
const dataStructure = 'grid';
const pattern = selectInfographicPattern(contentType, dataStructure);

// pattern = 'iconGrid'
const features = extractFeaturesFromContent(userContent);
createIconGridInfographic(slide, features);
```
