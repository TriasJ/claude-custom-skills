<tex_objects>
**Text and LaTeX**

```python
# Plain text
text = Text("Hello World", font_size=48)

# LaTeX text (supports LaTeX commands)
tex = Tex(r"This is \textbf{bold} and \textit{italic}")

# Mathematical expressions
math = MathTex(r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")

# Multi-line equations
equations = MathTex(
    r"f(x) &= x^2 + 2x + 1 \\",
    r"&= (x + 1)^2"
)

# Colored parts
colored_eq = MathTex(
    r"\frac{d}{dx}",
    r"e^x",
    r"=",
    r"e^x"
)
colored_eq[0].set_color(BLUE)   # derivative operator
colored_eq[1].set_color(RED)    # e^x
colored_eq[3].set_color(RED)    # e^x result
```
</tex_objects>

<number_objects>
**Numbers and Number Lines**

```python
# Integer
integer = Integer(42)

# Decimal number
decimal = DecimalNumber(3.14159, num_decimal_places=4)

# Number line
number_line = NumberLine(
    x_range=[-5, 5, 1],
    length=10,
    include_numbers=True,
    include_tip=True
)

# Number plane (2D grid)
plane = NumberPlane(
    x_range=[-5, 5, 1],
    y_range=[-3, 3, 1],
    x_length=10,
    y_length=6,
    background_line_style={
        "stroke_color": BLUE_D,
        "stroke_width": 1,
        "stroke_opacity": 0.5
    }
)

# Complex plane
complex_plane = ComplexPlane(
    x_range=[-3, 3],
    y_range=[-3, 3]
)
```
</number_objects>

<axes_graphs>
**Axes and Graphing**

```python
# Basic axes
axes = Axes(
    x_range=[-5, 5, 1],
    y_range=[-3, 3, 1],
    x_length=10,
    y_length=6,
    axis_config={
        "include_numbers": True,
        "include_tip": True,
        "numbers_to_include": np.arange(-4, 5, 2)
    },
    x_axis_config={"color": BLUE},
    y_axis_config={"color": RED}
)

# Plot function
graph = axes.plot(lambda x: x**2, color=YELLOW)

# Plot with domain restriction
restricted = axes.plot(
    lambda x: 1/x,
    x_range=[-5, -0.1],  # Avoid singularity
    color=GREEN
)

# Parametric plot
parametric = axes.plot_parametric_curve(
    lambda t: np.array([np.cos(t), np.sin(t), 0]),
    t_range=[0, TAU],
    color=PURPLE
)

# Implicit curve (requires more setup)
# Plot area between curves
area = axes.get_area(
    graph,
    x_range=[-2, 2],
    color=BLUE,
    opacity=0.3
)

# Riemann rectangles
riemann = axes.get_riemann_rectangles(
    graph,
    x_range=[-2, 2],
    dx=0.5,
    color=[BLUE, GREEN],
    fill_opacity=0.5
)

# Vertical lines to graph
lines = axes.get_vertical_lines_to_graph(
    graph,
    x_range=[-2, 2],
    num_lines=10,
    color=YELLOW
)
```
</axes_graphs>

<3d_objects>
**3D Mathematical Objects**

```python
# 3D Axes
axes_3d = ThreeDAxes(
    x_range=[-5, 5, 1],
    y_range=[-5, 5, 1],
    z_range=[-3, 3, 1],
    x_length=10,
    y_length=10,
    z_length=6
)

# Surface from function z = f(x, y)
surface = Surface(
    lambda u, v: np.array([u, v, np.sin(u) * np.cos(v)]),
    u_range=[-PI, PI],
    v_range=[-PI, PI],
    resolution=(30, 30)
)

# Parametric surface (torus)
torus = Surface(
    lambda u, v: np.array([
        (2 + np.cos(v)) * np.cos(u),
        (2 + np.cos(v)) * np.sin(u),
        np.sin(v)
    ]),
    u_range=[0, TAU],
    v_range=[0, TAU],
    resolution=(30, 30)
)

# 3D parametric curve
helix = ParametricFunction(
    lambda t: np.array([
        np.cos(t),
        np.sin(t),
        t * 0.2
    ]),
    t_range=[0, 4 * TAU],
    color=RED
).set_shade_in_3d(True)

# Sphere
sphere = Sphere(radius=1, resolution=(20, 20))

# Arrow3D
arrow = Arrow3D(
    start=ORIGIN,
    end=[1, 1, 1],
    color=RED
)
```
</3d_objects>

