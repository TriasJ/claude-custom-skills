# Scientific Video Templates

<overview>
Templates optimized for scientific presentations, research communication, data visualization, and academic content. Emphasizes precision, clarity, and professional aesthetics suitable for conferences, journals, and educational institutions.
</overview>

<design_principles>
- **Accuracy first:** Data representation must be precise and truthful
- **Citation ready:** Include space for references and attributions
- **Professional aesthetics:** Clean, academic-appropriate styling
- **Color accessibility:** Colorblind-safe palettes
- **High resolution:** Support 4K for detailed graphs and imagery
</design_principles>

<template name="DataVisualization" purpose="Charts and graphs">
<description>
Animated data visualization with D3.js integration for accurate, beautiful charts.
</description>

```tsx
// src/compositions/DataVisualization.tsx
import React, {useMemo} from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from 'remotion';

interface DataPoint {
  label: string;
  value: number;
  color?: string;
}

interface DataVisualizationProps {
  title: string;
  subtitle?: string;
  data: DataPoint[];
  chartType: 'bar' | 'line' | 'pie';
  source?: string;
  yAxisLabel?: string;
  xAxisLabel?: string;
}

// Colorblind-safe palette (Wong palette)
const SAFE_COLORS = [
  '#0072B2', // Blue
  '#E69F00', // Orange
  '#009E73', // Green
  '#CC79A7', // Pink
  '#F0E442', // Yellow
  '#56B4E9', // Sky Blue
  '#D55E00', // Vermillion
];

export const DataVisualization: React.FC<DataVisualizationProps> = ({
  title,
  subtitle,
  data,
  chartType,
  source,
  yAxisLabel,
  xAxisLabel,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();

  const maxValue = Math.max(...data.map(d => d.value));
  const chartWidth = width - 300;
  const chartHeight = height - 400;

  // Animation progress (0 to 1 over 60 frames)
  const animationProgress = interpolate(frame, [30, 90], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Title animation
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0f172a',
        padding: 80,
        fontFamily: 'Inter, system-ui, sans-serif',
      }}
    >
      {/* Header */}
      <div style={{marginBottom: 40, opacity: titleOpacity}}>
        <h1 style={{color: '#f8fafc', fontSize: 48, margin: 0, fontWeight: 600}}>
          {title}
        </h1>
        {subtitle && (
          <p style={{color: '#94a3b8', fontSize: 24, margin: '10px 0 0'}}>
            {subtitle}
          </p>
        )}
      </div>

      {/* Chart Area */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* Y-Axis Label */}
        {yAxisLabel && (
          <div
            style={{
              position: 'absolute',
              left: 20,
              top: '50%',
              transform: 'rotate(-90deg) translateX(-50%)',
              color: '#64748b',
              fontSize: 16,
            }}
          >
            {yAxisLabel}
          </div>
        )}

        {/* Chart Container */}
        <div style={{flex: 1, display: 'flex', alignItems: 'flex-end', gap: 20, paddingLeft: 60}}>
          {chartType === 'bar' && (
            <BarChart
              data={data}
              maxValue={maxValue}
              chartHeight={chartHeight}
              animationProgress={animationProgress}
            />
          )}
          {chartType === 'line' && (
            <LineChart
              data={data}
              maxValue={maxValue}
              chartWidth={chartWidth}
              chartHeight={chartHeight}
              animationProgress={animationProgress}
            />
          )}
        </div>

        {/* X-Axis Label */}
        {xAxisLabel && (
          <div
            style={{
              textAlign: 'center',
              color: '#64748b',
              fontSize: 16,
              marginTop: 20,
            }}
          >
            {xAxisLabel}
          </div>
        )}
      </div>

      {/* Source Citation */}
      {source && (
        <div
          style={{
            color: '#64748b',
            fontSize: 14,
            marginTop: 20,
            fontStyle: 'italic',
          }}
        >
          Source: {source}
        </div>
      )}
    </AbsoluteFill>
  );
};

// Bar Chart Component
const BarChart: React.FC<{
  data: DataPoint[];
  maxValue: number;
  chartHeight: number;
  animationProgress: number;
}> = ({data, maxValue, chartHeight, animationProgress}) => {
  return (
    <>
      {data.map((point, index) => {
        const barHeight = (point.value / maxValue) * chartHeight * animationProgress;
        const color = point.color || SAFE_COLORS[index % SAFE_COLORS.length];

        return (
          <div
            key={point.label}
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              flex: 1,
            }}
          >
            {/* Value Label */}
            <span
              style={{
                color: '#f8fafc',
                fontSize: 18,
                fontWeight: 600,
                marginBottom: 8,
                opacity: animationProgress,
              }}
            >
              {Math.round(point.value * animationProgress).toLocaleString()}
            </span>

            {/* Bar */}
            <div
              style={{
                width: '60%',
                height: barHeight,
                backgroundColor: color,
                borderRadius: '4px 4px 0 0',
              }}
            />

            {/* Label */}
            <span
              style={{
                color: '#94a3b8',
                fontSize: 14,
                marginTop: 12,
                textAlign: 'center',
              }}
            >
              {point.label}
            </span>
          </div>
        );
      })}
    </>
  );
};

// Line Chart Component
const LineChart: React.FC<{
  data: DataPoint[];
  maxValue: number;
  chartWidth: number;
  chartHeight: number;
  animationProgress: number;
}> = ({data, maxValue, chartWidth, chartHeight, animationProgress}) => {
  const points = data.map((point, index) => ({
    x: (index / (data.length - 1)) * chartWidth,
    y: chartHeight - (point.value / maxValue) * chartHeight,
    ...point,
  }));

  const pathLength = points.length;
  const visiblePoints = Math.floor(pathLength * animationProgress);

  const pathD = points
    .slice(0, visiblePoints + 1)
    .map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`)
    .join(' ');

  return (
    <svg width={chartWidth} height={chartHeight} style={{overflow: 'visible'}}>
      {/* Grid Lines */}
      {[0, 0.25, 0.5, 0.75, 1].map((ratio) => (
        <line
          key={ratio}
          x1={0}
          y1={chartHeight * ratio}
          x2={chartWidth}
          y2={chartHeight * ratio}
          stroke="#1e293b"
          strokeWidth={1}
        />
      ))}

      {/* Line Path */}
      <path
        d={pathD}
        fill="none"
        stroke={SAFE_COLORS[0]}
        strokeWidth={3}
        strokeLinecap="round"
        strokeLinejoin="round"
      />

      {/* Data Points */}
      {points.slice(0, visiblePoints + 1).map((point, index) => (
        <g key={index}>
          <circle
            cx={point.x}
            cy={point.y}
            r={6}
            fill={SAFE_COLORS[0]}
            stroke="#0f172a"
            strokeWidth={2}
          />
          <text
            x={point.x}
            y={point.y - 15}
            fill="#f8fafc"
            fontSize={14}
            textAnchor="middle"
          >
            {point.value}
          </text>
        </g>
      ))}
    </svg>
  );
};
```
</template>

<template name="MolecularViewer" purpose="3D molecular structures">
<description>
3D molecule rendering using Three.js for chemistry and biology content.
</description>

```tsx
// src/compositions/MolecularViewer.tsx
// Requires: @remotion/three, @react-three/fiber
import React, {useRef, useEffect} from 'react';
import {ThreeCanvas} from '@remotion/three';
import {useFrame, useThree} from '@react-three/fiber';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from 'remotion';
import * as THREE from 'three';

