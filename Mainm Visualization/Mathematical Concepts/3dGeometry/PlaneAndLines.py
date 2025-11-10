# plane_explainer_3d.py
# Manim Community v0.19.0
#
# Run:
#   manim -pql plane_explainer_3d.py PlaneExplainerScene
#
# This script builds an explanatory animation for:
# 1) general plane equation ax + by + cz + d = 0
# 2) intercept form x/a + y/b + z/c = 1
# 3) normal form l x + m y + n z = p  (where (l,m,n) is unit normal and p distance)
# 4) angle between two planes
# 5) angle between a line and a plane
# 6) perpendicular distance from point to plane
#
# Style:
# - Left: 3D visual (axes, plane, line, etc.)
# - Right: mathematical equations + textual explanation
# - Top: short title for the current concept
# - Variables (a,b,c,d,l,m,n,p, etc.) colored and matched between visual and right text
#
# Note: This uses ThreeDScene from Manim Community v0.19.0

from manim import *
import numpy as np

# Color map for variables so the same variable color appears in both 3D visuals and right-side text.
VAR_COLORS = {
    "a": RED,
    "b": BLUE,
    "c": GREEN,
    "d": ORANGE,
    "l": MAROON,
    "m": TEAL,
    "n": PURPLE,
    "p": GOLD,
    "x0": WHITE,  # for points if desired
}

# Utility: color occurrences of tokens in MathTex (searches substrings)
def color_math_by_tokens(mobj: MathTex, token_color_map: dict):
    for tok, col in token_color_map.items():
        mobj.set_color_by_tex(tok, col)

