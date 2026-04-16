# 3D Integration with Three.js

<overview>
Integrate Three.js 3D graphics into Remotion videos using `@remotion/three`. Supports custom GLB models, shaders, camera animations, and complex 3D scenes.
</overview>

<setup>
```bash
# Install required packages
npm install @remotion/three three @react-three/fiber @react-three/drei
npm install -D @types/three
```

<webpack_config>
```ts
// remotion.config.ts
import {Config} from '@remotion/cli/config';

Config.overrideWebpackConfig((config) => {
  return {
    ...config,
    module: {
      ...config.module,
      rules: [
        ...(config.module?.rules || []),
        {
          test: /\.(glb|gltf)$/,
          type: 'asset/resource',
        },
      ],
    },
  };
});
```
</webpack_config>
</setup>

<basic_scene>
```tsx
// src/components/Basic3DScene.tsx
import React, {useEffect, useRef} from 'react';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import * as THREE from 'three';

const Scene: React.FC = () => {
  const frame = useCurrentFrame();
  const {camera} = useThree();
  const meshRef = useRef<THREE.Mesh>(null);

  // Setup camera
  useEffect(() => {
    camera.position.set(0, 2, 5);
    camera.lookAt(0, 0, 0);
  }, [camera]);

  // Animate rotation based on frame
  const rotation = (frame / 30) * Math.PI * 0.5;

  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.4} />
      <directionalLight position={[10, 10, 5]} intensity={0.8} />
      <pointLight position={[-10, -10, -5]} intensity={0.3} color="#ff6b6b" />

      {/* Animated Mesh */}
      <mesh ref={meshRef} rotation={[0, rotation, 0]}>
        <boxGeometry args={[2, 2, 2]} />
        <meshStandardMaterial color="#4287f5" />
      </mesh>

      {/* Ground Plane */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.5, 0]}>
        <planeGeometry args={[20, 20]} />
        <meshStandardMaterial color="#1a1a2e" />
      </mesh>
    </>
  );
};

export const Basic3DScene: React.FC = () => {
  const {width, height} = useVideoConfig();

  return (
    <ThreeCanvas
      width={width}
      height={height}
      camera={{fov: 50}}
    >
      <Scene />
    </ThreeCanvas>
  );
};
```
</basic_scene>

<loading_glb_models>
```tsx
// src/components/GLBModel.tsx
import React, {useEffect, useRef, Suspense} from 'react';
import {ThreeCanvas} from '@remotion/three';
import {useLoader, useThree} from '@react-three/fiber';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader';
import {useCurrentFrame, useVideoConfig, staticFile, interpolate, spring} from 'remotion';
import * as THREE from 'three';

interface ModelProps {
  modelPath: string;
  scale?: number;
  position?: [number, number, number];
}

const Model: React.FC<ModelProps> = ({
  modelPath,
  scale = 1,
  position = [0, 0, 0],
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const groupRef = useRef<THREE.Group>(null);

  // Load GLB/GLTF model
  const gltf = useLoader(GLTFLoader, staticFile(modelPath));

  // Animation
  const entranceScale = spring({
    frame,
    fps,
    config: {damping: 100},
  });
  const rotation = (frame / 60) * Math.PI * 2;

  return (
    <group ref={groupRef} position={position}>
      <primitive
        object={gltf.scene.clone()}
        scale={scale * entranceScale}
        rotation={[0, rotation, 0]}
      />
    </group>
  );
};

const Scene: React.FC<{modelPath: string}> = ({modelPath}) => {
  const {camera} = useThree();

  useEffect(() => {
    camera.position.set(0, 2, 8);
    camera.lookAt(0, 0, 0);
  }, [camera]);

  return (
    <>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 10, 5]} intensity={1} castShadow />
      <Suspense fallback={null}>
        <Model modelPath={modelPath} scale={1} />
      </Suspense>
    </>
  );
};

export const GLBViewer: React.FC<{modelPath: string}> = ({modelPath}) => {
  const {width, height} = useVideoConfig();

  return (
    <ThreeCanvas width={width} height={height}>
      <Scene modelPath={modelPath} />
    </ThreeCanvas>
  );
};

// Usage:
// Place model in public/3d/model.glb
// <GLBViewer modelPath="3d/model.glb" />
```
</loading_glb_models>

