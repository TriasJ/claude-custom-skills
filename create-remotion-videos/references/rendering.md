# Rendering Configuration

<overview>
Configure and execute video rendering in Remotion using CLI, Node.js API, or cloud (Lambda) options. Includes headless browser rendering for automation and CI/CD pipelines.
</overview>

<cli_rendering>
<basic_commands>
```bash
# Preview in browser
npm start
# Or: npx remotion studio

# Render single composition
npx remotion render src/index.ts CompositionId output.mp4

# Render with specific settings
npx remotion render src/index.ts CompositionId output.mp4 \
  --codec h264 \
  --crf 18 \
  --pixel-format yuv420p

# List all compositions
npx remotion compositions src/index.ts
```
</basic_commands>

<cli_options>
```bash
# Common rendering options
npx remotion render src/index.ts MyVideo output.mp4 \
  --codec h264              # Video codec (h264, h265, vp8, vp9, prores)
  --crf 18                  # Quality (0-51, lower = better, 18-23 recommended)
  --pixel-format yuv420p    # Pixel format for compatibility
  --fps 30                  # Override FPS
  --height 1080             # Override height
  --width 1920              # Override width
  --frames 0-150            # Render specific frame range
  --concurrency 50%         # CPU usage (number or percentage)
  --log verbose             # Logging level
  --props '{"title":"My Video"}'  # Pass input props as JSON

# Audio options
  --muted                   # Render without audio
  --enforce-audio-track     # Ensure audio track exists

# Output options
  --overwrite               # Overwrite existing file
  --image-format png        # For image sequences (png, jpeg)
  --quality 80              # JPEG quality (0-100)
```
</cli_options>

<codec_comparison>
| Codec | Use Case | Quality | File Size | Compatibility |
|-------|----------|---------|-----------|---------------|
| h264 | General distribution | Excellent | Medium | Universal |
| h265 | High efficiency | Excellent | Small | Modern devices |
| vp8 | Web (legacy) | Good | Medium | Browsers |
| vp9 | Web (modern) | Excellent | Small | Modern browsers |
| prores | Professional editing | Lossless | Very large | Final Cut, Premiere |
| gif | Simple animations | Limited | Variable | Universal |
</codec_comparison>

<crf_guide>
```
CRF (Constant Rate Factor) - Quality vs File Size

0-17:  Visually lossless (large files)
18-23: High quality (recommended range)
24-28: Medium quality (smaller files)
29-51: Low quality (very small files)

Recommended:
- YouTube/Vimeo upload: CRF 18-20
- Social media: CRF 20-23
- Archive/master: CRF 15-17
- Quick preview: CRF 28-30
```
</crf_guide>
</cli_rendering>

<nodejs_rendering>
<programmatic_render>
```typescript
// render.ts - Programmatic rendering with Node.js
import {bundle} from '@remotion/bundler';
import {
  renderMedia,
  selectComposition,
  getCompositions,
} from '@remotion/renderer';
import path from 'path';

const render = async () => {
  // Bundle the Remotion project
  console.log('Bundling project...');
  const bundleLocation = await bundle({
    entryPoint: path.resolve('./src/index.ts'),
    webpackOverride: (config) => config,
  });

  // Select composition
  const compositionId = 'MyVideo';
  const inputProps = {
    title: 'Generated Video',
    subtitle: 'Created with Remotion',
  };

  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: compositionId,
    inputProps,
  });

  console.log(`Rendering ${compositionId}...`);

  // Render video
  await renderMedia({
    composition,
    serveUrl: bundleLocation,
    codec: 'h264',
    outputLocation: `out/${compositionId}.mp4`,
    inputProps,
    // Optional callbacks
    onProgress: ({progress}) => {
      console.log(`Progress: ${(progress * 100).toFixed(1)}%`);
    },
    onStart: ({frameCount}) => {
      console.log(`Starting render of ${frameCount} frames`);
    },
  });

  console.log('Render complete!');
};

render().catch(console.error);
```
</programmatic_render>

<render_all_compositions>
```typescript
// render-all.ts - Render all compositions in project
import {bundle} from '@remotion/bundler';
import {getCompositions, renderMedia} from '@remotion/renderer';
import path from 'path';
import fs from 'fs';

const renderAll = async () => {
  // Ensure output directory exists
  const outDir = './out';
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, {recursive: true});
  }

  // Bundle project
  const bundleLocation = await bundle({
    entryPoint: path.resolve('./src/index.ts'),
  });

  // Get all compositions
  const compositions = await getCompositions(bundleLocation);
  console.log(`Found ${compositions.length} compositions`);

  // Render each composition
  for (const composition of compositions) {
    console.log(`Rendering ${composition.id}...`);

    await renderMedia({
      composition,
      serveUrl: bundleLocation,
      codec: 'h264',
      outputLocation: path.join(outDir, `${composition.id}.mp4`),
      onProgress: ({progress}) => {
        process.stdout.write(`\r${composition.id}: ${(progress * 100).toFixed(1)}%`);
      },
    });

    console.log(`\n${composition.id} complete!`);
  }

  console.log('All renders complete!');
};

renderAll().catch(console.error);
```
</render_all_compositions>

