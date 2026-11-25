"""
Build pipeline for the voice-free 1080p MP4 with soft ambient background music.
Run:
    python3 build_video.py
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from generate_music import generate_ambient_music

CODE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CODE_DIR.parent
BUILD_DIR = CODE_DIR / "build"
FINAL_VIDEO = ROOT_DIR / "_Video.mp4"
TIMINGS_FILE = CODE_DIR / "beat_timings.json"
MUSIC_FILE = CODE_DIR / "music" / "soft_ambient_bg.wav"

SCENE_SPECS = [
    ("scenes_part1.py", "OpeningFrame"),
    ("scenes_part1.py", "Scene1Hook"),
    ("scenes_part1.py", "Scene2ConceptIntro"),
    ("scenes_part1.py", "Scene3VisualIntuition"),
    ("scenes_part2.py", "Scene4WorkedExample"),
    ("scenes_part2.py", "Scene5Verification"),
    ("scenes_part2.py", "Scene6SummaryCredits"),
]


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd or CODE_DIR), check=True)


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def render_silent_video() -> Path:
    """Render all 7 Manim scenes at 1920x1080 30fps and concatenate into silent MP4."""
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    manim_bin = str(ROOT_DIR / ".venv" / "bin" / "manim")

    clips: list[Path] = []
    for script, scene_name in SCENE_SPECS:
        run(
            [
                manim_bin,
                "-r",
                "1920,1080",
                "--fps",
                "30",
                "--disable_caching",
                script,
                scene_name,
            ]
        )
        raw_mp4 = CODE_DIR / "media" / "videos" / Path(script).stem / "1080p30" / f"{scene_name}.mp4"
        if not raw_mp4.exists():
            raise FileNotFoundError(f"Expected rendered clip at {raw_mp4}")
        clips.append(raw_mp4)

    concat_list = BUILD_DIR / "concat_silent.txt"
    concat_list.write_text(
        "\n".join(f"file '{clip.resolve()}'" for clip in clips),
        encoding="utf-8",
    )
    silent_mp4 = BUILD_DIR / "silent_1080p.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "18",
            "-preset",
            "medium",
            "-an",
            str(silent_mp4),
        ]
    )
    return silent_mp4


def main() -> None:
    silent_mp4 = render_silent_video()
    vid_dur = probe_duration(silent_mp4)

    generate_ambient_music(vid_dur, MUSIC_FILE)

    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(silent_mp4),
            "-i",
            str(MUSIC_FILE),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(FINAL_VIDEO),
        ]
    )
    final_dur = probe_duration(FINAL_VIDEO)
    print(f"\nSUCCESS: Built {FINAL_VIDEO} ({final_dur:.2f}s / {final_dur / 60:.2f} min)")


if __name__ == "__main__":
    main()
