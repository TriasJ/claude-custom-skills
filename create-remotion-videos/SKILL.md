---
name: create-remotion-videos
description: Create programmatic videos using Remotion (React-based video framework) for social media, educational, and scientific content. Supports 3D (Three.js), data visualization (D3.js), generative art (P5.js), animations (GSAP), voice-over tracks, custom assets, and headless rendering. Use when creating videos programmatically, generating video content, or building animated video compositions.
---

<objective>
Create professional programmatic videos using Remotion with React. This skill handles three video categories (social media, educational, scientific), integrates with image-generation and fetch-media skills for dynamic content, supports 3D rendering with Three.js, and enables headless browser rendering for automation.
</objective>

<context>
Remotion is a React-based framework for creating videos programmatically. Videos are composed using React components, animated with interpolation and spring physics, and rendered frame-by-frame to produce MP4, WebM, or other video formats.

<library_ids>
Use Context7 MCP to fetch current documentation:
- Remotion: `/remotion-dev/remotion`
- Three.js: `/mrdoob/three.js`
- GSAP: `/websites/gsap_v3`
- D3.js: `/d3/d3`
- P5.js: `/websites/p5js_reference`
</library_ids>
</context>

<quick_start>
<step_1>
**Initialize Remotion project:**
```bash
npx create-video@latest my-video --template blank
cd my-video
npm install
```
</step_1>

<step_2>
**Create a composition in `src/Root.tsx`:**
```tsx
import {Composition} from 'remotion';
import {MyVideo} from './MyVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MyVideo"
      component={MyVideo}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
```
</step_2>

<step_3>
**Create animated component `src/MyVideo.tsx`:**
```tsx
import {useCurrentFrame, useVideoConfig, interpolate, spring, AbsoluteFill} from 'remotion';

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const opacity = interpolate(frame, [0, 30], [0, 1], {extrapolateRight: 'clamp'});
  const scale = spring({frame, fps, config: {damping: 200}});

  return (
    <AbsoluteFill style={{backgroundColor: '#000', justifyContent: 'center', alignItems: 'center'}}>
      <h1 style={{color: '#fff', opacity, transform: `scale(${scale})`}}>
        Hello Remotion!
      </h1>
    </AbsoluteFill>
  );
};
```
</step_3>

<step_4>
**Preview and render:**
```bash
npm start                    # Preview in browser
npx remotion render src/index.ts MyVideo out/video.mp4
```
</step_4>
</quick_start>

<video_categories>
<social_media>
**Dimensions:** 1080x1920 (9:16 vertical), 1080x1080 (1:1 square), 1920x1080 (16:9 horizontal)
**Duration:** 15-60 seconds typical
**FPS:** 30 or 60
**Use cases:** TikTok, Instagram Reels, YouTube Shorts, Stories

Templates: See [references/templates-social.md](references/templates-social.md)
</social_media>

<educational>
**Dimensions:** 1920x1080 (16:9), 2560x1440 (QHD), 3840x2160 (4K)
**Duration:** 2-15 minutes typical
**FPS:** 30
**Use cases:** Tutorials, explainers, course content, how-to videos

Templates: See [references/templates-educational.md](references/templates-educational.md)
</educational>

<scientific>
**Dimensions:** 1920x1080 (16:9), 3840x2160 (4K for high detail)
**Duration:** Variable (30 seconds to 30+ minutes)
**FPS:** 30 or 60 for smooth animations
**Use cases:** Research presentations, data visualization, simulation playback, conference talks

Templates: See [references/templates-scientific.md](references/templates-scientific.md)
</scientific>
</video_categories>

<workflow>
<phase name="Planning">
1. Determine video category and target platform
2. Select appropriate template or create custom composition
3. Gather assets (images, videos, audio, 3D models)
4. Create storyboard if complex (see [references/storyboard.md](references/storyboard.md))
5. Plan voice-over timing and script
</phase>

