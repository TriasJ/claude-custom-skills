# D3.js Integration with reveal.js

Complete guide to embedding D3.js data visualizations in reveal.js presentations using the reveald3 plugin.

## Overview

The reveald3 plugin (reveal.js-d3) enables full integration of animated JavaScript-based visualizations into reveal.js presentations, maintaining interactivity and supporting fragment transitions.

## Installation

### CDN (Recommended)

```html
<!-- Add to your HTML head or before closing body -->
<script src="https://cdn.jsdelivr.net/npm/reveald3@1.5.5/reveald3.js"></script>
```

### NPM

```bash
npm install reveald3
```

## Basic Usage

### Method 1: External HTML File (Recommended)

Create a separate HTML file for your D3 visualization:

**visualizations/chart.html:**
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    body {
      margin: 0;
      padding: 20px;
      background: transparent;
    }
    .bar {
      fill: #00FFF5;
      transition: fill 0.3s;
    }
    .bar:hover {
      fill: #0080FF;
    }
  </style>
</head>
<body>
  <svg id="chart" width="800" height="400"></svg>
  <script>
    // Sample data
    const data = [30, 86, 168, 281, 303, 365];

    // Create bar chart
    const svg = d3.select("#chart");
    const margin = {top: 20, right: 20, bottom: 30, left: 40};
    const width = 800 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const x = d3.scaleBand()
      .range([0, width])
      .padding(0.1);

    const y = d3.scaleLinear()
      .range([height, 0]);

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    x.domain(data.map((d, i) => `Item ${i + 1}`));
    y.domain([0, d3.max(data)]);

    g.selectAll(".bar")
      .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", (d, i) => x(`Item ${i + 1}`))
        .attr("y", d => y(d))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d));

    // Add axes
    g.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x));

    g.append("g")
      .call(d3.axisLeft(y));
  </script>
</body>
</html>
```

**In your presentation:**
```html
<section>
  <h2>Sales Data</h2>
  <div class="fig-container"
       data-file="visualizations/chart.html"
       style="height: 600px;">
  </div>
  <aside class="notes">
    This interactive chart shows our quarterly sales growth.
    Hover over bars to see the hover effect.
  </aside>
</section>
```

### Method 2: Inline D3 Code

For simpler visualizations, you can embed D3 code directly:

```html
<section>
  <h2>Inline Visualization</h2>
  <div id="inline-viz"></div>

  <script>
    // Wait for slide to be shown
    Reveal.on('slidechanged', event => {
      if (event.currentSlide.querySelector('#inline-viz')) {
        // Create visualization
        const svg = d3.select("#inline-viz")
          .append("svg")
          .attr("width", 600)
          .attr("height", 400);

        // Add your D3 code here
        svg.selectAll("circle")
          .data([50, 100, 150, 200])
          .enter()
          .append("circle")
          .attr("cx", (d, i) => 100 + i * 150)
          .attr("cy", 200)
          .attr("r", d => d / 4)
          .attr("fill", "#00FFF5")
          .attr("opacity", 0)
          .transition()
          .duration(1000)
          .attr("opacity", 1);
      }
    });
  </script>
</section>
```

## Fragment Integration

reveald3 supports reveal.js fragments for progressive visualization disclosure:

**In your external D3 HTML:**
```html
<script>
  // Define fragments for progressive reveal
  const stages = [
    { selector: ".bar:nth-child(1)", delay: 0 },
    { selector: ".bar:nth-child(2)", delay: 200 },
    { selector: ".bar:nth-child(3)", delay: 400 }
  ];

  // Listen for fragment events from parent
  window.addEventListener('message', (event) => {
    if (event.data.type === 'fragment-shown') {
      const index = event.data.index;
      // Show visualization stage
      d3.select(stages[index].selector)
        .transition()
        .duration(500)
        .style("opacity", 1);
    }
  });
</script>
```

**In your presentation:**
```html
<section>
  <h2>Progressive Chart Build</h2>
  <div class="fig-container"
       data-file="visualizations/progressive-chart.html"
       data-fragments="3"
       style="height: 600px;">
  </div>
  <ul>
    <li class="fragment">First data point</li>
    <li class="fragment">Second data point</li>
    <li class="fragment">Third data point</li>
  </ul>
</section>
```

## Advanced Patterns

### Animated Transitions

```javascript
// Smooth transition between data states
function updateChart(newData) {
  const bars = svg.selectAll(".bar")
    .data(newData);

  bars.transition()
    .duration(750)
    .attr("y", d => y(d))
    .attr("height", d => height - y(d));
}

// Trigger on fragment reveal
Reveal.on('fragmentshown', event => {
  if (event.fragment.dataset.update === 'chart') {
    updateChart(nextDataSet);
  }
});
```

### Interactive Tooltips

```javascript
// Add tooltips to D3 elements
const tooltip = d3.select("body")
  .append("div")
  .attr("class", "tooltip")
  .style("opacity", 0)
  .style("position", "absolute")
  .style("background", "#1a1a1a")
  .style("color", "#00FFF5")
  .style("padding", "10px")
  .style("border-radius", "8px")
  .style("pointer-events", "none");

