# Storyboard Workflow

<overview>
Create structured storyboards to plan video content, synchronize visuals with voice-over, and ensure consistency across complex video projects. Essential for educational and scientific videos with multiple scenes.
</overview>

<when_to_storyboard>
Use storyboards for:
- Videos longer than 60 seconds
- Educational content with multiple topics
- Scientific presentations with data sequences
- Videos with voice-over narration
- Complex animations requiring timing coordination
- Team collaboration on video projects
</when_to_storyboard>

<storyboard_format>
<json_structure>
```typescript
// src/types/storyboard.ts
export interface StoryboardScene {
  id: string;
  title: string;
  description: string;
  duration: number;        // In seconds
  startTime: number;       // Cumulative start time in seconds
  visualType: 'intro' | 'title' | 'content' | 'diagram' | 'code' | 'data' | 'transition' | 'outro';
  voiceOver?: {
    script: string;
    audioFile?: string;    // Path to voice-over file
  };
  visuals: {
    component: string;     // React component name
    props: Record<string, any>;
    assets?: string[];     // Required asset paths
  };
  transitions?: {
    in?: 'fade' | 'slide' | 'zoom' | 'none';
    out?: 'fade' | 'slide' | 'zoom' | 'none';
    duration?: number;     // Transition duration in frames
  };
  notes?: string;          // Production notes
}

export interface Storyboard {
  projectName: string;
  version: string;
  totalDuration: number;   // Total video duration in seconds
  fps: number;
  resolution: {
    width: number;
    height: number;
  };
  category: 'social' | 'educational' | 'scientific';
  scenes: StoryboardScene[];
  metadata: {
    author: string;
    createdAt: string;
    updatedAt: string;
    voiceOverReady: boolean;
    assetsComplete: boolean;
  };
}
```
</json_structure>

<example_storyboard>
```json
{
  "projectName": "Introduction to Machine Learning",
  "version": "1.0",
  "totalDuration": 180,
  "fps": 30,
  "resolution": {"width": 1920, "height": 1080},
  "category": "educational",
  "scenes": [
    {
      "id": "scene-001",
      "title": "Opening Hook",
      "description": "Attention-grabbing intro with animated neural network",
      "duration": 5,
      "startTime": 0,
      "visualType": "intro",
      "voiceOver": {
        "script": "What if computers could learn just like humans do?",
        "audioFile": "audio/voiceover/scene-001.mp3"
      },
      "visuals": {
        "component": "AnimatedNeuralNetwork",
        "props": {
          "theme": "dark",
          "animationSpeed": 1.5
        },
        "assets": ["images/generated/neural-bg.png"]
      },
      "transitions": {
        "in": "fade",
        "out": "fade",
        "duration": 15
      },
      "notes": "Use fetch-media skill to get neural network diagram"
    },
    {
      "id": "scene-002",
      "title": "Title Card",
      "description": "Video title with branding",
      "duration": 3,
      "startTime": 5,
      "visualType": "title",
      "voiceOver": {
        "script": "Welcome to Introduction to Machine Learning."
      },
      "visuals": {
        "component": "ChapterSlide",
        "props": {
          "chapterNumber": 0,
          "title": "Introduction to Machine Learning",
          "subtitle": "Understanding the Basics",
          "theme": "dark"
        }
      },
      "transitions": {
        "in": "slide",
        "out": "fade"
      }
    },
    {
      "id": "scene-003",
      "title": "What is ML?",
      "description": "Definition and key concepts",
      "duration": 20,
      "startTime": 8,
      "visualType": "content",
      "voiceOver": {
        "script": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. Unlike traditional programming where we write specific rules, machine learning algorithms discover patterns on their own."
      },
      "visuals": {
        "component": "BulletPointReveal",
        "props": {
          "title": "What is Machine Learning?",
          "points": [
            {"text": "Subset of Artificial Intelligence", "icon": "brain"},
            {"text": "Learns from data patterns", "icon": "chart"},
            {"text": "Improves with experience", "icon": "arrow-up"},
            {"text": "Makes predictions & decisions", "icon": "target"}
          ],
          "theme": "dark"
        }
      }
    },
    {
      "id": "scene-004",
      "title": "Types of ML",
      "description": "Diagram showing supervised, unsupervised, reinforcement",
      "duration": 25,
      "startTime": 28,
      "visualType": "diagram",
      "voiceOver": {
        "script": "There are three main types of machine learning. Supervised learning uses labeled data to train models. Unsupervised learning finds hidden patterns in unlabeled data. And reinforcement learning teaches agents through trial and error with rewards."
      },
      "visuals": {
        "component": "DiagramExplainer",
        "props": {
          "title": "Types of Machine Learning",
          "nodes": [
            {"id": "ml", "label": "Machine Learning", "x": 50, "y": 20, "color": "#3b82f6"},
            {"id": "supervised", "label": "Supervised", "x": 20, "y": 60, "color": "#22c55e"},
            {"id": "unsupervised", "label": "Unsupervised", "x": 50, "y": 60, "color": "#f59e0b"},
            {"id": "reinforcement", "label": "Reinforcement", "x": 80, "y": 60, "color": "#ef4444"}
          ],
          "connections": [
            {"from": "ml", "to": "supervised"},
            {"from": "ml", "to": "unsupervised"},
            {"from": "ml", "to": "reinforcement"}
          ],
          "highlightSequence": ["ml", "supervised", "unsupervised", "reinforcement"]
        }
      },
      "notes": "Animate nodes in sequence with voice-over timing"
    }
  ],
  "metadata": {
    "author": "Video Team",
    "createdAt": "2024-01-15",
    "updatedAt": "2024-01-16",
    "voiceOverReady": false,
    "assetsComplete": false
  }
}
```
</example_storyboard>
</storyboard_format>