<phase name="Asset Preparation">
1. **Dynamic images:** Invoke `image-generation` skill for AI-generated visuals
2. **Stock media:** Invoke `fetch-media` skill for contextual images
3. **Match aesthetics:** Request images with matching background colors/styles
4. **3D models:** Place `.glb` files in `public/` folder
5. **Audio:** Place voice-over and music in `public/` folder
</phase>

<phase name="Development">
1. Create composition with correct dimensions/fps
2. Build component hierarchy with `<Sequence>` for timing
3. Add animations using `interpolate()` and `spring()`
4. Integrate media with `<Video>`, `<Audio>`, `<Img>`, `<OffthreadVideo>`
5. Add 3D elements with `@remotion/three` (see [references/3d-integration.md](references/3d-integration.md))
6. Preview with `npm start`
</phase>

<phase name="Voice-Over Integration">
```tsx
import {Audio, staticFile, Sequence} from 'remotion';

// Add voice-over track
<Sequence from={0}>
  <Audio src={staticFile('voiceover.mp3')} volume={1} />
</Sequence>

// Sync visuals to voice-over timestamps
<Sequence from={30} durationInFrames={90}>
  <AnimatedSection />
</Sequence>
```
</phase>

<phase name="Rendering">
See [references/rendering.md](references/rendering.md) for headless rendering options.

```bash
# Basic render
npx remotion render src/index.ts CompositionId out/video.mp4

# High quality with specific codec
npx remotion render src/index.ts CompositionId out/video.mp4 \
  --codec h264 --crf 18 --pixel-format yuv420p
```
</phase>
</workflow>

<core_apis>
<animations>
```tsx
import {interpolate, spring, Easing, interpolateColors, useCurrentFrame, useVideoConfig} from 'remotion';

const frame = useCurrentFrame();
const {fps, durationInFrames} = useVideoConfig();

// Linear interpolation with clamping
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});

// Spring physics animation
const scale = spring({frame, fps, config: {damping: 200, stiffness: 100, mass: 0.5}});

// Custom easing
const position = interpolate(frame, [0, 60], [0, 500], {
  easing: Easing.bezier(0.25, 0.1, 0.25, 1),
});

// Color interpolation
const color = interpolateColors(frame, [0, 60, 120], ['#ff0000', '#00ff00', '#0000ff']);
```
</animations>

<sequences>
```tsx
import {Sequence, AbsoluteFill} from 'remotion';

<AbsoluteFill>
  <Sequence from={0} durationInFrames={60}>
    <IntroSection />
  </Sequence>
  <Sequence from={60} durationInFrames={120}>
    <MainContent />
  </Sequence>
  <Sequence from={180}>
    <OutroSection />
  </Sequence>
</AbsoluteFill>
```
</sequences>

<media>
```tsx
import {Video, Audio, Img, OffthreadVideo, staticFile} from 'remotion';

// Static assets from public/ folder
<Img src={staticFile('logo.png')} />
<Audio src={staticFile('music.mp3')} volume={0.5} />
<Video src={staticFile('background.mp4')} startFrom={0} endAt={150} />

// Better performance for video
<OffthreadVideo src={staticFile('clip.mp4')} />

// Dynamic volume
<Audio src={staticFile('voiceover.mp3')} volume={(f) => interpolate(f, [0, 30], [0, 1])} />
```
</media>
</core_apis>

<skill_integrations>
<image_generation>
Before creating video frames that need custom imagery:
```
Invoke the image-generation skill to create:
- Background images matching template style (e.g., "dark gradient background, 1920x1080")
- Custom illustrations for concepts
- Thumbnails and preview images
- Logo variations

Important: Request images with backgrounds that match your template's color scheme for seamless integration.
```
</image_generation>

<fetch_media>
For stock imagery and scientific illustrations:
```
Invoke the fetch-media skill to search:
- Wikimedia Commons for scientific diagrams
- NIH BioArt for medical/biological imagery
- NASA Images for space/astronomy content
- Unsplash/Pixabay for general stock photos

Tip: Search with style keywords (e.g., "neuron diagram black background") to match templates.
```
</fetch_media>
</skill_integrations>

