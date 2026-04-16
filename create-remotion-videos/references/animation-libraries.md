# Animation Libraries Integration

<overview>
Extend Remotion's animation capabilities with specialized JavaScript libraries: D3.js for data visualization, P5.js for generative art, and GSAP for complex timeline animations.
</overview>

<d3_integration>
<setup>
```bash
npm install d3 @types/d3
```
</setup>

<basic_chart>
```tsx
// src/components/D3BarChart.tsx
import React, {useMemo} from 'react';
import {AbsoluteFill, useCurrentFrame, interpolate} from 'remotion';
import * as d3 from 'd3';

interface DataPoint {
  label: string;
  value: number;
}

interface D3BarChartProps {
  data: DataPoint[];
  width?: number;
  height?: number;
  barColor?: string;
}

export const D3BarChart: React.FC<D3BarChartProps> = ({
  data,
  width = 800,
  height = 400,
  barColor = '#3b82f6',
}) => {
  const frame = useCurrentFrame();
  const margin = {top: 20, right: 20, bottom: 40, left: 60};

  // Animation progress
  const progress = interpolate(frame, [0, 60], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // D3 scales
  const {xScale, yScale, maxValue} = useMemo(() => {
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const max = d3.max(data, d => d.value) || 0;

    return {
      xScale: d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([0, innerWidth])
        .padding(0.3),
      yScale: d3.scaleLinear()
        .domain([0, max])
        .range([innerHeight, 0]),
      maxValue: max,
    };
  }, [data, width, height, margin]);

  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  return (
    <svg width={width} height={height}>
      <g transform={`translate(${margin.left}, ${margin.top})`}>
        {/* Y-axis grid lines */}
        {yScale.ticks(5).map((tick, i) => (
          <g key={i}>
            <line
              x1={0}
              x2={innerWidth}
              y1={yScale(tick)}
              y2={yScale(tick)}
              stroke="#e2e8f0"
              strokeDasharray="4,4"
            />
            <text
              x={-10}
              y={yScale(tick)}
              textAnchor="end"
              alignmentBaseline="middle"
              fill="#64748b"
              fontSize={12}
            >
              {tick}
            </text>
          </g>
        ))}

        {/* Bars */}
        {data.map((d, i) => {
          const barHeight = (innerHeight - yScale(d.value)) * progress;
          const barDelay = i * 5;
          const barProgress = interpolate(
            frame - barDelay,
            [0, 30],
            [0, 1],
            {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
          );

          return (
            <g key={d.label}>
              <rect
                x={xScale(d.label)}
                y={innerHeight - barHeight * barProgress}
                width={xScale.bandwidth()}
                height={barHeight * barProgress}
                fill={barColor}
                rx={4}
              />
              {/* Value label */}
              <text
                x={(xScale(d.label) || 0) + xScale.bandwidth() / 2}
                y={innerHeight - barHeight * barProgress - 8}
                textAnchor="middle"
                fill="#1e293b"
                fontSize={14}
                fontWeight="bold"
                opacity={barProgress}
              >
                {Math.round(d.value * barProgress)}
              </text>
              {/* X-axis label */}
              <text
                x={(xScale(d.label) || 0) + xScale.bandwidth() / 2}
                y={innerHeight + 25}
                textAnchor="middle"
                fill="#64748b"
                fontSize={12}
              >
                {d.label}
              </text>
            </g>
          );
        })}
      </g>
    </svg>
  );
};
```
</basic_chart>

