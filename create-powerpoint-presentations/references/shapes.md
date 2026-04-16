# PowerPoint Shapes Reference

Complete catalog of 185+ PptxGenJS shapes organized by category with contextual usage examples.

## CRITICAL - Coordinate System

**All coordinates in this file are for WIDESCREEN (16:9) layout:**
- Layout dimensions: **10 inches wide × 5.625 inches tall**
- All values (x, y, w, h) are in **INCHES**, NOT percentages
- Ensure all shapes fit: `x + w ≤ 10` and `y + h ≤ 5.625`
- Use margins: Keep shapes at least 0.3-0.5 inches from edges

## Shape Categories

### Basic Shapes (20+)
Core geometric shapes for diagrams and emphasis.

**Available Shapes:**
- `rect` - Rectangle
- `roundRect` - Rounded rectangle
- `ellipse` - Circle/Ellipse
- `triangle` - Triangle
- `rtTriangle` - Right triangle
- `diamond` - Diamond/Rhombus
- `pentagon` - Pentagon
- `hexagon` - Hexagon
- `heptagon` - Heptagon
- `octagon` - Octagon
- `decagon` - Decagon
- `dodecagon` - Dodecagon
- `parallelogram` - Parallelogram
- `trapezoid` - Trapezoid
- `pie` - Pie wedge
- `chord` - Chord
- `arc` - Arc
- `cube` - 3D cube
- `can` - Cylinder
- `bevel` - Beveled rectangle

**Common Uses:**
```javascript
// Process boxes
slide.addShape(pptx.ShapeType.roundRect, {
  x: 2,
  y: 3,
  w: 2.5,
  h: 1,
  fill: { color: '4472C4' },
  line: { color: '000000', width: 1 }
});

slide.addText('Process Step', {
  x: 2,
  y: 3,
  w: 2.5,
  h: 1,
  fontSize: 14,
  color: 'FFFFFF',
  align: 'center',
  valign: 'middle'
});

// Emphasis circle
slide.addShape(pptx.ShapeType.ellipse, {
  x: 5,
  y: 2,
  w: 1.5,
  h: 1.5,
  fill: { color: 'FFD700' },
  line: { color: 'FF6B35', width: 3 }
});

// Decision diamond
slide.addShape(pptx.ShapeType.diamond, {
  x: 4,
  y: 3.5,
  w: 2,
  h: 1.5,
  fill: { color: 'EC4899' },
  line: { color: '000000', width: 2 }
});
```

### Arrow Shapes (30+)
Directional indicators for processes and flows.

**Available Arrows:**
- `rightArrow` - Right-pointing arrow
- `leftArrow` - Left-pointing arrow
- `upArrow` - Up-pointing arrow
- `downArrow` - Down-pointing arrow
- `leftRightArrow` - Bi-directional horizontal arrow
- `upDownArrow` - Bi-directional vertical arrow
- `bentArrow` - 90-degree bent arrow
- `bentUpArrow` - Bent upward arrow
- `curvedRightArrow` - Curved right arrow
- `curvedLeftArrow` - Curved left arrow
- `curvedUpArrow` - Curved up arrow
- `curvedDownArrow` - Curved down arrow
- `stripedRightArrow` - Striped right arrow
- `notchedRightArrow` - Notched right arrow
- `chevron` - Chevron arrow
- `leftRightUpArrow` - Three-way arrow
- `leftUpArrow` - L-shaped arrow
- `circularArrow` - Circular arrow
- `leftCircularArrow` - Left circular arrow
- `leftRightCircularArrow` - Bi-directional circular
- `swooshArrow` - Swoosh arrow
- `uturnArrow` - U-turn arrow

**Arrow Callouts:**
- `rightArrowCallout` - Right arrow with text box
- `leftArrowCallout` - Left arrow with text box
- `upArrowCallout` - Up arrow with text box
- `downArrowCallout` - Down arrow with text box
- `leftRightArrowCallout` - Bi-directional arrow callout
- `upDownArrowCallout` - Vertical bi-directional callout