interface Atom {
  element: string;
  position: [number, number, number];
  color?: string;
  radius?: number;
}

interface Bond {
  from: number;
  to: number;
}

interface MolecularViewerProps {
  title: string;
  atoms: Atom[];
  bonds: Bond[];
  rotationSpeed?: number;
}

// Element colors (CPK coloring convention)
const ELEMENT_COLORS: Record<string, string> = {
  H: '#ffffff',
  C: '#909090',
  N: '#3050f8',
  O: '#ff0d0d',
  S: '#ffff30',
  P: '#ff8000',
  F: '#90e050',
  Cl: '#1ff01f',
  default: '#ff1493',
};

const ELEMENT_RADII: Record<string, number> = {
  H: 0.3,
  C: 0.5,
  N: 0.5,
  O: 0.5,
  S: 0.6,
  P: 0.6,
  default: 0.5,
};

const MoleculeScene: React.FC<{
  atoms: Atom[];
  bonds: Bond[];
  frame: number;
  rotationSpeed: number;
}> = ({atoms, bonds, frame, rotationSpeed}) => {
  const groupRef = useRef<THREE.Group>(null);
  const {camera} = useThree();

  useEffect(() => {
    camera.position.set(0, 0, 10);
    camera.lookAt(0, 0, 0);
  }, [camera]);

  // Rotate molecule
  const rotation = (frame / 30) * rotationSpeed;

  return (
    <group ref={groupRef} rotation={[0, rotation, 0]}>
      {/* Atoms */}
      {atoms.map((atom, index) => {
        const color = atom.color || ELEMENT_COLORS[atom.element] || ELEMENT_COLORS.default;
        const radius = atom.radius || ELEMENT_RADII[atom.element] || ELEMENT_RADII.default;

        return (
          <mesh key={`atom-${index}`} position={atom.position}>
            <sphereGeometry args={[radius, 32, 32]} />
            <meshStandardMaterial color={color} />
          </mesh>
        );
      })}

      {/* Bonds */}
      {bonds.map((bond, index) => {
        const from = new THREE.Vector3(...atoms[bond.from].position);
        const to = new THREE.Vector3(...atoms[bond.to].position);
        const direction = new THREE.Vector3().subVectors(to, from);
        const length = direction.length();
        const midpoint = new THREE.Vector3().addVectors(from, to).multiplyScalar(0.5);

        return (
          <mesh
            key={`bond-${index}`}
            position={midpoint}
            quaternion={new THREE.Quaternion().setFromUnitVectors(
              new THREE.Vector3(0, 1, 0),
              direction.normalize()
            )}
          >
            <cylinderGeometry args={[0.1, 0.1, length, 8]} />
            <meshStandardMaterial color="#666666" />
          </mesh>
        );
      })}

      {/* Lighting */}
      <ambientLight intensity={0.4} />
      <pointLight position={[10, 10, 10]} intensity={0.8} />
      <pointLight position={[-10, -10, -10]} intensity={0.4} />
    </group>
  );
};

