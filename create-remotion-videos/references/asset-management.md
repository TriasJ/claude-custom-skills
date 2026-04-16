# Asset Management

<overview>
Organize, load, and manage assets (images, videos, audio, 3D models) for Remotion video projects. Includes integration with image-generation and fetch-media skills for dynamic content.
</overview>

<folder_structure>
```
my-video-project/
├── public/                    # Static assets (accessible via staticFile())
│   ├── audio/
│   │   ├── voiceover/        # Voice-over tracks
│   │   │   └── chapter-01.mp3
│   │   ├── music/            # Background music
│   │   │   └── ambient.mp3
│   │   └── sfx/              # Sound effects
│   │       └── whoosh.mp3
│   │
│   ├── images/
│   │   ├── generated/        # AI-generated images
│   │   │   └── hero-bg.png
│   │   ├── stock/            # Downloaded stock images
│   │   │   └── office.jpg
│   │   ├── logos/            # Brand assets
│   │   │   └── company-logo.svg
│   │   └── thumbnails/       # Video thumbnails
│   │       └── thumb.png
│   │
│   ├── videos/
│   │   ├── clips/            # Video clips
│   │   │   └── intro.mp4
│   │   └── backgrounds/      # Background videos
│   │       └── particles.mp4
│   │
│   ├── 3d/
│   │   ├── models/           # GLB/GLTF models
│   │   │   └── product.glb
│   │   ├── textures/         # 3D textures
│   │   │   └── wood.jpg
│   │   └── hdri/             # Environment maps
│   │       └── studio.hdr
│   │
│   ├── fonts/                # Custom fonts
│   │   └── CustomFont.woff2
│   │
│   └── user-assets/          # User-provided assets
│       └── (organized by user)
│
├── src/
│   ├── assets/               # TypeScript asset references
│   │   └── index.ts
│   ├── components/
│   ├── compositions/
│   └── Root.tsx
│
├── data/                     # JSON data files
│   └── video-data.json
│
└── remotion.config.ts
```
</folder_structure>

<loading_assets>
<static_files>
```tsx
import {staticFile, Img, Audio, Video, OffthreadVideo} from 'remotion';

// Images
<Img src={staticFile('images/logos/company-logo.svg')} />

// Audio
<Audio src={staticFile('audio/music/ambient.mp3')} volume={0.5} />

// Video (blocks main thread)
<Video src={staticFile('videos/clips/intro.mp4')} />

// Video (better performance)
<OffthreadVideo src={staticFile('videos/clips/intro.mp4')} />
```
</static_files>

<asset_registry>
```tsx
// src/assets/index.ts
// Centralized asset registry for type safety and easy management

import {staticFile} from 'remotion';

export const Assets = {
  // Audio
  audio: {
    voiceover: {
      chapter01: staticFile('audio/voiceover/chapter-01.mp3'),
      chapter02: staticFile('audio/voiceover/chapter-02.mp3'),
    },
    music: {
      ambient: staticFile('audio/music/ambient.mp3'),
      upbeat: staticFile('audio/music/upbeat.mp3'),
    },
    sfx: {
      whoosh: staticFile('audio/sfx/whoosh.mp3'),
      click: staticFile('audio/sfx/click.mp3'),
    },
  },

  // Images
  images: {
    logos: {
      main: staticFile('images/logos/company-logo.svg'),
      white: staticFile('images/logos/company-logo-white.svg'),
    },
    backgrounds: {
      dark: staticFile('images/generated/dark-bg.png'),
      gradient: staticFile('images/generated/gradient-bg.png'),
    },
  },

  // Videos
  videos: {
    intro: staticFile('videos/clips/intro.mp4'),
    particles: staticFile('videos/backgrounds/particles.mp4'),
  },

  // 3D
  models: {
    product: staticFile('3d/models/product.glb'),
    scene: staticFile('3d/models/scene.glb'),
  },

  // Fonts
  fonts: {
    heading: staticFile('fonts/Heading.woff2'),
    body: staticFile('fonts/Body.woff2'),
  },
} as const;

// Usage in components:
// import {Assets} from '../assets';
// <Img src={Assets.images.logos.main} />
```
</asset_registry>

<dynamic_assets>
```tsx
// Loading assets dynamically based on props or data
import React from 'react';
import {staticFile, Img} from 'remotion';

interface DynamicImageProps {
  imageName: string;
  folder?: string;
}

export const DynamicImage: React.FC<DynamicImageProps> = ({
  imageName,
  folder = 'images',
}) => {
  // Construct path dynamically
  const imagePath = staticFile(`${folder}/${imageName}`);

  return (
    <Img
      src={imagePath}
      style={{width: '100%', height: '100%', objectFit: 'cover'}}
    />
  );
};

// Usage:
// <DynamicImage imageName="hero.png" folder="images/generated" />
```
</dynamic_assets>
</loading_assets>