**Usage Patterns:**
```javascript
// Process flow
function createProcessFlow(slide, steps, startX, startY) {
  const stepWidth = 2;
  const arrowWidth = 0.8;
  const spacing = 0.3;

  steps.forEach((step, idx) => {
    const x = startX + idx * (stepWidth + arrowWidth + spacing);

    // Step box
    slide.addShape(pptx.ShapeType.roundRect, {
      x: x,
      y: startY,
      w: stepWidth,
      h: 1,
      fill: { color: '4472C4' }
    });

    slide.addText(step, {
      x: x,
      y: startY,
      w: stepWidth,
      h: 1,
      fontSize: 12,
      color: 'FFFFFF',
      align: 'center',
      valign: 'middle'
    });

    // Arrow to next step (except last)
    if (idx < steps.length - 1) {
      slide.addShape(pptx.ShapeType.rightArrow, {
        x: x + stepWidth + spacing,
        y: startY + 0.25,
        w: arrowWidth,
        h: 0.5,
        fill: { color: '666666' }
      });
    }
  });
}

// Usage
createProcessFlow(slide, ['Plan', 'Build', 'Test', 'Deploy'], 1, 3);

// Feedback loop
slide.addShape(pptx.ShapeType.curvedRightArrow, {
  x: 2,
  y: 4,
  w: 3,
  h: 1,
  fill: { color: '00D9C0' },
  line: { color: '000000', width: 1 }
});

// Return flow
slide.addShape(pptx.ShapeType.uturnArrow, {
  x: 6,
  y: 3,
  w: 1.5,
  h: 2,
  fill: { color: 'FF6B35' }
});
```

### Callout Shapes (15+)
Text boxes with pointers for annotations and emphasis.

**Available Callouts:**
- `wedgeRectCallout` - Rectangular callout with wedge pointer
- `wedgeRoundRectCallout` - Rounded rectangle callout
- `wedgeEllipseCallout` - Ellipse callout
- `cloudCallout` - Cloud-style callout
- `borderCallout1` - Simple border callout
- `borderCallout2` - Two-line border callout
- `borderCallout3` - Three-line border callout
- `accentCallout1` - Accent callout (single line)
- `accentCallout2` - Accent callout (two lines)
- `accentCallout3` - Accent callout (three lines)
- `accentBorderCallout1` - Bordered accent callout
- `accentBorderCallout2` - Two-line bordered accent
- `accentBorderCallout3` - Three-line bordered accent

**Usage Examples:**
```javascript
// Emphasize a point
slide.addShape(pptx.ShapeType.cloudCallout, {
  x: 5,
  y: 2,
  w: 3,
  h: 1.5,
  fill: { color: 'FFE66D' },
  line: { color: 'FF6B35', width: 2 }
});

slide.addText('Key Insight!', {
  x: 5,
  y: 2,
  w: 3,
  h: 1.5,
  fontSize: 16,
  bold: true,
  color: '000000',
  align: 'center',
  valign: 'middle'
});

// Annotation
slide.addShape(pptx.ShapeType.wedgeRectCallout, {
  x: 6,
  y: 4,
  w: 2.5,
  h: 1,
  fill: { color: 'F5F5F5' },
  line: { color: '0088CC', width: 1 }
});

slide.addText('See note here', {
  x: 6,
  y: 4,
  w: 2.5,
  h: 1,
  fontSize: 11,
  color: '333333',
  align: 'center',
  valign: 'middle'
});
```

### Flowchart Shapes (20+)
Standardized shapes for flowcharts and diagrams.

**Available Flowchart Shapes:**
- `flowChartProcess` - Process rectangle
- `flowChartAlternateProcess` - Alternate process
- `flowChartDecision` - Decision diamond
- `flowChartInputOutput` - Input/Output parallelogram
- `flowChartPredefinedProcess` - Predefined process
- `flowChartInternalStorage` - Internal storage
- `flowChartDocument` - Document
- `flowChartMultidocument` - Multiple documents
- `flowChartTerminator` - Terminator (start/end)
- `flowChartPreparation` - Preparation hexagon
- `flowChartManualInput` - Manual input
- `flowChartManualOperation` - Manual operation
- `flowChartConnector` - Connector circle
- `flowChartOffpageConnector` - Off-page connector
- `flowChartPunchedCard` - Punched card
- `flowChartPunchedTape` - Punched tape
- `flowChartSummingJunction` - Summing junction
- `flowChartOr` - OR gate
- `flowChartCollate` - Collate
- `flowChartSort` - Sort
- `flowChartExtract` - Extract
- `flowChartMerge` - Merge
- `flowChartDelay` - Delay
- `flowChartMagneticDisk` - Magnetic disk
- `flowChartMagneticDrum` - Magnetic drum
- `flowChartMagneticTape` - Magnetic tape
- `flowChartOnlineStorage` - Online storage
- `flowChartOfflineStorage` - Offline storage
- `flowChartDisplay` - Display

