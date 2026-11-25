"""
Manim Scenes Part 1 — Elementary Row Operations (word-for-word synced):
  - OpeningFrame
  - Scene1Hook
  - Scene2ConceptIntro
  - Scene3VisualIntuition
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    NumberPlane,
    Scene,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
    config,
)

from math_helpers import (
    BG_COLOR,
    COLOR_A,
    COLOR_HIGHLIGHT,
    COLOR_LAMBDA,
    COLOR_NON,
    COLOR_V1,
    COLOR_V2,
    FONT_NAME,
    PANEL_BORDER,
    TEXT_MUTED,
    TEXT_PRIMARY,
    BeatClock,
    beat_dur,
    card_box,
    load_beat_timings,
    math_svg,
    scene_badge,
)

config.background_color = BG_COLOR


def clip_line_to_box(
    center: tuple[float, float],
    direction: tuple[float, float],
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Clip infinite line center + t*direction to [xmin,xmax]x[ymin,ymax]."""
    cx, cy = center
    dx, dy = direction
    ts: list[float] = []
    if abs(dx) > 1e-8:
        for xb in (xmin, xmax):
            t = (xb - cx) / dx
            yb = cy + t * dy
            if ymin - 1e-6 <= yb <= ymax + 1e-6:
                ts.append(t)
    if abs(dy) > 1e-8:
        for yb in (ymin, ymax):
            t = (yb - cy) / dy
            xb = cx + t * dx
            if xmin - 1e-6 <= xb <= xmax + 1e-6:
                ts.append(t)
    if len(ts) < 2:
        return (cx, cy), (cx, cy)
    t_min, t_max = min(ts), max(ts)
    return (cx + t_min * dx, cy + t_min * dy), (cx + t_max * dx, cy + t_max * dy)


class OpeningFrame(Scene):
    def construct(self) -> None:
        timings = load_beat_timings()
        t_open = beat_dur(timings, "00_opening", 8.8)
        clk = BeatClock(self, t_open)

        course = Text(
            "LINEAR ALGEBRA AND CALCULUS (M3)  •  INTERNAL ASSESSMENT",
            font=FONT_NAME,
            font_size=20,
            weight="BOLD",
            color=COLOR_A,
        )
        title = Text(
            "Elementary Row Operations",
            font=FONT_NAME,
            font_size=54,
            weight="BOLD",
            color=TEXT_PRIMARY,
        )
        subtitle = Text(
            "Row Swaps, Nonzero Scaling, Replacement & Solution-Set Invariance",
            font=FONT_NAME,
            font_size=24,
            color=TEXT_MUTED,
        )
        eq_left = math_svg(
            r"\begin{bmatrix} 2 & 6 & \;\;10 \\ 1 & 2 & \;\;4 \end{bmatrix}",
            color=COLOR_HIGHLIGHT,
            height=0.95,
        )
        eq_tilde = math_svg(r"\sim", color=COLOR_HIGHLIGHT, height=0.22)
        eq_right = math_svg(
            r"\begin{bmatrix} 1 & 0 & \;\;2 \\ 0 & 1 & \;\;1 \end{bmatrix}",
            color=COLOR_HIGHLIGHT,
            height=0.95,
        )
        eq_grp_left = VGroup(
            eq_left,
            DashedLine(UP * 0.45, DOWN * 0.45, color=TEXT_MUTED, stroke_width=2.0).move_to(
                eq_left.get_center() + RIGHT * 0.25
            ),
        )
        eq_grp_right = VGroup(
            eq_right,
            DashedLine(UP * 0.45, DOWN * 0.45, color=TEXT_MUTED, stroke_width=2.0).move_to(
                eq_right.get_center() + RIGHT * 0.32
            ),
        )
        eq = VGroup(eq_grp_left, eq_tilde, eq_grp_right).arrange(RIGHT, buff=0.3)
        divider = Line(LEFT * 4.4, RIGHT * 4.4, stroke_color=PANEL_BORDER, stroke_width=2)
        student = Text(
            "Yash Kumar   |   Student ID: E25B071037",
            font=FONT_NAME,
            font_size=24,
            weight="BOLD",
            color=TEXT_PRIMARY,
        )

        stack = VGroup(course, title, subtitle, eq, divider, student).arrange(DOWN, buff=0.34)
        stack.move_to(ORIGIN)

        # 0.0-1.2: Course & Student ID; 1.2-4.8: Title & Subtitle; 4.8-8.3: Matrix
        clk.play(FadeIn(course, shift=DOWN * 0.12), Create(divider), FadeIn(student), run_time=1.0)
        clk.play(Write(title), run_time=1.6)
        clk.play(FadeIn(subtitle, shift=UP * 0.1), FadeIn(eq, scale=0.94), run_time=1.4)
        clk.wait(max(0.2, t_open - clk.elapsed - 0.5))
        clk.play(FadeOut(stack), run_time=0.5)
        clk.finish()


