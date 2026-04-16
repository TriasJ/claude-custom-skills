# Educational Video Templates

<overview>
Templates optimized for educational content including tutorials, explainers, course content, and instructional videos. Designed for clarity, accessibility, and knowledge retention.
</overview>

<design_principles>
- **Clarity over aesthetics:** Information must be easily readable
- **Consistent pacing:** Allow time for comprehension
- **Visual hierarchy:** Guide attention to key concepts
- **Accessibility:** High contrast, readable fonts, caption support
- **Repetition:** Reinforce key points through visual cues
</design_principles>

<template name="ChapterSlide" purpose="Section transitions">
<description>
Title card for chapter/section transitions with clean typography and subtle animations.
</description>

```tsx
// src/compositions/ChapterSlide.tsx
import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from 'remotion';

interface ChapterSlideProps {
  chapterNumber: number;
  title: string;
  subtitle?: string;
  theme?: 'dark' | 'light';
}

export const ChapterSlide: React.FC<ChapterSlideProps> = ({
  chapterNumber,
  title,
  subtitle,
  theme = 'dark',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const colors = theme === 'dark'
    ? {bg: '#0f172a', text: '#f8fafc', accent: '#3b82f6', muted: '#64748b'}
    : {bg: '#f8fafc', text: '#0f172a', accent: '#2563eb', muted: '#64748b'};

  // Chapter number animation
  const numberScale = spring({frame, fps, config: {damping: 100}});
  const numberOpacity = interpolate(frame, [0, 15], [0, 1], {extrapolateRight: 'clamp'});

  // Line expansion
  const lineWidth = spring({
    frame: frame - 10,
    fps,
    config: {damping: 200, stiffness: 80},
  });

  // Title slide-up
  const titleY = spring({
    frame: frame - 20,
    fps,
    config: {damping: 200},
  });
  const titleTranslate = interpolate(titleY, [0, 1], [30, 0]);

  // Subtitle fade
  const subtitleOpacity = interpolate(frame, [40, 55], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.bg,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 100,
      }}
    >
      {/* Chapter Number */}
      <div
        style={{
          fontSize: 24,
          color: colors.accent,
          fontWeight: 600,
          letterSpacing: 4,
          textTransform: 'uppercase',
          opacity: numberOpacity,
          transform: `scale(${numberScale})`,
        }}
      >
        Chapter {chapterNumber}
      </div>

      {/* Decorative Line */}
      <div
        style={{
          width: `${interpolate(lineWidth, [0, 1], [0, 200])}px`,
          height: 2,
          backgroundColor: colors.accent,
          margin: '30px 0',
        }}
      />

      {/* Title */}
      <h1
        style={{
          fontSize: 72,
          fontWeight: 'bold',
          color: colors.text,
          textAlign: 'center',
          margin: 0,
          opacity: titleY,
          transform: `translateY(${titleTranslate}px)`,
        }}
      >
        {title}
      </h1>

      {/* Subtitle */}
      {subtitle && (
        <p
          style={{
            fontSize: 28,
            color: colors.muted,
            marginTop: 20,
            opacity: subtitleOpacity,
            textAlign: 'center',
          }}
        >
          {subtitle}
        </p>
      )}
    </AbsoluteFill>
  );
};
```
</template>

<template name="CodeWalkthrough" purpose="Code demonstrations">
<description>
Syntax-highlighted code with line-by-line reveal and annotation support.
</description>

```tsx
// src/compositions/CodeWalkthrough.tsx
import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  Sequence,
} from 'remotion';

interface CodeLine {
  code: string;
  highlight?: boolean;
  annotation?: string;
}

interface CodeWalkthroughProps {
  title: string;
  language: string;
  lines: CodeLine[];
  framesPerLine?: number;
  theme?: 'dark' | 'light';
}

// Simple syntax highlighting (extend as needed)
const highlightSyntax = (code: string, language: string): React.ReactNode => {
  const keywords = ['const', 'let', 'var', 'function', 'return', 'import', 'export', 'from', 'if', 'else', 'for', 'while'];
  const strings = /'[^']*'|"[^"]*"|`[^`]*`/g;
  const comments = /\/\/.*/g;

  let result = code;

  // This is simplified - use a proper syntax highlighter in production
  keywords.forEach(kw => {
    result = result.replace(new RegExp(`\\b${kw}\\b`, 'g'), `<span style="color:#c678dd">${kw}</span>`);
  });

  return <span dangerouslySetInnerHTML={{__html: result}} />;
};