<custom_shaders>
```tsx
// src/components/ShaderMaterial.tsx
import React, {useRef, useMemo} from 'react';
import {ThreeCanvas} from '@remotion/three';
import {useFrame, useThree, extend} from '@react-three/fiber';
import {shaderMaterial} from '@react-three/drei';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import * as THREE from 'three';

// Custom shader material
const WaveShaderMaterial = shaderMaterial(
  // Uniforms
  {
    uTime: 0,
    uColor: new THREE.Color('#4287f5'),
    uAmplitude: 0.3,
    uFrequency: 2.0,
  },
  // Vertex Shader
  `
    uniform float uTime;
    uniform float uAmplitude;
    uniform float uFrequency;

    varying vec2 vUv;
    varying float vElevation;

    void main() {
      vUv = uv;

      // Wave displacement
      float elevation = sin(position.x * uFrequency + uTime) *
                       sin(position.y * uFrequency + uTime) *
                       uAmplitude;

      vElevation = elevation;

      vec3 newPosition = position;
      newPosition.z += elevation;

      gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
    }
  `,
  // Fragment Shader
  `
    uniform vec3 uColor;

    varying vec2 vUv;
    varying float vElevation;

    void main() {
      float intensity = vElevation + 0.5;
      vec3 color = mix(uColor * 0.5, uColor * 1.5, intensity);

      gl_FragColor = vec4(color, 1.0);
    }
  `
);

// Extend Three.js with custom material
extend({WaveShaderMaterial});

// TypeScript declaration
declare module '@react-three/fiber' {
  interface ThreeElements {
    waveShaderMaterial: any;
  }
}

const ShaderPlane: React.FC = () => {
  const frame = useCurrentFrame();
  const materialRef = useRef<any>(null);

  // Update time uniform based on frame
  const time = frame / 30;

  return (
    <mesh rotation={[-Math.PI / 4, 0, 0]}>
      <planeGeometry args={[10, 10, 64, 64]} />
      <waveShaderMaterial
        ref={materialRef}
        uTime={time}
        uColor={new THREE.Color('#00d9ff')}
        uAmplitude={0.4}
        uFrequency={3.0}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
};

const Scene: React.FC = () => {
  const {camera} = useThree();

  React.useEffect(() => {
    camera.position.set(0, 5, 10);
    camera.lookAt(0, 0, 0);
  }, [camera]);

  return (
    <>
      <ambientLight intensity={0.5} />
      <ShaderPlane />
    </>
  );
};

export const ShaderDemo: React.FC = () => {
  const {width, height} = useVideoConfig();

  return (
    <ThreeCanvas width={width} height={height}>
      <Scene />
    </ThreeCanvas>
  );
};
```
</custom_shaders>

<camera_animations>
```tsx
// src/components/AnimatedCamera.tsx
import React, {useEffect} from 'react';
import {useThree} from '@react-three/fiber';
import {useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';
import * as THREE from 'three';

interface CameraPath {
  frame: number;
  position: [number, number, number];
  lookAt: [number, number, number];
}

interface AnimatedCameraProps {
  path: CameraPath[];
}

export const AnimatedCamera: React.FC<AnimatedCameraProps> = ({path}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {camera} = useThree();

  useEffect(() => {
    if (path.length < 2) return;

    // Find current segment
    let segmentIndex = 0;
    for (let i = 0; i < path.length - 1; i++) {
      if (frame >= path[i].frame && frame < path[i + 1].frame) {
        segmentIndex = i;
        break;
      }
      if (frame >= path[path.length - 1].frame) {
        segmentIndex = path.length - 2;
      }
    }

    const from = path[segmentIndex];
    const to = path[segmentIndex + 1];

    // Interpolate between keyframes
    const progress = interpolate(
      frame,
      [from.frame, to.frame],
      [0, 1],
      {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
    );

    // Smooth easing
    const smoothProgress = spring({
      frame: Math.floor(progress * 30),
      fps: 30,
      config: {damping: 200},
    });

    // Interpolate position
    camera.position.set(
      THREE.MathUtils.lerp(from.position[0], to.position[0], smoothProgress),
      THREE.MathUtils.lerp(from.position[1], to.position[1], smoothProgress),
      THREE.MathUtils.lerp(from.position[2], to.position[2], smoothProgress)
    );

    // Interpolate lookAt
    const lookAtTarget = new THREE.Vector3(
      THREE.MathUtils.lerp(from.lookAt[0], to.lookAt[0], smoothProgress),
      THREE.MathUtils.lerp(from.lookAt[1], to.lookAt[1], smoothProgress),
      THREE.MathUtils.lerp(from.lookAt[2], to.lookAt[2], smoothProgress)
    );
    camera.lookAt(lookAtTarget);
  }, [frame, path, camera, fps]);

  return null;
};

// Usage example:
// const cameraPath: CameraPath[] = [
//   {frame: 0, position: [0, 5, 10], lookAt: [0, 0, 0]},
//   {frame: 60, position: [10, 3, 5], lookAt: [0, 1, 0]},
//   {frame: 120, position: [0, 10, 0], lookAt: [0, 0, 0]},
//   {frame: 180, position: [-5, 2, 8], lookAt: [0, 0, 0]},
// ];
```
</camera_animations>

