---
name: create-manim-animations
description: Create and render animated mathematics videos using Manim (Mathematical Animation Engine). Use when the user asks to create math animations, animate equations, plot functions, visualize calculus concepts, create 3D surfaces, or build educational math videos. Triggers on manim, 3Blue1Brown style, theorem animation, calculus visualization, or mathematical visualization.
---

<objective>
Create and automatically render professional mathematical animations using Manim Community Edition. This skill generates the scene code, writes it to a file, executes the render, and returns the output video path. Works on Windows (PowerShell), macOS, and Linux.
</objective>

<platform_detection>
**IMPORTANT: Detect the platform first and use appropriate commands throughout.**

The skill works on:
- **Windows**: Uses PowerShell, `python` command, backslash paths
- **Linux/macOS**: Uses Bash, `python3` command, forward slash paths

Use the `Platform:` value from Claude Code's environment info to determine which commands to use.
</platform_detection>

<quick_start>
**Minimal Example** - Write this to the manim projects folder:

```python
from manim import *

class HelloMath(Scene):
    def construct(self):
        eq = MathTex(r"e^{i\pi} + 1 = 0")
        self.play(Write(eq))
        self.wait()
```

Then render using platform-appropriate commands (see execution_workflow).
</quick_start>

<execution_workflow>
**IMPORTANT: Follow these steps to create and render animations:**

<step_1>
**Determine Platform and Set Variables**

First, identify the platform from Claude Code's environment. Then set the project directory:

**Windows (PowerShell):**
```powershell
$MANIM_DIR = "$env:USERPROFILE\manim_projects"
```

**Linux/macOS (Bash):**
```bash
MANIM_DIR="$HOME/manim_projects"
```
</step_1>

<step_2>
**Check Manim Installation**

**Windows (PowerShell):**
```powershell
python -c "import manim; print('Manim ' + manim.__version__ + ' installed')"
```

If not installed:
```powershell
pip install manim
```

**Linux/macOS (Bash):**
```bash
python3 -c "import manim; print(f'Manim {manim.__version__} installed')" 2>/dev/null || echo "NOT_INSTALLED"
```

If NOT_INSTALLED:
```bash
pip install manim
```
</step_2>

<step_3>
**Create Output Directory**

**Windows (PowerShell):**
```powershell
if (-not (Test-Path $env:USERPROFILE\manim_projects)) { New-Item -ItemType Directory -Path $env:USERPROFILE\manim_projects -Force }
```

**Linux/macOS (Bash):**
```bash
mkdir -p ~/manim_projects
```
</step_3>

<step_4>
**Generate Scene Code**

Based on user's request, write a complete Manim scene to the project folder.

**Windows path:** `$env:USERPROFILE\manim_projects\scene.py`
**Linux/macOS path:** `~/manim_projects/scene.py`

Always include:
```python
from manim import *
import numpy as np

class [SceneName](Scene):  # or ThreeDScene for 3D
    def construct(self):
        # Animation code here
        pass
```
</step_4>

<step_5>
**Render the Animation**

**Windows (PowerShell):**
```powershell
Set-Location $env:USERPROFILE\manim_projects; manim -ql scene.py [SceneName]
```

Or as a single command:
```powershell
Push-Location $env:USERPROFILE\manim_projects; try { manim -ql scene.py [SceneName] } finally { Pop-Location }
```

**Linux/macOS (Bash):**
```bash
cd ~/manim_projects && manim -ql scene.py [SceneName] 2>&1
```

Quality options (all platforms):
- `-ql` (low/fast) for preview - **use this by default**
- `-qm` (medium) for better quality
- `-qh` (high) for final render
- `--format gif` to output GIF instead of MP4
</step_5>

<step_6>
**Return Output Path**

After successful render, the video is at:

**Windows:**
```
$env:USERPROFILE\manim_projects\media\videos\scene\480p15\[SceneName].mp4
```

**Linux/macOS:**
```
~/manim_projects/media/videos/scene/480p15/[SceneName].mp4
```

Quality folder mapping:
- `-ql` → `480p15/`
- `-qm` → `720p30/`
- `-qh` → `1080p60/`

Report the full path to user so they can view it.
</step_6>
</execution_workflow>

<templates>
<template name="equation_animation">
```python
from manim import *

class EquationAnimation(Scene):
    def construct(self):
        # Title
        title = Tex("Euler's Identity")
        title.to_edge(UP)

        # Equation
        equation = MathTex(r"e^{i\pi} + 1 = 0")
        equation.scale(1.5)

        # Animate
        self.play(Write(title))
        self.play(Write(equation))
        self.wait(2)
```
</template>

<template name="function_plot">
```python
from manim import *
import numpy as np

class FunctionPlot(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True}
        )

        graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        label = axes.get_graph_label(graph, label=r"\sin(x)")

        self.play(Create(axes), run_time=2)
        self.play(Create(graph), Write(label), run_time=2)
        self.wait()
```
</template>

<template name="geometric_proof">
```python
from manim import *

class GeometricProof(Scene):
    def construct(self):
        # Create shapes
        square = Square(side_length=2, color=BLUE)
        circle = Circle(radius=1, color=RED)

        # Position
        square.shift(LEFT * 2)
        circle.shift(RIGHT * 2)

        # Animate
        self.play(Create(square), Create(circle))
        self.play(Transform(square.copy(), circle))
        self.wait()
```
</template>

<template name="3d_surface">
```python
from manim import *
import numpy as np

class Surface3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes()

        surface = Surface(
            lambda u, v: np.array([u, v, np.sin(u) * np.cos(v)]),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30)
        )
        surface.set_style(fill_opacity=0.7, stroke_color=GREEN)

        self.play(Create(axes))
        self.play(Create(surface), run_time=3)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
```
</template>