<storyboard_to_remotion>
<converter_component>
```tsx
// src/utils/StoryboardRenderer.tsx
import React from 'react';
import {Sequence, useVideoConfig, AbsoluteFill} from 'remotion';
import type {Storyboard, StoryboardScene} from '../types/storyboard';

// Component registry - map component names to actual components
import {ChapterSlide} from '../compositions/ChapterSlide';
import {BulletPointReveal} from '../compositions/BulletPointReveal';
import {DiagramExplainer} from '../compositions/DiagramExplainer';
import {CodeWalkthrough} from '../compositions/CodeWalkthrough';
import {DataVisualization} from '../compositions/DataVisualization';

const componentRegistry: Record<string, React.FC<any>> = {
  ChapterSlide,
  BulletPointReveal,
  DiagramExplainer,
  CodeWalkthrough,
  DataVisualization,
  // Add more components as needed
};

interface StoryboardRendererProps {
  storyboard: Storyboard;
}

export const StoryboardRenderer: React.FC<StoryboardRendererProps> = ({
  storyboard,
}) => {
  const {fps} = useVideoConfig();

  return (
    <AbsoluteFill>
      {storyboard.scenes.map((scene) => {
        const Component = componentRegistry[scene.visuals.component];

        if (!Component) {
          console.warn(`Component not found: ${scene.visuals.component}`);
          return null;
        }

        const startFrame = Math.floor(scene.startTime * fps);
        const durationFrames = Math.floor(scene.duration * fps);

        return (
          <Sequence
            key={scene.id}
            from={startFrame}
            durationInFrames={durationFrames}
            name={scene.title}
          >
            <SceneWrapper scene={scene}>
              <Component {...scene.visuals.props} />
            </SceneWrapper>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

// Wrapper for transitions
const SceneWrapper: React.FC<{
  scene: StoryboardScene;
  children: React.ReactNode;
}> = ({scene, children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const durationFrames = scene.duration * fps;

  let opacity = 1;
  let transform = 'none';

  const transitionDuration = scene.transitions?.duration || 15;

  // Entrance transition
  if (scene.transitions?.in === 'fade') {
    opacity = interpolate(frame, [0, transitionDuration], [0, 1], {
      extrapolateRight: 'clamp',
    });
  } else if (scene.transitions?.in === 'slide') {
    const progress = spring({frame, fps, config: {damping: 200}});
    transform = `translateX(${interpolate(progress, [0, 1], [100, 0])}px)`;
    opacity = progress;
  }

  // Exit transition
  if (scene.transitions?.out === 'fade') {
    const exitStart = durationFrames - transitionDuration;
    if (frame > exitStart) {
      opacity *= interpolate(frame, [exitStart, durationFrames], [1, 0], {
        extrapolateLeft: 'clamp',
      });
    }
  }

  return (
    <AbsoluteFill style={{opacity, transform}}>
      {children}
    </AbsoluteFill>
  );
};

// Helper imports
import {useCurrentFrame, interpolate, spring} from 'remotion';
```
</converter_component>

<composition_setup>
```tsx
// src/Root.tsx
import React from 'react';
import {Composition, staticFile} from 'remotion';
import {StoryboardRenderer} from './utils/StoryboardRenderer';
import storyboardData from '../data/storyboard.json';
import type {Storyboard} from './types/storyboard';

const storyboard = storyboardData as Storyboard;

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="StoryboardVideo"
      component={() => <StoryboardRenderer storyboard={storyboard} />}
      durationInFrames={storyboard.totalDuration * storyboard.fps}
      fps={storyboard.fps}
      width={storyboard.resolution.width}
      height={storyboard.resolution.height}
    />
  );
};
```
</composition_setup>
</storyboard_to_remotion>

