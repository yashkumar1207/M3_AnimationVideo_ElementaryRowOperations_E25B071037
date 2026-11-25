# M3 Animation Video Project — Elementary Row Operations

- **Course:** Linear Algebra and Calculus (M3) — Internal Assessment (10%)
- **Topic:** Elementary Row Operations (Swap, Nonzero Scaling, Replacement & Solution-Set Invariance)
- **Student:** Yash Kumar (`E25B071037`)
- **Recommended Public GitHub Repo Name:** `M3_AnimationVideo_ElementaryRowOperations_E25B071037`
- **Duration:** ~3 minutes 24 seconds (strictly under 4 minutes)

## Repository Contents

| Deliverable | Path | Description |
|---|---|---|
| Final 1080p Video | [`_Video.mp4`](_Video.mp4) | 1920×1080 16:9 MP4 with Opening Frame, 6 scenes, Closing Frame, student voice-over, and soft background music |
| Animation Source Code | [`_Code/`](_Code/) | Modular Manim Python scripts, MathJax LaTeX-SVG helper, music generator, and FFmpeg sync/build pipeline |
| 6-Scene Storyboard PDF | [`Storyboard_Elementary_Row_Operations_E25B071037.pdf`](Storyboard_Elementary_Row_Operations_E25B071037.pdf) | Complete 6-scene visual, narration, and math plan |
| Narration Script | [`_Code/NARRATION_SCRIPT.md`](_Code/NARRATION_SCRIPT.md) | Short, easy-to-read cue-by-cue script (~464 words) |
| References & AI Disclosure | [`AI_DISCLOSURE_AND_REFERENCES.md`](AI_DISCLOSURE_AND_REFERENCES.md) | Mathematical sources, music credit, and AI disclosure |

## Mathematical Summary (Worked Example)

We solve the linear system:

$$
\begin{cases}
2x + 6y = 10 \\
x + 2y = 4
\end{cases}
\qquad \Longleftrightarrow \qquad
\left[\begin{array}{cc|c}
2 & 6 & 10 \\
1 & 2 & 4
\end{array}\right]
$$

1. **Row Swap ($R_1 \leftrightarrow R_2$):** $\left[\begin{array}{cc|c} 1 & 2 & 4 \\ 2 & 6 & 10 \end{array}\right]$
2. **Row Replacement ($R_2 \leftarrow R_2 - 2R_1$):** $\left[\begin{array}{cc|c} 1 & 2 & 4 \\ 0 & 2 & 2 \end{array}\right]$
3. **Row Scaling ($R_2 \leftarrow \tfrac{1}{2} R_2$):** $\left[\begin{array}{cc|c} 1 & 2 & 4 \\ 0 & 1 & 1 \end{array}\right] \implies y = 1$
4. **Row Replacement ($R_1 \leftarrow R_1 - 2R_2$):** $\left[\begin{array}{cc|c} 1 & 0 & 2 \\ 0 & 1 & 1 \end{array}\right] \implies x = 2,\; y = 1$
5. **Verification:** $2(2) + 6(1) = 10\;\checkmark$, $2 + 2(1) = 4\;\checkmark$.

## Building & Syncing Your Voice Recording

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r _Code/requirements.txt
cd _Code && npm install

# Build 1080p video with soft background music
python3 build_video.py

# After recording narration, sync every frame to your speech and mix over music:
python3 sync_narration.py path/to/your_recording.m4a
```
