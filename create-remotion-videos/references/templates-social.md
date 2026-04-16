# Social Media Video Templates

<overview>
Templates optimized for social media platforms with appropriate dimensions, durations, and engagement-focused animations.
</overview>

<platform_specs>
| Platform | Dimensions | Aspect Ratio | Max Duration | Recommended FPS |
|----------|------------|--------------|--------------|-----------------|
| TikTok | 1080x1920 | 9:16 | 10 min | 30 |
| Instagram Reels | 1080x1920 | 9:16 | 90 sec | 30 |
| Instagram Stories | 1080x1920 | 9:16 | 60 sec | 30 |
| Instagram Feed | 1080x1080 | 1:1 | 60 sec | 30 |
| YouTube Shorts | 1080x1920 | 9:16 | 60 sec | 30-60 |
| Twitter/X | 1920x1080 | 16:9 | 2:20 min | 30 |
</platform_specs>

<template name="VerticalIntro" aspect="9:16">
<description>
Animated text reveal with dynamic background for TikTok/Reels intros.
</description>

```tsx
// src/compositions/VerticalIntro.tsx
import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
} from 'remotion';

interface VerticalIntroProps {
  title: string;
  subtitle?: string;
  backgroundColor?: string;
  textColor?: string;
}

export const VerticalIntro: React.FC<VerticalIntroProps> = ({
  title,
  subtitle,
  backgroundColor = '#0a0a0a',
  textColor = '#ffffff',
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();

  // Title animation
  const titleY = spring({
    frame,
    fps,
    config: {damping: 200, stiffness: 100},
  });
  const titleTranslate = interpolate(titleY, [0, 1], [100, 0]);
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {extrapolateRight: 'clamp'});

  // Subtitle animation (delayed)
  const subtitleOpacity = interpolate(frame, [20, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Background pulse effect
  const pulse = Math.sin(frame * 0.05) * 0.1 + 1;

  return (
    <AbsoluteFill
      style={{
        backgroundColor,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 60,
      }}
    >
      {/* Animated background gradient */}
      <div
        style={{
          position: 'absolute',
          width: width * pulse,
          height: height * pulse,
          background: `radial-gradient(circle at 50% 50%, ${backgroundColor}00, ${backgroundColor})`,
          opacity: 0.5,
        }}
      />

      {/* Title */}
      <h1
        style={{
          color: textColor,
          fontSize: 72,
          fontWeight: 'bold',
          textAlign: 'center',
          opacity: titleOpacity,
          transform: `translateY(${titleTranslate}px)`,
          margin: 0,
          zIndex: 1,
        }}
      >
        {title}
      </h1>

      {/* Subtitle */}
      {subtitle && (
        <p
          style={{
            color: textColor,
            fontSize: 32,
            opacity: subtitleOpacity,
            marginTop: 20,
            textAlign: 'center',
            zIndex: 1,
          }}
        >
          {subtitle}
        </p>
      )}
    </AbsoluteFill>
  );
};

// Register composition
// In Root.tsx:
// <Composition
//   id="VerticalIntro"
//   component={VerticalIntro}
//   durationInFrames={90}
//   fps={30}
//   width={1080}
//   height={1920}
//   defaultProps={{title: 'Your Title', subtitle: 'Your Subtitle'}}
// />
```
</template>

<template name="SquarePromo" aspect="1:1">
<description>
Product showcase template with zoom and reveal effects for Instagram feed.
</description>

