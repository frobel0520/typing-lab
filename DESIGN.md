# Typing Lab v0 — Design notes

## Design Read

- Artifact: 800×600 desktop practice utility
- Audience: people using short work breaks to build touch-typing muscle memory
- Visual language: restrained dark builder-tool interface with a quiet practice-room feel
- Mode: greenfield
- Dials: visual variance 3 / motion 2 / information density 7 / asset dependence 1 / brand fidelity 7 (Codex dark-theme reference)

## Positioning

- Narrative role: the practice surface is the product; no landing or result screen interrupts the loop.
- Viewing distance: close laptop distance; compact type scale with a large, readable target line.
- Visual temperature: quiet, focused, slightly technical.
- Capacity check: the 800×600 canvas uses a stable two-column spine; the practice line receives the largest area, while the right rail only carries actionable state.

## Design decisions

- Palette: layered charcoal surfaces, light gray text, muted lavender focus, green left-hand guidance, blue-violet right-hand guidance, amber thumb guidance, coral error feedback.
- Typography: UI uses IBM Plex Sans with Noto Sans TC / Segoe UI fallbacks; target text and key labels use IBM Plex Mono with Cascadia Mono / Consolas fallbacks.
- Spacing: 4px base, composed primarily from 4 / 8 / 12 / 16px units.
- Radius: 4px keycaps, 6px controls, 9–10px panels; rounded corners signal grouping, not decoration.
- Shadow: one quiet elevation for the prompt card and settings panel only.
- Motion: short state feedback only; reduced-motion styles remove caret and key animations.

## Behavior notes

The app judges the physical key code and keeps the cursor on the same target after a wrong key. Software cannot sense which physical finger touched the key, so the UI uses the standard finger assignment as an explicit guide rather than claiming to detect the user's actual finger.

The Zhuyin mode uses the Dachen standard mapping. It presents Chinese practice phrases plus their current Zhuyin key sequence, and requires Space as the selection / syllable boundary key. The content stream is assembled from a local phrase bank so it can continue without a timer, login, or network connection.