class Scene1Hook(Scene):
    def construct(self) -> None:
        timings = load_beat_timings()
        t_prob = beat_dur(timings, "01_hook_problem", 10.8)
        t_puz = beat_dur(timings, "01_hook_puzzle", 9.5)

        badge = scene_badge("SCENE 1", "The Matrix Simplification Puzzle")

        left_card = card_box(5.8, 5.2, stroke_color=PANEL_BORDER).move_to(LEFT * 3.4 + DOWN * 0.25)
        sys_lbl = Text("Linear System → Matrix", font=FONT_NAME, font_size=22, weight="BOLD", color=COLOR_A)
        sys_eq = math_svg(
            r"\begin{cases} 2x + 6y = 10 \\ x + 2y = 4 \end{cases}",
            color=TEXT_PRIMARY,
            height=1.0,
        )
        aug_init_m = math_svg(
            r"\begin{bmatrix} 2 & 6 & \;\;10 \\ 1 & 2 & \;\;4 \end{bmatrix}",
            color=COLOR_HIGHLIGHT,
            height=1.1,
        )
        aug_bar1 = DashedLine(UP * 0.52, DOWN * 0.52, color=TEXT_MUTED, stroke_width=2.0).move_to(
            aug_init_m.get_center() + RIGHT * 0.30
        )
        aug_init = VGroup(aug_init_m, aug_bar1)
        VGroup(sys_lbl, sys_eq, aug_init).arrange(DOWN, buff=0.45).move_to(left_card)

        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=6.0,
            y_length=5.0,
            background_line_style={"stroke_color": "#23425E", "stroke_width": 1.2},
            axis_config={"stroke_color": "#52789A", "stroke_width": 2.0},
        ).move_to(RIGHT * 3.25 + DOWN * 0.25)

        line1 = Line(plane.c2p(-1, 2.0), plane.c2p(5, 0.0), color=COLOR_A, stroke_width=4.5)
        line2 = Line(plane.c2p(-1, 2.5), plane.c2p(5, -0.5), color=COLOR_V2, stroke_width=4.5)
        sol_dot = Dot(plane.c2p(2, 1), color=COLOR_HIGHLIGHT, radius=0.12)
        sol_lbl = Text("Solution (2, 1)", font=FONT_NAME, font_size=20, weight="BOLD", color=COLOR_HIGHLIGHT)
        sol_lbl.next_to(sol_dot, UP + RIGHT, buff=0.14)

        # Beat 1a (8.8 -> 19.6s):
        # 0.0-3.2: "When we solve linear equations..."
        # 3.2-6.2: "...inside a matrix."
        # 6.2-10.8: "Look at these two lines meeting at one glowing point."
        c1 = BeatClock(self, t_prob)
        c1.play(FadeIn(badge), FadeIn(left_card), FadeIn(sys_lbl), Write(sys_eq), Create(plane), run_time=2.4)
        c1.wait(0.6)
        c1.play(Write(aug_init), run_time=2.2)
        c1.wait(0.8)
        c1.play(Create(line1), Create(line2), FadeIn(sol_dot, scale=1.5), FadeIn(sol_lbl), run_time=2.6)
        c1.play(Indicate(sol_dot, color=COLOR_HIGHLIGHT, scale_factor=1.35), run_time=1.0)
        c1.finish()

        # Beat 1b (19.6 -> 29.1s):
        # 0.0-5.0: "How can we simplify the matrix step by step without ever moving that intersection point?"
        # 5.0-9.5: "That is the job of elementary row operations."
        c2 = BeatClock(self, t_puz)
        aug_final_m = math_svg(
            r"\begin{bmatrix} 1 & 0 & \;\;2 \\ 0 & 1 & \;\;1 \end{bmatrix}",
            color=COLOR_V1,
            height=1.1,
        ).move_to(aug_init_m)
        aug_bar2 = DashedLine(UP * 0.52, DOWN * 0.52, color=TEXT_MUTED, stroke_width=2.0).move_to(
            aug_final_m.get_center() + RIGHT * 0.36
        )
        aug_final = VGroup(aug_final_m, aug_bar2)
        line1_final = Line(plane.c2p(2, -1), plane.c2p(2, 4), color=COLOR_A, stroke_width=4.5)
        line2_final = Line(plane.c2p(-1, 1), plane.c2p(5, 1), color=COLOR_V2, stroke_width=4.5)

        q_bg = card_box(11.6, 0.78, stroke_color=COLOR_HIGHLIGHT).to_edge(DOWN, buff=0.28)
        q_txt = Text(
            "How do we simplify the matrix without ever moving the intersection (2, 1)?",
            font=FONT_NAME,
            font_size=22,
            weight="BOLD",
            color=COLOR_HIGHLIGHT,
        ).move_to(q_bg)

        c2.play(
            Transform(aug_init, aug_final),
            Transform(line1, line1_final),
            Transform(line2, line2_final),
            run_time=3.4,
        )
        c2.play(Indicate(sol_dot, color=COLOR_V1, scale_factor=1.3), run_time=1.1)
        c2.play(FadeIn(q_bg), FadeIn(q_txt), run_time=1.2)
        c2.wait(max(0.2, t_puz - c2.elapsed - 0.5))
        c2.play(FadeOut(*self.mobjects), run_time=0.5)
        c2.finish()


