"""
Sync a user-recorded voice-over audio file to the Manim animation beats and mix
cleanly over the soft ambient background music.

Usage:
    python3 sync_narration.py path/to/recording.m4a
    python3 sync_narration.py path/to/recording.m4a --use-existing-timings
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

from build_video import CODE_DIR, FINAL_VIDEO, MUSIC_FILE, probe_duration, render_silent_video, run
from generate_music import generate_ambient_music

TIMINGS_FILE = CODE_DIR / "beat_timings.json"
BEAT_KEYS = [
    "00_opening",
    "01_hook_problem",
    "01_hook_puzzle",
    "02_concept_three",
    "02_concept_goal",
    "03_intuition_swap_scale",
    "03_intuition_replace",
    "04_example_setup",
    "04_example_swap",
    "04_example_replace",
    "04_example_scale_finish",
    "05_verify_check",
    "05_verify_reverse",
    "06_summary",
]


def detect_speech_segments(audio_path: Path, min_silence_dur: float = 0.65, noise_db: str = "-32dB") -> list[tuple[float, float]]:
    """Detect non-silent intervals in the user's recording using FFmpeg silencedetect."""
    total_dur = probe_duration(audio_path)
    proc = subprocess.run(
        [
            "ffmpeg",
            "-i",
            str(audio_path),
            "-af",
            f"silencedetect=noise={noise_db}:d={min_silence_dur}",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    silences: list[tuple[float, float]] = []
    cur_start: float | None = None
    for line in proc.stderr.splitlines():
        m1 = re.search(r"silence_start:\s*([0-9.]+)", line)
        m2 = re.search(r"silence_end:\s*([0-9.]+)", line)
        if m1:
            cur_start = float(m1.group(1))
        elif m2 and cur_start is not None:
            silences.append((cur_start, float(m2.group(1))))
            cur_start = None
    if cur_start is not None:
        silences.append((cur_start, total_dur))

    speech: list[tuple[float, float]] = []
    pos = 0.0
    for s_start, s_end in silences:
        if s_start - pos > 0.25:
            speech.append((pos, s_start))
        pos = max(pos, s_end)
    if total_dur - pos > 0.25:
        speech.append((pos, total_dur))
    return speech


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("recording", type=Path, help="Path to recorded voice-over (.m4a, .mp3, .wav)")
    parser.add_argument("--use-existing-timings", action="store_true")
    args = parser.parse_args()

    rec = args.recording.resolve()
    if not rec.exists():
        raise FileNotFoundError(f"Recording not found: {rec}")

    if not args.use_existing_timings:
        segs = detect_speech_segments(rec)
        print(f"Detected {len(segs)} spoken segments (expected {len(BEAT_KEYS)}).")
        if len(segs) == len(BEAT_KEYS):
            timings: dict[str, float] = {}
            for idx, key in enumerate(BEAT_KEYS):
                start, end = segs[idx]
                next_start = segs[idx + 1][0] if idx + 1 < len(segs) else end + 0.8
                dur = (next_start - start) if idx > 0 else next_start
                timings[key] = round(max(4.0, dur), 3)
            TIMINGS_FILE.write_text(json.dumps(timings, indent=2), encoding="utf-8")
            print("Updated beat_timings.json from detected speech cues.")
        else:
            print("Segment count differs from 14; scaling beat_timings.json proportionally to recording duration.")
            old_timings = json.loads(TIMINGS_FILE.read_text(encoding="utf-8"))
            old_total = sum(old_timings.values())
            rec_dur = probe_duration(rec)
            ratio = rec_dur / old_total
            scaled = {k: round(v * ratio, 3) for k, v in old_timings.items()}
            TIMINGS_FILE.write_text(json.dumps(scaled, indent=2), encoding="utf-8")

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
            str(rec),
            "-i",
            str(MUSIC_FILE),
            "-filter_complex",
            "[1:a]highpass=f=85,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11,"
            "aformat=channel_layouts=stereo,apad=whole_dur="
            f"{vid_dur:.3f}[voice];"
            "[2:a]volume=0.38[bg];"
            "[voice][bg]amix=inputs=2:duration=first:normalize=0[aout]",
            "-map",
            "0:v:0",
            "-map",
            "[aout]",
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
    print(f"SUCCESS: Synced narration + music into {FINAL_VIDEO}")


if __name__ == "__main__":
    main()