<animated_line_chart>
```tsx
// src/components/D3LineChart.tsx
import React, {useMemo} from 'react';
import {useCurrentFrame, interpolate} from 'remotion';
import * as d3 from 'd3';

interface TimeSeriesPoint {
  date: Date | string;
  value: number;
}

interface D3LineChartProps {
  data: TimeSeriesPoint[];
  width?: number;
  height?: number;
  lineColor?: string;
  areaColor?: string;
}

export const D3LineChart: React.FC<D3LineChartProps> = ({
  data,
  width = 800,
  height = 400,
  lineColor = '#3b82f6',
  areaColor = 'rgba(59, 130, 246, 0.2)',
}) => {
  const frame = useCurrentFrame();
  const margin = {top: 20, right: 20, bottom: 40, left: 60};

  // Parse dates if strings
  const parsedData = useMemo(() =>
    data.map(d => ({
      date: typeof d.date === 'string' ? new Date(d.date) : d.date,
      value: d.value,
    })),
    [data]
  );

  // D3 scales
  const {xScale, yScale, line, area} = useMemo(() => {
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const x = d3.scaleTime()
      .domain(d3.extent(parsedData, d => d.date) as [Date, Date])
      .range([0, innerWidth]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(parsedData, d => d.value) || 0])
      .nice()
      .range([innerHeight, 0]);

    const lineGenerator = d3.line<TimeSeriesPoint>()
      .x(d => x(d.date))
      .y(d => y(d.value))
      .curve(d3.curveMonotoneX);

    const areaGenerator = d3.area<TimeSeriesPoint>()
      .x(d => x(d.date))
      .y0(innerHeight)
      .y1(d => y(d.value))
      .curve(d3.curveMonotoneX);

    return {xScale: x, yScale: y, line: lineGenerator, area: areaGenerator};
  }, [parsedData, width, height, margin]);

  // Animation: reveal line from left to right
  const progress = interpolate(frame, [0, 90], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  const clipWidth = innerWidth * progress;

  return (
    <svg width={width} height={height}>
      <defs>
        <clipPath id="line-clip">
          <rect x={0} y={0} width={clipWidth} height={innerHeight + 20} />
        </clipPath>
      </defs>

      <g transform={`translate(${margin.left}, ${margin.top})`}>
        {/* Grid lines */}
        {yScale.ticks(5).map((tick, i) => (
          <line
            key={i}
            x1={0}
            x2={innerWidth}
            y1={yScale(tick)}
            y2={yScale(tick)}
            stroke="#e2e8f0"
            strokeDasharray="4,4"
          />
        ))}

        {/* Area fill */}
        <path
          d={area(parsedData) || ''}
          fill={areaColor}
          clipPath="url(#line-clip)"
        />

        {/* Line */}
        <path
          d={line(parsedData) || ''}
          fill="none"
          stroke={lineColor}
          strokeWidth={3}
          clipPath="url(#line-clip)"
        />

        {/* Data points */}
        {parsedData.map((d, i) => {
          const x = xScale(d.date);
          const opacity = x <= clipWidth ? 1 : 0;
          return (
            <circle
              key={i}
              cx={x}
              cy={yScale(d.value)}
              r={5}
              fill={lineColor}
              opacity={opacity}
            />
          );
        })}
      </g>
    </svg>
  );
};
```
</animated_line_chart>

