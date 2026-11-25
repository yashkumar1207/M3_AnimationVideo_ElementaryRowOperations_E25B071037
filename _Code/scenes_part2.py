"""
Manim Scenes Part 2 — Elementary Row Operations (word-for-word synced):
  - Scene4WorkedExample
  - Scene5Verification
  - Scene6SummaryCredits
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
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
    VGroup,
    Write,
    config,
)

from math_helpers import (
    BG_COLOR,
    COLOR_A,
    COLOR_HIGHLIGHT,
    COLOR_LAMBDA,
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


def make_aug_matrix(r1: tuple[str, str, str], r2: tuple[str, str, str], r1_col=TEXT_PRIMARY, r2_col=TEXT_PRIMARY) -> VGroup:
    """Build an aligned augmented matrix with independently movable/colorable rows."""
    a11 = math_svg(r1[0], color=r1_col, height=0.38)
    a12 = math_svg(r1[1], color=r1_col, height=0.38)
    b1 = math_svg(r1[2], color=r1_col, height=0.38)

    a21 = math_svg(r2[0], color=r2_col, height=0.38)
    a22 = math_svg(r2[1], color=r2_col, height=0.38)
    b2 = math_svg(r2[2], color=r2_col, height=0.38)

    xs = [-1.15, -0.35, 0.75]
    row1 = VGroup(
        a11.move_to([xs[0], 0.42, 0]),
        a12.move_to([xs[1], 0.42, 0]),
        b1.move_to([xs[2], 0.42, 0]),
    )
    row2 = VGroup(
        a21.move_to([xs[0], -0.42, 0]),
        a22.move_to([xs[1], -0.42, 0]),
        b2.move_to([xs[2], -0.42, 0]),
    )

    sep = DashedLine([0.22, 0.85, 0], [0.22, -0.85, 0], color=TEXT_MUTED, stroke_width=2.0, dash_length=0.1)
    l_brack = VGroup(
        Line([-1.65, 0.9, 0], [-1.65, -0.9, 0], color=TEXT_PRIMARY, stroke_width=2.8),
        Line([-1.65, 0.9, 0], [-1.45, 0.9, 0], color=TEXT_PRIMARY, stroke_width=2.8),
        Line([-1.65, -0.9, 0], [-1.45, -0.9, 0], color=TEXT_PRIMARY, stroke_width=2.8),
    )
    r_brack = VGroup(
        Line([1.25, 0.9, 0], [1.25, -0.9, 0], color=TEXT_PRIMARY, stroke_width=2.8),
        Line([1.05, 0.9, 0], [1.25, 0.9, 0], color=TEXT_PRIMARY, stroke_width=2.8),
        Line([1.05, -0.9, 0], [1.25, -0.9, 0], color=TEXT_PRIMARY, stroke_width=2.8),
    )
    return VGroup(l_brack, r_brack, sep, row1, row2)


class Scene4WorkedExample(Scene):
    def construct(self) -> None:
        timings = load_beat_timings()
        t_setup = beat_dur(timings, "04_example_setup", 12.8)
        t_swap = beat_dur(timings, "04_example_swap", 10.9)
        t_rep = beat_dur(timings, "04_example_replace", 13.8)
        t_sf = beat_dur(timings, "04_example_scale_finish", 17.1)

        badge = scene_badge("SCENE 4", "Step-by-Step Worked Example")

        mat_card = card_box(5.6, 5.4, stroke_color=COLOR_A).move_to(LEFT * 3.45 + DOWN * 0.25)
        work_card = card_box(6.6, 5.4, stroke_color=PANEL_BORDER).move_to(RIGHT * 3.05 + DOWN * 0.25)
        work_center = work_card.get_center()

        mat_title = Text("Augmented Matrix", font=FONT_NAME, font_size=22, weight="BOLD", color=COLOR_A)
        mat_title.move_to(mat_card.get_top() + DOWN * 0.45)

        aug = make_aug_matrix(("2", "6", "10"), ("1", "2", "4"), COLOR_A, COLOR_V2)
        aug.scale(1.15).move_to(mat_card.get_center() + DOWN * 0.15)
        r1_lbl = Text("R₁", font=FONT_NAME, font_size=18, weight="BOLD", color=TEXT_MUTED).next_to(aug[3], LEFT, buff=0.55)
        r2_lbl = Text("R₂", font=FONT_NAME, font_size=18, weight="BOLD", color=TEXT_MUTED).next_to(aug[4], LEFT, buff=0.55)

        # Beat 4a (99.0 -> 111.8s, 12.8s):
        # 0.0-4.2: "Let's solve a complete example step by step"
        # 4.2-9.0: "2x + 6y = 10 and x + 2y = 4"
        # 9.0-12.0: "written as augmented matrix"
        c1 = BeatClock(self, t_setup)
        s0_t = Text("Original System", font=FONT_NAME, font_size=23, weight="BOLD", color=COLOR_HIGHLIGHT)
        s0_eq = math_svg(r"\begin{cases} 2x + 6y = 10 \\ x + 2y = 4 \end{cases}", color=TEXT_PRIMARY, height=1.15)
        s0_note = Text("Goal: Transform left side into the identity matrix.", font=FONT_NAME, font_size=18, color=TEXT_MUTED)
        s0_grp = VGroup(s0_t, s0_eq, s0_note).arrange(DOWN, buff=0.45).move_to(work_center)

        c1.play(FadeIn(badge), FadeIn(mat_card), FadeIn(work_card), FadeIn(mat_title), FadeIn(s0_t), run_time=1.4)
        c1.wait(2.5)
        c1.play(Write(s0_eq), run_time=2.8)
        c1.wait(1.8)
        c1.play(FadeIn(aug), FadeIn(r1_lbl), FadeIn(r2_lbl), FadeIn(s0_note), run_time=2.0)
        c1.finish()

        # Beat 4b (111.8 -> 122.7s, 10.9s):
        # 0.0-4.5: "Step one, swap row one and row two..."
        # 4.5-10.4: "...clean leading one at top left. Now row one is 1, 2, 4."
        c2 = BeatClock(self, t_swap)
        c2.play(FadeOut(s0_grp), run_time=0.4)

        s1_t = Text("Step 1: Row Swap", font=FONT_NAME, font_size=24, weight="BOLD", color=COLOR_A)
        s1_op = math_svg(r"R_1 \leftrightarrow R_2", color=COLOR_HIGHLIGHT, height=0.48)
        s1_why = Text("Put leading 1 in the top-left pivot spot!", font=FONT_NAME, font_size=19, color=TEXT_PRIMARY)
        s1_grp = VGroup(s1_t, s1_op, s1_why).arrange(DOWN, buff=0.4).move_to(work_center)

        c2.play(FadeIn(s1_t), Write(s1_op), run_time=1.4)
        row1_mob = aug[3]
        row2_mob = aug[4]
        p_r1 = row1_mob.get_center()
        p_r2 = row2_mob.get_center()
        c2.play(
            row1_mob.animate.move_to(p_r2),
            row2_mob.animate.move_to(p_r1),
            path_arc=0.65,
            run_time=2.4,
        )
        aug_after_swap = make_aug_matrix(("1", "2", "4"), ("2", "6", "10"), COLOR_V2, COLOR_A).scale(1.15).move_to(aug.get_center())
        self.remove(aug)
        aug = aug_after_swap
        self.add(aug)
        c2.play(FadeIn(s1_why), Indicate(aug[3], color=COLOR_HIGHLIGHT), run_time=1.8)
        c2.finish()

        # Beat 4c (122.7 -> 136.5s, 13.8s):
        # 0.0-4.5: "Step two, replace row two with row two minus two times row one."
        # 4.5-9.0: "Subtracting 2, 4, 8 from 2, 6, 10..."
        # 9.0-13.1: "...leaves 0, 2, 2 eliminating x cleanly."
        c3 = BeatClock(self, t_rep)
        c3.play(FadeOut(s1_grp), run_time=0.4)

        s2_t = Text("Step 2: Row Replacement", font=FONT_NAME, font_size=24, weight="BOLD", color=COLOR_V1)
        s2_op = math_svg(r"R_2 \leftarrow R_2 - 2R_1", color=COLOR_V1, height=0.48)
        s2_calc = math_svg(
            r"\begin{aligned} (2,\; 6,\; 10) &- 2(1,\; 2,\; 4) \\ &= (2-2,\; 6-4,\; 10-8) \\ &= (0,\; 2,\; 2) \end{aligned}",
            color=TEXT_PRIMARY,
            height=1.45,
        )
        s2_why = Text("Eliminates x from Row 2 cleanly!", font=FONT_NAME, font_size=19, color=COLOR_HIGHLIGHT)
        s2_grp = VGroup(s2_t, s2_op, s2_calc, s2_why).arrange(DOWN, buff=0.35).move_to(work_center)

        c3.play(FadeIn(s2_t), Write(s2_op), run_time=1.8)
        c3.wait(1.8)
        c3.play(Write(s2_calc), run_time=3.2)
        aug_after_rep = make_aug_matrix(("1", "2", "4"), ("0", "2", "2"), COLOR_V2, COLOR_V1).scale(1.15).move_to(aug.get_center())
        c3.play(Transform(aug, aug_after_rep), FadeIn(s2_why), run_time=2.0)
        c3.finish()

        # Beat 4d (136.5 -> 153.6s, 17.1s):
        # 0.0-8.6: "Step three, scale row two by one-half to get 0, 1, 1, which tells us y = 1."
        # 8.6-16.1: "Finally, replace row one with row one minus two row two to get x = 2."
        c4 = BeatClock(self, t_sf)
        c4.play(FadeOut(s2_grp), run_time=0.4)

        s3_t = Text("Step 3: Scale & Finish", font=FONT_NAME, font_size=24, weight="BOLD", color=COLOR_LAMBDA)
        s3_op1 = math_svg(r"R_2 \leftarrow \tfrac{1}{2} R_2 \;\Longrightarrow\; (0,\; 1,\; 1)", color=COLOR_V1, height=0.52)
        s3_op2 = math_svg(r"R_1 \leftarrow R_1 - 2R_2 \;\Longrightarrow\; (1,\; 0,\; 2)", color=COLOR_A, height=0.48)
        s3_ans = math_svg(r"x = 2, \qquad y = 1", color=COLOR_HIGHLIGHT, height=0.52)
        s3_grp = VGroup(s3_t, s3_op1, s3_op2, s3_ans).arrange(DOWN, buff=0.38).move_to(work_center)

        c4.play(FadeIn(s3_t), Write(s3_op1), run_time=2.4)
        aug_after_scale = make_aug_matrix(("1", "2", "4"), ("0", "1", "1"), COLOR_V2, COLOR_V1).scale(1.15).move_to(aug.get_center())
        c4.play(Transform(aug, aug_after_scale), run_time=1.6)
        c4.wait(4.2)  # Wait until "Finally, replace row one..." at 8.6s

        c4.play(Write(s3_op2), run_time=2.4)
        aug_final = make_aug_matrix(("1", "0", "2"), ("0", "1", "1"), COLOR_HIGHLIGHT, COLOR_HIGHLIGHT).scale(1.15).move_to(aug.get_center())
        c4.play(Transform(aug, aug_final), Write(s3_ans), Indicate(s3_ans, color=COLOR_HIGHLIGHT), run_time=2.2)
        c4.wait(max(0.2, t_sf - c4.elapsed - 0.5))
        c4.play(FadeOut(*self.mobjects), run_time=0.5)
        c4.finish()


class Scene5Verification(Scene):
    def construct(self) -> None:
        timings = load_beat_timings()
        t_chk = beat_dur(timings, "05_verify_check", 15.5)
        t_rev = beat_dur(timings, "05_verify_reverse", 15.6)

        badge = scene_badge("SCENE 5", "Verification & Why Moves Are Reversible")

        left_card = card_box(6.1, 5.4, stroke_color=PANEL_BORDER).move_to(LEFT * 3.35 + DOWN * 0.25)

        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=5.8,
            y_length=4.8,
            background_line_style={"stroke_color": "#23425E", "stroke_width": 1.2},
            axis_config={"stroke_color": "#52789A", "stroke_width": 2.0},
        ).move_to(RIGHT * 3.3 + DOWN * 0.25)

        orig1 = DashedLine(plane.c2p(-1, 2.0), plane.c2p(5, 0.0), color=COLOR_A, stroke_opacity=0.6, stroke_width=3.0)
        orig2 = DashedLine(plane.c2p(-1, 2.5), plane.c2p(5, -0.5), color=COLOR_V2, stroke_opacity=0.6, stroke_width=3.0)
        fin1 = Line(plane.c2p(2, -1), plane.c2p(2, 4), color=COLOR_V1, stroke_width=4.5)
        fin2 = Line(plane.c2p(-1, 1), plane.c2p(5, 1), color=COLOR_HIGHLIGHT, stroke_width=4.5)
        sol_dot = Dot(plane.c2p(2, 1), color=COLOR_HIGHLIGHT, radius=0.14)
        sol_lbl = Text("(2, 1) ✓", font=FONT_NAME, font_size=22, weight="BOLD", color=COLOR_HIGHLIGHT).next_to(sol_dot, UP + RIGHT, buff=0.14)

        # Beat 5a (153.6 -> 169.1s, 15.5s):
        # 0.0-6.5: "Let's verify in the original equations: 2(2) + 6(1) = 10"
        # 6.5-10.5: "and 2 + 2(1) = 4."
        # 10.5-14.5: "Both match, and the graph confirms the same point, 2, 1."
        c1 = BeatClock(self, t_chk)
        chk_t = Text("Check in Original Equations", font=FONT_NAME, font_size=23, weight="BOLD", color=COLOR_V1)
        chk1 = math_svg(r"2(2) + 6(1) = 4 + 6 = 10 \;\checkmark", color=COLOR_A, height=0.48)
        chk2 = math_svg(r"(2) + 2(1) = 2 + 2 = 4 \;\checkmark", color=COLOR_V2, height=0.48)
        chk_note = Text("Same intersection on the graph!", font=FONT_NAME, font_size=19, color=COLOR_HIGHLIGHT)
        chk_grp = VGroup(chk_t, chk1, chk2, chk_note).arrange(DOWN, buff=0.45).move_to(left_card)

        c1.play(FadeIn(badge), FadeIn(left_card), Create(plane), Create(orig1), Create(orig2), FadeIn(chk_t), run_time=1.5)
        c1.wait(1.0)
        c1.play(Write(chk1), run_time=3.0)
        c1.wait(1.0)
        c1.play(Write(chk2), run_time=2.6)
        c1.wait(1.2)
        c1.play(Create(fin1), Create(fin2), FadeIn(sol_dot), FadeIn(sol_lbl), FadeIn(chk_note), run_time=2.4)
        c1.finish()

        # Beat 5b (169.1 -> 184.7s, 15.6s):
        # 0.0-6.0: "Why is the solution set guaranteed not to change? Because every elementary row operation is reversible."
        # 6.0-8.2: "You can undo a swap,"
        # 8.2-10.8: "divide out the scale factor,"
        # 10.8-14.5: "or subtract back a row multiple."
        c2 = BeatClock(self, t_rev)
        c2.play(FadeOut(chk_grp), run_time=0.4)

        rev_t = Text("Why Solutions Never Change:\nEvery Move Is Reversible!", font=FONT_NAME, font_size=22, weight="BOLD", color=COLOR_HIGHLIGHT, line_spacing=1.2)
        rev_list = VGroup(
            math_svg(r"R_i \leftrightarrow R_j \;\;\xrightarrow{\text{undo}}\;\; R_i \leftrightarrow R_j", color=COLOR_A, height=0.44),
            math_svg(r"c R_i \;(c \neq 0) \;\;\xrightarrow{\text{undo}}\;\; \tfrac{1}{c} R_i", color=COLOR_V2, height=0.52),
            math_svg(r"R_i + k R_j \;\;\xrightarrow{\text{undo}}\;\; R_i - k R_j", color=COLOR_V1, height=0.44),
        ).arrange(DOWN, buff=0.42)
        rev_foot = Text("No solutions lost, no false solutions added.", font=FONT_NAME, font_size=18, color=TEXT_PRIMARY)
        VGroup(rev_t, rev_list, rev_foot).arrange(DOWN, buff=0.42).move_to(left_card)

        c2.play(FadeIn(rev_t), run_time=1.4)
        c2.wait(4.0)
        c2.play(Write(rev_list[0]), run_time=1.8)
        c2.play(Write(rev_list[1]), run_time=2.2)
        c2.play(Write(rev_list[2]), run_time=2.2)
        c2.play(FadeIn(rev_foot), Indicate(sol_dot, color=COLOR_V1, scale_factor=1.3), run_time=1.2)
        c2.wait(max(0.2, t_rev - c2.elapsed - 0.5))
        c2.play(FadeOut(*self.mobjects), run_time=0.5)
        c2.finish()


class Scene6SummaryCredits(Scene):
    def construct(self) -> None:
        timings = load_beat_timings()
        t_sum = beat_dur(timings, "06_summary", 19.8)
        clk = BeatClock(self, t_sum)

        badge = scene_badge("SCENE 6", "Summary & Credits")

        takeaways = [
            ("1. Three Allowed Moves", "Swap (Rᵢ ↔ Rⱼ), nonzero scale (cRᵢ, c ≠ 0), and replacement (Rᵢ + kRⱼ).", COLOR_A),
            ("2. Solution-Set Invariance", "Every move is reversible — the exact solution set never changes.", COLOR_V1),
            ("3. Clear Matrix Solving", "Row operations reduce any augmented system [A | b] to simple answers.", COLOR_HIGHLIGHT),
        ]
        cards = VGroup()
        for t_title, t_desc, col in takeaways:
            b = card_box(12.6, 0.95, stroke_color=col)
            h = Text(t_title, font=FONT_NAME, font_size=21, weight="BOLD", color=col)
            d = Text(t_desc, font=FONT_NAME, font_size=19, color=TEXT_PRIMARY)
            txt = VGroup(h, d).arrange(RIGHT, buff=0.38).move_to(b)
            cards.add(VGroup(b, txt))
        cards.arrange(DOWN, buff=0.18).shift(UP * 1.18)

        cred_bg = card_box(12.6, 2.38, stroke_color=PANEL_BORDER).shift(DOWN * 2.15)
        cred_head = Text("References, Music Credit & AI Disclosure", font=FONT_NAME, font_size=20, weight="BOLD", color=COLOR_A)
        cred_body = Text(
            "• References: D. Lay (Linear Algebra & Its Applications); G. Strang (Intro to Linear Algebra); H. Anton & C. Rorres\n"
            "• Software & Music: Manim (Python), MathJax, FFmpeg, ReportLab; original ambient music via Python/SciPy (royalty-free)\n"
            "• AI Disclosure: Google Gemini (Antigravity) assisted with script, Manim code & storyboard; math verified independently.\n"
            "• Narrated & Created by: Yash Kumar  |  Student ID: E25B071037  |  Linear Algebra and Calculus (M3)",
            font=FONT_NAME,
            font_size=15,
            color=TEXT_MUTED,
            line_spacing=1.28,
        )
        cred_grp = VGroup(cred_head, cred_body).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(cred_bg)

        # 0.0-6.5: Card 1 ("three moves are swap, nonzero scale, and row replacement")
        # 6.5-11.2: Card 2 ("every move is reversible...")
        # 11.2-15.5: Card 3 ("together they turn any system into easy reading")
        # 15.5-19.8: Credits + "Thanks for watching!"
        clk.play(FadeIn(badge), run_time=0.6)
        clk.wait(1.2)
        clk.play(FadeIn(cards[0], shift=UP * 0.14), run_time=2.2)
        clk.wait(2.5)
        clk.play(FadeIn(cards[1], shift=UP * 0.14), run_time=2.2)
        clk.wait(2.4)
        clk.play(FadeIn(cards[2], shift=UP * 0.14), run_time=2.2)
        clk.wait(1.8)
        clk.play(FadeIn(cred_bg), FadeIn(cred_grp), run_time=1.4)
        clk.wait(max(0.2, t_sum - clk.elapsed - 0.6))
        clk.play(FadeOut(*self.mobjects), run_time=0.6)
        clk.finish()