```tsx
// src/compositions/SquarePromo.tsx
import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Img,
  Sequence,
  staticFile,
} from 'remotion';

interface SquarePromoProps {
  productImage: string;
  headline: string;
  tagline: string;
  ctaText?: string;
  brandColor?: string;
}

export const SquarePromo: React.FC<SquarePromoProps> = ({
  productImage,
  headline,
  tagline,
  ctaText = 'Shop Now',
  brandColor = '#ff6b35',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Product zoom-in effect
  const productScale = spring({
    frame,
    fps,
    config: {damping: 100, stiffness: 80},
    from: 1.5,
    to: 1,
  });

  // Text slide-in
  const headlineSlide = spring({
    frame: frame - 15,
    fps,
    config: {damping: 200},
  });
  const headlineX = interpolate(headlineSlide, [0, 1], [-200, 0]);

  const taglineOpacity = interpolate(frame, [30, 45], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // CTA button animation
  const ctaScale = spring({
    frame: frame - 50,
    fps,
    config: {damping: 150, stiffness: 200},
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#ffffff'}}>
      {/* Product Image */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '60%',
          overflow: 'hidden',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Img
          src={staticFile(productImage)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transform: `scale(${productScale})`,
          }}
        />
      </div>

      {/* Text Content */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: '40%',
          padding: 40,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}
      >
        <h2
          style={{
            fontSize: 48,
            fontWeight: 'bold',
            margin: 0,
            transform: `translateX(${headlineX}px)`,
          }}
        >
          {headline}
        </h2>
        <p
          style={{
            fontSize: 24,
            color: '#666',
            opacity: taglineOpacity,
            marginTop: 10,
          }}
        >
          {tagline}
        </p>

        {/* CTA Button */}
        <div
          style={{
            marginTop: 30,
            transform: `scale(${ctaScale})`,
            transformOrigin: 'left center',
          }}
        >
          <span
            style={{
              backgroundColor: brandColor,
              color: '#fff',
              padding: '15px 40px',
              borderRadius: 30,
              fontSize: 20,
              fontWeight: 'bold',
            }}
          >
            {ctaText}
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
```
</template>

<template name="HorizontalTeaser" aspect="16:9">
<description>
Cinematic teaser with letterbox effect and dramatic text reveals.
</description>

```tsx
// src/compositions/HorizontalTeaser.tsx
import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Video,
  staticFile,
  Sequence,
} from 'remotion';

interface HorizontalTeaserProps {
  backgroundVideo?: string;
  mainText: string;
  secondaryText?: string;
  releaseDate?: string;
}

export const HorizontalTeaser: React.FC<HorizontalTeaserProps> = ({
  backgroundVideo,
  mainText,
  secondaryText,
  releaseDate,
}) => {
  const frame = useCurrentFrame();
  const {fps, height} = useVideoConfig();

  // Letterbox animation
  const letterboxHeight = interpolate(frame, [0, 30], [0, height * 0.12], {
    extrapolateRight: 'clamp',
  });

  // Main text character-by-character reveal
  const textProgress = interpolate(frame, [30, 60], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Secondary text fade
  const secondaryOpacity = interpolate(frame, [70, 90], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Release date slide-up
  const dateY = spring({
    frame: frame - 100,
    fps,
    config: {damping: 200},
  });
  const dateTranslate = interpolate(dateY, [0, 1], [50, 0]);

  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      {/* Background Video */}
      {backgroundVideo && (
        <Video
          src={staticFile(backgroundVideo)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            opacity: 0.6,
          }}
        />
      )}

      {/* Top Letterbox */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: letterboxHeight,
          backgroundColor: '#000',
          zIndex: 10,
        }}
      />

      {/* Bottom Letterbox */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: letterboxHeight,
          backgroundColor: '#000',
          zIndex: 10,
        }}
      />

      {/* Text Content */}
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 5,
        }}
      >
        {/* Main Text with reveal effect */}
        <h1
          style={{
            fontSize: 96,
            fontWeight: 'bold',
            color: '#fff',
            textTransform: 'uppercase',
            letterSpacing: 20,
            clipPath: `inset(0 ${(1 - textProgress) * 100}% 0 0)`,
          }}
        >
          {mainText}
        </h1>

        {secondaryText && (
          <p
            style={{
              fontSize: 28,
              color: '#ccc',
              opacity: secondaryOpacity,
              marginTop: 30,
              letterSpacing: 5,
            }}
          >
            {secondaryText}
          </p>
        )}

        {releaseDate && (
          <p
            style={{
              fontSize: 24,
              color: '#fff',
              marginTop: 50,
              transform: `translateY(${dateTranslate}px)`,
              opacity: dateY,
            }}
          >
            {releaseDate}
          </p>
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```
</template>