<asset_management>
<folder_structure>
```
my-video/
├── public/
│   ├── audio/
│   │   ├── voiceover.mp3
│   │   └── background-music.mp3
│   ├── images/
│   │   ├── generated/      # AI-generated images
│   │   └── stock/          # Downloaded stock images
│   ├── videos/
│   │   └── clips/
│   └── 3d/
│       ├── models/         # .glb files
│       └── textures/
├── src/
│   ├── components/
│   ├── compositions/
│   └── Root.tsx
└── remotion.config.ts
```
</folder_structure>

<user_assets>
When user provides asset folders:
```tsx
// Reference user-provided assets
import {staticFile} from 'remotion';

// User places files in public/user-assets/
const userImage = staticFile('user-assets/my-image.png');
const user3DModel = staticFile('user-assets/model.glb');
```
</user_assets>

See [references/asset-management.md](references/asset-management.md) for detailed asset handling.
</asset_management>

<advanced_features>
**3D Integration (Three.js):** See [references/3d-integration.md](references/3d-integration.md)
- ThreeCanvas setup with Remotion
- Loading .glb models
- Custom shaders (vertex/fragment)
- Camera animations
- Lighting and materials

**Animation Libraries:** See [references/animation-libraries.md](references/animation-libraries.md)
- D3.js for data visualization
- P5.js for generative art
- GSAP for timeline-based animations

**Storyboarding:** See [references/storyboard.md](references/storyboard.md)
- Scene planning format
- Timing calculations
- Voice-over synchronization

**Rendering Options:** See [references/rendering.md](references/rendering.md)
- Headless browser rendering
- CLI options and codecs
- Node.js programmatic rendering
- Lambda cloud rendering
</advanced_features>

<templates_overview>
<social_templates>
1. **VerticalIntro** - Animated text reveal (9:16)
2. **SquarePromo** - Product showcase (1:1)
3. **HorizontalTeaser** - Cinematic preview (16:9)
</social_templates>

<educational_templates>
1. **ChapterSlide** - Title cards with transitions
2. **CodeWalkthrough** - Syntax-highlighted code animation
3. **DiagramExplainer** - Animated diagrams with callouts
</educational_templates>

<scientific_templates>
1. **DataVisualization** - D3-powered charts and graphs
2. **MolecularViewer** - 3D molecule rendering
3. **TimelinePresentation** - Research timeline with citations
</scientific_templates>

Full template code: See [templates/](templates/) folder
</templates_overview>

<success_criteria>
A successful Remotion video implementation has:
- Correct dimensions and FPS for target platform
- Smooth animations (60fps playback, no jank)
- Properly synchronized audio/voice-over
- Assets loading without errors
- Clean render output in target format
- Voice-over placeholder tracks ready for final audio
</success_criteria>

<anti_patterns>
- Using `<Video>` for many concurrent videos (use `<OffthreadVideo>` instead)
- Hardcoding frame numbers instead of calculating from fps/duration
- Not clamping interpolation values (causes overshooting)
- Placing assets outside `public/` folder
- Using blocking operations during render (fetch data beforehand)
- Ignoring aspect ratios when mixing content types
</anti_patterns>

<reference_guides>
- [references/templates-social.md](references/templates-social.md) - Social media templates
- [references/templates-educational.md](references/templates-educational.md) - Educational templates
- [references/templates-scientific.md](references/templates-scientific.md) - Scientific templates
- [references/3d-integration.md](references/3d-integration.md) - Three.js and 3D content
- [references/animation-libraries.md](references/animation-libraries.md) - D3, P5, GSAP integration
- [references/asset-management.md](references/asset-management.md) - Asset handling and organization
- [references/rendering.md](references/rendering.md) - Render configurations
- [references/storyboard.md](references/storyboard.md) - Storyboard workflow
</reference_guides>
