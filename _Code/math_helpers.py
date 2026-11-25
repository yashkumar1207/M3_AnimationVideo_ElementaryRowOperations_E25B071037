"""
Shared helpers, palette constants, proportional beat timing, and LaTeX-to-SVG rendering.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from manim import (
    BLACK,
    LEFT,
    RIGHT,
    UP,
    RoundedRectangle,
    SVGMobject,
    Text,
    VGroup,
)

CODE_DIR = Path(__file__).resolve().parent
TEX2SVG_SCRIPT = CODE_DIR / "tex2svg.mjs"
TEX_CACHE_DIR = CODE_DIR / ".tex_cache"
TIMINGS_FILE = CODE_DIR / "beat_timings.json"

# Clean 1080p high-contrast palette
BG_COLOR = "#0D1117"
PANEL_BG = "#161B22"
PANEL_BORDER = "#30363D"
TEXT_PRIMARY = "#F0F6FC"
TEXT_MUTED = "#9DA7B3"

COLOR_A = "#58A6FF"        # Matrix A / blue
COLOR_V1 = "#3FB950"       # Eigenvector v1 (lambda = 2) / green
COLOR_V2 = "#FFA657"       # Eigenvector v2 (lambda = -1) / amber-orange
COLOR_NON = "#F85149"      # Non-eigenvector e1 / coral red
COLOR_LAMBDA = "#D2A8FF"   # Eigenvalue lambda / violet
COLOR_HIGHLIGHT = "#F2CC60"

FONT_NAME = "Helvetica Neue"


def load_beat_timings() -> dict[str, float]:
    """Load exact target durations (seconds) per beat."""
    if not TIMINGS_FILE.exists():
        return {}
    return json.loads(TIMINGS_FILE.read_text(encoding="utf-8"))


def beat_dur(timings: dict[str, float], key: str, default: float) -> float:
    return float(timings.get(key, default))


def math_svg(
    tex: str,
    color: str = TEXT_PRIMARY,
    height: float | None = None,
    scale: float = 1.0,
) -> SVGMobject:
    """Render a LaTeX expression to a cached Manim SVGMobject using MathJax."""
    TEX_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = subprocess.check_output(
        ["node", str(TEX2SVG_SCRIPT), tex, str(TEX_CACHE_DIR)],
        text=True,
    ).strip()
    mob = SVGMobject(svg_path)
    mob.set_color(color)
    mob.scale(0.32 * scale)
    if height is not None:
        mob.scale_to_fit_height(height)
    return mob


def scene_badge(scene_num: str, title: str) -> VGroup:
    """Create a consistent top-left scene header pill + title."""
    pill_text = Text(scene_num, font=FONT_NAME, font_size=18, weight="BOLD", color=BLACK)
    pill_bg = RoundedRectangle(
        corner_radius=0.12,
        width=pill_text.width + 0.36,
        height=pill_text.height + 0.18,
        fill_color=COLOR_A,
        fill_opacity=1.0,
        stroke_width=0,
    )
    pill = VGroup(pill_bg, pill_text)
    pill_text.move_to(pill_bg.get_center())

    label = Text(title, font=FONT_NAME, font_size=26, weight="BOLD", color=TEXT_PRIMARY)
    group = VGroup(pill, label).arrange(RIGHT, buff=0.22, aligned_edge=UP)
    group.to_corner(UP + LEFT, buff=0.45)
    return group


def card_box(
    width: float,
    height: float,
    fill_color: str = PANEL_BG,
    stroke_color: str = PANEL_BORDER,
    corner_radius: float = 0.18,
) -> RoundedRectangle:
    """Consistent rounded card background for formulas and panels."""
    return RoundedRectangle(
        corner_radius=corner_radius,
        width=width,
        height=height,
        fill_color=fill_color,
        fill_opacity=0.92,
        stroke_color=stroke_color,
        stroke_width=1.8,
    )


class BeatClock:
    """
    Tracks elapsed animation time inside a beat and pads cleanly to the
    exact beat duration from beat_timings.json so frames match spoken words.
    """

    def __init__(self, scene, target_sec: float) -> None:
        self.scene = scene
        self.target = target_sec
        self.elapsed = 0.0

    def play(self, *anims, run_time: float = 1.0, **kwargs) -> None:
        rt = max(0.1, run_time)
        self.scene.play(*anims, run_time=rt, **kwargs)
        self.elapsed += rt

    def wait(self, sec: float) -> None:
        if sec > 0.02:
            self.scene.wait(sec)
            self.elapsed += sec

    def finish(self) -> None:
        rem = self.target - self.elapsed
        if rem > 0.04:
            self.scene.wait(rem)
            self.elapsed += rem