<particle_systems>
```tsx
// src/components/ParticleSystem.tsx
import React, {useMemo, useRef} from 'react';
import {useCurrentFrame} from 'remotion';
import * as THREE from 'three';

interface ParticleSystemProps {
  count?: number;
  size?: number;
  color?: string;
  spread?: number;
}

export const ParticleSystem: React.FC<ParticleSystemProps> = ({
  count = 1000,
  size = 0.05,
  color = '#ffffff',
  spread = 10,
}) => {
  const frame = useCurrentFrame();
  const pointsRef = useRef<THREE.Points>(null);

  // Generate particle positions
  const [positions, velocities] = useMemo(() => {
    const pos = new Float32Array(count * 3);
    const vel = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      // Random positions in a sphere
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const r = Math.random() * spread;

      pos[i3] = r * Math.sin(phi) * Math.cos(theta);
      pos[i3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      pos[i3 + 2] = r * Math.cos(phi);

      // Random velocities
      vel[i3] = (Math.random() - 0.5) * 0.02;
      vel[i3 + 1] = Math.random() * 0.02;
      vel[i3 + 2] = (Math.random() - 0.5) * 0.02;
    }

    return [pos, vel];
  }, [count, spread]);

  // Animate particles
  const animatedPositions = useMemo(() => {
    const animated = new Float32Array(positions.length);
    const time = frame / 30;

    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      animated[i3] = positions[i3] + Math.sin(time + i * 0.1) * 0.5;
      animated[i3 + 1] = positions[i3 + 1] + velocities[i3 + 1] * time * 10;
      animated[i3 + 2] = positions[i3 + 2] + Math.cos(time + i * 0.1) * 0.5;
    }

    return animated;
  }, [frame, positions, velocities, count]);

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={animatedPositions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={size}
        color={color}
        transparent
        opacity={0.8}
        sizeAttenuation
      />
    </points>
  );
};
```
</particle_systems>

<environment_and_lighting>
```tsx
// src/components/SceneLighting.tsx
import React from 'react';
import {Environment, ContactShadows, softShadows} from '@react-three/drei';
import {useCurrentFrame, interpolate} from 'remotion';

// Enable soft shadows
softShadows();

export const ProfessionalLighting: React.FC = () => {
  const frame = useCurrentFrame();

  // Animated light position
  const lightAngle = (frame / 60) * Math.PI * 0.5;
  const lightX = Math.sin(lightAngle) * 10;
  const lightZ = Math.cos(lightAngle) * 10;

  return (
    <>
      {/* Ambient fill light */}
      <ambientLight intensity={0.3} />

      {/* Key light (main) */}
      <directionalLight
        position={[lightX, 10, lightZ]}
        intensity={1}
        castShadow
        shadow-mapSize={[2048, 2048]}
        shadow-camera-far={50}
        shadow-camera-left={-10}
        shadow-camera-right={10}
        shadow-camera-top={10}
        shadow-camera-bottom={-10}
      />

      {/* Fill light */}
      <directionalLight
        position={[-5, 5, -5]}
        intensity={0.3}
      />

      {/* Rim light */}
      <pointLight
        position={[0, 5, -10]}
        intensity={0.5}
        color="#ff6b6b"
      />

      {/* Contact shadows for grounding */}
      <ContactShadows
        position={[0, -1.5, 0]}
        opacity={0.5}
        scale={20}
        blur={2}
        far={4}
      />

      {/* HDRI Environment (optional) */}
      {/* <Environment preset="sunset" /> */}
    </>
  );
};
```
</environment_and_lighting>

<postprocessing>
```tsx
// src/components/PostProcessing.tsx
// Note: Post-processing can be heavy; use sparingly
import React from 'react';
import {EffectComposer, Bloom, ChromaticAberration, Vignette} from '@react-three/postprocessing';
import {BlendFunction} from 'postprocessing';
import {useCurrentFrame, interpolate} from 'remotion';

export const CinematicEffects: React.FC = () => {
  const frame = useCurrentFrame();

  // Animate bloom intensity
  const bloomIntensity = interpolate(
    frame,
    [0, 60, 120],
    [0, 1.5, 0.5],
    {extrapolateRight: 'clamp'}
  );

  return (
    <EffectComposer>
      <Bloom
        luminanceThreshold={0.9}
        luminanceSmoothing={0.9}
        intensity={bloomIntensity}
      />
      <ChromaticAberration
        blendFunction={BlendFunction.NORMAL}
        offset={[0.002, 0.002]}
      />
      <Vignette
        eskil={false}
        offset={0.1}
        darkness={1.1}
      />
    </EffectComposer>
  );
};
```
</postprocessing>

<performance_tips>
- Use `<OffthreadVideo>` instead of `<Video>` for video textures
- Limit polygon count on 3D models (< 100k triangles recommended)
- Use instancing for repeated objects
- Disable shadows when not needed
- Lower shadow map resolution for faster renders
- Use LOD (Level of Detail) for complex scenes
- Pre-compute animations when possible
- Use `useMemo` for expensive calculations
</performance_tips>

<troubleshooting>
| Issue | Solution |
|-------|----------|
| GLB not loading | Check file path, ensure webpack is configured |
| Black screen | Add lighting (ambientLight + directionalLight) |
| Camera not moving | Ensure camera dependencies are in useEffect |
| Texture flickering | Use power-of-2 texture dimensions |
| Low performance | Reduce geometry complexity, disable shadows |
| Memory issues | Dispose of geometries and materials properly |
</troubleshooting>