<pie_chart>
```tsx
// src/components/D3PieChart.tsx
import React, {useMemo} from 'react';
import {useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';
import * as d3 from 'd3';

interface PieDataPoint {
  label: string;
  value: number;
  color?: string;
}

interface D3PieChartProps {
  data: PieDataPoint[];
  size?: number;
  innerRadius?: number;
}

const COLORS = ['#3b82f6', '#ef4444', '#22c55e', '#f59e0b', '#8b5cf6', '#ec4899'];

export const D3PieChart: React.FC<D3PieChartProps> = ({
  data,
  size = 400,
  innerRadius = 0,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const radius = size / 2;
  const center = size / 2;

  // D3 pie and arc generators
  const {pie, arc, arcs} = useMemo(() => {
    const pieGenerator = d3.pie<PieDataPoint>()
      .value(d => d.value)
      .sort(null);

    const arcGenerator = d3.arc<d3.PieArcDatum<PieDataPoint>>()
      .innerRadius(innerRadius)
      .outerRadius(radius - 10);

    return {
      pie: pieGenerator,
      arc: arcGenerator,
      arcs: pieGenerator(data),
    };
  }, [data, radius, innerRadius]);

  // Animation progress
  const overallProgress = interpolate(frame, [0, 60], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <svg width={size} height={size}>
      <g transform={`translate(${center}, ${center})`}>
        {arcs.map((arcData, i) => {
          // Staggered animation per slice
          const sliceProgress = spring({
            frame: frame - i * 5,
            fps,
            config: {damping: 100},
          });

          // Animate endAngle
          const animatedArc = {
            ...arcData,
            endAngle: arcData.startAngle +
              (arcData.endAngle - arcData.startAngle) * sliceProgress,
          };

          const color = arcData.data.color || COLORS[i % COLORS.length];
          const centroid = arc.centroid(animatedArc);

          return (
            <g key={arcData.data.label}>
              <path
                d={arc(animatedArc) || ''}
                fill={color}
                stroke="#ffffff"
                strokeWidth={2}
              />
              {/* Label */}
              {sliceProgress > 0.5 && (
                <text
                  x={centroid[0] * 1.4}
                  y={centroid[1] * 1.4}
                  textAnchor="middle"
                  fill="#1e293b"
                  fontSize={14}
                  fontWeight="bold"
                  opacity={interpolate(sliceProgress, [0.5, 1], [0, 1])}
                >
                  {arcData.data.label}
                </text>
              )}
            </g>
          );
        })}
      </g>
    </svg>
  );
};
```
</pie_chart>
</d3_integration>

<p5_integration>
<setup>
```bash
npm install p5 @types/p5
```
</setup>

<generative_art>
```tsx
// src/components/P5Canvas.tsx
import React, {useEffect, useRef} from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import p5 from 'p5';

interface P5CanvasProps {
  seed?: number;
  backgroundColor?: string;
}

export const P5GenerativeArt: React.FC<P5CanvasProps> = ({
  seed = 12345,
  backgroundColor = '#0a0a0a',
}) => {
  const frame = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Create off-screen canvas for p5
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    canvasRef.current = canvas;

    return () => {
      canvasRef.current = null;
    };
  }, [width, height]);

  useEffect(() => {
    if (!canvasRef.current) return;

    const ctx = canvasRef.current.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, width, height);

    // Seed random for reproducibility
    const seededRandom = (seed: number) => {
      const x = Math.sin(seed++) * 10000;
      return x - Math.floor(x);
    };

    // Flow field parameters
    const scale = 20;
    const cols = Math.floor(width / scale);
    const rows = Math.floor(height / scale);
    const time = frame / fps;

    // Generate flow field
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < cols; x++) {
        const angle = (seededRandom(seed + x + y * cols) * Math.PI * 2 + time) % (Math.PI * 2);
        const length = 15;

        const startX = x * scale + scale / 2;
        const startY = y * scale + scale / 2;
        const endX = startX + Math.cos(angle) * length;
        const endY = startY + Math.sin(angle) * length;

        // Color based on angle
        const hue = (angle / (Math.PI * 2)) * 360;
        ctx.strokeStyle = `hsl(${hue}, 70%, 60%)`;
        ctx.lineWidth = 2;

        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(endX, endY);
        ctx.stroke();
      }
    }
  }, [frame, width, height, backgroundColor, seed, fps]);

  // Convert canvas to data URL and display
  const [imageData, setImageData] = React.useState<string>('');

  useEffect(() => {
    if (canvasRef.current) {
      setImageData(canvasRef.current.toDataURL());
    }
  }, [frame]);

  return (
    <div ref={containerRef} style={{width, height}}>
      {imageData && (
        <img src={imageData} alt="" style={{width: '100%', height: '100%'}} />
      )}
    </div>
  );
};
```
</generative_art>