<template name="calculus_integral">
```python
from manim import *
import numpy as np

class IntegralDemo(Scene):
    def construct(self):
        axes = Axes(x_range=[0, 5], y_range=[0, 3], x_length=7, y_length=4)

        func = lambda x: 0.1 * x**2
        graph = axes.plot(func, color=YELLOW)

        # Riemann sum rectangles
        rects = axes.get_riemann_rectangles(
            graph, x_range=[1, 4], dx=0.5,
            color=[BLUE, GREEN], fill_opacity=0.5
        )

        # Area under curve
        area = axes.get_area(graph, x_range=[1, 4], color=BLUE, opacity=0.3)

        integral = MathTex(r"\int_1^4 0.1x^2 \, dx").to_edge(UP)

        self.play(Create(axes), Create(graph))
        self.play(Write(integral))
        self.play(Create(rects))
        self.wait()
        self.play(Transform(rects, area))
        self.wait()
```
</template>
</templates>

<core_patterns>
<pattern name="equations">
LaTeX Equations with MathTex

```python
# Single equation
eq = MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}")

# Colored parts
eq = MathTex(r"E", r"=", r"m", r"c^2")
eq[0].set_color(BLUE)
eq[2].set_color(RED)

# Transform between equations
eq1 = MathTex(r"a^2 + b^2 = c^2")
eq2 = MathTex(r"c = \sqrt{a^2 + b^2}")
self.play(TransformMatchingTex(eq1, eq2))
```
</pattern>

<pattern name="function_plots">
Plotting Functions

```python
axes = Axes(x_range=[-3, 3, 1], y_range=[-2, 2, 1])
graph = axes.plot(lambda x: np.sin(x), color=BLUE)
area = axes.get_area(graph, x_range=[0, PI], opacity=0.3)
```
</pattern>

<pattern name="3d_scenes">
3D Surfaces (use ThreeDScene)

```python
class My3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        surface = Surface(
            lambda u, v: np.array([u, v, func(u,v)]),
            u_range=[-2, 2], v_range=[-2, 2]
        )
        self.begin_ambient_camera_rotation(rate=0.2)
```
</pattern>
</core_patterns>

<animation_reference>
| Animation | Usage |
|-----------|-------|
| `Write(tex)` | Handwrite text/equations |
| `Create(shape)` | Draw shapes |
| `FadeIn(mob)` | Fade in |
| `FadeOut(mob)` | Fade out |
| `Transform(a, b)` | Morph a into b |
| `TransformMatchingTex(a, b)` | Smart equation transform |
| `mob.animate.shift(dir)` | Move object |
| `mob.animate.scale(n)` | Scale object |
| `mob.animate.rotate(angle)` | Rotate object |
| `Indicate(mob)` | Highlight briefly |
| `Circumscribe(mob)` | Circle around |
| `MoveAlongPath(mob, path)` | Follow path |
</animation_reference>

<colors>
Available: `RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK, TEAL, GOLD, WHITE, GRAY, BLACK`

Variants: `BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E` (light to dark)
</colors>

<positioning>
```python
mob.to_edge(UP)           # Edge of screen
mob.to_corner(UR)         # Corner (UL, UR, DL, DR)
mob.move_to(ORIGIN)       # Absolute position
mob.shift(RIGHT * 2)      # Relative move
mob.next_to(other, DOWN)  # Relative to another
VGroup(a, b, c).arrange(RIGHT, buff=0.5)  # Arrange group
```
</positioning>

<success_criteria>
- Scene file written to the manim_projects folder
- Render completes without errors
- Output video path reported to user
- Animation matches user's mathematical concept request
</success_criteria>

<troubleshooting>
| Error | Solution (Windows) | Solution (Linux/macOS) |
|-------|-------------------|------------------------|
| `ModuleNotFoundError: manim` | `pip install manim` | `pip install manim` |
| `python not found` | Ensure Python is in PATH, or use `py` | Use `python3` |
| `LaTeX not found` | Install MiKTeX or TeX Live | `sudo apt install texlive texlive-latex-extra` |
| Black output | Ensure `self.play()` or `self.add()` called on mobjects | Same |
| 3D not working | Use `ThreeDScene` base class, not `Scene` | Same |
| Slow render | Use `-ql` flag for faster preview | Same |
| Path issues | Use `$env:USERPROFILE` not `~` in PowerShell | `~` works in Bash |
| Command chaining | Use `;` or wrap in script block | Use `&&` |
</troubleshooting>

<platform_quick_reference>
| Task | Windows (PowerShell) | Linux/macOS (Bash) |
|------|---------------------|-------------------|
| Python command | `python` or `py` | `python3` |
| Home directory | `$env:USERPROFILE` | `$HOME` or `~` |
| Create directory | `New-Item -ItemType Directory -Path X -Force` | `mkdir -p X` |
| Change directory | `Set-Location X` or `Push-Location X` | `cd X` |
| Chain commands | `; ` or `&& ` (PS7+) | `&&` |
| Suppress errors | `2>$null` or `-ErrorAction SilentlyContinue` | `2>/dev/null` |
| Path separator | `\` | `/` |
</platform_quick_reference>

<reference_guides>
For advanced topics:
- [references/advanced-animations.md](references/advanced-animations.md) - Updaters, rate functions, animation groups
- [references/math-objects.md](references/math-objects.md) - Matrices, vector fields, all math objects
- [references/camera-control.md](references/camera-control.md) - Camera movement, zooming, 3D camera
- [references/custom-mobjects.md](references/custom-mobjects.md) - Creating custom shapes
</reference_guides>