export const MolecularViewer: React.FC<MolecularViewerProps> = ({
  title,
  atoms,
  bonds,
  rotationSpeed = 0.5,
}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{backgroundColor: '#0a0a0a'}}>
      {/* 3D Canvas */}
      <ThreeCanvas
        width={width}
        height={height}
        style={{position: 'absolute', top: 0, left: 0}}
      >
        <MoleculeScene
          atoms={atoms}
          bonds={bonds}
          frame={frame}
          rotationSpeed={rotationSpeed}
        />
      </ThreeCanvas>

      {/* Title Overlay */}
      <div
        style={{
          position: 'absolute',
          bottom: 80,
          left: 80,
          opacity: titleOpacity,
        }}
      >
        <h1 style={{color: '#ffffff', fontSize: 48, margin: 0}}>
          {title}
        </h1>
      </div>
    </AbsoluteFill>
  );
};

// Example usage for water molecule (H2O):
// <MolecularViewer
//   title="Water Molecule (H₂O)"
//   atoms={[
//     {element: 'O', position: [0, 0, 0]},
//     {element: 'H', position: [0.96, 0, 0]},
//     {element: 'H', position: [-0.24, 0.93, 0]},
//   ]}
//   bonds={[
//     {from: 0, to: 1},
//     {from: 0, to: 2},
//   ]}
// />
```
</template>

<template name="TimelinePresentation" purpose="Research timelines">
<description>
Animated timeline for presenting research history, methodology phases, or chronological data.
</description>

```tsx
// src/compositions/TimelinePresentation.tsx
import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from 'remotion';