<batch_rendering>
```typescript
// batch-render.ts - Render multiple videos from dataset
import {bundle} from '@remotion/bundler';
import {selectComposition, renderMedia} from '@remotion/renderer';
import path from 'path';

interface VideoData {
  id: string;
  title: string;
  subtitle: string;
  outputName: string;
}

const dataset: VideoData[] = [
  {id: 'intro', title: 'Welcome', subtitle: 'Getting Started', outputName: 'welcome'},
  {id: 'chapter1', title: 'Chapter 1', subtitle: 'The Basics', outputName: 'chapter-1'},
  {id: 'chapter2', title: 'Chapter 2', subtitle: 'Advanced Topics', outputName: 'chapter-2'},
];

const batchRender = async () => {
  const bundleLocation = await bundle({
    entryPoint: path.resolve('./src/index.ts'),
  });

  const compositionId = 'DynamicVideo'; // Template composition

  for (const data of dataset) {
    console.log(`Rendering: ${data.title}`);

    const composition = await selectComposition({
      serveUrl: bundleLocation,
      id: compositionId,
      inputProps: data,
    });

    await renderMedia({
      composition,
      serveUrl: bundleLocation,
      codec: 'h264',
      outputLocation: `out/${data.outputName}.mp4`,
      inputProps: data,
    });

    console.log(`Complete: ${data.outputName}.mp4`);
  }
};

batchRender().catch(console.error);
```
</batch_rendering>
</nodejs_rendering>

<headless_rendering>
<docker_setup>
```dockerfile
# Dockerfile for headless Remotion rendering
FROM node:20-slim

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set Chrome path
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy project files
COPY . .

# Build and render
CMD ["npm", "run", "render"]
```
</docker_setup>

<github_actions>
```yaml
# .github/workflows/render-video.yml
name: Render Video

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      composition:
        description: 'Composition ID to render'
        required: true
        default: 'MainVideo'

jobs:
  render:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Chrome
        run: npx remotion browser ensure

      - name: Render video
        run: |
          npx remotion render src/index.ts ${{ github.event.inputs.composition || 'MainVideo' }} \
            out/video.mp4 \
            --codec h264 \
            --crf 20

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: rendered-video
          path: out/video.mp4
          retention-days: 7
```
</github_actions>

<ci_script>
```typescript
// scripts/ci-render.ts
// Render script for CI/CD pipelines
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition, ensureBrowser} from '@remotion/renderer';
import path from 'path';

const ciRender = async () => {
  // Ensure browser is available
  await ensureBrowser();

  const compositionId = process.env.COMPOSITION_ID || 'MainVideo';
  const outputPath = process.env.OUTPUT_PATH || 'out/video.mp4';

  console.log(`CI Render: ${compositionId}`);
  console.log(`Output: ${outputPath}`);

  // Bundle
  const bundleLocation = await bundle({
    entryPoint: path.resolve('./src/index.ts'),
    webpackOverride: (config) => config,
  });

  // Get composition
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: compositionId,
  });

  // Render with CI-optimized settings
  await renderMedia({
    composition,
    serveUrl: bundleLocation,
    codec: 'h264',
    outputLocation: outputPath,
    chromiumOptions: {
      disableWebSecurity: true,
      headless: true,
    },
    concurrency: 4, // Limit for CI resources
    onProgress: ({progress}) => {
      // Log every 10%
      const percent = Math.floor(progress * 10) * 10;
      if (progress * 100 >= percent && progress * 100 < percent + 10) {
        console.log(`Progress: ${percent}%`);
      }
    },
  });

  console.log('CI Render complete!');
};

ciRender().catch((err) => {
  console.error('Render failed:', err);
  process.exit(1);
});
```
</ci_script>
</headless_rendering>

<lambda_rendering>
<setup>
```bash
# Install Lambda package
npm install @remotion/lambda

# Configure AWS credentials
aws configure

# Deploy Remotion Lambda
npx remotion lambda sites create src/index.ts --site-name my-video

# Deploy Lambda function
npx remotion lambda functions deploy
```
</setup>