<geometric_shapes>
**Geometric Primitives**

```python
# Basic shapes
circle = Circle(radius=1, color=BLUE)
ellipse = Ellipse(width=4, height=2, color=GREEN)
square = Square(side_length=2, color=RED)
rectangle = Rectangle(width=4, height=2, color=YELLOW)
triangle = Triangle(color=PURPLE)
polygon = Polygon(
    [-2, -1, 0], [0, 2, 0], [2, -1, 0],
    color=ORANGE
)

# Regular polygon
hexagon = RegularPolygon(n=6, color=TEAL)

# Arc and sectors
arc = Arc(radius=2, start_angle=0, angle=PI/2)
sector = Sector(outer_radius=2, inner_radius=1, angle=PI/3)
annulus = Annulus(inner_radius=1, outer_radius=2)

# Lines and arrows
line = Line(LEFT * 2, RIGHT * 2)
arrow = Arrow(LEFT * 2, RIGHT * 2)
double_arrow = DoubleArrow(LEFT * 2, RIGHT * 2)
dashed_line = DashedLine(LEFT * 2, RIGHT * 2)

# Dot and points
dot = Dot(point=ORIGIN, radius=0.1, color=RED)
dots = VGroup(*[Dot(point=[x, 0, 0]) for x in range(-3, 4)])

# Brace
brace = Brace(square, direction=DOWN)
brace_label = brace.get_tex("width")

# Angle
angle = Angle(line1, line2, radius=0.5)
angle_label = angle.get_value()
```
</geometric_shapes>

<vector_fields>
**Vector Fields**

```python
# 2D vector field
func = lambda pos: np.array([pos[1], -pos[0], 0])
vector_field = ArrowVectorField(
    func,
    x_range=[-3, 3],
    y_range=[-3, 3]
)

# Stream lines
stream_lines = StreamLines(
    func,
    x_range=[-3, 3],
    y_range=[-3, 3],
    stroke_width=2
)

# Animate stream lines
self.play(stream_lines.create())
```
</vector_fields>

<matrices>
**Matrices and Tables**

```python
# Matrix
matrix = Matrix([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# Access elements
matrix.get_entries()  # All entries
matrix.get_rows()     # List of rows
matrix.get_columns()  # List of columns

# Determinant notation
det_matrix = Matrix(
    [[1, 2], [3, 4]],
    left_bracket="|",
    right_bracket="|"
)

# Integer matrix
int_matrix = IntegerMatrix([
    [1, 0],
    [0, 1]
])

# Table
table = Table(
    [["a", "b"],
     ["c", "d"]],
    col_labels=[Text("X"), Text("Y")],
    row_labels=[Text("1"), Text("2")],
    include_outer_lines=True
)
```
</matrices>

<special_objects>
**Special Mathematical Objects**

```python
# Function machine (conceptual)
# Create custom using rectangles and arrows

# Set notation
set_notation = MathTex(r"\{x \in \mathbb{R} : x > 0\}")

# Summation
summation = MathTex(r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}")

# Integral
integral = MathTex(r"\int_a^b f(x)\,dx")

# Limit
limit = MathTex(r"\lim_{x \to \infty} \frac{1}{x} = 0")

# Derivative
derivative = MathTex(r"\frac{d}{dx} x^n = nx^{n-1}")

# Fraction
fraction = MathTex(r"\frac{a}{b}")

# Square root
sqrt = MathTex(r"\sqrt{x^2 + y^2}")

# Greek letters
greek = MathTex(r"\alpha, \beta, \gamma, \delta, \epsilon, \theta, \phi, \psi, \omega")
```
</special_objects>
