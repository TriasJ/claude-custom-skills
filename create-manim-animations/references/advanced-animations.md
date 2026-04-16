<table_of_contents>
- animation_groups: Running multiple animations simultaneously
- rate_functions: Animation timing and easing
- updaters: Dynamic animations with value trackers
- complex_transforms: TransformMatchingShapes, TransformMatchingTex
- homotopy: Continuous deformations
- path_animations: Following paths with MoveAlongPath
- succession: Chained animations
- custom_animations: Creating custom animation classes
</table_of_contents>

<animation_groups>
Running Multiple Animations

```python
class MultipleAnimations(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()
        VGroup(circle, square, triangle).arrange(RIGHT, buff=1)

        # Simultaneous animations
        self.play(
            Create(circle),
            Create(square),
            Create(triangle)
        )

        # AnimationGroup with lag_ratio
        shapes = VGroup(*[Circle() for _ in range(5)]).arrange(RIGHT)
        self.play(AnimationGroup(
            *[Create(s) for s in shapes],
            lag_ratio=0.5  # Each starts 0.5 after previous
        ))

        # LaggedStart shorthand
        self.play(LaggedStart(
            *[FadeOut(s, shift=DOWN) for s in shapes],
            lag_ratio=0.2
        ))
```
</animation_groups>

<rate_functions>
Animation Timing with Rate Functions

```python
from manim import *

class RateFunctionDemo(Scene):
    def construct(self):
        # Available rate functions:
        # linear, smooth, rush_into, rush_from
        # slow_into, double_smooth, there_and_back
        # running_start, wiggle, ease_in_sine, ease_out_sine
        # ease_in_out_sine, ease_in_quad, ease_out_quad

        dot = Dot()

        # Linear (constant speed)
        self.play(dot.animate.shift(RIGHT * 3), rate_func=linear)

        # Smooth (default - ease in/out)
        self.play(dot.animate.shift(LEFT * 3), rate_func=smooth)

        # Rush into (fast start, slow end)
        self.play(dot.animate.shift(RIGHT * 3), rate_func=rush_into)

        # There and back
        self.play(dot.animate.shift(UP * 2), rate_func=there_and_back)
```
</rate_functions>

<updaters>
Dynamic Animations with Updaters

```python
class UpdaterDemo(Scene):
    def construct(self):
        # Value tracker for animation parameter
        t = ValueTracker(0)

        # Create objects
        dot = Dot(color=RED)
        path = Circle(radius=2)

        # Add updater - function called every frame
        dot.add_updater(
            lambda m: m.move_to(path.point_from_proportion(t.get_value()))
        )

        self.add(path, dot)

        # Animate the tracker
        self.play(t.animate.set_value(1), run_time=4, rate_func=linear)

        # Remove updater when done
        dot.clear_updaters()

        # Always-on updater example
        label = always_redraw(
            lambda: MathTex(f"t = {t.get_value():.2f}").to_edge(UP)
        )
        self.add(label)
        self.play(t.animate.set_value(0), run_time=2)
```
</updaters>

<complex_transforms>
Complex Transformations

```python
class ComplexTransforms(Scene):
    def construct(self):
        # TransformMatchingShapes - matches similar submobjects
        source = Text("Hello")
        target = Text("World")
        self.play(Write(source))
        self.play(TransformMatchingShapes(source, target))

        # Successive transformations
        eq1 = MathTex("x^2", "+", "2x", "+", "1")
        eq2 = MathTex("(x", "+", "1)", "^2")

        # Specify which parts transform to which
        self.play(Write(eq1))
        self.play(TransformMatchingTex(eq1, eq2))

        # ApplyMethod vs animate
        circle = Circle()
        # These are equivalent:
        self.play(ApplyMethod(circle.shift, RIGHT))
        self.play(circle.animate.shift(RIGHT))

        # ApplyFunction for custom transformations
        def custom_func(mob):
            mob.scale(2)
            mob.set_color(RED)
            return mob

        self.play(ApplyFunction(custom_func, circle))
```
</complex_transforms>

<homotopy>
Homotopy Animations (Continuous Deformations)

```python
class HomotopyDemo(Scene):
    def construct(self):
        square = Square()

        # Homotopy function: (x, y, z, t) -> (new_x, new_y, new_z)
        # t goes from 0 to 1 during animation
        def wave_homotopy(x, y, z, t):
            return (
                x + 0.5 * np.sin(y * 2 + t * TAU),
                y,
                z
            )

        self.play(
            Homotopy(wave_homotopy, square, run_time=3)
        )

        # Another example: morphing to circle
        def to_circle(x, y, z, t):
            angle = np.arctan2(y, x)
            radius = np.sqrt(x**2 + y**2)
            new_radius = radius * (1 - t) + 2 * t
            return (
                new_radius * np.cos(angle),
                new_radius * np.sin(angle),
                z
            )

        self.play(Homotopy(to_circle, square, run_time=2))
```
</homotopy>

<path_animations>
Following Paths

```python
class PathAnimations(Scene):
    def construct(self):
        # MoveAlongPath
        circle = Circle(radius=2)
        dot = Dot(color=RED)

        self.play(
            MoveAlongPath(dot, circle),
            run_time=3,
            rate_func=linear
        )

        # Trace path while moving
        trace = TracedPath(dot.get_center, stroke_color=YELLOW)
        self.add(trace)

        spiral = ParametricFunction(
            lambda t: np.array([
                t * np.cos(3 * t),
                t * np.sin(3 * t),
                0
            ]) * 0.5,
            t_range=[0, TAU]
        )

        self.play(MoveAlongPath(dot, spiral), run_time=4)
```
</path_animations>

<succession>
Succession - Chained Animations

```python
class SuccessionDemo(Scene):
    def construct(self):
        dot = Dot()

        # Play animations one after another in single play call
        self.play(Succession(
            Create(dot),
            dot.animate.shift(RIGHT * 2),
            dot.animate.shift(UP * 2),
            dot.animate.shift(LEFT * 2),
            dot.animate.shift(DOWN * 2),
            FadeOut(dot)
        ))
```
</succession>

<custom_animations>
Creating Custom Animations

```python
class CustomAnimation(Animation):
    def __init__(self, mobject, **kwargs):
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        # alpha goes from 0 to 1
        # Modify self.mobject based on alpha
        self.mobject.set_opacity(alpha)
        self.mobject.rotate(alpha * PI)

class UseCustomAnimation(Scene):
    def construct(self):
        square = Square()
        self.play(CustomAnimation(square), run_time=2)
```
</custom_animations>