<render_on_lambda>
```typescript
// lambda-render.ts
import {
  renderMediaOnLambda,
  getRenderProgress,
  downloadMedia,
} from '@remotion/lambda';

const lambdaRender = async () => {
  const functionName = 'remotion-render-function';
  const serveUrl = 'https://your-remotion-site.s3.amazonaws.com/';
  const composition = 'MyVideo';

  // Start render
  const { renderId, bucketName } = await renderMediaOnLambda({
    region: 'us-east-1',
    functionName,
    serveUrl,
    composition,
    codec: 'h264',
    inputProps: {
      title: 'Lambda Rendered Video',
    },
  });

  console.log(`Render started: ${renderId}`);

  // Poll for progress
  let progress = 0;
  while (progress < 1) {
    const status = await getRenderProgress({
      renderId,
      bucketName,
      functionName,
      region: 'us-east-1',
    });

    if (status.fatalErrorEncountered) {
      throw new Error('Render failed: ' + status.errors?.join(', '));
    }

    progress = status.overallProgress;
    console.log(`Progress: ${(progress * 100).toFixed(1)}%`);

    if (status.done) {
      console.log('Render complete!');
      console.log('Output:', status.outputFile);
      break;
    }

    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
};

lambdaRender().catch(console.error);
```
</render_on_lambda>
</lambda_rendering>

<output_formats>
<video_output>
```bash
# MP4 (H.264) - Most compatible
npx remotion render src/index.ts MyVideo out.mp4 --codec h264

# WebM (VP9) - Smaller files, web-optimized
npx remotion render src/index.ts MyVideo out.webm --codec vp9

# ProRes - Professional editing
npx remotion render src/index.ts MyVideo out.mov --codec prores

# GIF - Simple animations (use sparingly)
npx remotion render src/index.ts MyVideo out.gif

# Image sequence
npx remotion render src/index.ts MyVideo frames/ --image-format png --sequence
```
</video_output>

<still_image>
```bash
# Render a single frame as image
npx remotion still src/index.ts MyVideo thumbnail.png --frame 30
```

```typescript
// Programmatic still rendering
import {renderStill, selectComposition} from '@remotion/renderer';

const renderThumbnail = async () => {
  const composition = await selectComposition({
    serveUrl: bundleLocation,
    id: 'MyVideo',
  });

  await renderStill({
    composition,
    serveUrl: bundleLocation,
    output: 'thumbnail.png',
    frame: 30, // Frame to capture
    imageFormat: 'png',
  });
};
```
</still_image>

<transparent_video>
```bash
# Render with alpha channel (WebM)
npx remotion render src/index.ts MyVideo out.webm \
  --codec vp9 \
  --pixel-format yuva420p

# Render with alpha channel (ProRes)
npx remotion render src/index.ts MyVideo out.mov \
  --codec prores \
  --prores-profile 4444
```

```tsx
// Ensure composition has transparent background
<Composition
  id="TransparentVideo"
  component={MyComponent}
  width={1920}
  height={1080}
  fps={30}
  durationInFrames={150}
  defaultProps={{transparent: true}}
/>
```
</transparent_video>
</output_formats>

<performance_optimization>
<concurrency>
```typescript
// Adjust based on available CPU cores
import os from 'os';

const cpuCount = os.cpus().length;
const concurrency = Math.max(1, cpuCount - 1); // Leave one core free

await renderMedia({
  composition,
  serveUrl: bundleLocation,
  outputLocation: 'out.mp4',
  concurrency, // Number of frames to render in parallel
});
```
</concurrency>

<memory_management>
```bash
# Limit memory usage
NODE_OPTIONS="--max-old-space-size=4096" npx remotion render ...

# For very long videos, use frame ranges
npx remotion render src/index.ts MyVideo part1.mp4 --frames 0-1000
npx remotion render src/index.ts MyVideo part2.mp4 --frames 1000-2000
# Then concatenate with ffmpeg
```
</memory_management>

<tips>
- Use `<OffthreadVideo>` instead of `<Video>` for better performance
- Reduce composition resolution for preview renders
- Use lower CRF (28-30) for quick test renders
- Enable GPU acceleration when available
- Pre-render heavy computations (3D, complex animations)
- Use `delayRender()` / `continueRender()` for async asset loading
</tips>
</performance_optimization>

<troubleshooting>
| Issue | Solution |
|-------|----------|
| "Browser not found" | Run `npx remotion browser ensure` |
| Out of memory | Increase `--max-old-space-size` or reduce concurrency |
| Render hangs | Check for infinite loops or missing `continueRender()` |
| Black frames | Ensure assets are loaded before render continues |
| Audio desync | Use consistent FPS; avoid variable frame rate sources |
| Slow render | Reduce resolution, use `OffthreadVideo`, lower concurrency |
</troubleshooting>