<user_provided_assets>
<setup_instructions>
When users provide their own asset folders:

1. **Copy assets to public folder:**
```bash
# User provides: /path/to/my-assets/
cp -r /path/to/my-assets/* ./public/user-assets/
```

2. **Reference in code:**
```tsx
import {staticFile, Img} from 'remotion';

// User's assets are now accessible
<Img src={staticFile('user-assets/my-image.png')} />
```

3. **Validate assets exist:**
```tsx
// src/utils/validateAssets.ts
import fs from 'fs';
import path from 'path';

export const validateUserAssets = (assetPaths: string[]): boolean => {
  const publicDir = path.join(process.cwd(), 'public');

  for (const assetPath of assetPaths) {
    const fullPath = path.join(publicDir, assetPath);
    if (!fs.existsSync(fullPath)) {
      console.error(`Asset not found: ${assetPath}`);
      return false;
    }
  }
  return true;
};
```
</setup_instructions>

<asset_manifest>
```tsx
// src/types/assets.ts
export interface UserAssetManifest {
  images?: string[];
  videos?: string[];
  audio?: string[];
  models?: string[];
}

// Example manifest file: public/user-assets/manifest.json
// {
//   "images": ["hero.png", "background.jpg"],
//   "videos": ["intro.mp4"],
//   "audio": ["voiceover.mp3"],
//   "models": ["product.glb"]
// }

// Load and validate manifest
import {staticFile} from 'remotion';

export const loadUserAssets = async (): Promise<UserAssetManifest> => {
  try {
    const response = await fetch(staticFile('user-assets/manifest.json'));
    return await response.json();
  } catch {
    console.warn('No user asset manifest found');
    return {};
  }
};
```
</asset_manifest>
</user_provided_assets>

<skill_integrations>
<image_generation_skill>
When invoking the image-generation skill, request images that match your video template:

```
Request to image-generation skill:

"Generate a hero background image with the following specifications:
- Dimensions: 1920x1080
- Style: Dark gradient with subtle particle effects
- Color scheme: Deep blue (#0f172a) to black (#000000)
- Format: PNG with transparency if needed
- Save to: public/images/generated/hero-bg.png

The image will be used as a video background, so ensure:
- No important content at edges (safe zone)
- Seamless or subtle patterns that won't distract
- Colors that provide good text contrast"
```

After generation, use in Remotion:
```tsx
import {staticFile, Img} from 'remotion';

<Img
  src={staticFile('images/generated/hero-bg.png')}
  style={{width: '100%', height: '100%', objectFit: 'cover'}}
/>
```
</image_generation_skill>

<fetch_media_skill>
When invoking the fetch-media skill, specify style requirements:

```
Request to fetch-media skill:

"Search for scientific diagram images with these requirements:
- Topic: Neural network architecture
- Background: Dark or transparent preferred
- Style: Clean, professional, suitable for educational video
- Minimum resolution: 1920x1080
- License: Open/Creative Commons for commercial use
- Download to: public/images/stock/

Search sources:
- Wikimedia Commons for scientific diagrams
- NIH BioArt for biological imagery
- NASA Images for space/tech visuals"
```

Usage after download:
```tsx
<Img
  src={staticFile('images/stock/neural-network.png')}
  style={{maxWidth: '80%', margin: '0 auto'}}
/>
```
</fetch_media_skill>

<matching_aesthetics>
When requesting images from either skill, ensure visual consistency:

```tsx
// Template color scheme
const theme = {
  background: '#0f172a',
  surface: '#1e293b',
  primary: '#3b82f6',
  text: '#f8fafc',
};

// Request images that match:
// "Generate/find images with:
// - Background color matching #0f172a or transparent
// - Accent colors in blue tones (#3b82f6 range)
// - High contrast for visibility on dark backgrounds"
```
</matching_aesthetics>
</skill_integrations>

<video_assets>
<formats>
| Format | Use Case | Notes |
|--------|----------|-------|
| MP4 (H.264) | General purpose | Best compatibility |
| WebM (VP9) | Web optimization | Smaller files, good quality |
| MOV (ProRes) | High quality source | Large files, use for processing |
| GIF | Simple animations | Limited colors, avoid for video |
</formats>