**Flowchart Example:**
```javascript
function createFlowchart(slide) {
  const y = 1;
  const spacing = 1.5;

  // Start
  slide.addShape(pptx.ShapeType.flowChartTerminator, {
    x: 4,
    y: y,
    w: 2,
    h: 0.8,
    fill: { color: '00AA00' }
  });
  slide.addText('Start', {
    x: 4,
    y: y,
    w: 2,
    h: 0.8,
    fontSize: 12,
    color: 'FFFFFF',
    align: 'center',
    valign: 'middle'
  });

  // Process
  slide.addShape(pptx.ShapeType.flowChartProcess, {
    x: 4,
    y: y + spacing,
    w: 2,
    h: 0.8,
    fill: { color: '4472C4' }
  });
  slide.addText('Process Data', {
    x: 4,
    y: y + spacing,
    w: 2,
    h: 0.8,
    fontSize: 11,
    color: 'FFFFFF',
    align: 'center',
    valign: 'middle'
  });

  // Decision
  slide.addShape(pptx.ShapeType.flowChartDecision, {
    x: 3.5,
    y: y + spacing * 2,
    w: 3,
    h: 1.2,
    fill: { color: 'FFD700' }
  });
  slide.addText('Valid?', {
    x: 3.5,
    y: y + spacing * 2,
    w: 3,
    h: 1.2,
    fontSize: 12,
    color: '000000',
    align: 'center',
    valign: 'middle'
  });

  // End
  slide.addShape(pptx.ShapeType.flowChartTerminator, {
    x: 4,
    y: y + spacing * 3.5,
    w: 2,
    h: 0.8,
    fill: { color: 'FF0000' }
  });
  slide.addText('End', {
    x: 4,
    y: y + spacing * 3.5,
    w: 2,
    h: 0.8,
    fontSize: 12,
    color: 'FFFFFF',
    align: 'center',
    valign: 'middle'
  });

  // Connecting arrows
  slide.addShape(pptx.ShapeType.line, {
    x: 5,
    y: y + 0.8,
    w: 0,
    h: spacing - 0.8,
    line: { color: '000000', width: 2, endArrowType: 'arrow' }
  });
}
```

### Star Shapes (10+)
Stars for highlights, ratings, and decorative elements.

**Available Stars:**
- `star4` - 4-point star
- `star5` - 5-point star (classic)
- `star6` - 6-point star
- `star7` - 7-point star
- `star8` - 8-point star
- `star10` - 10-point star
- `star12` - 12-point star
- `star16` - 16-point star
- `star24` - 24-point star
- `star32` - 32-point star

**Usage:**
```javascript
// Rating stars
function addRatingStars(slide, rating, x, y) {
  for (let i = 0; i < 5; i++) {
    slide.addShape(pptx.ShapeType.star5, {
      x: x + (i * 0.4),
      y: y,
      w: 0.35,
      h: 0.35,
      fill: { color: i < rating ? 'FFD700' : 'CCCCCC' },
      line: { color: 'FF6B35', width: 1 }
    });
  }
}

// Usage
addRatingStars(slide, 4, 2, 3); // 4 out of 5 stars

// Highlight badge
slide.addShape(pptx.ShapeType.star8, {
  x: 7,
  y: 2,
  w: 1.5,
  h: 1.5,
  fill: { color: 'FF6B35' },
  line: { color: 'FFD700', width: 3 }
});

slide.addText('NEW!', {
  x: 7,
  y: 2,
  w: 1.5,
  h: 1.5,
  fontSize: 18,
  bold: true,
  color: 'FFFFFF',
  align: 'center',
  valign: 'middle'
});
```

### Ribbon & Banner Shapes (10+)
Decorative ribbons for titles and callouts.

**Available Ribbons:**
- `ribbon` - Standard ribbon
- `ribbon2` - Ribbon variant 2
- `ellipseRibbon` - Ellipse ribbon
- `ellipseRibbon2` - Ellipse ribbon variant 2
- `verticalScroll` - Vertical scroll
- `horizontalScroll` - Horizontal scroll
- `wave` - Wave shape
- `doubleWave` - Double wave

**Usage:**
```javascript
// Title ribbon
slide.addShape(pptx.ShapeType.ribbon, {
  x: 2,
  y: 1,
  w: 6,
  h: 1,
  fill: { color: '4472C4' },
  line: { color: '003366', width: 2 }
});

slide.addText('Featured Section', {
  x: 2,
  y: 1,
  w: 6,
  h: 1,
  fontSize: 20,
  bold: true,
  color: 'FFFFFF',
  align: 'center',
  valign: 'middle'
});

// Scroll banner
slide.addShape(pptx.ShapeType.horizontalScroll, {
  x: 1.5,
  y: 5,
  w: 7,
  h: 1.2,
  fill: { color: 'F5F5DC' },
  line: { color: '800020', width: 2 }
});
```