interface TimelineEvent {
  date: string;
  title: string;
  description?: string;
  citation?: string;
}

interface TimelinePresentationProps {
  title: string;
  events: TimelineEvent[];
  framesPerEvent?: number;
}

export const TimelinePresentation: React.FC<TimelinePresentationProps> = ({
  title,
  events,
  framesPerEvent = 60,
}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();

  // Title animation
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {extrapolateRight: 'clamp'});

  // Calculate timeline progress
  const timelineProgress = interpolate(
    frame,
    [30, 30 + events.length * framesPerEvent],
    [0, 1],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
  );

  return (
    <AbsoluteFill style={{backgroundColor: '#0f172a', padding: 80}}>
      {/* Title */}
      <h1
        style={{
          color: '#f8fafc',
          fontSize: 48,
          marginBottom: 60,
          opacity: titleOpacity,
        }}
      >
        {title}
      </h1>

      {/* Timeline Container */}
      <div style={{flex: 1, position: 'relative', marginLeft: 100}}>
        {/* Timeline Line */}
        <div
          style={{
            position: 'absolute',
            left: 0,
            top: 0,
            bottom: 0,
            width: 4,
            backgroundColor: '#1e293b',
          }}
        >
          {/* Progress indicator */}
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${timelineProgress * 100}%`,
              backgroundColor: '#3b82f6',
            }}
          />
        </div>

        {/* Events */}
        {events.map((event, index) => {
          const eventStartFrame = 30 + index * framesPerEvent;
          const eventProgress = spring({
            frame: frame - eventStartFrame,
            fps,
            config: {damping: 200},
          });

          const isVisible = frame >= eventStartFrame - 10;

          if (!isVisible) return null;

          return (
            <div
              key={index}
              style={{
                position: 'absolute',
                top: `${(index / (events.length - 1 || 1)) * 80 + 5}%`,
                left: 0,
                display: 'flex',
                alignItems: 'flex-start',
                opacity: eventProgress,
                transform: `translateX(${interpolate(eventProgress, [0, 1], [-30, 0])}px)`,
              }}
            >
              {/* Timeline Node */}
              <div
                style={{
                  width: 20,
                  height: 20,
                  borderRadius: '50%',
                  backgroundColor: '#3b82f6',
                  marginLeft: -8,
                  marginRight: 30,
                  flexShrink: 0,
                  boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)',
                }}
              />

              {/* Event Content */}
              <div style={{maxWidth: width - 400}}>
                <span
                  style={{
                    color: '#3b82f6',
                    fontSize: 18,
                    fontWeight: 600,
                    display: 'block',
                    marginBottom: 8,
                  }}
                >
                  {event.date}
                </span>
                <h3
                  style={{
                    color: '#f8fafc',
                    fontSize: 28,
                    margin: '0 0 10px',
                    fontWeight: 600,
                  }}
                >
                  {event.title}
                </h3>
                {event.description && (
                  <p style={{color: '#94a3b8', fontSize: 18, margin: 0}}>
                    {event.description}
                  </p>
                )}
                {event.citation && (
                  <span
                    style={{
                      color: '#64748b',
                      fontSize: 14,
                      fontStyle: 'italic',
                      display: 'block',
                      marginTop: 8,
                    }}
                  >
                    [{event.citation}]
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```
</template>

<template name="EquationReveal" purpose="Mathematical equations">
```tsx
// src/compositions/EquationReveal.tsx
import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from 'remotion';

interface EquationPart {
  latex: string;  // For display (use actual LaTeX renderer in production)
  annotation?: string;
}

interface EquationRevealProps {
  title: string;
  equation: string;
  parts?: EquationPart[];
  explanation?: string;
}

export const EquationReveal: React.FC<EquationRevealProps> = ({
  title,
  equation,
  parts = [],
  explanation,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Title fade
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {extrapolateRight: 'clamp'});

  // Equation reveal (character by character simulation)
  const equationProgress = interpolate(frame, [30, 90], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const visibleChars = Math.floor(equation.length * equationProgress);

  // Explanation fade
  const explanationOpacity = interpolate(frame, [100, 120], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0f172a',
        padding: 100,
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      {/* Title */}
      <h2
        style={{
          position: 'absolute',
          top: 80,
          color: '#94a3b8',
          fontSize: 32,
          opacity: titleOpacity,
        }}
      >
        {title}
      </h2>

      {/* Main Equation */}
      <div
        style={{
          fontFamily: 'serif',
          fontSize: 72,
          color: '#f8fafc',
          letterSpacing: 4,
        }}
      >
        {equation.slice(0, visibleChars)}
        <span style={{opacity: frame % 30 < 15 ? 1 : 0, color: '#3b82f6'}}>|</span>
      </div>

      {/* Explanation */}
      {explanation && (
        <p
          style={{
            position: 'absolute',
            bottom: 150,
            color: '#94a3b8',
            fontSize: 28,
            textAlign: 'center',
            maxWidth: '80%',
            opacity: explanationOpacity,
          }}
        >
          {explanation}
        </p>
      )}
    </AbsoluteFill>
  );
};

// Note: For production, integrate with a LaTeX renderer like KaTeX or MathJax
// Example: npm install katex
// import katex from 'katex';
// const html = katex.renderToString(equation, {displayMode: true});
```
</template>

<color_palettes>
<palette name="Colorblind Safe (Wong)">
```tsx
// Optimized for deuteranopia, protanopia, and tritanopia
const wongPalette = {
  blue: '#0072B2',
  orange: '#E69F00',
  green: '#009E73',
  pink: '#CC79A7',
  yellow: '#F0E442',
  skyBlue: '#56B4E9',
  vermillion: '#D55E00',
  black: '#000000',
};
```
</palette>

<palette name="Scientific Journal">
```tsx
// Professional, print-friendly colors
const journalPalette = {
  primary: '#1a365d',
  secondary: '#2c5282',
  accent: '#3182ce',
  success: '#276749',
  warning: '#c05621',
  error: '#c53030',
  neutral: '#4a5568',
  background: '#f7fafc',
};
```
</palette>

<palette name="Neon Scientific">
```tsx
// Modern, dark theme for presentations
const neonScientific = {
  background: '#0a0a0a',
  surface: '#1a1a2e',
  primary: '#00d9ff',
  secondary: '#00ff88',
  accent: '#ff00ff',
  warning: '#ffaa00',
  text: '#ffffff',
  muted: '#888888',
};
```
</palette>
</color_palettes>

<citation_format>
```tsx
// Reusable citation component
interface CitationProps {
  authors: string;
  year: number;
  title: string;
  journal?: string;
  doi?: string;
}

const Citation: React.FC<CitationProps> = ({authors, year, title, journal, doi}) => (
  <div style={{fontSize: 14, color: '#64748b', fontStyle: 'italic'}}>
    {authors} ({year}). {title}.
    {journal && <em> {journal}</em>}.
    {doi && <span> doi: {doi}</span>}
  </div>
);
```
</citation_format>

<best_practices>
- **Data integrity:** Never distort axes or scales
- **Clear legends:** Always label data series
- **Error bars:** Include uncertainty when applicable
- **Reproducibility:** Document data sources
- **Resolution:** Use 4K for detailed charts
- **Animation pacing:** Slow enough for data comprehension (2-3 seconds per data point)
- **Color contrast:** Test with colorblind simulators
- **Font choice:** Sans-serif for labels, serif for equations
</best_practices>