<voice_over_timing>
<timing_calculation>
```typescript
// src/utils/voiceOverTiming.ts

// Average reading speeds (words per minute)
const READING_SPEEDS = {
  slow: 120,      // Deliberate, educational
  normal: 150,    // Conversational
  fast: 180,      // Energetic, social media
};

export const calculateVoiceOverDuration = (
  script: string,
  speed: 'slow' | 'normal' | 'fast' = 'normal'
): number => {
  const wordCount = script.split(/\s+/).length;
  const wpm = READING_SPEEDS[speed];
  return (wordCount / wpm) * 60; // Return seconds
};

// Calculate all scene timings from scripts
export const calculateSceneTimings = (
  scenes: StoryboardScene[],
  speed: 'slow' | 'normal' | 'fast' = 'normal'
): StoryboardScene[] => {
  let currentTime = 0;

  return scenes.map((scene) => {
    const calculatedDuration = scene.voiceOver?.script
      ? calculateVoiceOverDuration(scene.voiceOver.script, speed)
      : scene.duration;

    // Add buffer for visual comprehension
    const duration = Math.max(calculatedDuration + 1, scene.duration);

    const updatedScene = {
      ...scene,
      duration,
      startTime: currentTime,
    };

    currentTime += duration;
    return updatedScene;
  });
};

// Example usage:
// const timedScenes = calculateSceneTimings(storyboard.scenes, 'slow');
```
</timing_calculation>

<sync_markers>
```typescript
// src/utils/syncMarkers.ts

interface SyncMarker {
  time: number;           // Time in seconds
  frame: number;          // Frame number
  label: string;
  sceneId: string;
  type: 'scene_start' | 'scene_end' | 'emphasis' | 'visual_cue';
}

export const generateSyncMarkers = (
  scenes: StoryboardScene[],
  fps: number
): SyncMarker[] => {
  const markers: SyncMarker[] = [];

  scenes.forEach((scene) => {
    // Scene start marker
    markers.push({
      time: scene.startTime,
      frame: Math.floor(scene.startTime * fps),
      label: `Start: ${scene.title}`,
      sceneId: scene.id,
      type: 'scene_start',
    });

    // Scene end marker
    markers.push({
      time: scene.startTime + scene.duration,
      frame: Math.floor((scene.startTime + scene.duration) * fps),
      label: `End: ${scene.title}`,
      sceneId: scene.id,
      type: 'scene_end',
    });
  });

  return markers.sort((a, b) => a.time - b.time);
};

// Export for voice-over recording reference
export const exportTimingSheet = (markers: SyncMarker[]): string => {
  let output = 'TIMING SHEET\n============\n\n';

  markers.forEach((marker) => {
    const minutes = Math.floor(marker.time / 60);
    const seconds = (marker.time % 60).toFixed(1);
    output += `[${String(minutes).padStart(2, '0')}:${String(seconds).padStart(4, '0')}] (Frame ${marker.frame}) - ${marker.label}\n`;
  });

  return output;
};
```
</sync_markers>
</voice_over_timing>

<asset_checklist>
```typescript
// src/utils/assetChecklist.ts
import fs from 'fs';
import path from 'path';
import type {Storyboard} from '../types/storyboard';

interface AssetCheck {
  path: string;
  exists: boolean;
  sceneId: string;
  type: 'image' | 'video' | 'audio' | 'model';
}

export const validateStoryboardAssets = (
  storyboard: Storyboard,
  publicDir: string = './public'
): AssetCheck[] => {
  const checks: AssetCheck[] = [];

  storyboard.scenes.forEach((scene) => {
    // Check visual assets
    scene.visuals.assets?.forEach((assetPath) => {
      const fullPath = path.join(publicDir, assetPath);
      checks.push({
        path: assetPath,
        exists: fs.existsSync(fullPath),
        sceneId: scene.id,
        type: getAssetType(assetPath),
      });
    });

    // Check voice-over audio
    if (scene.voiceOver?.audioFile) {
      const fullPath = path.join(publicDir, scene.voiceOver.audioFile);
      checks.push({
        path: scene.voiceOver.audioFile,
        exists: fs.existsSync(fullPath),
        sceneId: scene.id,
        type: 'audio',
      });
    }
  });

  return checks;
};

const getAssetType = (path: string): 'image' | 'video' | 'audio' | 'model' => {
  const ext = path.split('.').pop()?.toLowerCase();
  if (['png', 'jpg', 'jpeg', 'svg', 'webp', 'gif'].includes(ext || '')) return 'image';
  if (['mp4', 'webm', 'mov'].includes(ext || '')) return 'video';
  if (['mp3', 'wav', 'ogg', 'aac'].includes(ext || '')) return 'audio';
  if (['glb', 'gltf'].includes(ext || '')) return 'model';
  return 'image';
};

// Generate missing assets report
export const generateAssetReport = (checks: AssetCheck[]): string => {
  const missing = checks.filter((c) => !c.exists);

  if (missing.length === 0) {
    return '✅ All assets present!';
  }

  let report = '⚠️ MISSING ASSETS\n==================\n\n';

  missing.forEach((asset) => {
    report += `Scene ${asset.sceneId}:\n`;
    report += `  - [${asset.type.toUpperCase()}] ${asset.path}\n`;
  });

  report += `\nTotal missing: ${missing.length}/${checks.length}\n`;

  return report;
};
```
</asset_checklist>