<particle_flow>
```tsx
// src/components/P5ParticleFlow.tsx
import React, {useEffect, useRef, useState} from 'react';
import {useCurrentFrame, useVideoConfig, AbsoluteFill} from 'remotion';

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
}

export const P5ParticleFlow: React.FC<{
  particleCount?: number;
  color?: string;
}> = ({
  particleCount = 500,
  color = '#00d9ff',
}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Initialize particles (only once)
  const [particles] = useState<Particle[]>(() => {
    const arr: Particle[] = [];
    for (let i = 0; i < particleCount; i++) {
      arr.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2,
        life: Math.random(),
      });
    }
    return arr;
  });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear with fade effect
    ctx.fillStyle = 'rgba(10, 10, 10, 0.1)';
    ctx.fillRect(0, 0, width, height);

    const time = frame / 30;

    // Update and draw particles
    particles.forEach((p) => {
      // Perlin-like noise for flow field
      const angle = Math.sin(p.x * 0.01 + time) * Math.cos(p.y * 0.01 + time) * Math.PI * 2;

      p.vx += Math.cos(angle) * 0.1;
      p.vy += Math.sin(angle) * 0.1;

      // Damping
      p.vx *= 0.99;
      p.vy *= 0.99;

      // Update position
      p.x += p.vx;
      p.y += p.vy;

      // Wrap around edges
      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      // Draw particle
      ctx.beginPath();
      ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
    });
  }, [frame, particles, width, height, color]);

  return (
    <AbsoluteFill style={{backgroundColor: '#0a0a0a'}}>
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        style={{width: '100%', height: '100%'}}
      />
    </AbsoluteFill>
  );
};
```
</particle_flow>
</p5_integration>

<gsap_integration>
<setup>
```bash
npm install gsap
```
</setup>

<timeline_animation>
```tsx
// src/components/GSAPTimeline.tsx
// Note: GSAP is typically used for imperative animations
// In Remotion, we need to adapt it to work with frame-based rendering

import React, {useMemo} from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {gsap} from 'gsap';

interface TimelineStep {
  target: string;
  props: gsap.TweenVars;
  position?: number | string;
}

// Convert GSAP easing to Remotion-compatible values
const gsapEase = (progress: number, easing: string = 'power2.out'): number => {
  // Simplified easing conversion
  switch (easing) {
    case 'power2.out':
      return 1 - Math.pow(1 - progress, 2);
    case 'power2.in':
      return progress * progress;
    case 'power3.out':
      return 1 - Math.pow(1 - progress, 3);
    case 'elastic.out':
      return progress === 0 ? 0 : progress === 1 ? 1 :
        Math.pow(2, -10 * progress) * Math.sin((progress * 10 - 0.75) * (2 * Math.PI / 3)) + 1;
    case 'bounce.out':
      const n1 = 7.5625;
      const d1 = 2.75;
      if (progress < 1 / d1) return n1 * progress * progress;
      if (progress < 2 / d1) return n1 * (progress -= 1.5 / d1) * progress + 0.75;
      if (progress < 2.5 / d1) return n1 * (progress -= 2.25 / d1) * progress + 0.9375;
      return n1 * (progress -= 2.625 / d1) * progress + 0.984375;
    default:
      return progress;
  }
};

// GSAP-style animation component
export const GSAPBox: React.FC<{
  fromProps: React.CSSProperties;
  toProps: React.CSSProperties;
  startFrame: number;
  duration: number;
  easing?: string;
  children?: React.ReactNode;
}> = ({
  fromProps,
  toProps,
  startFrame,
  duration,
  easing = 'power2.out',
  children,
}) => {
  const frame = useCurrentFrame();

  // Calculate progress
  const rawProgress = interpolate(
    frame,
    [startFrame, startFrame + duration],
    [0, 1],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );
  const progress = gsapEase(rawProgress, easing);

  // Interpolate each property
  const animatedStyle = useMemo(() => {
    const style: React.CSSProperties = {};

    Object.keys(toProps).forEach((key) => {
      const fromValue = (fromProps as any)[key];
      const toValue = (toProps as any)[key];

      if (typeof fromValue === 'number' && typeof toValue === 'number') {
        (style as any)[key] = fromValue + (toValue - fromValue) * progress;
      } else if (key === 'opacity') {
        style.opacity = (fromValue || 0) + ((toValue || 1) - (fromValue || 0)) * progress;
      }
    });

    return style;
  }, [fromProps, toProps, progress]);

  return (
    <div style={{...fromProps, ...animatedStyle}}>
      {children}
    </div>
  );
};

// Example composition with multiple animated elements
export const GSAPSequence: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{backgroundColor: '#0f172a', justifyContent: 'center', alignItems: 'center'}}>
      {/* Box 1 - Scale in */}
      <GSAPBox
        fromProps={{
          width: 100,
          height: 100,
          backgroundColor: '#3b82f6',
          borderRadius: 10,
          position: 'absolute',
          left: 200,
          transform: 'scale(0)',
        }}
        toProps={{
          transform: 'scale(1)',
        }}
        startFrame={0}
        duration={30}
        easing="elastic.out"
      />

      {/* Box 2 - Slide in */}
      <GSAPBox
        fromProps={{
          width: 100,
          height: 100,
          backgroundColor: '#22c55e',
          borderRadius: 10,
          position: 'absolute',
          left: -100,
          top: 300,
          opacity: 0,
        }}
        toProps={{
          left: 400,
          opacity: 1,
        }}
        startFrame={30}
        duration={45}
        easing="power2.out"
      />

      {/* Box 3 - Bounce */}
      <GSAPBox
        fromProps={{
          width: 100,
          height: 100,
          backgroundColor: '#f59e0b',
          borderRadius: 10,
          position: 'absolute',
          right: 200,
          top: -100,
        }}
        toProps={{
          top: 400,
        }}
        startFrame={60}
        duration={60}
        easing="bounce.out"
      />
    </AbsoluteFill>
  );
};
```
</timeline_animation>

