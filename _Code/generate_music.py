"""
Generate a warm, soft, royalty-free ambient background music track in Python.
No external copyrighted audio is needed.

Output:
    _Code/music/soft_ambient_bg.wav
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SAMPLE_RATE = 44100


def generate_ambient_music(duration_sec: float, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    n_samples = int(round(duration_sec * SAMPLE_RATE))
    t = np.linspace(0.0, duration_sec, n_samples, endpoint=False)

    # Gentle 4-chord progression (Cmaj7 -> Am7 -> Fmaj7 -> G6), 4 seconds per chord
    chords = [
        [261.63, 329.63, 392.00, 493.88],  # Cmaj7
        [220.00, 261.63, 329.63, 392.00],  # Am7
        [174.61, 220.00, 261.63, 329.63],  # Fmaj7
        [196.00, 246.94, 293.66, 329.63],  # G6
    ]
    chord_len = 4.0

    left = np.zeros(n_samples, dtype=np.float64)
    right = np.zeros(n_samples, dtype=np.float64)

    # Build smooth overlapping chord pads
    num_chords = int(np.ceil(duration_sec / chord_len))
    for i in range(num_chords):
        start_t = i * chord_len
        end_t = min(duration_sec, start_t + chord_len + 0.8)
        s0 = int(start_t * SAMPLE_RATE)
        s1 = min(n_samples, int(end_t * SAMPLE_RATE))
        if s1 <= s0:
            continue

        seg_t = t[s0:s1] - start_t
        seg_dur = (s1 - s0) / SAMPLE_RATE
        # Smooth raised-cosine envelope per chord
        attack = min(1.0, seg_dur * 0.3)
        release = min(1.2, seg_dur * 0.35)
        env = np.ones_like(seg_t)
        a_mask = seg_t < attack
        env[a_mask] = 0.5 * (1.0 - np.cos(np.pi * seg_t[a_mask] / attack))
        r_mask = seg_t > (seg_dur - release)
        env[r_mask] = 0.5 * (1.0 + np.cos(np.pi * (seg_t[r_mask] - (seg_dur - release)) / release))

        freqs = chords[i % len(chords)]
        pad_l = np.zeros_like(seg_t)
        pad_r = np.zeros_like(seg_t)
        for j, f in enumerate(freqs):
            # Subtle warm detune + second harmonic
            detune = 1.0 + (0.0015 if j % 2 == 0 else -0.0015)
            tone_l = np.sin(2.0 * np.pi * f * seg_t) + 0.15 * np.sin(2.0 * np.pi * 2.0 * f * seg_t)
            tone_r = np.sin(2.0 * np.pi * f * detune * seg_t) + 0.15 * np.sin(2.0 * np.pi * 2.0 * f * detune * seg_t)
            pan = 0.35 + 0.3 * (j / max(1, len(freqs) - 1))
            pad_l += (1.0 - pan) * tone_l
            pad_r += pan * tone_r

        # Soft bass root octave below
        bass_f = freqs[0] * 0.5
        bass = 0.45 * np.sin(2.0 * np.pi * bass_f * seg_t)
        left[s0:s1] += env * (pad_l * 0.18 + bass * 0.14)
        right[s0:s1] += env * (pad_r * 0.18 + bass * 0.14)

    # Gentle breathing LFO
    lfo = 0.88 + 0.12 * np.sin(2.0 * np.pi * 0.12 * t)
    left *= lfo
    right *= lfo

    # Warm low-pass filter at 1400 Hz so it never competes with human voice frequencies
    sos = butter(3, 1400.0, btype="low", fs=SAMPLE_RATE, output="sos")
    left = sosfilt(sos, left)
    right = sosfilt(sos, right)

    # Global 2.5s fade-in and 3.0s fade-out
    fade_in = min(n_samples, int(2.5 * SAMPLE_RATE))
    fade_out = min(n_samples, int(3.0 * SAMPLE_RATE))
    left[:fade_in] *= np.linspace(0.0, 1.0, fade_in)
    right[:fade_in] *= np.linspace(0.0, 1.0, fade_in)
    left[-fade_out:] *= np.linspace(1.0, 0.0, fade_out)
    right[-fade_out:] *= np.linspace(1.0, 0.0, fade_out)

    # Normalize to soft background level (-18 dBFS peak ≈ 0.125 amplitude)
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-9)
    gain = 0.12 / peak
    stereo = np.column_stack([left * gain, right * gain])
    pcm = np.clip(stereo * 32767.0, -32767, 32767).astype(np.int16)

    wavfile.write(str(out_path), SAMPLE_RATE, pcm)
    print(f"Generated soft ambient music: {out_path} ({duration_sec:.2f}s)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=220.0)
    args = parser.parse_args()
    out_path = Path(__file__).resolve().parent / "music" / "soft_ambient_bg.wav"
    generate_ambient_music(args.duration, out_path)


if __name__ == "__main__":
    main()
