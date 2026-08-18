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
- Chinese target sentences with Traditional Zhuyin / Dachen key guidance
- 11,282 unique English practice entries, including 10,000 frequency-ordered words, plus 1,259 Traditional Chinese sentences; each bank is shuffled without repeats until exhausted
- Endless local practice content
- No timer, score, accuracy percentage, or end screen
- Wrong keys do not advance the target
- Persistent cumulative character counts and recent daily practice heatmaps are kept separately for English and Chinese, using the system's local timezone
- Current key, hand, finger, and virtual keyboard guidance
- Local preference for mode and keycap labels

## Chinese mode

In Chinese mode, switch Windows to the ENG English keyboard layout. Type the Dachen keys shown by the app; Space is the first-tone key, while an explicit tone key finishes the other tones. The app displays the target Chinese sentence and advances by the correct Zhuyin sequence, so homophones such as 工 and 公 do not affect correctness. No candidate selection or Enter key is needed.

The keyboard can report which physical key was pressed, but a normal keyboard cannot report which finger pressed it. The app therefore gives a persistent standard-finger guide; it does not pretend to detect the user's actual finger.

The expanded offline bank includes the Google 10,000 English USA no-swears list, with a small COCA frequency sample used to complete 10,000 alphabetic words; the Chinese bank uses the Taiwan TOCFL/TBCL vocabulary list and Taiwan Ministry of Education pronunciation fields. See `native/bank_data.py` for the embedded generated data and source notes.