<usage>
```tsx
import {Video, OffthreadVideo, staticFile} from 'remotion';

// Standard video (use for short clips or when timing is critical)
<Video
  src={staticFile('videos/clip.mp4')}
  startFrom={0}     // Start from frame 0 of the video
  endAt={150}       // End at frame 150
  volume={0.5}
  muted={false}
/>

// Offthread video (better performance for longer videos)
<OffthreadVideo
  src={staticFile('videos/background.mp4')}
  style={{width: '100%', height: '100%', objectFit: 'cover'}}
/>

// Video with dynamic volume
<Video
  src={staticFile('videos/clip.mp4')}
  volume={(f) => {
    // Fade in first 30 frames, fade out last 30 frames
    if (f < 30) return f / 30;
    if (f > 120) return Math.max(0, 1 - (f - 120) / 30);
    return 1;
  }}
/>
```
</usage>
</video_assets>

<audio_assets>
<formats>
| Format | Use Case | Notes |
|--------|----------|-------|
| MP3 | Voice-over, music | Universal support |
| WAV | High quality source | Larger files |
| AAC | Compressed audio | Good quality, smaller |
| OGG | Web optimization | Not supported everywhere |
</formats>

<voice_over_workflow>
```tsx
// 1. Place voice-over file in public/audio/voiceover/
// 2. Reference with timing

import {Audio, Sequence, staticFile} from 'remotion';

export const VideoWithVoiceover: React.FC = () => {
  return (
    <>
      {/* Voice-over track */}
      <Audio
        src={staticFile('audio/voiceover/narration.mp3')}
        volume={1}
      />

      {/* Background music (lower volume) */}
      <Audio
        src={staticFile('audio/music/ambient.mp3')}
        volume={0.2}
      />

      {/* Synced visual content */}
      <Sequence from={0} durationInFrames={90}>
        <IntroSection />
      </Sequence>

      <Sequence from={90} durationInFrames={180}>
        <MainContent />
      </Sequence>
    </>
  );
};
```
</voice_over_workflow>

<audio_synchronization>
```tsx
// Timing configuration for voice-over sync
interface VoiceoverCue {
  text: string;        // Script text
  startTime: number;   // Seconds
  endTime: number;     // Seconds
  visualId: string;    // Component to show
}

const voiceoverCues: VoiceoverCue[] = [
  {text: "Welcome to our tutorial", startTime: 0, endTime: 3, visualId: "intro"},
  {text: "Let's explore the basics", startTime: 3, endTime: 6, visualId: "basics"},
  // ...
];

// Convert to frames (30fps)
const cuesToFrames = (cues: VoiceoverCue[], fps: number) =>
  cues.map(cue => ({
    ...cue,
    startFrame: Math.floor(cue.startTime * fps),
    endFrame: Math.floor(cue.endTime * fps),
  }));
```
</audio_synchronization>
</audio_assets>

<custom_fonts>
```tsx
// 1. Place font files in public/fonts/
// 2. Load with @font-face in component

import React from 'react';
import {staticFile} from 'remotion';

// Define font-face inline or in CSS
const fontStyles = `
  @font-face {
    font-family: 'CustomHeading';
    src: url('${staticFile('fonts/Heading.woff2')}') format('woff2');
    font-weight: bold;
    font-style: normal;
  }

  @font-face {
    font-family: 'CustomBody';
    src: url('${staticFile('fonts/Body.woff2')}') format('woff2');
    font-weight: normal;
    font-style: normal;
  }
`;

export const FontLoader: React.FC<{children: React.ReactNode}> = ({children}) => {
  return (
    <>
      <style>{fontStyles}</style>
      {children}
    </>
  );
};

// Usage
<FontLoader>
  <h1 style={{fontFamily: 'CustomHeading'}}>Title</h1>
  <p style={{fontFamily: 'CustomBody'}}>Body text</p>
</FontLoader>
```
</custom_fonts>

<preloading>
```tsx
// Preload critical assets to avoid loading delays during render
import {prefetch} from 'remotion';

// In your composition setup
const preloadAssets = async () => {
  await Promise.all([
    prefetch(staticFile('images/hero.png')),
    prefetch(staticFile('videos/intro.mp4')),
    prefetch(staticFile('audio/music.mp3')),
  ]);
};

// Or use delayRender for synchronous loading
import {delayRender, continueRender, staticFile} from 'remotion';

export const PreloadedComposition: React.FC = () => {
  const [handle] = React.useState(() => delayRender());

  React.useEffect(() => {
    // Load assets
    Promise.all([
      fetch(staticFile('data/video-data.json')).then(r => r.json()),
    ]).then(() => {
      continueRender(handle);
    });
  }, [handle]);

  return <MainContent />;
};
```
</preloading>

<optimization>
- **Images:** Use WebP for smaller files; optimize with tools like sharp
- **Videos:** Compress with ffmpeg; use appropriate bitrate for quality/size
- **Audio:** 128-192 kbps MP3 for voice; 256+ for music
- **3D Models:** Reduce polygon count; use Draco compression for GLB
- **Lazy loading:** Only load assets when needed in timeline
- **Caching:** Remotion caches assets between renders
</optimization>