class PlaneExplainerScene(ThreeDScene):
    def construct(self):
        # top title that will be updated for each concept
        title = MarkupText("Plane: overview", font_size=36).to_edge(UP)
        self.add(title)

        # We'll create and show six concept groups in sequence.
        # Each group has:
        #   - left_3d_group: a VGroup of 3D objects (axes, plane, markers, arrows)
        #   - right_text_group: explanation and equations (MathTex), anchored to the right
        # We will fade between them.

        # Concept 1: General plane equation: ax + by + cz + d = 0
        c1_3d = self.make_plane_general(a=2, b=-1, c=1.2, d=-1.5)
        c1_text = self.text_for_general_equation()
        self.play(FadeIn(c1_3d), FadeIn(c1_text), run_time=1.2)
        title.become(MarkupText("1 — General plane: $ax+by+cz+d=0$", font_size=36).to_edge(UP))
        self.add_fixed_in_frame_mobjects(title)
        self.wait(1.0)
        # animate the plane coefficients highlighting
        self.play(
            c1_3d["normal_arrow"].animate.set_opacity(1.0),
            c1_text.animate.scale(1.0),
            run_time=1.6,
        )
        # rotate a bit to show 3D
        self.begin_ambient_camera_rotation(rate=0.12)  # subtle continuous rotation
        self.wait(2.0)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)

        # Fade out concept 1
        self.play(FadeOut(c1_3d), FadeOut(c1_text))
        self.wait(0.3)

        # Concept 2: Intercept form: x/a + y/b + z/c = 1
        c2_3d = self.make_plane_intercept_form(a=3, b=2, c=4)  # intercepts at (a,0,0), etc.
        c2_text = self.text_for_intercept_form()
        title.become(MarkupText("2 — Intercept form: $\\frac{x}{a}+\\frac{y}{b}+\\frac{z}{c}=1$", font_size=36).to_edge(UP))
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(c2_3d), FadeIn(c2_text), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(c2_3d), FadeOut(c2_text))
        self.wait(0.3)

        # Concept 3: Normal form: l x + m y + n z = p  (l,m,n are direction cosines of normal; p is distance)
        c3_3d = self.make_plane_normal_form(l=0.6, m=0.3, n=0.74, p=2.2)
        c3_text = self.text_for_normal_form()
        title.become(MarkupText("3 — Normal form: $l x + m y + n z = p$ (unit normal)", font_size=36).to_edge(UP))
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(c3_3d), FadeIn(c3_text))
        self.wait(2.0)
        # explain unit-normal visually: animate unit vector
        self.play(c3_3d["unit_normal"].animate.scale(1.0).set_opacity(1), run_time=1.2)
        self.wait(1.0)
        self.play(FadeOut(c3_3d), FadeOut(c3_text))
        self.wait(0.3)

        # Concept 4: Angle between two planes: cosθ = |n1·n2|/(||n1|| ||n2||)
        c4_3d = self.make_angle_between_planes_example()
        c4_text = self.text_for_angle_between_planes()
        title.become(MarkupText("4 — Angle between planes: $\\cos\\theta = \\dfrac{\\mathbf{n}_1\\cdot\\mathbf{n}_2}{\\|\\mathbf{n}_1\\|\\,\\|\\mathbf{n}_2\\|}$", font_size=32).to_edge(UP))
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(c4_3d), FadeIn(c4_text))
        self.wait(2.2)
        # animate normals highlighting
        self.play(
            c4_3d["n1_arrow"].animate.set_color(YELLOW),
            c4_3d["n2_arrow"].animate.set_color(YELLOW),
            run_time=1.0
        )
        self.wait(1.2)
        self.play(FadeOut(c4_3d), FadeOut(c4_text))
        self.wait(0.3)

        # Concept 5: Angle between a line and a plane
        c5_3d = self.make_line_plane_angle_example()
        c5_text = self.text_for_line_plane_angle()
        title.become(MarkupText("5 — Angle between line & plane: $\\sin\\phi = \\dfrac{|\\mathbf{n}\\cdot\\mathbf{v}|}{\\|\\mathbf{n}\\|\\,\\|\\mathbf{v}\\|}$", font_size=30).to_edge(UP))
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(c5_3d), FadeIn(c5_text))
        self.wait(1.8)
        # animate line moving and showing projection on plane
        self.play(c5_3d["line"].animate.shift(UP*0.5), run_time=1.2)
        self.wait(1.0)
        self.play(FadeOut(c5_3d), FadeOut(c5_text))
        self.wait(0.3)

        # Concept 6: Perpendicular distance from point to plane
        c6_3d = self.make_point_to_plane_distance_example()
        c6_text = self.text_for_point_plane_distance()
        title.become(MarkupText("6 — Perpendicular distance from $P(x_0,y_0,z_0)$ to plane: $\\dfrac{|ax_0+by_0+cz_0+d|}{\\sqrt{a^2+b^2+c^2}}$", font_size=28).to_edge(UP))
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(c6_3d), FadeIn(c6_text))
        self.wait(2.2)
        # animate dropping perpendicular
        self.play(c6_3d["perp_line"].animate.set_stroke(width=4).set_opacity(1.0), run_time=1.2)
        self.wait(1.4)

        # Final summary: fade everything and present a short recap
        self.play(FadeOut(c6_3d), FadeOut(c6_text))
        recap = MarkupText("Recap: Plane equations, normals, angles, and perpendicular distance.", font_size=28).to_edge(UP)
        self.add_fixed_in_frame_mobjects(recap)
        self.play(FadeIn(recap))
        self.wait(2.0)
        self.play(FadeOut(recap), FadeOut(title))

    # ----------------------------
    # Factory methods to build each 3D visual and the text blocks
    # Each `make_...` returns a VGroup and also stores named submobjects in a dict for animation control
    # ----------------------------
    def make_plane_general(self, a=1.0, b=1.0, c=1.0, d=0.0):
        """Create a 3D scene illustrating ax+by+cz+d=0 and the normal vector."""
        group = VGroup()
        sub = {}  # store named submobjects for later animation

        # axes
        axes = ThreeDAxes(x_range=[-5,5,1], y_range=[-5,5,1], z_range=[-3,3,1], length=6)
        axes.shift(LEFT*2.2)  # keep left
        group.add(axes)
        sub["axes"] = axes

        # Define plane by normal n = (a,b,c) and constant d
        normal = np.array([a, b, c], dtype=float)
        # choose a point on the plane: solve for x when y=z=0 -> x = -d/a (if a!=0)
        if abs(a) > 1e-6:
            point_on_plane = np.array([-d/a, 0, 0])
        elif abs(b) > 1e-6:
            point_on_plane = np.array([0, -d/b, 0])
        elif abs(c) > 1e-6:
            point_on_plane = np.array([0, 0, -d/c])
        else:
            point_on_plane = np.array([0,0,0])

        # Create a Parametric surface for the plane: for (u,v) -> point = p0 + u * e1 + v * e2
        # Find two orthogonal basis vectors on plane:
        n = normal / (np.linalg.norm(normal) + 1e-12)
        # pick any vector not parallel to n
        arbitrary = np.array([1,0,0]) if abs(n[0]) < 0.9 else np.array([0,1,0])
        e1 = np.cross(n, arbitrary)
        e1 = e1 / (np.linalg.norm(e1) + 1e-12)
        e2 = np.cross(n, e1)
        # surface function
        def plane_point(u, v):
            p = point_on_plane + u * 3 * e1 + v * 3 * e2
            return p

        plane = Surface(
            lambda u, v: plane_point(u, v),
            u_range=[-1,1],
            v_range=[-1,1],
            resolution=(15, 15)
        )
        plane.set_opacity(0.6)
        plane.set_material_specular(0.2)
        plane.set_fill(GREY_BROWN, opacity=0.5)
        plane.shift(LEFT*2.2)
        group.add(plane)
        sub["plane"] = plane

        # draw normal arrow anchored at point_on_plane
        normal_arrow = Arrow3D(
            start=point_on_plane + LEFT*2.2,
            end=point_on_plane + LEFT*2.2 + normal/np.linalg.norm(normal)*1.6,
            thickness=0.05
        )
        normal_arrow.set_color(YELLOW)
        normal_arrow.set_opacity(0.9)
        group.add(normal_arrow)
        sub["normal_arrow"] = normal_arrow

        # place small label near arrow
        n_label = MathTex("\\vec{n}=(a,b,c)").next_to(normal_arrow.get_end(), UP+RIGHT*0.2)
        n_label.shift(RIGHT*0.5)  # keep readable
        n_label.set_color(YELLOW)
        # color the a,b,c parts in label
        n_label.set_color_by_tex("a", VAR_COLORS["a"])
        n_label.set_color_by_tex("b", VAR_COLORS["b"])
        n_label.set_color_by_tex("c", VAR_COLORS["c"])
        n_label.shift(UP*0.1).scale(0.7)
        # Add right-side text (separate creation function)
        # Keep label as fixed in frame for clarity
        self.add_fixed_in_frame_mobjects(n_label)

        # Add group subdictionary to group so code can reference named parts later
        group.submobjects_dict = sub
        return group

    def text_for_general_equation(self):
        """Right-side text explaining ax+by+cz+d=0 with color-coded variables"""
        right = VGroup()
        # Primary equation
        eq = MathTex("ax + by + cz + d = 0", font_size=36)
        color_math_by_tokens(eq, {"a": VAR_COLORS["a"], "b": VAR_COLORS["b"], "c": VAR_COLORS["c"], "d": VAR_COLORS["d"]})
        eq.to_edge(RIGHT).shift(LEFT*0.5 + DOWN*0.5)

        # Explanatory bullets
        lines = VGroup(
            MathTex("\\text{Where }(a,b,c)\\text{ is a normal vector to the plane.}", font_size=22),
            MathTex("\\text{If }a\\neq 0\\text{, a point on plane: }( -d/a,\\,0,\\,0).", font_size=20),
            MathTex("\\text{Plane orientation is given by }(a,b,c).", font_size=20),
        )
        for i, l in enumerate(lines):
            l.next_to(eq, DOWN, buff=0.6 + i*0.5).align_to(eq, LEFT)

        # Color occurrences of a,b,c,d inside lines
        for m in lines:
            color_math_by_tokens(m, {"a": VAR_COLORS["a"], "b": VAR_COLORS["b"], "c": VAR_COLORS["c"], "d": VAR_COLORS["d"]})

        right.add(eq, lines)
        # anchor to right side
        right.to_edge(RIGHT)
        return right

    def make_plane_intercept_form(self, a=2, b=2, c=2):
        """Construct plane in intercept form: x/a + y/b + z/c = 1"""
        group = VGroup()
        sub = {}

        axes = ThreeDAxes(x_range=[-1, max(a,4)+1,1], y_range=[-1, max(b,4)+1,1], z_range=[-1, max(c,4)+1,1], length=6)
        axes.shift(LEFT*2.2)
        group.add(axes)
        sub["axes"] = axes

        # plane points at intercepts (a,0,0), (0,b,0), (0,0,c)
        A = np.array([a,0,0])
        B = np.array([0,b,0])
        C = np.array([0,0,c])
        # create plane as triangle patch that passes through A,B,C
        tri = Polygon3D(A+LEFT*2.2, B+LEFT*2.2, C+LEFT*2.2)
        tri.set_fill(opacity=0.6)
        tri.set_opacity(0.6)
        group.add(tri)
        sub["plane_triangle"] = tri

        # highlight intercept points with dots
        dotA = Sphere(radius=0.08, color=VAR_COLORS["a"]).move_to(A+LEFT*2.2)
        dotB = Sphere(radius=0.08, color=VAR_COLORS["b"]).move_to(B+LEFT*2.2)
        dotC = Sphere(radius=0.08, color=VAR_COLORS["c"]).move_to(C+LEFT*2.2)
        group.add(dotA, dotB, dotC)
        sub["dots"] = VGroup(dotA, dotB, dotC)

        # labels for intercepts
        A_label = MathTex("(", str(a), ",0,0)").next_to(dotA, RIGHT).scale(0.7)
        A_label.set_color_by_tex(str(a), VAR_COLORS["a"])
        B_label = MathTex("(0,", str(b), ",0)").next_to(dotB, RIGHT).scale(0.7)
        B_label.set_color_by_tex(str(b), VAR_COLORS["b"])
        C_label = MathTex("(0,0,", str(c), ")").next_to(dotC, RIGHT).scale(0.7)
        C_label.set_color_by_tex(str(c), VAR_COLORS["c"])
        A_label.shift(RIGHT*0.5)
        group.add(A_label, B_label, C_label)

        group.submobjects_dict = sub
        return group

    def text_for_intercept_form(self):
        right = VGroup()
        eq = MathTex("\\dfrac{x}{a} + \\dfrac{y}{b} + \\dfrac{z}{c} = 1", font_size=34)
        color_math_by_tokens(eq, {"a": VAR_COLORS["a"], "b": VAR_COLORS["b"], "c": VAR_COLORS["c"]})
        eq.to_edge(RIGHT).shift(LEFT*0.5 + DOWN*0.2)

        lines = VGroup(
            MathTex("\\text{Intercepts: }(a,0,0),\\,(0,b,0),\\,(0,0,c).", font_size=20),
            MathTex("\\text{This assumes }a,b,c\\neq 0.", font_size=18),
            MathTex("\\text{If one intercept is infinite, plane is parallel to that axis.}", font_size=18),
        )
        for i, l in enumerate(lines):
            l.next_to(eq, DOWN, buff=0.6 + i*0.45).align_to(eq, LEFT)

        for m in lines:
            color_math_by_tokens(m, {"a": VAR_COLORS["a"], "b": VAR_COLORS["b"], "c": VAR_COLORS["c"]})

        right.add(eq, lines)
        right.to_edge(RIGHT)
        return right

    def make_plane_normal_form(self, l=0.5, m=0.5, n=0.7071, p=2.0):
        """Create plane in normal form: l x + m y + n z = p (where l,m,n form a unit normal)"""
        group = VGroup()
        sub = {}

        axes = ThreeDAxes(x_range=[-4,4,1], y_range=[-4,4,1], z_range=[-3,3,1], length=6)
        axes.shift(LEFT*2.2)
        group.add(axes)
        sub["axes"] = axes

        # unit normal vector
        normal = np.array([l,m,n], dtype=float)
        norm_len = np.linalg.norm(normal)
        if norm_len == 0:
            normal = np.array([0,0,1.0])
            norm_len = 1.0
        normal_unit = normal / norm_len

        # find point on plane = normal_unit * p
        p_point = normal_unit * p

        # small surface
        def plane_point(u, v):
            # build orthonormal basis on plane:
            arbitrary = np.array([1, 0, 0]) if abs(normal_unit[0]) < 0.9 else np.array([0, 1, 0])
            e1 = np.cross(normal_unit, arbitrary)
            e1 = e1 / (np.linalg.norm(e1) + 1e-12)
            e2 = np.cross(normal_unit, e1)
            return p_point + u * e1 * 3 + v * e2 * 3

        plane = Surface(lambda u, v: plane_point(u, v), u_range=[-0.9,0.9], v_range=[-0.9,0.9], resolution=(12,12))
        plane.shift(LEFT*2.2)
        plane.set_fill(GREY_BROWN, opacity=0.5)
        plane.set_opacity(0.6)
        group.add(plane)
        sub["plane"] = plane

        # unit normal arrow from origin to p_point (since p = distance along unit normal)
        unit_normal_arrow = Arrow3D(start=ORIGIN+LEFT*2.2, end=p_point+LEFT*2.2, thickness=0.06)
        unit_normal_arrow.set_color(VAR_COLORS["p"])
        unit_normal_arrow.set_opacity(0.9)
        group.add(unit_normal_arrow)
        sub["unit_normal"] = unit_normal_arrow

        # label shows l,m,n,p with colors
        label = MathTex("l x + m y + n z = p", font_size=28).next_to(plane, RIGHT+UP*0.6)
        color_math_by_tokens(label, {"l": VAR_COLORS["l"], "m": VAR_COLORS["m"], "n": VAR_COLORS["n"], "p": VAR_COLORS["p"]})
        self.add_fixed_in_frame_mobjects(label)

        group.submobjects_dict = sub
        return group

    def text_for_normal_form(self):
        right = VGroup()
        eq = MathTex("l x + m y + n z = p", font_size=38)
        color_math_by_tokens(eq, {"l": VAR_COLORS["l"], "m": VAR_COLORS["m"], "n": VAR_COLORS["n"], "p": VAR_COLORS["p"]})
        eq.to_edge(RIGHT).shift(LEFT*0.5)
        lines = VGroup(
            MathTex("\\text{Here }(l,m,n)\\text{ is a unit normal (direction cosines).}", font_size=20),
            MathTex("\\text{And }p\\text{ is the (signed) distance from origin to plane.}", font_size=20),
            MathTex("\\text{Convert from }ax+by+cz+d=0\\text{ by dividing by }\\sqrt{a^2+b^2+c^2}.", font_size=18),
        )
        for i, l in enumerate(lines):
            l.next_to(eq, DOWN, buff=0.6 + i*0.45).align_to(eq, LEFT)

        # color tokens in lines
        for m in lines:
            color_math_by_tokens(m, {"l": VAR_COLORS["l"], "m": VAR_COLORS["m"], "n": VAR_COLORS["n"], "p": VAR_COLORS["p"]})

        right.add(eq, lines)
        right.to_edge(RIGHT)
        return right

    def make_angle_between_planes_example(self):
        """Create two planes with different normals and show angle between them via normals."""
        group = VGroup()
        sub = {}

        axes = ThreeDAxes(x_range=[-4,4,1], y_range=[-4,4,1], z_range=[-3,3,1], length=6)
        axes.shift(LEFT*2.2)
        group.add(axes)
        sub["axes"] = axes

        # first plane: normal n1
        n1 = np.array([1, 0.8, 0.2])
        p1_point = np.array([0.8, 0.2, 1.0])
        n1_unit = n1 / np.linalg.norm(n1)
        # second plane: normal n2
        n2 = np.array([0.2, -1.0, 0.6])
        p2_point = np.array([-0.8, -0.1, -0.6])
        n2_unit = n2 / np.linalg.norm(n2)

        # create small surfaces for planes
        def plane1(u, v):
            arbitrary = np.array([1,0,0]) if abs(n1_unit[0]) < 0.9 else np.array([0,1,0])
            e1 = np.cross(n1_unit, arbitrary); e1 /= np.linalg.norm(e1)
            e2 = np.cross(n1_unit, e1)
            return p1_point + u*e1*2.7 + v*e2*2.7
        def plane2(u, v):
            arbitrary = np.array([1,0,0]) if abs(n2_unit[0]) < 0.9 else np.array([0,1,0])
            e1 = np.cross(n2_unit, arbitrary); e1 /= np.linalg.norm(e1)
            e2 = np.cross(n2_unit, e1)
            return p2_point + u*e1*2.7 + v*e2*2.7

        surf1 = Surface(lambda u,v: plane1(u,v), u_range=[-1,1], v_range=[-1,1], resolution=(12,12))
        surf2 = Surface(lambda u,v: plane2(u,v), u_range=[-1,1], v_range=[-1,1], resolution=(12,12))
        surf1.shift(LEFT*2.2); surf2.shift(LEFT*2.2)
        surf1.set_opacity(0.6)
        surf2.set_opacity(0.6)
        surf1.set_fill(BLUE_E, opacity=0.4)
        surf2.set_fill(ORANGE, opacity=0.4)
        group.add(surf1, surf2)
        sub["surf1"] = surf1; sub["surf2"] = surf2

        # normals arrows (positioned at each plane's p_point)
        n1_arrow = Arrow3D(start=p1_point+LEFT*2.2, end=p1_point+LEFT*2.2 + n1_unit*1.4, thickness=0.04)
        n2_arrow = Arrow3D(start=p2_point+LEFT*2.2, end=p2_point+LEFT*2.2 + n2_unit*1.4, thickness=0.04)
        n1_arrow.set_color(YELLOW)
        n2_arrow.set_color(YELLOW)
        group.add(n1_arrow, n2_arrow)
        sub["n1_arrow"] = n1_arrow; sub["n2_arrow"] = n2_arrow

        # small arc showing angle between normals (project to plane that contains both arrows)
        # compute angle
        dot = float(np.dot(n1_unit, n2_unit))
        theta = np.arccos(np.clip(dot, -1.0, 1.0))
        # place an Arc at a midpoint near origin for visual measure
        arc_radius = 0.8
        # find plane of arc: use a simple location near origin in front of axes
        arc = Arc3D(
            center=LEFT*2.2 + ORIGIN,
            axis=np.array([0,0,1]),
            radius=arc_radius,
            angle=theta,
            start_angle=0
        )
        # Note: Arc3D is for reference; if unavailable, fallback to a 2D arc in 3D space approximation.
        arc.set_color(YELLOW)
        arc.set_opacity(0.9)
        # If Arc3D is not perfect in your Manim version, you may replace with a CurvedArrow or similar.
        # We'll add a MathTex label for theta
        theta_label = MathTex("\\theta", font_size=24).move_to(LEFT*2.2 + np.array([arc_radius*0.6,0.2,0]))
        theta_label.set_color(YELLOW)
        group.add(arc, theta_label)
        sub["theta_arc"] = arc; sub["theta_label"] = theta_label

        group.submobjects_dict = sub
        return group

    def text_for_angle_between_planes(self):
        right = VGroup()
        eq = MathTex("\\cos\\theta = \\dfrac{\\mathbf{n}_1\\cdot\\mathbf{n}_2}{\\|\\mathbf{n}_1\\|\\,\\|\\mathbf{n}_2\\|}", font_size=30)
        eq.to_edge(RIGHT).shift(LEFT*0.5)
        expl = MathTex("\\text{Angle between planes equals angle between their normals.}", font_size=20)
        expl.next_to(eq, DOWN, buff=0.6).align_to(eq, LEFT)
        right.add(eq, expl)
        right.to_edge(RIGHT)
        return right

    def make_line_plane_angle_example(self):
        """Show a line intersecting a plane, mark the angle between line and plane."""
        group = VGroup()
        sub = {}

        axes = ThreeDAxes(x_range=[-4,4,1], y_range=[-4,4,1], z_range=[-3,3,1], length=6)
        axes.shift(LEFT*2.2)
        group.add(axes)
        sub["axes"] = axes

        # plane (horizontal-ish)
        plane_point = np.array([0.0, 0.0, 0.0])
        normal = np.array([0.2, 0.3, 1.0])  # not purely vertical → tilted plane
        normal_unit = normal / np.linalg.norm(normal)
        def plane_p(u, v):
            arbitrary = np.array([1, 0, 0]) if abs(normal_unit[0]) < 0.9 else np.array([0,1,0])
            e1 = np.cross(normal_unit, arbitrary); e1 /= np.linalg.norm(e1)
            e2 = np.cross(normal_unit, e1)
            return plane_point + u*e1*3 + v*e2*3
        surf = Surface(lambda u, v: plane_p(u, v), u_range=[-1,1], v_range=[-1,1], resolution=(12,12))
        surf.shift(LEFT*2.2)
        surf.set_fill(GREY_BROWN, opacity=0.5)
        group.add(surf)
        sub["plane"] = surf

        # line direction vector v (diagonal through space)
        v = np.array([1.0, 0.8, 0.6])
        line_start = np.array([-2.0, -1.2, -1.5])
        line_end = line_start + v*4.0
        line = Line3D(start=line_start+LEFT*2.2, end=line_end+LEFT*2.2).set_stroke(width=4)
        line.set_color(TEAL)
        group.add(line)
        sub["line"] = line

        # intersection point approximate where line meets plane: solve for t such that point lies on plane:
        # plane eq: normal.(x - plane_point) = 0 -> normal.dot(line_start + t*v - plane_point)=0 => t = -normal.dot(line_start - plane_point)/normal.dot(v)
        denom = float(np.dot(normal, v))
        if abs(denom) > 1e-6:
            t = -np.dot(normal, (line_start - plane_point)) / denom
            intersect = line_start + t * v
        else:
            intersect = line_start  # parallel - fallback
        inter_dot = Sphere(radius=0.08, color=WHITE).move_to(intersect+LEFT*2.2)
        group.add(inter_dot)
        sub["intersection"] = inter_dot

        # draw normal arrow at intersection
        n_arrow = Arrow3D(start=intersect+LEFT*2.2, end=intersect+LEFT*2.2 + normal_unit*1.6, thickness=0.04)
        n_arrow.set_color(YELLOW)
        n_arrow.set_opacity(0.85)
        group.add(n_arrow)
        sub["normal_arrow"] = n_arrow

        # show small angle between line and plane: use right triangle construction -
        # angle between line and normal α satisfies cosα = |n·v|/(||n|| ||v||)
        # angle between line and plane φ = 90° - α, but we visualize φ and display formula sinφ = |n·v|/(||n|| ||v||)
        # draw projection of v onto plane: v_proj = v - (n_unit·v) n_unit
        v_proj = v - np.dot(normal_unit, v) * normal_unit
        # create small arrow for projection starting at intersection
        proj_arrow = Arrow3D(start=intersect+LEFT*2.2, end=intersect+LEFT*2.2 + v_proj/np.linalg.norm(v_proj)*1.6, thickness=0.04)
        proj_arrow.set_color(GREEN)
        proj_arrow.set_opacity(0.9)
        group.add(proj_arrow)
        sub["proj_arrow"] = proj_arrow

        # draw arc between line direction and the projection to indicate angle phi
        # For visual simplicity, we will place a small 2D Arc near the intersection in camera-facing plane:
        arc = Circle(radius=0.5).move_to(intersect+LEFT*2.2 + UP*0.2)
        arc.set_opacity(0.0)  # invisible guide
        # place theta label
        phi_label = MathTex("\\phi").move_to(intersect+LEFT*2.2 + UP*0.6)
        phi_label.set_color(ORANGE)
        group.add(phi_label)

        group.submobjects_dict = sub
        return group

    def text_for_line_plane_angle(self):
        right = VGroup()
        eq = MathTex("\\sin \\phi = \\dfrac{|\\mathbf{n}\\cdot\\mathbf{v}|}{\\|\\mathbf{n}\\|\\,\\|\\mathbf{v}\\|}", font_size=30)
        eq.to_edge(RIGHT).shift(LEFT*0.5)
        expl = MathTex("\\text{Where }\\phi\\text{ is the angle between the line and the plane.}", font_size=20)
        expl.next_to(eq, DOWN, buff=0.6).align_to(eq, LEFT)
        right.add(eq, expl)
        right.to_edge(RIGHT)
        return right

    def make_point_to_plane_distance_example(self):
        """Show a point and drop perpendicular to plane; animate length formula."""
        group = VGroup()
        sub = {}

        axes = ThreeDAxes(x_range=[-4,4,1], y_range=[-4,4,1], z_range=[-3,3,1], length=6)
        axes.shift(LEFT*2.2)
        group.add(axes); sub["axes"] = axes

        # plane: ax + by + cz + d = 0 with chosen a,b,c,d
        a, b, c, d = 1.2, -0.6, 0.8, -1.0
        normal = np.array([a,b,c], dtype=float)
        n_unit = normal / np.linalg.norm(normal)
        # pick a point on plane (as before)
        if abs(a) > 1e-6:
            p0 = np.array([-d/a, 0, 0])
        elif abs(b) > 1e-6:
            p0 = np.array([0, -d/b, 0])
        else:
            p0 = np.array([0,0,-d/c])

        def plane_p(u, v):
            arbitrary = np.array([1,0,0]) if abs(n_unit[0]) < 0.9 else np.array([0,1,0])
            e1 = np.cross(n_unit, arbitrary); e1 /= np.linalg.norm(e1)
            e2 = np.cross(n_unit, e1)
            return p0 + u*e1*3 + v*e2*3

        surf = Surface(lambda u,v: plane_p(u,v), u_range=[-1,1], v_range=[-1,1], resolution=(12,12))
        surf.shift(LEFT*2.2)
        surf.set_fill(GREY_BROWN, opacity=0.6)
        group.add(surf)
        sub["plane"] = surf

        # point P in space
        P = np.array([2.2, 1.1, 1.8])
        P_dot = Sphere(radius=0.09, color=WHITE).move_to(P+LEFT*2.2)
        group.add(P_dot); sub["P"] = P_dot

        # drop perpendicular from P to plane: foot Q = P - ((a x0 + b y0 + c z0 + d) / (a^2+b^2+c^2)) * [a,b,c]
        numerator = a*P[0] + b*P[1] + c*P[2] + d
        denom = a*a + b*b + c*c
        dist_signed = numerator / (np.sqrt(denom) + 1e-12)
        factor = numerator / (denom + 1e-12)
        Q = P - factor * normal
        Q_dot = Sphere(radius=0.07, color=VAR_COLORS["p"]).move_to(Q+LEFT*2.2)
        group.add(Q_dot); sub["Q"] = Q_dot

        perp_line = Line3D(start=P+LEFT*2.2, end=Q+LEFT*2.2).set_stroke(width=3).set_opacity(0.6)
        perp_line.set_color(VAR_COLORS["p"])
        perp_line.set_opacity(0.7)
        perp_line.set_stroke(width=2)
        group.add(perp_line)
        sub["perp_line"] = perp_line

        # label showing formula and numeric computed length
        formula = MathTex(
            "d(P,\\Pi)=\\dfrac{|ax_0+by_0+cz_0+d|}{\\sqrt{a^2+b^2+c^2}}",
            font_size=26
        )
        # color a,b,c,d tokens
        color_math_by_tokens(formula, {"a": VAR_COLORS["a"], "b": VAR_COLORS["b"], "c": VAR_COLORS["c"], "d": VAR_COLORS["d"]})
        # numeric value
        value = MathTex(f"=\\;{abs(numerator)/np.sqrt(denom):.3f}", font_size=24).next_to(formula, RIGHT, buff=0.5)
        value.shift(RIGHT*0.3)
        formula_group = VGroup(formula, value)
        self.add_fixed_in_frame_mobjects(formula_group)

        group.submobjects_dict = sub
        return group

    def text_for_point_plane_distance(self):
        right = VGroup()
        eq = MathTex("d(P,\\Pi)=\\dfrac{|ax_0+by_0+cz_0+d|}{\\sqrt{a^2+b^2+c^2}}", font_size=30)
        color_math_by_tokens(eq, {"a": VAR_COLORS["a"], "b": VAR_COLORS["b"], "c": VAR_COLORS["c"], "d": VAR_COLORS["d"]})
        eq.to_edge(RIGHT).shift(LEFT*0.5)
        expl = MathTex("\\text{Absolute value makes distance non-negative; denominator normalizes the normal vector.}", font_size=18)
        expl.next_to(eq, DOWN, buff=0.6).align_to(eq, LEFT)
        right.add(eq, expl)
        right.to_edge(RIGHT)
        return right

# ---------- Helper 3D primitives (Arrow3D, Line3D, Polygon3D) ----------
# Manim's core includes some 3D primitives, but depending on the local install you may want to use
# simple wrappers. If Arrow3D/Line3D/Polygon3D are not present, you can replace with
# `Arrow` and `Line` after projecting points using axes.c2p, or adapt as needed.

# If Arrow3D/Line3D/Polygon3D are missing in your setup, Manim still will show Surface and ThreeDAxes.
# The code above uses Arrow3D/Line3D as convenience wrappers; replace them with proper 3D objects if needed.

# End of script