<template name="TextOverlay" aspect="any">
<description>
Reusable animated text overlay component for any aspect ratio.
</description>

```tsx
// src/components/TextOverlay.tsx
import React from 'react';
import {useCurrentFrame, interpolate, spring, useVideoConfig} from 'remotion';

type AnimationType = 'fadeIn' | 'slideUp' | 'slideLeft' | 'typewriter' | 'scale';

interface TextOverlayProps {
  text: string;
  fontSize?: number;
  color?: string;
  animation?: AnimationType;
  delay?: number;
  duration?: number;
  style?: React.CSSProperties;
}

export const TextOverlay: React.FC<TextOverlayProps> = ({
  text,
  fontSize = 48,
  color = '#ffffff',
  animation = 'fadeIn',
  delay = 0,
  duration = 30,
  style = {},
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const adjustedFrame = Math.max(0, frame - delay);

  let animatedStyle: React.CSSProperties = {};

  switch (animation) {
    case 'fadeIn':
      animatedStyle = {
        opacity: interpolate(adjustedFrame, [0, duration], [0, 1], {
          extrapolateRight: 'clamp',
        }),
      };
      break;

    case 'slideUp':
      const slideY = spring({frame: adjustedFrame, fps, config: {damping: 200}});
      animatedStyle = {
        opacity: interpolate(adjustedFrame, [0, duration / 2], [0, 1], {
          extrapolateRight: 'clamp',
        }),
        transform: `translateY(${interpolate(slideY, [0, 1], [50, 0])}px)`,
      };
      break;

    case 'slideLeft':
      const slideX = spring({frame: adjustedFrame, fps, config: {damping: 200}});
      animatedStyle = {
        opacity: interpolate(adjustedFrame, [0, duration / 2], [0, 1], {
          extrapolateRight: 'clamp',
        }),
        transform: `translateX(${interpolate(slideX, [0, 1], [100, 0])}px)`,
      };
      break;

    case 'typewriter':
      const charsToShow = Math.floor(
        interpolate(adjustedFrame, [0, duration], [0, text.length], {
          extrapolateRight: 'clamp',
        })
      );
      return (
        <span style={{fontSize, color, fontFamily: 'monospace', ...style}}>
          {text.slice(0, charsToShow)}
          <span style={{opacity: frame % 30 < 15 ? 1 : 0}}>|</span>
        </span>
      );

    case 'scale':
      const scale = spring({frame: adjustedFrame, fps, config: {damping: 100, stiffness: 200}});
      animatedStyle = {
        transform: `scale(${scale})`,
        opacity: scale,
      };
      break;
  }

  return (
    <span style={{fontSize, color, ...animatedStyle, ...style}}>
      {text}
    </span>
  );
};
```
</template>

<color_schemes>
<scheme name="Dark Mode">
```tsx
const darkMode = {
  background: '#0a0a0a',
  surface: '#1a1a1a',
  primary: '#ffffff',
  secondary: '#888888',
  accent: '#ff6b35',
};
```
</scheme>

<scheme name="Vibrant">
```tsx
const vibrant = {
  background: '#6366f1',
  surface: '#818cf8',
  primary: '#ffffff',
  secondary: '#e0e7ff',
  accent: '#fbbf24',
};
```
</scheme>

<scheme name="Minimal">
```tsx
const minimal = {
  background: '#ffffff',
  surface: '#f5f5f5',
  primary: '#1a1a1a',
  secondary: '#666666',
  accent: '#2563eb',
};
```
</scheme>
</color_schemes>

<best_practices>
- **Hook early:** First 3 seconds determine if viewers stay
- **Text readability:** Minimum 32px for body text, 64px+ for headlines on mobile
- **Safe zones:** Keep critical content away from edges (10% margin)
- **Sound design:** Add subtle sound effects for engagement
- **Captions:** Always include for accessibility and sound-off viewing
- **Loop consideration:** Design smooth endings that loop well for Stories
</best_practices>