class Scene2ConceptIntro(Scene):
    def construct(self) -> None:
        timings = load_beat_timings()
        t_three = beat_dur(timings, "02_concept_three", 13.0)
        t_goal = beat_dur(timings, "02_concept_goal", 17.4)

        badge = scene_badge("SCENE 2", "The Three Elementary Row Operations")

        op_specs = [
            ("1. Row Swap", r"R_i \leftrightarrow R_j", "Exchange the positions\nof any two rows", COLOR_A),
            ("2. Row Scaling", r"R_i \leftarrow c R_i \;\;(c \neq 0)", "Multiply a row by a\nnonzero constant c", COLOR_V2),
            ("3. Row Replacement", r"R_i \leftarrow R_i + k R_j", "Add a multiple k of row j\nto another row i", COLOR_V1),
        ]
        cards = VGroup()
        for title_s, tex_s, desc_s, col in op_specs:
            box = card_box(4.0, 3.05, stroke_color=col)
            h = Text(title_s, font=FONT_NAME, font_size=22, weight="BOLD", color=col)
            eq = math_svg(tex_s, color=TEXT_PRIMARY, height=0.45)
            d = Text(desc_s, font=FONT_NAME, font_size=18, color=TEXT_MUTED, line_spacing=1.25)
            grp = VGroup(h, eq, d).arrange(DOWN, buff=0.36).move_to(box)
            cards.add(VGroup(box, grp))
        cards.arrange(RIGHT, buff=0.35).shift(UP * 0.65)

        # Beat 2a (29.1 -> 42.1s, 13.0s):
        # 0.0-3.7: intro; 3.7-5.6: Swap; 5.6-8.6: Scale; 8.6-12.0: Replace
        c1 = BeatClock(self, t_three)
        c1.play(FadeIn(badge), run_time=0.8)
        c1.wait(2.7)
        c1.play(FadeIn(cards[0], shift=UP * 0.16), run_time=1.2)
        c1.wait(0.8)
        c1.play(FadeIn(cards[1], shift=UP * 0.16), run_time=1.3)
        c1.wait(1.6)
        c1.play(FadeIn(cards[2], shift=UP * 0.16), run_time=1.3)
        c1.finish()

        # Beat 2b (42.1 -> 59.5s, 17.4s):
        # 0.0-6.5: "Here Ri stands for row i, and the vertical bar separates coefficients from constants."
        # 6.5-12.5: "By the end, you'll see why every move keeps the exact same solution."
        c2 = BeatClock(self, t_goal)
        not_bg = card_box(12.7, 1.15, stroke_color=COLOR_LAMBDA).shift(DOWN * 1.65)
        not_txt = Text(
            "Notation:   Rᵢ = Row i  of the matrix    |    [ A | b ] = Augmented Matrix (coefficients | constants)",
            font=FONT_NAME,
            font_size=20,
            color=TEXT_PRIMARY,
        ).move_to(not_bg)

        goal_bg = card_box(12.7, 1.05, stroke_color=COLOR_HIGHLIGHT).shift(DOWN * 2.95)
        goal_txt = Text(
            "Goal: Understand visually & algebraically why all three moves preserve the exact solution set.",
            font=FONT_NAME,
            font_size=20,
            weight="BOLD",
            color=COLOR_HIGHLIGHT,
        ).move_to(goal_bg)

        c2.play(FadeIn(not_bg), FadeIn(not_txt), run_time=1.5)
        c2.wait(5.0)
        c2.play(FadeIn(goal_bg), FadeIn(goal_txt), run_time=1.5)
        c2.wait(max(0.2, t_goal - c2.elapsed - 0.5))
        c2.play(FadeOut(*self.mobjects), run_time=0.5)
        c2.finish()