svg.selectAll(".bar")
  .on("mouseover", (event, d) => {
    tooltip.transition().duration(200).style("opacity", .9);
    tooltip.html(`Value: ${d}`)
      .style("left", (event.pageX + 10) + "px")
      .style("top", (event.pageY - 28) + "px");
  })
  .on("mouseout", () => {
    tooltip.transition().duration(500).style("opacity", 0);
  });
```

### Responsive D3 Charts

```javascript
// Make D3 visualization responsive
function responsivefy(svg) {
  const container = d3.select(svg.node().parentNode),
        width = parseInt(svg.style('width'), 10),
        height = parseInt(svg.style('height'), 10),
        aspect = width / height;

  svg.attr('viewBox', `0 0 ${width} ${height}`)
     .attr('preserveAspectRatio', 'xMinYMin')
     .call(resize);

  d3.select(window).on('resize.' + container.attr('id'), resize);

  function resize() {
    const w = parseInt(container.style('width'));
    svg.attr('width', w);
    svg.attr('height', Math.round(w / aspect));
  }
}

// Apply to your SVG
const svg = d3.select("#chart")
  .append("svg")
  .call(responsivefy);
```

## Common D3 Visualizations for Presentations

### 1. Bar Chart (shown above)

### 2. Line Chart with Animations

```javascript
const line = d3.line()
  .x((d, i) => x(i))
  .y(d => y(d))
  .curve(d3.curveMonotoneX);

const path = svg.append("path")
  .datum(data)
  .attr("class", "line")
  .attr("d", line)
  .attr("stroke", "#00FFF5")
  .attr("stroke-width", 3)
  .attr("fill", "none");

// Animate line drawing
const totalLength = path.node().getTotalLength();
path
  .attr("stroke-dasharray", totalLength + " " + totalLength)
  .attr("stroke-dashoffset", totalLength)
  .transition()
  .duration(2000)
  .ease(d3.easeLinear)
  .attr("stroke-dashoffset", 0);
```

### 3. Pie/Donut Chart

```javascript
const pie = d3.pie().value(d => d.value);
const arc = d3.arc()
  .innerRadius(100) // 0 for pie, > 0 for donut
  .outerRadius(200);

const colors = d3.scaleOrdinal()
  .domain(data.map(d => d.name))
  .range(["#00FFF5", "#0080FF", "#B026FF", "#00FF41"]);

const arcs = svg.selectAll("arc")
  .data(pie(data))
  .enter()
  .append("g");

arcs.append("path")
  .attr("d", arc)
  .attr("fill", d => colors(d.data.name))
  .attr("stroke", "#0a0a0a")
  .attr("stroke-width", 2)
  .transition()
  .duration(1000)
  .attrTween("d", function(d) {
    const i = d3.interpolate(d.startAngle, d.endAngle);
    return function(t) {
      d.endAngle = i(t);
      return arc(d);
    };
  });
```

### 4. Force-Directed Network Graph

```javascript
const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id))
  .force("charge", d3.forceManyBody().strength(-400))
  .force("center", d3.forceCenter(width / 2, height / 2));

const link = svg.selectAll(".link")
  .data(links)
  .enter().append("line")
  .attr("class", "link")
  .attr("stroke", "#00FFF5")
  .attr("stroke-opacity", 0.6);

const node = svg.selectAll(".node")
  .data(nodes)
  .enter().append("circle")
  .attr("class", "node")
  .attr("r", 8)
  .attr("fill", "#0080FF")
  .call(d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended));

simulation.on("tick", () => {
  link
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);

  node
    .attr("cx", d => d.x)
    .attr("cy", d => d.y);
});
```

## Troubleshooting

### Visualization not appearing

1. Check console for errors
2. Ensure D3 library is loaded before your code
3. Verify file path in `data-file` attribute
4. Check that container has defined height

### Fragments not working

1. Ensure reveald3 plugin is loaded
2. Add `data-fragments` attribute to container
3. Check that fragment classes match reveal.js syntax

### Performance issues

1. Limit data points for complex visualizations
2. Use `d3.transition()` judiciously
3. Remove old SVG elements before creating new ones
4. Consider using canvas instead of SVG for > 1000 elements

## Best Practices

1. **Keep it simple**: Presentations aren't the place for overly complex visualizations
2. **Animate progressively**: Use fragments to build visualizations step-by-step
3. **Test on target display**: Ensure readability on projector/large screen
4. **Provide context**: Always include axis labels, legends, and titles
5. **Use brand colors**: Match D3 colors to your presentation theme
6. **Add interactivity sparingly**: Too much interaction can be distracting
7. **Fallback static image**: Include screenshot for PDF export or offline viewing

## Resources

- [reveald3 GitHub](https://github.com/gcalmettes/reveal.js-d3)
- [reveald3 Live Demo](https://gcalmettes.github.io/reveal.js-d3/)
- [D3.js Documentation](https://d3js.org/)
- [D3 Observable](https://observablehq.com/@d3) - D3 examples and tutorials
- [D3 Gallery](https://observablehq.com/@d3/gallery) - Visualization examples

## Complete Example

See [examples/d3-presentation/](../examples/d3-presentation/) for a complete working example with multiple D3 visualizations integrated into a reveal.js presentation.
