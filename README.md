# Typing Lab

Typing Lab is a native Windows desktop application for endless typing practice. The primary deliverable is `dist/TypingLab.exe`; it opens an independent 800×600 window and does not use a browser.

## Use the application

Double-click:

```text
dist/TypingLab.exe
```

The `native/` folder contains the Python source, a direct `.pyw` launcher, and the PyInstaller recipe used to build the executable.

## Included

- English QWERTY and Traditional Zhuyin / Dachen key mapping
- Chinese target sentences with Traditional Zhuyin / Dachen key guidance; non-tone components are order-flexible and replaceable within their groups
- Chinese displays one audited primary reading, while official word-level alternatives (including common neutral-tone variants) are accepted as valid input
- 15,114 English complete-sentence entries plus 1,659 Traditional Chinese sentence entries; each bank is shuffled without repeats until exhausted
- 32 original anime/Genshin-inspired sentences are included in both language modes
- Endless local practice content
- No timer, score, accuracy percentage, or end screen
- Wrong keys do not advance the target
- Persistent cumulative character counts and recent daily practice heatmaps are kept separately for English and Chinese, using the system's local timezone
- Current key, hand, finger, and virtual keyboard guidance
- Local preference for mode and keycap labels

## Chinese mode

In Chinese mode, switch Windows to the ENG English keyboard layout. Type the Dachen keys shown by the app; initials (ㄅ–ㄙ), medials (ㄧ–ㄩ), and finals (ㄚ–ㄥ) may be entered in any order, with a later key in the same group replacing the earlier one. ㄦ is independent. The tone key must be the final key: Space is first tone, while an explicit tone key finishes the other tones. The app displays one primary reading for each character, but accepts additional word-level readings supported by the dictionaries; for example, 子 can accept both ㄗˇ and ㄗ˙ where the practice word permits it. The app displays a Traditional Chinese sentence and highlights one Chinese character at a time. Punctuation is displayed but skipped automatically; no candidate selection or Enter key is needed.

The keyboard can report which physical key was pressed, but a normal keyboard cannot report which finger pressed it. The app therefore gives a persistent standard-finger guide; it does not pretend to detect the user's actual finger.

The Chinese bank is audited against the Taiwan Ministry of Education's current
Concised Mandarin Dictionary first, with the Revised Mandarin Dictionary as a
fallback for uncommon and fictional text; TBCL is used for modern vocabulary
boundaries. The audit covers all 1,627 sentence entries and 413 corrected tone
spans, and every sentence has an official-dictionary word segmentation. The
authoritative output is `native/zhuyin_data.py`; `native/bank_data.py`,
`native/fiction_data.py`, and `native/fiction_english_data.py` retain the
generated source banks and theme-based practice content.