### Special Shapes (20+)
Unique shapes for specific purposes.

**Available Special Shapes:**
- `heart` - Heart
- `smileyFace` - Smiley face
- `sun` - Sun
- `moon` - Moon
- `lightningBolt` - Lightning bolt
- `gear6` - 6-tooth gear
- `gear9` - 9-tooth gear
- `homePlate` - Home plate (pentagon)
- `frame` - Frame/border
- `halfFrame` - Half frame
- `corner` - Corner bracket
- `diagStripe` - Diagonal stripe
- `donut` - Donut/ring
- `noSmoking` - No smoking symbol
- `blockArc` - Block arc
- `foldedCorner` - Folded corner
- `plaque` - Plaque
- `teardrop` - Teardrop

**Charts & Diagrams:**
- `chartPlus` - Plus sign for charts
- `chartStar` - Star for charts
- `chartX` - X for charts

**Usage:**
```javascript
// Satisfaction indicator
slide.addShape(pptx.ShapeType.smileyFace, {
  x: 4,
  y: 3,
  w: 2,
  h: 2,
  fill: { color: 'FFD700' },
  line: { color: '000000', width: 2 }
});

// Warning symbol
slide.addShape(pptx.ShapeType.lightningBolt, {
  x: 1,
  y: 1,
  w: 0.8,
  h: 1.2,
  fill: { color: 'FF6B35' },
  line: { color: 'FFFFFF', width: 2 }
});

// Gear for settings/process
slide.addShape(pptx.ShapeType.gear9, {
  x: 7,
  y: 5,
  w: 1.5,
  h: 1.5,
  fill: { color: '666666' },
  line: { color: '000000', width: 1 }
});

// Love/like indicator
slide.addShape(pptx.ShapeType.heart, {
  x: 5,
  y: 4,
  w: 1,
  h: 1,
  fill: { color: 'EC4899' },
  line: { type: 'none' }
});
```

### Action Button Shapes (15+)
Pre-designed buttons for interactive presentations.

**Available Action Buttons:**
- `actionButtonBackPrevious` - Back/Previous button
- `actionButtonForwardNext` - Forward/Next button
- `actionButtonBeginning` - Go to beginning
- `actionButtonEnd` - Go to end
- `actionButtonHome` - Home button
- `actionButtonInformation` - Information icon
- `actionButtonReturn` - Return button
- `actionButtonMovie` - Movie/video button
- `actionButtonDocument` - Document button
- `actionButtonSound` - Sound/audio button
- `actionButtonHelp` - Help/question mark
- `actionButtonBlank` - Blank button

**Usage:**
```javascript
// Navigation buttons
slide.addShape(pptx.ShapeType.actionButtonForwardNext, {
  x: 9,
  y: 6.5,
  w: 0.6,
  h: 0.6,
  fill: { color: '4472C4' },
  hyperlink: { slide: 'next' }
});

slide.addShape(pptx.ShapeType.actionButtonBackPrevious, {
  x: 0.4,
  y: 6.5,
  w: 0.6,
  h: 0.6,
  fill: { color: '4472C4' },
  hyperlink: { slide: 'prev' }
});

// Help button
slide.addShape(pptx.ShapeType.actionButtonHelp, {
  x: 9,
  y: 0.5,
  w: 0.5,
  h: 0.5,
  fill: { color: '0088CC' }
});
```

## Contextual Shape Selection

**Helper function to choose shapes based on context:**