<stagger_animation>
```tsx
// src/components/GSAPStagger.tsx
import React from 'react';
import {AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig} from 'remotion';

interface StaggerProps {
  items: string[];
  staggerDelay?: number;
}

export const GSAPStagger: React.FC<StaggerProps> = ({
  items,
  staggerDelay = 5,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0f172a',
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        gap: 20,
      }}
    >
      {items.map((item, index) => {
        const itemDelay = index * staggerDelay;
        const progress = spring({
          frame: frame - itemDelay,
          fps,
          config: {damping: 100},
        });

        const opacity = interpolate(progress, [0, 1], [0, 1]);
        const translateX = interpolate(progress, [0, 1], [-100, 0]);
        const scale = interpolate(progress, [0, 1], [0.5, 1]);

        return (
          <div
            key={index}
            style={{
              padding: '20px 40px',
              backgroundColor: '#3b82f6',
              borderRadius: 10,
              color: '#ffffff',
              fontSize: 24,
              fontWeight: 'bold',
              opacity,
              transform: `translateX(${translateX}px) scale(${scale})`,
            }}
          >
            {item}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// Usage:
// <GSAPStagger items={['First Item', 'Second Item', 'Third Item', 'Fourth Item']} />
```
</stagger_animation>
</gsap_integration>

<best_practices>
- **D3.js:** Pre-calculate scales and generators with `useMemo` to avoid recalculation every frame
- **P5.js:** Use canvas-based rendering for better performance; avoid recreating sketches
- **GSAP:** Convert GSAP timelines to frame-based calculations; GSAP's real-time animations don't work directly
- **All libraries:** Cache expensive computations; Remotion re-renders every frame
- **Memory:** Clean up resources (canvas contexts, WebGL) in useEffect cleanup
- **Seeding:** Use seeded random for reproducible generative art
</best_practices>

<context7_lookup>
For current documentation, use Context7 MCP:
- D3.js: `/d3/d3`
- P5.js: `/websites/p5js_reference`
- GSAP: `/websites/gsap_v3`
</context7_lookup>