class Scene3VisualIntuition(Scene):
    def construct(self) -> None:
        timings = load_beat_timings()
        t_ss = beat_dur(timings, "03_intuition_swap_scale", 19.7)
        t_rep = beat_dur(timings, "03_intuition_replace", 19.8)

        badge = scene_badge("SCENE 3", "Why Solutions Never Change (Geometry)")

        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=5.8,
            y_length=4.8,
            background_line_style={"stroke_color": "#23425E", "stroke_width": 1.2},
            axis_config={"stroke_color": "#52789A", "stroke_width": 2.0},
        ).move_to(RIGHT * 3.3 + DOWN * 0.25)

        line1 = Line(plane.c2p(-1, 2.0), plane.c2p(5, 0.0), color=COLOR_A, stroke_width=4.5)
        line2 = Line(plane.c2p(-1, 2.5), plane.c2p(5, -0.5), color=COLOR_V2, stroke_width=4.5)
        sol_dot = Dot(plane.c2p(2, 1), color=COLOR_HIGHLIGHT, radius=0.12)
        sol_lbl = Text("(2, 1)", font=FONT_NAME, font_size=20, weight="BOLD", color=COLOR_HIGHLIGHT)
        sol_lbl.next_to(sol_dot, UP + RIGHT, buff=0.1)

        left_card = card_box(5.9, 5.2, stroke_color=PANEL_BORDER).move_to(LEFT * 3.35 + DOWN * 0.25)

        # Beat 3a (59.5 -> 79.2s, 19.7s):
        # 0.0-7.0: Swap; 7.0-13.8: Scale; 13.8-19.0: Zero is banned
        c1 = BeatClock(self, t_ss)
        sw_title = Text("1. Swap:  R₁ ↔ R₂", font=FONT_NAME, font_size=22, weight="BOLD", color=COLOR_A)
        sw_desc = Text("Just reorders the equations —\nneither line moves on the graph!", font=FONT_NAME, font_size=18, color=TEXT_PRIMARY, line_spacing=1.2)

        sc_title = Text("2. Scale:  R₁ ← ½ R₁", font=FONT_NAME, font_size=22, weight="BOLD", color=COLOR_V2)
        sc_eq = math_svg(r"2x + 6y = 10 \;\Longleftrightarrow\; x + 3y = 5", color=TEXT_PRIMARY, height=0.38)
        sc_desc = Text("Same line! Every point (x, y) still fits.", font=FONT_NAME, font_size=18, color=COLOR_V1)
        sc_warn = Text("✗  c = 0 is banned: 0 = 0 erases the line!", font=FONT_NAME, font_size=18, weight="BOLD", color=COLOR_NON)

        l_grp = VGroup(sw_title, sw_desc, sc_title, sc_eq, sc_desc, sc_warn).arrange(DOWN, buff=0.28).move_to(left_card)

        c1.play(FadeIn(badge), FadeIn(left_card), Create(plane), Create(line1), Create(line2), FadeIn(sol_dot), FadeIn(sol_lbl), run_time=1.3)
        c1.play(FadeIn(sw_title), FadeIn(sw_desc), Indicate(line1), Indicate(line2), run_time=2.2)
        c1.wait(3.5)
        c1.play(FadeIn(sc_title), Write(sc_eq), FadeIn(sc_desc), Indicate(line1, color=COLOR_V1), run_time=2.6)
        c1.wait(4.2)
        c1.play(FadeIn(sc_warn, shift=UP * 0.12), run_time=1.4)
        c1.finish()

        # Beat 3b (79.2 -> 99.0s, 19.8s):
        # 0.0-4.3: Row replacement title & formula
        # 4.3-8.8: "Watch the second line pivot smoothly around the intersection point." -> pivot!
        # 8.8-19.8: "Because both equations are already true at that point..." -> why + pulse
        c2 = BeatClock(self, t_rep)
        c2.play(FadeOut(l_grp), run_time=0.4)

        rep_title = Text("3. Row Replacement", font=FONT_NAME, font_size=23, weight="BOLD", color=COLOR_V1)
        rep_eq = math_svg(r"R_2 \leftarrow R_2 + k R_1", color=COLOR_V1, height=0.48)
        rep_note = Text(
            "Watch Line 2 pivot around (2, 1)\nas k slides from 0 to −2:",
            font=FONT_NAME,
            font_size=18,
            color=TEXT_PRIMARY,
            line_spacing=1.25,
        )
        k_tracker = ValueTracker(0.0)
        k_readout = always_redraw(
            lambda: Text(
                f"k = {k_tracker.get_value():.2f}",
                font=FONT_NAME,
                font_size=26,
                weight="BOLD",
                color=COLOR_HIGHLIGHT,
            ).move_to(left_card.get_center() + DOWN * 0.85)
        )
        rep_why = Text(
            "Both equations hold at (2, 1), so any\ncombination still passes through (2, 1)!",
            font=FONT_NAME,
            font_size=17,
            color=COLOR_A,
            line_spacing=1.25,
        )
        VGroup(rep_title, rep_eq, rep_note).arrange(DOWN, buff=0.3).move_to(left_card.get_top() + DOWN * 1.45)
        rep_why.move_to(left_card.get_bottom() + UP * 0.85)

        ghost_orig = DashedLine(plane.c2p(-1, 2.0), plane.c2p(5, 0.0), color=COLOR_A, stroke_opacity=0.35, stroke_width=2.5)
        self.add(ghost_orig)
        self.remove(line1)

        def get_pivoting_line():
            k = k_tracker.get_value()
            p1, p2 = clip_line_to_box((2.0, 1.0), (-(6.0 + 2.0 * k), 2.0 + k), -1.0, 5.0, -1.0, 4.0)
            return Line(plane.c2p(*p1), plane.c2p(*p2), color=COLOR_V1, stroke_width=5.0)

        pivoting_line = always_redraw(get_pivoting_line)
        self.add(pivoting_line, sol_dot)

        c2.play(FadeIn(rep_title), Write(rep_eq), FadeIn(rep_note), FadeIn(k_readout), run_time=2.0)
        c2.wait(1.8)
        c2.play(k_tracker.animate.set_value(-2.0), run_time=4.5)
        c2.play(FadeIn(rep_why, shift=UP * 0.14), Indicate(sol_dot, color=COLOR_HIGHLIGHT, scale_factor=1.3), run_time=1.8)
        c2.wait(max(0.2, t_rep - c2.elapsed - 0.5))
        c2.play(FadeOut(*self.mobjects), run_time=0.5)
        c2.finish()
