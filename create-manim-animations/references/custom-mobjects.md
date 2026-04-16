<basic_custom>
**Creating Custom Mobjects**

```python
class CustomShape(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Define points that make up the shape
        self.set_points_as_corners([
            LEFT + UP,
            RIGHT + UP,
            RIGHT + DOWN,
            LEFT + DOWN,
            LEFT + UP  # Close the shape
        ])
        self.set_fill(BLUE, opacity=0.5)
        self.set_stroke(WHITE, width=2)

class UseCustomShape(Scene):
    def construct(self):
        shape = CustomShape()
        self.play(Create(shape))
```
</basic_custom>

<composite_mobjects>
**Composite Mobjects (VGroup)**

```python
class LabeledCircle(VGroup):
    def __init__(self, label_text, radius=1, **kwargs):
        super().__init__(**kwargs)

        # Create components
        self.circle = Circle(radius=radius, color=BLUE)
        self.label = Text(label_text, font_size=24)
        self.label.move_to(self.circle.get_center())

        # Add to group
        self.add(self.circle, self.label)

    def set_label(self, new_text):
        new_label = Text(new_text, font_size=24)
        new_label.move_to(self.circle.get_center())
        self.remove(self.label)
        self.label = new_label
        self.add(self.label)

class UseLabeledCircle(Scene):
    def construct(self):
        lc = LabeledCircle("A", radius=1.5)
        self.play(Create(lc))
        self.wait()
        lc.set_label("B")
        self.wait()
```
</composite_mobjects>

<parametric_mobjects>
**Parametric Custom Shapes**

```python
class Star(VMobject):
    def __init__(self, n_points=5, outer_radius=2, inner_radius=1, **kwargs):
        super().__init__(**kwargs)

        points = []
        for i in range(2 * n_points):
            angle = i * PI / n_points - PI / 2
            radius = outer_radius if i % 2 == 0 else inner_radius
            points.append([
                radius * np.cos(angle),
                radius * np.sin(angle),
                0
            ])
        points.append(points[0])  # Close

        self.set_points_as_corners(points)
        self.set_fill(YELLOW, opacity=0.8)
        self.set_stroke(ORANGE, width=2)

class Heart(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Parametric heart curve
        t_range = np.linspace(0, TAU, 100)
        points = []
        for t in t_range:
            x = 16 * np.sin(t)**3
            y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
            points.append([x * 0.1, y * 0.1, 0])

        self.set_points_smoothly(points)
        self.set_fill(RED, opacity=0.8)
        self.set_stroke(DARK_RED, width=2)
```
</parametric_mobjects>

<mobject_methods>
**Essential Mobject Methods**

```python
class MobjectMethodsDemo(Scene):
    def construct(self):
        mob = Square()

        # Positioning
        mob.move_to(ORIGIN)
        mob.shift(RIGHT * 2)
        mob.to_edge(UP)
        mob.to_corner(UL)
        mob.next_to(other_mob, RIGHT, buff=0.5)
        mob.align_to(other_mob, UP)

        # Transformations
        mob.scale(2)
        mob.stretch(2, dim=0)  # Stretch horizontally
        mob.rotate(PI / 4)
        mob.rotate(PI / 4, about_point=ORIGIN)
        mob.flip(UP)  # Mirror

        # Styling
        mob.set_color(RED)
        mob.set_fill(BLUE, opacity=0.5)
        mob.set_stroke(GREEN, width=3)
        mob.set_opacity(0.7)

        # Information
        center = mob.get_center()
        width = mob.get_width()
        height = mob.get_height()
        corners = mob.get_corner(UR)
        edge = mob.get_edge_center(RIGHT)

        # Copying
        copy = mob.copy()
        mob.save_state()
        # ... modify mob ...
        mob.restore()

        # Target for animation
        mob.generate_target()
        mob.target.shift(UP)
        self.play(MoveToTarget(mob))
```
</mobject_methods>

<svg_import>
**Importing SVG Files**

```python
class SVGDemo(Scene):
    def construct(self):
        # Import SVG
        svg = SVGMobject("path/to/file.svg")
        svg.scale(2)

        # Access sub-elements
        svg[0].set_color(RED)
        svg[1].set_color(BLUE)

        # Iterate through parts
        for i, part in enumerate(svg):
            part.set_color(random_color())

        self.play(Create(svg))
```
</svg_import>

<image_mobjects>
**Image Mobjects**

```python
class ImageDemo(Scene):
    def construct(self):
        # Import image
        img = ImageMobject("path/to/image.png")
        img.scale(2)
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])

        self.add(img)

        # Animate image
        self.play(img.animate.shift(RIGHT))

        # Image with opacity
        img.set_opacity(0.5)
```
</image_mobjects>

<updater_mobjects>
**Mobjects with Built-in Updaters**

```python
class DynamicMobject(VGroup):
    def __init__(self, tracker, **kwargs):
        super().__init__(**kwargs)
        self.tracker = tracker

        self.circle = Circle(radius=1)
        self.label = DecimalNumber(0, num_decimal_places=2)
        self.label.move_to(self.circle.get_center())

        self.add(self.circle, self.label)

        # Add permanent updater
        self.add_updater(self._update)

    def _update(self, mob, dt):
        value = self.tracker.get_value()
        self.circle.set_fill(
            interpolate_color(BLUE, RED, value),
            opacity=0.5
        )
        self.label.set_value(value)
        self.label.move_to(self.circle.get_center())

class UseDynamicMobject(Scene):
    def construct(self):
        tracker = ValueTracker(0)
        dynamic = DynamicMobject(tracker)

        self.add(dynamic)
        self.play(tracker.animate.set_value(1), run_time=3)
        self.play(tracker.animate.set_value(0), run_time=3)
```
</updater_mobjects>

<3d_custom>
**Custom 3D Mobjects**

```python
class Custom3D(ThreeDScene):
    def construct(self):
        # Create custom 3D surface
        surface = Surface(
            self.param_func,
            u_range=[0, TAU],
            v_range=[0, PI],
            resolution=(30, 30)
        )
        surface.set_style(
            fill_opacity=0.7,
            stroke_color=WHITE,
            stroke_width=0.5
        )

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Create(surface))
        self.begin_ambient_camera_rotation()
        self.wait(5)

    def param_func(self, u, v):
        # Sphere with bumps
        r = 1 + 0.3 * np.sin(5 * u) * np.sin(5 * v)
        return np.array([
            r * np.sin(v) * np.cos(u),
            r * np.sin(v) * np.sin(u),
            r * np.cos(v)
        ])
```
</3d_custom>

<always_redraw>
**Always Redraw Pattern**

```python
class AlwaysRedrawDemo(Scene):
    def construct(self):
        # Tracker
        x = ValueTracker(0)

        # Always redrawn line from origin to moving point
        line = always_redraw(
            lambda: Line(
                ORIGIN,
                [x.get_value(), x.get_value()**2, 0],
                color=YELLOW
            )
        )

        # Always redrawn label
        label = always_redraw(
            lambda: MathTex(
                f"x = {x.get_value():.2f}"
            ).to_corner(UR)
        )

        self.add(line, label)
        self.play(x.animate.set_value(3), run_time=4)
        self.play(x.animate.set_value(-2), run_time=4)
```
</always_redraw>