```javascript
function selectShapeForContext(slideContext, slideContent) {
  const ctx = slideContext.toLowerCase();
  const content = slideContent.toLowerCase();

  // Process/Workflow
  if (/process|workflow|steps|procedure/i.test(ctx)) {
    return {
      primary: 'flowChartProcess',
      connector: 'rightArrow',
      decision: 'flowChartDecision'
    };
  }

  // Highlights/Important
  if (/highlight|important|key|critical|featured/i.test(ctx)) {
    return {
      primary: 'star6',
      secondary: 'cloudCallout',
      accent: 'lightningBolt'
    };
  }

  // Data/Metrics
  if (/data|metric|statistic|number|kpi/i.test(ctx)) {
    return {
      primary: 'roundRect',
      container: 'frame',
      accent: 'chartPlus'
    };
  }

  // Positive/Success
  if (/success|achievement|win|positive|growth/i.test(content)) {
    return {
      primary: 'star5',
      accent: 'smileyFace',
      indicator: 'upArrow'
    };
  }

  // Warning/Caution
  if (/warning|caution|alert|risk|issue/i.test(content)) {
    return {
      primary: 'triangle',
      accent: 'lightningBolt',
      indicator: 'noSmoking'
    };
  }

  // Creative/Fun
  if (/creative|fun|exciting|innovative/i.test(content)) {
    return {
      primary: 'star8',
      shapes: ['heart', 'sun', 'moon'],
      accent: 'swooshArrow'
    };
  }

  // Technical/Process
  if (/technical|system|architecture|infrastructure/i.test(content)) {
    return {
      primary: 'gear9',
      shapes: ['hexagon', 'octagon'],
      flow: 'flowChartProcess'
    };
  }

  // Default
  return {
    primary: 'roundRect',
    accent: 'rightArrow'
  };
}
```

## Shape Positioning Strategies

**Grid layout:**
```javascript
function positionShapesInGrid(slide, shapes, cols, startX, startY, spacing) {
  shapes.forEach((shape, idx) => {
    const col = idx % cols;
    const row = Math.floor(idx / cols);

    slide.addShape(pptx.ShapeType[shape.type], {
      x: startX + col * (shape.width + spacing),
      y: startY + row * (shape.height + spacing),
      w: shape.width,
      h: shape.height,
      fill: { color: shape.color },
      line: { color: '000000', width: 1 }
    });
  });
}
```

**Circular arrangement:**
```javascript
function positionShapesInCircle(slide, shapes, centerX, centerY, radius) {
  const angleStep = (2 * Math.PI) / shapes.length;

  shapes.forEach((shape, idx) => {
    const angle = idx * angleStep;
    const x = centerX + radius * Math.cos(angle) - shape.width / 2;
    const y = centerY + radius * Math.sin(angle) - shape.height / 2;

    slide.addShape(pptx.ShapeType[shape.type], {
      x: x,
      y: y,
      w: shape.width,
      h: shape.height,
      fill: { color: shape.color }
    });
  });
}
```

**Hierarchical diagram:**
```javascript
function createHierarchy(slide, data, startX, startY) {
  // Top level
  slide.addShape(pptx.ShapeType.roundRect, {
    x: startX,
    y: startY,
    w: 3,
    h: 0.8,
    fill: { color: '4472C4' }
  });
  slide.addText(data.top, {
    x: startX,
    y: startY,
    w: 3,
    h: 0.8,
    color: 'FFFFFF',
    align: 'center',
    valign: 'middle'
  });

  // Second level
  const childWidth = 2;
  const childSpacing = 0.5;
  const totalWidth = data.children.length * childWidth + (data.children.length - 1) * childSpacing;
  const childStartX = startX + (3 - totalWidth) / 2;

  data.children.forEach((child, idx) => {
    const x = childStartX + idx * (childWidth + childSpacing);

    slide.addShape(pptx.ShapeType.roundRect, {
      x: x,
      y: startY + 1.5,
      w: childWidth,
      h: 0.7,
      fill: { color: 'ED7D31' }
    });
    slide.addText(child, {
      x: x,
      y: startY + 1.5,
      w: childWidth,
      h: 0.7,
      color: 'FFFFFF',
      fontSize: 11,
      align: 'center',
      valign: 'middle'
    });

    // Connecting line
    slide.addShape(pptx.ShapeType.line, {
      x: startX + 1.5,
      y: startY + 0.8,
      w: x + childWidth / 2 - (startX + 1.5),
      h: 0.7,
      line: { color: '666666', width: 2 }
    });
  });
}
```

## Best Practices

**Shape Selection:**
- Use standard flowchart shapes for process diagrams (consistency)
- Choose stars for highlights and important points
- Use arrows to show direction and flow
- Apply callouts for annotations and emphasis

**Styling:**
- Match shape colors to presentation template
- Use consistent line widths throughout
- Apply shadows sparingly for depth
- Ensure text is readable (contrast, size)

**Positioning:**
- Align shapes to a grid for professional appearance
- Maintain consistent spacing between elements
- Group related shapes together
- Leave adequate whitespace around shapes

**Performance:**
- Limit shapes per slide (< 20 for best performance)
- Use simpler shapes when possible
- Avoid excessive rotation or effects
- Test presentation on target display system