export const CodeWalkthrough: React.FC<CodeWalkthroughProps> = ({
  title,
  language,
  lines,
  framesPerLine = 20,
  theme = 'dark',
}) => {
  const frame = useCurrentFrame();

  const colors = theme === 'dark'
    ? {bg: '#1e1e1e', surface: '#2d2d2d', text: '#d4d4d4', lineNum: '#858585', highlight: '#264f78'}
    : {bg: '#ffffff', surface: '#f5f5f5', text: '#1e1e1e', lineNum: '#999999', highlight: '#fff3cd'};

  // Calculate visible lines based on frame
  const visibleLines = Math.min(
    lines.length,
    Math.floor(frame / framesPerLine) + 1
  );

  return (
    <AbsoluteFill style={{backgroundColor: colors.bg, padding: 60}}>
      {/* Header */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 30,
        }}
      >
        <h2 style={{color: colors.text, fontSize: 36, margin: 0}}>{title}</h2>
        <span
          style={{
            backgroundColor: colors.surface,
            color: colors.lineNum,
            padding: '8px 16px',
            borderRadius: 6,
            fontSize: 14,
            textTransform: 'uppercase',
          }}
        >
          {language}
        </span>
      </div>

      {/* Code Container */}
      <div
        style={{
          backgroundColor: colors.surface,
          borderRadius: 12,
          padding: 30,
          fontFamily: 'JetBrains Mono, Fira Code, monospace',
          fontSize: 20,
          lineHeight: 1.8,
          overflow: 'hidden',
        }}
      >
        {lines.slice(0, visibleLines).map((line, index) => {
          const lineFrame = frame - (index * framesPerLine);
          const lineOpacity = interpolate(lineFrame, [0, 10], [0, 1], {
            extrapolateRight: 'clamp',
          });

          return (
            <div
              key={index}
              style={{
                display: 'flex',
                alignItems: 'flex-start',
                backgroundColor: line.highlight ? colors.highlight : 'transparent',
                margin: '0 -30px',
                padding: '4px 30px',
                opacity: lineOpacity,
              }}
            >
              {/* Line Number */}
              <span
                style={{
                  color: colors.lineNum,
                  minWidth: 40,
                  textAlign: 'right',
                  marginRight: 20,
                  userSelect: 'none',
                }}
              >
                {index + 1}
              </span>

              {/* Code */}
              <code style={{color: colors.text, flex: 1}}>
                {highlightSyntax(line.code, language)}
              </code>

              {/* Annotation */}
              {line.annotation && lineFrame > 10 && (
                <span
                  style={{
                    color: '#4ade80',
                    fontSize: 16,
                    marginLeft: 20,
                    opacity: interpolate(lineFrame, [10, 20], [0, 1], {
                      extrapolateRight: 'clamp',
                    }),
                  }}
                >
                  // {line.annotation}
                </span>
              )}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Usage example:
// <CodeWalkthrough
//   title="React Hook Example"
//   language="typescript"
//   lines={[
//     {code: "import {useState} from 'react';", annotation: "Import the hook"},
//     {code: ""},
//     {code: "function Counter() {"},
//     {code: "  const [count, setCount] = useState(0);", highlight: true, annotation: "State declaration"},
//     {code: "  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;"},
//     {code: "}"},
//   ]}
// />
```
</template>

<template name="DiagramExplainer" purpose="Animated diagrams">
<description>
Animated diagrams with progressive reveal and callout annotations.
</description>

```tsx
// src/compositions/DiagramExplainer.tsx
import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
} from 'remotion';

interface DiagramNode {
  id: string;
  label: string;
  x: number;
  y: number;
  color?: string;
}

interface DiagramConnection {
  from: string;
  to: string;
  label?: string;
}

interface DiagramExplainerProps {
  title: string;
  nodes: DiagramNode[];
  connections: DiagramConnection[];
  highlightSequence?: string[]; // Node IDs to highlight in order
}

export const DiagramExplainer: React.FC<DiagramExplainerProps> = ({
  title,
  nodes,
  connections,
  highlightSequence = [],
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Find node by ID
  const getNode = (id: string) => nodes.find(n => n.id === id);

  // Calculate which node is currently highlighted
  const framesPerHighlight = 60;
  const currentHighlightIndex = Math.floor(frame / framesPerHighlight);
  const currentHighlight = highlightSequence[currentHighlightIndex];

  return (
    <AbsoluteFill style={{backgroundColor: '#0f172a', padding: 60}}>
      {/* Title */}
      <h1
        style={{
          color: '#f8fafc',
          fontSize: 48,
          marginBottom: 40,
          textAlign: 'center',
        }}
      >
        {title}
      </h1>

      {/* Diagram Area */}
      <div
        style={{
          flex: 1,
          position: 'relative',
        }}
      >
        {/* Connections (lines) */}
        <svg
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            overflow: 'visible',
          }}
        >
          {connections.map((conn, index) => {
            const fromNode = getNode(conn.from);
            const toNode = getNode(conn.to);
            if (!fromNode || !toNode) return null;

            const lineProgress = interpolate(
              frame,
              [index * 15, index * 15 + 30],
              [0, 1],
              {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
            );

            const midX = (fromNode.x + toNode.x) / 2;
            const midY = (fromNode.y + toNode.y) / 2;

            return (
              <g key={`${conn.from}-${conn.to}`}>
                <line
                  x1={`${fromNode.x}%`}
                  y1={`${fromNode.y}%`}
                  x2={`${fromNode.x + (toNode.x - fromNode.x) * lineProgress}%`}
                  y2={`${fromNode.y + (toNode.y - fromNode.y) * lineProgress}%`}
                  stroke="#64748b"
                  strokeWidth={2}
                  markerEnd="url(#arrowhead)"
                />
                {conn.label && lineProgress > 0.5 && (
                  <text
                    x={`${midX}%`}
                    y={`${midY}%`}
                    fill="#94a3b8"
                    fontSize={14}
                    textAnchor="middle"
                    dy={-10}
                  >
                    {conn.label}
                  </text>
                )}
              </g>
            );
          })}
          <defs>
            <marker
              id="arrowhead"
              markerWidth="10"
              markerHeight="7"
              refX="9"
              refY="3.5"
              orient="auto"
            >
              <polygon points="0 0, 10 3.5, 0 7" fill="#64748b" />
            </marker>
          </defs>
        </svg>

        {/* Nodes */}
        {nodes.map((node, index) => {
          const nodeDelay = index * 10;
          const nodeScale = spring({
            frame: frame - nodeDelay,
            fps,
            config: {damping: 100},
          });

          const isHighlighted = node.id === currentHighlight;
          const baseColor = node.color || '#3b82f6';

          return (
            <div
              key={node.id}
              style={{
                position: 'absolute',
                left: `${node.x}%`,
                top: `${node.y}%`,
                transform: `translate(-50%, -50%) scale(${nodeScale})`,
              }}
            >
              <div
                style={{
                  backgroundColor: isHighlighted ? '#22c55e' : baseColor,
                  padding: '20px 30px',
                  borderRadius: 12,
                  boxShadow: isHighlighted
                    ? '0 0 30px rgba(34, 197, 94, 0.5)'
                    : '0 4px 20px rgba(0,0,0,0.3)',
                  transition: 'all 0.3s ease',
                }}
              >
                <span
                  style={{
                    color: '#ffffff',
                    fontSize: 18,
                    fontWeight: 600,
                  }}
                >
                  {node.label}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Usage:
// <DiagramExplainer
//   title="Client-Server Architecture"
//   nodes={[
//     {id: 'client', label: 'Client', x: 20, y: 50, color: '#8b5cf6'},
//     {id: 'server', label: 'Server', x: 50, y: 50, color: '#3b82f6'},
//     {id: 'database', label: 'Database', x: 80, y: 50, color: '#10b981'},
//   ]}
//   connections={[
//     {from: 'client', to: 'server', label: 'HTTP Request'},
//     {from: 'server', to: 'database', label: 'Query'},
//   ]}
//   highlightSequence={['client', 'server', 'database']}
// />
```
</template>

<template name="BulletPointReveal" purpose="Key points">
<description>
Animated bullet point list with progressive reveal.
</description>

```tsx
// src/compositions/BulletPointReveal.tsx
import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from 'remotion';

interface BulletPoint {
  text: string;
  icon?: string;
}

interface BulletPointRevealProps {
  title: string;
  points: BulletPoint[];
  framesPerPoint?: number;
  theme?: 'dark' | 'light';
}

export const BulletPointReveal: React.FC<BulletPointRevealProps> = ({
  title,
  points,
  framesPerPoint = 30,
  theme = 'dark',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const colors = theme === 'dark'
    ? {bg: '#0f172a', text: '#f8fafc', muted: '#94a3b8', accent: '#3b82f6'}
    : {bg: '#ffffff', text: '#1e293b', muted: '#64748b', accent: '#2563eb'};

  // Title animation
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill
      style={{
        backgroundColor: colors.bg,
        padding: 80,
        justifyContent: 'center',
      }}
    >
      {/* Title */}
      <h1
        style={{
          color: colors.text,
          fontSize: 56,
          marginBottom: 60,
          opacity: titleOpacity,
        }}
      >
        {title}
      </h1>

      {/* Bullet Points */}
      <div style={{display: 'flex', flexDirection: 'column', gap: 30}}>
        {points.map((point, index) => {
          const pointFrame = frame - 30 - (index * framesPerPoint);
          const pointProgress = spring({
            frame: pointFrame,
            fps,
            config: {damping: 200},
          });

          const translateX = interpolate(pointProgress, [0, 1], [-50, 0]);
          const opacity = interpolate(pointFrame, [0, 15], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          if (pointFrame < -10) return null;

          return (
            <div
              key={index}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 24,
                opacity,
                transform: `translateX(${translateX}px)`,
              }}
            >
              {/* Bullet Icon */}
              <div
                style={{
                  width: 48,
                  height: 48,
                  borderRadius: '50%',
                  backgroundColor: colors.accent,
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  fontSize: 24,
                  flexShrink: 0,
                }}
              >
                {point.icon || (index + 1)}
              </div>

              {/* Text */}
              <span
                style={{
                  color: colors.text,
                  fontSize: 32,
                }}
              >
                {point.text}
              </span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```
</template>

<template name="SplitScreenComparison" purpose="Before/After comparisons">
```tsx
// src/compositions/SplitScreenComparison.tsx
import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  Img,
  staticFile,
} from 'remotion';

interface SplitScreenComparisonProps {
  leftTitle: string;
  rightTitle: string;
  leftImage?: string;
  rightImage?: string;
  leftContent?: React.ReactNode;
  rightContent?: React.ReactNode;
}

export const SplitScreenComparison: React.FC<SplitScreenComparisonProps> = ({
  leftTitle,
  rightTitle,
  leftImage,
  rightImage,
  leftContent,
  rightContent,
}) => {
  const frame = useCurrentFrame();

  // Divider animation
  const dividerX = interpolate(frame, [0, 30], [0, 50], {extrapolateRight: 'clamp'});

  // Left panel
  const leftOpacity = interpolate(frame, [10, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Right panel
  const rightOpacity = interpolate(frame, [40, 60], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#0f172a'}}>
      {/* Left Panel */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: 0,
          width: '50%',
          height: '100%',
          opacity: leftOpacity,
          padding: 60,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <h2 style={{color: '#ef4444', fontSize: 36, marginBottom: 30}}>
          {leftTitle}
        </h2>
        {leftImage && (
          <Img
            src={staticFile(leftImage)}
            style={{width: '100%', height: 'auto', borderRadius: 12}}
          />
        )}
        {leftContent}
      </div>

      {/* Right Panel */}
      <div
        style={{
          position: 'absolute',
          right: 0,
          top: 0,
          width: '50%',
          height: '100%',
          opacity: rightOpacity,
          padding: 60,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <h2 style={{color: '#22c55e', fontSize: 36, marginBottom: 30}}>
          {rightTitle}
        </h2>
        {rightImage && (
          <Img
            src={staticFile(rightImage)}
            style={{width: '100%', height: 'auto', borderRadius: 12}}
          />
        )}
        {rightContent}
      </div>

      {/* Center Divider */}
      <div
        style={{
          position: 'absolute',
          left: `${dividerX}%`,
          top: 0,
          width: 4,
          height: '100%',
          backgroundColor: '#64748b',
          transform: 'translateX(-50%)',
        }}
      />

      {/* VS Badge */}
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          transform: 'translate(-50%, -50%)',
          backgroundColor: '#1e293b',
          borderRadius: '50%',
          width: 80,
          height: 80,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          border: '3px solid #64748b',
          opacity: interpolate(frame, [50, 60], [0, 1], {extrapolateRight: 'clamp'}),
        }}
      >
        <span style={{color: '#f8fafc', fontSize: 24, fontWeight: 'bold'}}>VS</span>
      </div>
    </AbsoluteFill>
  );
};
```
</template>

<voice_over_sync>
<timing_strategy>
```tsx
// Voice-over timing configuration
interface VoiceOverSegment {
  text: string;          // Script text for reference
  startFrame: number;    // When this segment begins
  endFrame: number;      // When this segment ends
  visualComponent: React.FC;  // Component to show during this segment
}

// Example timing for a 5-minute educational video (30fps = 9000 frames)
const segments: VoiceOverSegment[] = [
  {text: "Welcome to this tutorial...", startFrame: 0, endFrame: 150, visualComponent: IntroSlide},
  {text: "Let's start with the basics...", startFrame: 150, endFrame: 450, visualComponent: Chapter1},
  {text: "Now let's look at an example...", startFrame: 450, endFrame: 900, visualComponent: CodeDemo},
  // ...
];
```
</timing_strategy>

<audio_placeholder>
```tsx
// Use silent placeholder during development, replace with actual voice-over later
import {Audio, staticFile} from 'remotion';

const VoiceOverTrack: React.FC<{src?: string}> = ({src}) => {
  if (!src) {
    // Development mode: no audio
    return null;
  }
  return <Audio src={staticFile(src)} volume={1} />;
};
```
</audio_placeholder>
</voice_over_sync>

<accessibility>
- Use high contrast colors (WCAG AA minimum: 4.5:1 for text)
- Font size minimum: 24px for body, 36px+ for headings
- Avoid red/green only color coding
- Include text alternatives for diagrams
- Design for caption overlay space (bottom 20% of frame)
- Pace animations to allow reading time (~150 words/minute)
</accessibility>