<storyboard_template>
```typescript
// src/utils/createStoryboard.ts

import type {Storyboard, StoryboardScene} from '../types/storyboard';

export const createEmptyStoryboard = (
  projectName: string,
  category: 'social' | 'educational' | 'scientific',
  fps: number = 30,
  resolution: {width: number; height: number} = {width: 1920, height: 1080}
): Storyboard => {
  return {
    projectName,
    version: '1.0',
    totalDuration: 0,
    fps,
    resolution,
    category,
    scenes: [],
    metadata: {
      author: '',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      voiceOverReady: false,
      assetsComplete: false,
    },
  };
};

export const addScene = (
  storyboard: Storyboard,
  scene: Omit<StoryboardScene, 'startTime'>
): Storyboard => {
  // Calculate start time from existing scenes
  const lastScene = storyboard.scenes[storyboard.scenes.length - 1];
  const startTime = lastScene
    ? lastScene.startTime + lastScene.duration
    : 0;

  const newScene: StoryboardScene = {
    ...scene,
    startTime,
  };

  const totalDuration = startTime + scene.duration;

  return {
    ...storyboard,
    scenes: [...storyboard.scenes, newScene],
    totalDuration,
    metadata: {
      ...storyboard.metadata,
      updatedAt: new Date().toISOString(),
    },
  };
};

// Quick scene creators
export const createIntroScene = (
  title: string,
  duration: number = 5
): Omit<StoryboardScene, 'startTime'> => ({
  id: `intro-${Date.now()}`,
  title: 'Introduction',
  description: `Intro: ${title}`,
  duration,
  visualType: 'intro',
  visuals: {
    component: 'VerticalIntro',
    props: {title},
  },
  transitions: {in: 'fade', out: 'fade'},
});

export const createChapterScene = (
  chapterNumber: number,
  title: string,
  subtitle?: string,
  duration: number = 3
): Omit<StoryboardScene, 'startTime'> => ({
  id: `chapter-${chapterNumber}-${Date.now()}`,
  title: `Chapter ${chapterNumber}: ${title}`,
  description: subtitle || '',
  duration,
  visualType: 'title',
  visuals: {
    component: 'ChapterSlide',
    props: {chapterNumber, title, subtitle},
  },
  transitions: {in: 'slide', out: 'fade'},
});
```
</storyboard_template>

<workflow_integration>
<skill_invocation>
When creating a storyboard, invoke supporting skills:

```
1. For each scene requiring custom imagery:
   → Invoke image-generation skill with scene description
   → Specify dimensions matching video resolution
   → Request style matching video category (dark for scientific, etc.)

2. For scenes requiring stock media:
   → Invoke fetch-media skill with scene topic
   → Specify style requirements (background color, mood)
   → Download to public/images/stock/

3. After storyboard is complete:
   → Generate timing sheet for voice-over recording
   → Run asset validation to identify missing files
   → Create Remotion composition from storyboard
```
</skill_invocation>

<production_checklist>
```markdown
## Storyboard Production Checklist

### Pre-Production
- [ ] Define video category and target audience
- [ ] Create initial storyboard outline
- [ ] Calculate scene durations from script
- [ ] Generate timing sheet

### Asset Creation
- [ ] Invoke image-generation for custom visuals
- [ ] Invoke fetch-media for stock imagery
- [ ] Prepare 3D models if needed
- [ ] Record voice-over using timing sheet

### Development
- [ ] Create Remotion project
- [ ] Implement component registry
- [ ] Import storyboard JSON
- [ ] Validate all assets exist
- [ ] Preview each scene

### Review
- [ ] Check voice-over sync
- [ ] Verify transitions are smooth
- [ ] Test on target platforms
- [ ] Export for distribution
```
</production_checklist>
</workflow_integration>

<best_practices>
- **Script first:** Write all voice-over scripts before calculating timings
- **Buffer time:** Add 1-2 seconds buffer per scene for visual processing
- **Consistent pacing:** Educational videos: ~120 WPM; social: ~150 WPM
- **Transition awareness:** Account for transition duration in scene timing
- **Asset naming:** Use scene IDs in asset filenames for easy tracking
- **Version control:** Keep storyboard JSON in version control
- **Iterative review:** Preview after each major section, not just at the end
</best_practices>
