<2d_camera>
**2D Camera Control**

```python
class CameraDemo(Scene):
    def construct(self):
        # Access camera frame
        self.camera.frame

        # Zoom (scale the frame)
        self.play(self.camera.frame.animate.scale(0.5))  # Zoom in
        self.play(self.camera.frame.animate.scale(2))    # Zoom out

        # Pan (move the frame)
        self.play(self.camera.frame.animate.move_to(RIGHT * 3))

        # Combined zoom and pan
        self.play(
            self.camera.frame.animate.scale(0.7).move_to(UP * 2)
        )
```
</2d_camera>

<moving_camera>
**Moving Camera Scene**

```python
class MovingCameraDemo(MovingCameraScene):
    def construct(self):
        # Create many objects
        circles = VGroup(*[
            Circle(radius=0.5).shift(RIGHT * i * 1.5)
            for i in range(10)
        ])
        self.add(circles)

        # Save initial camera state
        self.camera.frame.save_state()

        # Focus on first circle
        self.play(
            self.camera.frame.animate.set_width(circles[0].width * 4).move_to(circles[0])
        )
        self.wait()

        # Pan through circles
        for circle in circles[1:5]:
            self.play(
                self.camera.frame.animate.move_to(circle),
                run_time=0.5
            )

        # Restore original view
        self.play(Restore(self.camera.frame))
```
</moving_camera>

<3d_camera>
**3D Camera Control**

```python
class ThreeDCameraDemo(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        sphere = Sphere(radius=1)
        self.add(axes, sphere)

        # Set initial camera orientation
        # phi: angle from z-axis (0 = top down, 90 = side view)
        # theta: rotation around z-axis
        # gamma: roll angle
        self.set_camera_orientation(
            phi=75 * DEGREES,
            theta=-45 * DEGREES,
            gamma=0
        )

        # Animate camera movement
        self.move_camera(
            phi=60 * DEGREES,
            theta=45 * DEGREES,
            run_time=2
        )

        # Set camera distance (zoom)
        self.set_camera_orientation(zoom=0.5)

        # Continuous ambient rotation
        self.begin_ambient_camera_rotation(
            rate=0.2,      # radians per second
            about="theta"  # or "phi"
        )
        self.wait(5)
        self.stop_ambient_camera_rotation()

        # Focus on specific point
        self.set_camera_orientation(frame_center=[1, 1, 1])
```
</3d_camera>

<zoomed_scene>
**Zoomed Display (Picture-in-Picture)**

```python
class ZoomedSceneDemo(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=3,
            zoomed_display_width=3,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
            },
            **kwargs
        )

    def construct(self):
        # Create detailed object
        dot = Dot().shift(LEFT * 2)
        image = ImageMobject("complex_image.png").scale(0.5)

        self.add(image, dot)

        # Activate zoom display
        self.activate_zooming(animate=True)

        # Move zoom frame
        self.play(
            self.zoomed_camera.frame.animate.move_to(dot)
        )

        # Position the zoomed display
        self.play(
            self.zoomed_display.animate.to_corner(UR)
        )

        self.wait()
```
</zoomed_scene>

<scene_configuration>
**Scene Configuration**

```python
# In manim.cfg file or via code:
class ConfiguredScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Override config
        config.pixel_height = 1080
        config.pixel_width = 1920
        config.frame_rate = 60
        config.background_color = "#1e1e1e"

    def construct(self):
        # Access config values
        width = config.frame_width    # Scene width in units
        height = config.frame_height  # Scene height in units
        # Default: 14.22 x 8 units
```
</scene_configuration>

<multi_scene>
**Multiple Scenes in One File**

```python
# All scenes in one file
class Scene1(Scene):
    def construct(self):
        self.play(Write(Text("Scene 1")))

class Scene2(Scene):
    def construct(self):
        self.play(Write(Text("Scene 2")))

class Scene3(Scene):
    def construct(self):
        self.play(Write(Text("Scene 3")))

# Render specific scene:
# manim file.py Scene2

# Render all scenes:
# manim -a file.py
```
</multi_scene>

<sections>
**Scene Sections (for Video Editing)**

```python
class SectionDemo(Scene):
    def construct(self):
        # Create sections for easy video editing
        self.next_section("Introduction")
        self.play(Write(Text("Welcome")))
        self.wait()

        self.next_section("Main Content", skip_animations=False)
        self.play(Write(MathTex("E = mc^2")))
        self.wait()

        self.next_section("Conclusion")
        self.play(Write(Text("Thank you")))

# Render with --save_sections to get separate video files
```
</sections>

<frame_control>
**Frame-by-Frame Control**

```python
class FrameControl(Scene):
    def construct(self):
        dot = Dot()
        self.add(dot)

        # Wait for specific duration
        self.wait(2)  # 2 seconds

        # Wait for specific number of frames
        self.wait(1 / config.frame_rate)  # One frame

        # Freeze frame
        self.wait(freeze_frame=True)

        # Access current time
        current_time = self.renderer.time
```
</frame_control>

<background>
**Background and Colors**

```python
class BackgroundDemo(Scene):
    def construct(self):
        # Set via config
        config.background_color = WHITE

        # Or create background rectangle
        bg = FullScreenRectangle(
            fill_color=color_gradient([BLUE, GREEN], 2),
            fill_opacity=1
        )
        self.add(bg)

        # Gradient background
        gradient = Rectangle(
            width=config.frame_width,
            height=config.frame_height
        )
        gradient.set_fill(
            color=[RED, BLUE],
            opacity=1
        )
        gradient.set_stroke(width=0)
        self.add(gradient)
```
</background>
