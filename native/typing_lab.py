"""Typing Lab: a small native Windows typing practice app.

The Chinese mode uses the English keyboard layout and checks the physical
Dachen key sequence. Space is the first-tone key; an explicit tone key
finishes the other tones. No IME candidate or Enter key is involved.
"""

from __future__ import annotations

import json
import os
import random
import string
import tkinter as tk
from datetime import date, datetime, timedelta
from pathlib import Path

from bank_data import GENERATED_ENGLISH_FRAGMENTS, GENERATED_ZHUYIN_SAMPLES


COLORS = {
    "bg": "#0f1013",
    "surface": "#15171b",
    "raised": "#1b1e23",
    "soft": "#20242b",
    "line": "#292d35",
    "line_strong": "#373c47",
    "text": "#eef0f3",
    "text_soft": "#c2c6cf",
    "muted": "#858b96",
    "muted_deep": "#5c626d",
    "accent": "#a89cff",
    "accent_strong": "#8d7fff",
    "accent_soft": "#27243d",
    "left": "#80c9af",
    "left_soft": "#1d302d",
    "right": "#9eabec",
    "right_soft": "#252a43",
    "thumb": "#d6b375",
    "thumb_soft": "#332d20",
    "error": "#ed8d9a",
    "error_soft": "#3a252d",
}

FONT_UI = ("Segoe UI", 9)
FONT_UI_SMALL = ("Segoe UI", 8)
FONT_UI_MEDIUM = ("Segoe UI", 10)
FONT_MONO_SMALL = ("Cascadia Mono", 8)


FINGERS = {
    "leftPinky": {"name": "左手小指", "short": "小指", "hand": "left", "hand_name": "LEFT HAND", "letter": "L1"},
    "leftRing": {"name": "左手無名指", "short": "無名", "hand": "left", "hand_name": "LEFT HAND", "letter": "L2"},
    "leftMiddle": {"name": "左手中指", "short": "中指", "hand": "left", "hand_name": "LEFT HAND", "letter": "L3"},
    "leftIndex": {"name": "左手食指", "short": "食指", "hand": "left", "hand_name": "LEFT HAND", "letter": "L4"},
    "rightIndex": {"name": "右手食指", "short": "食指", "hand": "right", "hand_name": "RIGHT HAND", "letter": "R4"},
    "rightMiddle": {"name": "右手中指", "short": "中指", "hand": "right", "hand_name": "RIGHT HAND", "letter": "R3"},
    "rightRing": {"name": "右手無名指", "short": "無名", "hand": "right", "hand_name": "RIGHT HAND", "letter": "R2"},
    "rightPinky": {"name": "右手小指", "short": "小指", "hand": "right", "hand_name": "RIGHT HAND", "letter": "R1"},
    "thumb": {"name": "拇指", "short": "拇指", "hand": "thumb", "hand_name": "THUMB", "letter": "TH"},
}

FINGER_MAP: dict[str, dict[str, str]] = {}


def assign_finger(finger: str, codes: list[str]) -> None:
    for code in codes:
        FINGER_MAP[code] = FINGERS[finger]


assign_finger("leftPinky", ["Backquote", "Digit1", "KeyQ", "KeyA", "KeyZ", "Tab", "CapsLock", "ShiftLeft"])
assign_finger("leftRing", ["Digit2", "KeyW", "KeyS", "KeyX"])
assign_finger("leftMiddle", ["Digit3", "KeyE", "KeyD", "KeyC"])
assign_finger("leftIndex", ["Digit4", "Digit5", "KeyR", "KeyT", "KeyF", "KeyG", "KeyV", "KeyB"])
assign_finger("rightIndex", ["Digit6", "Digit7", "KeyY", "KeyU", "KeyH", "KeyJ", "KeyN", "KeyM"])
assign_finger("rightMiddle", ["Digit8", "KeyI", "KeyK", "Comma"])
assign_finger("rightRing", ["Digit9", "KeyO", "KeyL", "Period"])
assign_finger("rightPinky", ["Digit0", "Minus", "Equal", "KeyP", "BracketLeft", "BracketRight", "Backslash", "Semicolon", "Quote", "Slash", "Enter", "Backspace", "ShiftRight"])
assign_finger("thumb", ["Space", "AltLeft", "AltRight"])


KEY_LABELS = {
    "Backquote": "`", "Digit1": "1", "Digit2": "2", "Digit3": "3", "Digit4": "4", "Digit5": "5",
    "Digit6": "6", "Digit7": "7", "Digit8": "8", "Digit9": "9", "Digit0": "0", "Minus": "-", "Equal": "=",
    "KeyQ": "Q", "KeyW": "W", "KeyE": "E", "KeyR": "R", "KeyT": "T", "KeyY": "Y", "KeyU": "U", "KeyI": "I",
    "KeyO": "O", "KeyP": "P", "BracketLeft": "[", "BracketRight": "]", "Backslash": "\\",
    "KeyA": "A", "KeyS": "S", "KeyD": "D", "KeyF": "F", "KeyG": "G", "KeyH": "H", "KeyJ": "J", "KeyK": "K",
    "KeyL": "L", "Semicolon": ";", "Quote": "'", "KeyZ": "Z", "KeyX": "X", "KeyC": "C", "KeyV": "V",
    "KeyB": "B", "KeyN": "N", "KeyM": "M", "Comma": ",", "Period": ".", "Slash": "/",
    "Tab": "TAB", "CapsLock": "CAPS", "Enter": "ENTER", "Backspace": "⌫", "ShiftLeft": "SHIFT",
    "ShiftRight": "SHIFT", "ControlLeft": "CTRL", "ControlRight": "CTRL", "AltLeft": "ALT",
    "AltRight": "ALT", "Space": "SPACE",
}


KEYBOARD_ROWS = [
    [("Backquote", 1), ("Digit1", 1), ("Digit2", 1), ("Digit3", 1), ("Digit4", 1), ("Digit5", 1), ("Digit6", 1), ("Digit7", 1), ("Digit8", 1), ("Digit9", 1), ("Digit0", 1), ("Minus", 1), ("Equal", 1), ("Backspace", 1.55)],
    [("Tab", 1.55), ("KeyQ", 1), ("KeyW", 1), ("KeyE", 1), ("KeyR", 1), ("KeyT", 1), ("KeyY", 1), ("KeyU", 1), ("KeyI", 1), ("KeyO", 1), ("KeyP", 1), ("BracketLeft", 1), ("BracketRight", 1), ("Backslash", 1)],
    [("CapsLock", 1.9), ("KeyA", 1), ("KeyS", 1), ("KeyD", 1), ("KeyF", 1), ("KeyG", 1), ("KeyH", 1), ("KeyJ", 1), ("KeyK", 1), ("KeyL", 1), ("Semicolon", 1), ("Quote", 1), ("Enter", 1.9)],
    [("ShiftLeft", 2.55), ("KeyZ", 1), ("KeyX", 1), ("KeyC", 1), ("KeyV", 1), ("KeyB", 1), ("KeyN", 1), ("KeyM", 1), ("Comma", 1), ("Period", 1), ("Slash", 1), ("ShiftRight", 2.55)],
    [("ControlLeft", 1.55), ("AltLeft", 1.55), ("Space", 5.6), ("AltRight", 1.55), ("ControlRight", 1.55)],
]


# Windows Microsoft Bopomofo / Dachen key arrangement.
ZHUYIN_TO_KEY = {
    "ㄅ": ("1", "Digit1"), "ㄆ": ("Q", "KeyQ"), "ㄇ": ("A", "KeyA"), "ㄈ": ("Z", "KeyZ"),
    "ㄉ": ("2", "Digit2"), "ㄊ": ("W", "KeyW"), "ㄋ": ("S", "KeyS"), "ㄌ": ("X", "KeyX"),
    "ㄍ": ("E", "KeyE"), "ㄎ": ("D", "KeyD"), "ㄏ": ("C", "KeyC"),
    "ㄐ": ("R", "KeyR"), "ㄑ": ("F", "KeyF"), "ㄒ": ("V", "KeyV"),
    "ㄓ": ("5", "Digit5"), "ㄔ": ("T", "KeyT"), "ㄕ": ("G", "KeyG"), "ㄖ": ("B", "KeyB"),
    "ㄗ": ("Y", "KeyY"), "ㄘ": ("H", "KeyH"), "ㄙ": ("N", "KeyN"),
    "ㄧ": ("U", "KeyU"), "ㄨ": ("J", "KeyJ"), "ㄩ": ("M", "KeyM"),
    "ㄚ": ("8", "Digit8"), "ㄛ": ("I", "KeyI"), "ㄜ": ("K", "KeyK"), "ㄝ": (",", "Comma"),
    "ㄞ": ("9", "Digit9"), "ㄟ": ("O", "KeyO"), "ㄠ": ("L", "KeyL"), "ㄡ": (".", "Period"),
    "ㄢ": ("0", "Digit0"), "ㄣ": ("P", "KeyP"), "ㄤ": (";", "Semicolon"), "ㄥ": ("/", "Slash"), "ㄦ": ("-", "Minus"),
    "ˊ": ("6", "Digit6"), "ˇ": ("3", "Digit3"), "ˋ": ("4", "Digit4"), "˙": ("7", "Digit7"),
}

TONE_SYMBOLS = {"ˊ", "ˇ", "ˋ", "˙"}


ZHUYIN_SAMPLES = [
    ("我喜歡打字", ["ㄨㄛˇ", "ㄒㄧˇ", "ㄏㄨㄢ", "ㄉㄚˇ", "ㄗˋ"]),
    ("每天練習注音", ["ㄇㄟˇ", "ㄊㄧㄢ", "ㄌㄧㄢˋ", "ㄒㄧˊ", "ㄓㄨˋ", "ㄧㄣ"]),
    ("專注讓手指穩定", ["ㄓㄨㄢ", "ㄓㄨˋ", "ㄖㄤˋ", "ㄕㄡˇ", "ㄓˇ", "ㄨㄣˇ", "ㄉㄧㄥˋ"]),
    ("中文輸入需要節奏", ["ㄓㄨㄥ", "ㄨㄣˊ", "ㄕㄨ", "ㄖㄨˋ", "ㄒㄩ", "ㄧㄠˋ", "ㄐㄧㄝˊ", "ㄗㄡˋ"]),
    ("工作空檔練習幾分鐘", ["ㄍㄨㄥ", "ㄗㄨㄛˋ", "ㄎㄨㄥˋ", "ㄉㄤˇ", "ㄌㄧㄢˋ", "ㄒㄧˊ", "ㄐㄧˇ", "ㄈㄣ", "ㄓㄨㄥ"]),
    ("慢慢打也能更準確", ["ㄇㄢˋ", "ㄇㄢˋ", "ㄉㄚˇ", "ㄧㄝˇ", "ㄋㄥˊ", "ㄍㄥˋ", "ㄓㄨㄣˇ", "ㄑㄩㄝˋ"]),
    ("熟悉鍵位之後更快", ["ㄕㄨˊ", "ㄒㄧˊ", "ㄐㄧㄢˋ", "ㄨㄟˋ", "ㄓ", "ㄏㄡˋ", "ㄍㄥˋ", "ㄎㄨㄞˋ"]),
    ("讓每次按鍵都更穩", ["ㄖㄤˋ", "ㄇㄟˇ", "ㄘˋ", "ㄢˋ", "ㄐㄧㄢˋ", "ㄉㄡ", "ㄍㄥˋ", "ㄨㄣˇ"]),
    ("工作空檔也能練習", ["ㄍㄨㄥ", "ㄗㄨㄛˋ", "ㄎㄨㄥˋ", "ㄉㄤˇ", "ㄧㄝˇ", "ㄋㄥˊ", "ㄌㄧㄢˋ", "ㄒㄧˊ"]),
    ("保持輕鬆慢慢輸入", ["ㄅㄠˇ", "ㄔˊ", "ㄑㄧㄥ", "ㄙㄨㄥ", "ㄇㄢˋ", "ㄇㄢˋ", "ㄕㄨ", "ㄖㄨˋ"]),
    ("專心完成手上的工作", ["ㄓㄨㄢ", "ㄒㄧㄣ", "ㄨㄢˊ", "ㄔㄥˊ", "ㄕㄡˇ", "ㄕㄤˋ", "ㄉㄜ˙", "ㄍㄨㄥ", "ㄗㄨㄛˋ"]),
    ("每天留一點時間練習", ["ㄇㄟˇ", "ㄊㄧㄢ", "ㄌㄧㄡˊ", "ㄧ", "ㄉㄧㄢˇ", "ㄕˊ", "ㄐㄧㄢ", "ㄌㄧㄢˋ", "ㄒㄧˊ"]),
    ("讓雙手保持放鬆", ["ㄖㄤˋ", "ㄕㄨㄤ", "ㄕㄡˇ", "ㄅㄠˇ", "ㄔˊ", "ㄈㄤˋ", "ㄙㄨㄥ"]),
    ("先看清楚再開始輸入", ["ㄒㄧㄢ", "ㄎㄢˋ", "ㄑㄧㄥ", "ㄔㄨˇ", "ㄗㄞˋ", "ㄎㄞ", "ㄕˇ", "ㄕㄨ", "ㄖㄨˋ"]),
    ("正確的節奏需要耐心", ["ㄓㄥˋ", "ㄑㄩㄝˋ", "ㄉㄜ˙", "ㄐㄧㄝˊ", "ㄗㄡˋ", "ㄒㄩ", "ㄧㄠˋ", "ㄋㄞˋ", "ㄒㄧㄣ"]),
    ("不要急著追求速度", ["ㄅㄨˋ", "ㄧㄠˋ", "ㄐㄧˊ", "ㄓㄜ˙", "ㄓㄨㄟ", "ㄑㄧㄡˊ", "ㄙㄨˋ", "ㄉㄨˋ"]),
    ("熟悉之後自然會更快", ["ㄕㄨˊ", "ㄒㄧˊ", "ㄓ", "ㄏㄡˋ", "ㄗˋ", "ㄖㄢˊ", "ㄏㄨㄟˋ", "ㄍㄥˋ", "ㄎㄨㄞˋ"]),
    ("每個按鍵都有固定位置", ["ㄇㄟˇ", "ㄍㄜˋ", "ㄢˋ", "ㄐㄧㄢˋ", "ㄉㄡ", "ㄧㄡˇ", "ㄍㄨˋ", "ㄉㄧㄥˋ", "ㄨㄟˋ", "ㄓˋ"]),
    ("手指應該回到基本位置", ["ㄕㄡˇ", "ㄓˇ", "ㄧㄥ", "ㄍㄞ", "ㄏㄨㄟˊ", "ㄉㄠˋ", "ㄐㄧ", "ㄅㄣˇ", "ㄨㄟˋ", "ㄓˋ"]),
    ("看到錯誤就放慢一點", ["ㄎㄢˋ", "ㄉㄠˋ", "ㄘㄨㄛˋ", "ㄨˋ", "ㄐㄧㄡˋ", "ㄈㄤˋ", "ㄇㄢˋ", "ㄧ", "ㄉㄧㄢˇ"]),
    ("安靜的環境適合練習", ["ㄢ", "ㄐㄧㄥˋ", "ㄉㄜ˙", "ㄏㄨㄢˊ", "ㄐㄧㄥˋ", "ㄕˋ", "ㄏㄜˊ", "ㄌㄧㄢˋ", "ㄒㄧˊ"]),
    ("短暫練習也能累積進步", ["ㄉㄨㄢˇ", "ㄗㄢˋ", "ㄌㄧㄢˋ", "ㄒㄧˊ", "ㄧㄝˇ", "ㄋㄥˊ", "ㄌㄟˇ", "ㄐㄧ", "ㄐㄧㄣˋ", "ㄅㄨˋ"]),
    ("把注意力放在當下", ["ㄅㄚˇ", "ㄓㄨˋ", "ㄧˋ", "ㄌㄧˋ", "ㄈㄤˋ", "ㄗㄞˋ", "ㄉㄤ", "ㄒㄧㄚˋ"]),
    ("今天也要保持專注", ["ㄐㄧㄣ", "ㄊㄧㄢ", "ㄧㄝˇ", "ㄧㄠˋ", "ㄅㄠˇ", "ㄔˊ", "ㄓㄨㄢ", "ㄓㄨˋ"]),
    ("一步一步慢慢熟悉", ["ㄧ", "ㄅㄨˋ", "ㄧ", "ㄅㄨˋ", "ㄇㄢˋ", "ㄇㄢˋ", "ㄕㄨˊ", "ㄒㄧˊ"]),
    ("不要讓手腕太過用力", ["ㄅㄨˋ", "ㄧㄠˋ", "ㄖㄤˋ", "ㄕㄡˇ", "ㄨㄢˇ", "ㄊㄞˋ", "ㄍㄨㄛˋ", "ㄩㄥˋ", "ㄌㄧˋ"]),
    ("先從簡單的字開始", ["ㄒㄧㄢ", "ㄘㄨㄥˊ", "ㄐㄧㄢˇ", "ㄉㄢ", "ㄉㄜ˙", "ㄗˋ", "ㄎㄞ", "ㄕˇ"]),
    ("讓節奏慢慢變得穩定", ["ㄖㄤˋ", "ㄐㄧㄝˊ", "ㄗㄡˋ", "ㄇㄢˋ", "ㄇㄢˋ", "ㄅㄧㄢˋ", "ㄉㄜ˙", "ㄨㄣˇ", "ㄉㄧㄥˋ"]),
    ("反覆練習會帶來進步", ["ㄈㄢˇ", "ㄈㄨˋ", "ㄌㄧㄢˋ", "ㄒㄧˊ", "ㄏㄨㄟˋ", "ㄉㄞˋ", "ㄌㄞˊ", "ㄐㄧㄣˋ", "ㄅㄨˋ"]),
    ("每天都給自己一點時間", ["ㄇㄟˇ", "ㄊㄧㄢ", "ㄉㄡ", "ㄍㄟˇ", "ㄗˋ", "ㄐㄧˇ", "ㄧ", "ㄉㄧㄢˇ", "ㄕˊ", "ㄐㄧㄢ"]),
    ("小小的改變會慢慢累積", ["ㄒㄧㄠˇ", "ㄒㄧㄠˇ", "ㄉㄜ˙", "ㄍㄞˇ", "ㄅㄧㄢˋ", "ㄏㄨㄟˋ", "ㄇㄢˋ", "ㄇㄢˋ", "ㄌㄟˇ", "ㄐㄧ"]),
    ("正確指法可以減少負擔", ["ㄓㄥˋ", "ㄑㄩㄝˋ", "ㄓˇ", "ㄈㄚˇ", "ㄎㄜˇ", "ㄧˇ", "ㄐㄧㄢˇ", "ㄕㄠˇ", "ㄈㄨˋ", "ㄉㄢ"]),
    ("打字時眼睛可以看前方", ["ㄉㄚˇ", "ㄗˋ", "ㄕˊ", "ㄧㄢˇ", "ㄐㄧㄥ", "ㄎㄜˇ", "ㄧˇ", "ㄎㄢˋ", "ㄑㄧㄢˊ", "ㄈㄤ"]),
    ("不要一直盯著鍵盤", ["ㄅㄨˋ", "ㄧㄠˋ", "ㄧ", "ㄓˊ", "ㄉㄧㄥ", "ㄓㄜ˙", "ㄐㄧㄢˋ", "ㄆㄢˊ"]),
    ("先找到自己的節奏", ["ㄒㄧㄢ", "ㄓㄠˇ", "ㄉㄠˋ", "ㄗˋ", "ㄐㄧˇ", "ㄉㄜ˙", "ㄐㄧㄝˊ", "ㄗㄡˋ"]),
    ("把每個字打得清楚", ["ㄅㄚˇ", "ㄇㄟˇ", "ㄍㄜˋ", "ㄗˋ", "ㄉㄚˇ", "ㄉㄜ˙", "ㄑㄧㄥ", "ㄔㄨˇ"]),
    ("工作完成後再休息", ["ㄍㄨㄥ", "ㄗㄨㄛˋ", "ㄨㄢˊ", "ㄔㄥˊ", "ㄏㄡˋ", "ㄗㄞˋ", "ㄒㄧㄡ", "ㄒㄧˊ"]),
    ("學會等待手指反應", ["ㄒㄩㄝˊ", "ㄏㄨㄟˋ", "ㄉㄥˇ", "ㄉㄞˋ", "ㄕㄡˇ", "ㄓˇ", "ㄈㄢˇ", "ㄧㄥˋ"]),
    ("輸入速度來自穩定", ["ㄕㄨ", "ㄖㄨˋ", "ㄙㄨˋ", "ㄉㄨˋ", "ㄌㄞˊ", "ㄗˋ", "ㄨㄣˇ", "ㄉㄧㄥˋ"]),
    ("練習可以從短句開始", ["ㄌㄧㄢˋ", "ㄒㄧˊ", "ㄎㄜˇ", "ㄧˇ", "ㄘㄨㄥˊ", "ㄉㄨㄢˇ", "ㄐㄩˋ", "ㄎㄞ", "ㄕˇ"]),
    ("留一點空間給自己", ["ㄌㄧㄡˊ", "ㄧ", "ㄉㄧㄢˇ", "ㄎㄨㄥ", "ㄐㄧㄢ", "ㄍㄟˇ", "ㄗˋ", "ㄐㄧˇ"]),
    ("注意每一個按鍵", ["ㄓㄨˋ", "ㄧˋ", "ㄇㄟˇ", "ㄧ", "ㄍㄜˋ", "ㄢˋ", "ㄐㄧㄢˋ"]),
    ("慢一點反而更準確", ["ㄇㄢˋ", "ㄧ", "ㄉㄧㄢˇ", "ㄈㄢˇ", "ㄦˊ", "ㄍㄥˋ", "ㄓㄨㄣˇ", "ㄑㄩㄝˋ"]),
    ("先練習再提高速度", ["ㄒㄧㄢ", "ㄌㄧㄢˋ", "ㄒㄧˊ", "ㄗㄞˋ", "ㄊㄧˊ", "ㄍㄠ", "ㄙㄨˋ", "ㄉㄨˋ"]),
    ("保持清醒也保持放鬆", ["ㄅㄠˇ", "ㄔˊ", "ㄑㄧㄥ", "ㄒㄧㄥˇ", "ㄧㄝˇ", "ㄅㄠˇ", "ㄔˊ", "ㄈㄤˋ", "ㄙㄨㄥ"]),
    ("熟練來自每天累積", ["ㄕㄨˊ", "ㄌㄧㄢˋ", "ㄌㄞˊ", "ㄗˋ", "ㄇㄟˇ", "ㄊㄧㄢ", "ㄌㄟˇ", "ㄐㄧ"]),
    ("每次輸入都值得專心", ["ㄇㄟˇ", "ㄘˋ", "ㄕㄨ", "ㄖㄨˋ", "ㄉㄡ", "ㄓˊ", "ㄉㄜ˙", "ㄓㄨㄢ", "ㄒㄧㄣ"]),
    ("鍵盤只是工具不是考試", ["ㄐㄧㄢˋ", "ㄆㄢˊ", "ㄓˇ", "ㄕˋ", "ㄍㄨㄥ", "ㄐㄩˋ", "ㄅㄨˋ", "ㄕˋ", "ㄎㄠˇ", "ㄕˋ"]),
    ("一個字一個字練習", ["ㄧ", "ㄍㄜˋ", "ㄗˋ", "ㄧ", "ㄍㄜˋ", "ㄗˋ", "ㄌㄧㄢˋ", "ㄒㄧˊ"]),
    ("讓手指記住新路徑", ["ㄖㄤˋ", "ㄕㄡˇ", "ㄓˇ", "ㄐㄧˋ", "ㄓㄨˋ", "ㄒㄧㄣ", "ㄌㄨˋ", "ㄐㄧㄥˋ"]),
    ("小心處理每個錯字", ["ㄒㄧㄠˇ", "ㄒㄧㄣ", "ㄔㄨˇ", "ㄌㄧˇ", "ㄇㄟˇ", "ㄍㄜˋ", "ㄘㄨㄛˋ", "ㄗˋ"]),
    ("清楚的目標讓人專注", ["ㄑㄧㄥ", "ㄔㄨˇ", "ㄉㄜ˙", "ㄇㄨˋ", "ㄅㄧㄠ", "ㄖㄤˋ", "ㄖㄣˊ", "ㄓㄨㄢ", "ㄓㄨˋ"]),
    ("簡單開始持續練習", ["ㄐㄧㄢˇ", "ㄉㄢ", "ㄎㄞ", "ㄕˇ", "ㄔˊ", "ㄒㄩˋ", "ㄌㄧㄢˋ", "ㄒㄧˊ"]),
    ("學習新的鍵位組合", ["ㄒㄩㄝˊ", "ㄒㄧˊ", "ㄒㄧㄣ", "ㄉㄜ˙", "ㄐㄧㄢˋ", "ㄨㄟˋ", "ㄗㄨˇ", "ㄏㄜˊ"]),
    ("每天用幾分鐘練習", ["ㄇㄟˇ", "ㄊㄧㄢ", "ㄩㄥˋ", "ㄐㄧˇ", "ㄈㄣ", "ㄓㄨㄥ", "ㄌㄧㄢˋ", "ㄒㄧˊ"]),
    ("先讓肩膀保持放鬆", ["ㄒㄧㄢ", "ㄖㄤˋ", "ㄐㄧㄢ", "ㄅㄤˇ", "ㄅㄠˇ", "ㄔˊ", "ㄈㄤˋ", "ㄙㄨㄥ"]),
    ("清楚感覺每次按鍵", ["ㄑㄧㄥ", "ㄔㄨˇ", "ㄍㄢˇ", "ㄐㄩㄝˊ", "ㄇㄟˇ", "ㄘˋ", "ㄢˋ", "ㄐㄧㄢˋ"]),
    ("從容地完成每個音節", ["ㄘㄨㄥˊ", "ㄖㄨㄥˊ", "ㄉㄜ˙", "ㄨㄢˊ", "ㄔㄥˊ", "ㄇㄟˇ", "ㄍㄜˋ", "ㄧㄣ", "ㄐㄧㄝˊ"]),
    ("注音鍵位需要熟悉", ["ㄓㄨˋ", "ㄧㄣ", "ㄐㄧㄢˋ", "ㄨㄟˋ", "ㄒㄩ", "ㄧㄠˋ", "ㄕㄨˊ", "ㄒㄧˊ"]),
]
ZHUYIN_SAMPLES.extend(GENERATED_ZHUYIN_SAMPLES)


ENGLISH_FRAGMENTS = [
    "keep your hands quiet and let each key arrive under the right finger",
    "small pauses are enough to make room for a careful practice session",
    "steady movement is more useful than rushing toward a faster number",
    "the keyboard becomes familiar when every letter has a place to land",
    "return to the home row and let your hands learn the shape of the work",
    "a clear rhythm starts with a light touch and a relaxed wrist",
    "practice one clean phrase, then allow the next phrase to appear",
    "good typing feels quiet because the fingers already know where to go",
    "when the workday gives you a minute, use it to build a little ease",
    "look ahead, breathe once, and keep the movement smaller than the thought",
    "clean keystrokes are easier to repeat than hurried corrections",
    "let the left hand stay calm while the right hand finds its place",
    "a short focused session can change how the whole keyboard feels",
    "make room for accuracy by giving each letter enough attention",
    "your wrists can stay loose while the fingers do the precise work",
    "begin with the home row and travel outward only when needed",
    "a slower rhythm today can become a smoother rhythm tomorrow",
    "use the space between words as a quiet reset for both hands",
    "the best practice is patient enough to notice small habits",
    "every familiar phrase started as a sequence of separate keys",
    "keep your shoulders down and let the hands move from the fingers",
    "a steady gaze helps the next letter arrive before the current one ends",
    "type the thought in front of you and leave the result for later",
    "simple words are useful when they reveal an uneven movement",
    "the next key is easier to find when the current key is released",
    "give difficult letters a little time instead of forcing them",
    "a light touch leaves more energy for the rest of the sentence",
    "consistent spacing makes a paragraph easier to read and easier to type",
    "your hands do not need to hurry to learn a new route",
    "repeat the motion carefully until it begins to feel ordinary",
    "a quiet desk is a good place to listen to the rhythm of typing",
    "small improvements become visible when the practice is regular",
    "let each word finish before the hands search for the next one",
    "use short breaks to build comfort rather than chase a score",
    "familiar keys can still teach something when the pace stays gentle",
    "a relaxed hand is ready to move in any direction",
    "the middle of the keyboard is a useful place to return",
    "clear attention makes even a common sentence worth practicing",
    "keep the thumb near the space bar and the fingers near home",
    "the hands learn patterns when the mind gives them enough time",
    "typing well is a collection of small decisions made in sequence",
    "a good rhythm has room for both speed and control",
    "notice where the hand wants to drift and guide it back",
    "every correct release prepares the finger for another clean press",
    "the keyboard is a map that becomes clearer with each visit",
    "use a soft landing for letters and a patient lift between words",
    "practice can fit inside a minute when the task is already waiting",
    "a careful beginning often saves time later in the sentence",
    "keep the next phrase visible and let the current word stay simple",
    "a balanced posture gives the hands more freedom to work",
    "slow typing is still progress when the movement is intentional",
    "learn the shape of a word through its keys rather than its outline",
    "a small correction now can prevent a stubborn habit later",
    "leave enough space for thought between one phrase and the next",
    "the hands become reliable when the same route is practiced calmly",
    "start again from the home row whenever the pattern feels lost",
    "a focused minute can make a busy afternoon feel more manageable",
    "let the letters pass through the hands without extra force",
    "good practice keeps the goal close and the pressure low",
    "type with curiosity and notice which keys feel less familiar",
    "each sentence offers another chance to make the movement smaller",
    "a calm pace gives the fingers time to choose the next key",
    "the easiest route is usually the one you can repeat without strain",
    "finish the phrase with the same care used to begin it",
    "a keyboard habit improves when the body stays comfortable",
    "keep the eyes moving forward and allow the hands to follow",
    "careful repetition turns a difficult combination into a normal one",
    "there is value in practicing words that rarely appear together",
    "make each press deliberate and each release quiet",
    "a little structure makes spare moments easier to use",
    "the goal is not to force speed but to remove unnecessary motion",
    "patient hands can learn more in a short session than rushed hands",
    "when a phrase feels awkward reduce the pace and keep going",
    "your best rhythm may be quieter than you expect",
    "familiar movement is built from many ordinary repetitions",
    "return to the same calm starting point whenever you need it",
    "every minute of deliberate practice gives the hands more options",
    "let the sentence guide the hands without asking them to leap",
    "a clean sequence is worth more than a fast but fragile one",
    "type one word well and let that care spread to the next",
    "the keyboard rewards attention to small details",
    "keep practicing until the correct path feels like the easy path",
]
ENGLISH_FRAGMENTS.extend(GENERATED_ENGLISH_FRAGMENTS)


KEYSYM_TO_CODE = {
    "space": "Space", "comma": "Comma", "period": "Period", "slash": "Slash", "minus": "Minus", "equal": "Equal",
    "bracketleft": "BracketLeft", "bracketright": "BracketRight", "backslash": "Backslash", "semicolon": "Semicolon",
    "apostrophe": "Quote", "grave": "Backquote", "tab": "Tab", "caps_lock": "CapsLock", "return": "Enter",
    "backspace": "Backspace", "shift_l": "ShiftLeft", "shift_r": "ShiftRight", "control_l": "ControlLeft", "control_r": "ControlRight",
    "alt_l": "AltLeft", "alt_r": "AltRight",
}

class TypingLabApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.settings_path = self._settings_path()
        self.settings = self._load_settings()
        self.mode = "zhuyin" if self.settings.get("mode") == "zhuyin" else "english"
        self.total_typed_by_mode = self._load_mode_totals(
            self.settings.get("total_typed_by_mode"),
            self._nonnegative_int(self.settings.get("total_typed", 0)),
        )
        self.daily_typed_by_mode = self._load_mode_daily_typed(
            self.settings.get("daily_typed_by_mode"),
            self._load_daily_typed(self.settings.get("daily_typed", {})),
        )

        self.target = ""
        self.index = 0
        self.zhuyin_units: list[dict] = []
        self.zhuyin_stream: list[dict] = []
        self.zhuyin_characters: list[dict] = []
        self.zhuyin_char_index = 0
        self.zhuyin_key_index = 0
        self.english_queue: list[str] = []
        self.zhuyin_queue: list[tuple[str, list[str]]] = []
        self.last_english_fragment: str | None = None
        self.last_zhuyin_text: str | None = None

        self.typed = 0
        self.feedback = ""
        self.feedback_kind = "idle"
        self.settings_window: tk.Toplevel | None = None
        self.save_after_id: str | None = None
        self.heatmap_tooltip: tk.Toplevel | None = None
        self.key_items: dict[str, tuple[int, int, int]] = {}
        self.wrong_code: str | None = None
        self.wrong_after_id: str | None = None

        self._configure_root()
        self._build_ui()
        self._reset_practice(focus=False)
        self.root.bind_all("<KeyPress>", self._handle_key, add="+")

    @staticmethod
    def _settings_path() -> Path:
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "TypingLab" / "settings.json"

    def _load_settings(self) -> dict:
        try:
            return json.loads(self.settings_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}

    @staticmethod
    def _nonnegative_int(value: object) -> int:
        try:
            return max(0, int(value))
        except (TypeError, ValueError):
            return 0

    def _load_daily_typed(self, value: object) -> dict[str, int]:
        if not isinstance(value, dict):
            return {}
        result: dict[str, int] = {}
        for day, count in value.items():
            if isinstance(day, str) and len(day) == 10:
                result[day] = self._nonnegative_int(count)
        return result

    def _load_mode_totals(self, value: object, legacy_total: int) -> dict[str, int]:
        result = {"english": 0, "zhuyin": 0}
        if isinstance(value, dict):
            for mode in result:
                result[mode] = self._nonnegative_int(value.get(mode, 0))
        else:
            result[self.mode] = legacy_total
        return result

    def _load_mode_daily_typed(self, value: object, legacy_daily: dict[str, int]) -> dict[str, dict[str, int]]:
        result = {"english": {}, "zhuyin": {}}
        if isinstance(value, dict):
            for mode in result:
                result[mode] = self._load_daily_typed(value.get(mode, {}))
        else:
            result[self.mode] = legacy_daily
        return result

    def _current_daily_typed(self) -> dict[str, int]:
        return self.daily_typed_by_mode[self.mode]

    def _save_settings(self) -> None:
        try:
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)
            combined_daily: dict[str, int] = {}
            for daily in self.daily_typed_by_mode.values():
                for day, count in daily.items():
                    combined_daily[day] = combined_daily.get(day, 0) + count
            self.settings_path.write_text(json.dumps({
                "mode": self.mode,
                "total_typed": sum(self.total_typed_by_mode.values()),
                "daily_typed": combined_daily,
                "total_typed_by_mode": self.total_typed_by_mode,
                "daily_typed_by_mode": self.daily_typed_by_mode,
            }, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass

    def _schedule_save_settings(self) -> None:
        if self.save_after_id:
            self.root.after_cancel(self.save_after_id)
        self.save_after_id = self.root.after(500, self._flush_scheduled_save)

    def _flush_scheduled_save(self) -> None:
        self.save_after_id = None
        self._save_settings()

    @staticmethod
    def _local_today() -> date:
        return datetime.now().astimezone().date()

    def _record_typed_character(self) -> None:
        self.typed += 1
        self.total_typed_by_mode[self.mode] += 1
        day = self._local_today().isoformat()
        daily_typed = self._current_daily_typed()
        daily_typed[day] = daily_typed.get(day, 0) + 1
        self._schedule_save_settings()

    def _configure_root(self) -> None:
        self.root.title("Typing Lab")
        self.root.geometry("800x600")
        self.root.minsize(720, 520)
        self.root.configure(bg=COLORS["bg"])
        self.root.option_add("*Font", ("Segoe UI", 9))
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def _frame(self, parent: tk.Misc, **kwargs) -> tk.Frame:
        return tk.Frame(parent, bg=kwargs.pop("bg", COLORS["surface"]), **kwargs)

    def _border_frame(self, parent: tk.Misc, bg: str = "surface", **kwargs) -> tk.Frame:
        return tk.Frame(parent, bg=COLORS[bg], highlightbackground=COLORS["line"], highlightthickness=1, bd=0, **kwargs)

    def _label(self, parent: tk.Misc, text: str = "", **kwargs) -> tk.Label:
        return tk.Label(parent, text=text, bg=kwargs.pop("bg", parent.cget("bg")), fg=kwargs.pop("fg", COLORS["text"]), **kwargs)

    def _button(self, parent: tk.Misc, text: str, command, **kwargs) -> tk.Button:
        bg = kwargs.pop("bg", COLORS["surface"])
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=kwargs.pop("fg", COLORS["muted"]),
            activebackground=kwargs.pop("activebackground", COLORS["soft"]),
            activeforeground=kwargs.pop("activeforeground", COLORS["text"]),
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2",
            **kwargs,
        )

    def _build_ui(self) -> None:
        self._build_topbar()

        workspace = self._frame(self.root, bg=COLORS["bg"])
        workspace.pack(fill="both", expand=True, padx=14, pady=(14, 10))
        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_columnconfigure(1, weight=0, minsize=184)
        workspace.grid_rowconfigure(0, weight=1)

        practice = self._frame(workspace, bg=COLORS["bg"])
        practice.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        practice.grid_rowconfigure(1, weight=1)
        practice.grid_columnconfigure(0, weight=1)
        self._build_practice(practice)

        side = self._frame(workspace, bg=COLORS["bg"], width=184)
        side.grid(row=0, column=1, sticky="nsew")
        side.grid_propagate(False)
        side.grid_columnconfigure(0, weight=1)
        side.grid_rowconfigure(1, weight=1)
        self._build_side_panel(side)

    def _build_topbar(self) -> None:
        topbar = self._frame(self.root, bg=COLORS["bg"], height=64)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        brand = self._frame(topbar, bg=COLORS["bg"])
        brand.pack(side="left", padx=(20, 0), fill="y")
        mark = tk.Canvas(brand, width=18, height=18, bg=COLORS["bg"], highlightthickness=0)
        mark.pack(side="left", pady=22, padx=(0, 10))
        for x, y, fill in [(3, 3, COLORS["accent"]), (9, 3, COLORS["accent"]), (3, 9, COLORS["accent"]), (9, 9, COLORS["muted_deep"])]:
            mark.create_rectangle(x, y, x + 4, y + 4, fill=fill, outline="")
        self._label(brand, "Typing Lab", bg=COLORS["bg"], fg=COLORS["text"], font=("Cascadia Mono", 11, "bold")).pack(side="left", pady=22)

        actions = self._frame(topbar, bg=COLORS["bg"])
        actions.pack(side="right", padx=(0, 18), pady=17)
        switch = self._border_frame(actions, bg="surface")
        switch.pack(side="left", padx=(0, 9))
        self.english_button = self._button(switch, "  英文  ", lambda: self._set_mode("english"), font=FONT_UI_SMALL, padx=6, pady=5)
        self.english_button.pack(side="left")
        self.zhuyin_button = self._button(switch, "  注音  ", lambda: self._set_mode("zhuyin"), font=FONT_UI_SMALL, padx=6, pady=5)
        self.zhuyin_button.pack(side="left")
        self.settings_button = self._button(actions, "SET", self._toggle_settings, bg=COLORS["bg"], fg=COLORS["muted"], font=FONT_MONO_SMALL, padx=7, pady=6)
        self.settings_button.pack(side="left")

    def _build_practice(self, parent: tk.Frame) -> None:
        header = self._frame(parent, bg=COLORS["bg"], height=38)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        self.mode_kicker = self._label(header, "", bg=COLORS["bg"], fg=COLORS["muted"], font=FONT_MONO_SMALL, anchor="w")
        self.mode_kicker.pack(anchor="w")

        self.prompt_card = self._border_frame(parent, bg="surface")
        self.prompt_card.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.prompt_card.grid_rowconfigure(1, weight=1)
        self.prompt_card.grid_columnconfigure(0, weight=1)

        topline = self._frame(self.prompt_card, bg=COLORS["surface"])
        topline.grid(row=0, column=0, sticky="ew", padx=18, pady=(11, 0))
        topline.grid_columnconfigure(0, weight=1)
        self.prompt_caption = self._label(topline, "", bg=COLORS["surface"], fg=COLORS["muted_deep"], font=FONT_MONO_SMALL, anchor="w")
        self.prompt_caption.grid(row=0, column=0, sticky="w")
        self._label(topline, "∞", bg=COLORS["surface"], fg=COLORS["accent"], font=("Georgia", 15), anchor="e").grid(row=0, column=1, sticky="e")

        self.prompt_text = tk.Text(
            self.prompt_card,
            height=3,
            wrap="word",
            state="disabled",
            relief="flat",
            borderwidth=0,
            bg=COLORS["surface"],
            fg=COLORS["muted_deep"],
            insertbackground=COLORS["accent"],
            font=("Cascadia Mono", 18),
            padx=20,
            pady=19,
            cursor="arrow",
            spacing1=3,
            spacing3=3,
        )
        self.prompt_text.grid(row=1, column=0, sticky="nsew")
        self.prompt_text.tag_configure("typed", foreground=COLORS["text_soft"])
        self.prompt_text.tag_configure("future", foreground=COLORS["muted_deep"])
        self.prompt_text.tag_configure("current", foreground=COLORS["text"], background=COLORS["accent_soft"], underline=True)
        self.prompt_text.tag_configure("current_space", foreground=COLORS["accent"], background=COLORS["accent_soft"], underline=True)
        self.prompt_text.tag_configure("zh_typed", foreground=COLORS["text_soft"])
        self.prompt_text.tag_configure("zh_current", foreground=COLORS["text"], background=COLORS["right_soft"])
        self.prompt_text.tag_configure("zh_future", foreground=COLORS["muted_deep"])

        self.zhuyin_guide = self._border_frame(self.prompt_card, bg="raised")
        self.zhuyin_guide.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 14))
        self.zhuyin_guide.grid_columnconfigure(1, weight=1)
        self._label(self.zhuyin_guide, "注音序列", bg=COLORS["raised"], fg=COLORS["muted"], font=FONT_UI_SMALL).grid(row=0, column=0, rowspan=2, padx=(9, 10), pady=7)
        self.guide_symbols = self._frame(self.zhuyin_guide, bg=COLORS["raised"])
        self.guide_symbols.grid(row=0, column=1, sticky="w", padx=(0, 7), pady=(6, 0))
        self.guide_keys = self._frame(self.zhuyin_guide, bg=COLORS["raised"])
        self.guide_keys.grid(row=1, column=1, sticky="w", padx=(0, 7), pady=(0, 6))

        focus = self._frame(parent, bg=COLORS["bg"], height=34)
        focus.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        focus.grid_columnconfigure(0, weight=1)
        focus.grid_columnconfigure(1, weight=0)
        readout = self._frame(focus, bg=COLORS["bg"])
        readout.grid(row=0, column=0, sticky="w")
        self._label(readout, "目前按鍵", bg=COLORS["bg"], fg=COLORS["muted"], font=FONT_UI_SMALL).pack(side="left", padx=(0, 8))
        self.current_key = self._label(readout, "—", bg=COLORS["accent_soft"], fg=COLORS["text"], font=("Cascadia Mono", 11, "bold"), width=5, pady=4)
        self.current_key.pack(side="left", padx=(0, 8))
        self.finger_name = self._label(readout, "", bg=COLORS["bg"], fg=COLORS["text_soft"], font=FONT_UI_SMALL)
        self.finger_name.pack(side="left", padx=(0, 8))
        self.hand_name = self._label(readout, "", bg=COLORS["bg"], fg=COLORS["muted"], font=FONT_MONO_SMALL)
        self.hand_name.pack(side="left")
        self.feedback_label = self._label(focus, "", bg=COLORS["bg"], fg=COLORS["muted"], font=FONT_MONO_SMALL, anchor="e")
        self.feedback_label.grid(row=0, column=1, sticky="e")

        keyboard_card = self._border_frame(parent, bg="surface")
        keyboard_card.grid(row=3, column=0, sticky="ew")
        keyboard_card.grid_columnconfigure(0, weight=1)
        keyboard_top = self._frame(keyboard_card, bg=COLORS["surface"])
        keyboard_top.grid(row=0, column=0, sticky="ew", padx=11, pady=(9, 3))
        keyboard_top.grid_columnconfigure(0, weight=1)
        self._label(keyboard_top, "鍵盤指法", bg=COLORS["surface"], fg=COLORS["text_soft"], font=FONT_MONO_SMALL, anchor="w").grid(row=0, column=0, sticky="w")
        self.keyboard_note = self._label(keyboard_top, "", bg=COLORS["surface"], fg=COLORS["muted_deep"], font=FONT_UI_SMALL, anchor="e")
        self.keyboard_note.grid(row=0, column=1, sticky="e")
        self.keyboard_canvas = tk.Canvas(keyboard_card, height=132, bg=COLORS["surface"], highlightthickness=0)
        self.keyboard_canvas.grid(row=1, column=0, sticky="ew", padx=10)
        self.keyboard_canvas.bind("<Configure>", lambda _event: self._draw_keyboard())
        legend = self._frame(keyboard_card, bg=COLORS["surface"])
        legend.grid(row=2, column=0, sticky="e", padx=11, pady=(1, 7))
        for color, text in [(COLORS["left"], "左手"), (COLORS["right"], "右手"), (COLORS["thumb"], "拇指")]:
            dot = tk.Canvas(legend, width=6, height=6, bg=COLORS["surface"], highlightthickness=0)
            dot.create_oval(1, 1, 5, 5, fill=color, outline="")
            dot.pack(side="left", padx=(9, 4))
            self._label(legend, text, bg=COLORS["surface"], fg=COLORS["muted"], font=FONT_UI_SMALL).pack(side="left")

    def _build_side_panel(self, parent: tk.Frame) -> None:
        session = self._border_frame(parent, bg="surface")
        session.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        self._side_heading(session, "練習狀態", "IDLE").pack(fill="x", padx=12, pady=(11, 0))
        self.typed_stat = self._label(session, "0", bg=COLORS["surface"], fg=COLORS["text"], font=("Cascadia Mono", 30), anchor="w")
        self.typed_stat.pack(anchor="w", padx=12, pady=(12, 0))
        self.typed_stat_label = self._label(session, "累計字數", bg=COLORS["surface"], fg=COLORS["muted"], font=FONT_UI_SMALL, anchor="w")
        self.typed_stat_label.pack(anchor="w", padx=12, pady=(3, 10))
        tk.Frame(session, height=1, bg=COLORS["line"]).pack(fill="x", padx=12)
        self.mode_stat = self._stat_row(session, "輸入模式")

        heatmap = self._border_frame(parent, bg="surface")
        heatmap.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        heatmap.grid_rowconfigure(1, weight=1)
        heatmap.grid_columnconfigure(0, weight=1)
        self.heatmap_title = self._label(heatmap, "每日練習", bg=COLORS["surface"], fg=COLORS["text_soft"], font=("Segoe UI", 9, "bold"), anchor="w")
        self.heatmap_title.grid(
            row=0, column=0, sticky="w", padx=12, pady=(11, 0)
        )
        self.heatmap_canvas = tk.Canvas(heatmap, height=190, bg=COLORS["surface"], highlightthickness=0)
        self.heatmap_canvas.grid(row=1, column=0, sticky="nsew", padx=8, pady=(5, 9))
        self.heatmap_canvas.bind("<Configure>", lambda _event: self._draw_heatmap())

        finger = self._frame(parent, bg=COLORS["bg"])
        finger.grid(row=2, column=0, sticky="se", pady=(0, 2))
        finger_line = self._frame(finger, bg=COLORS["bg"])
        finger_line.pack(anchor="e")
        self._label(finger_line, "目前指法", bg=COLORS["bg"], fg=COLORS["muted"], font=FONT_UI_SMALL).pack(side="left", padx=(0, 6))
        self.finger_orb = tk.Canvas(finger_line, width=34, height=34, bg=COLORS["bg"], highlightthickness=0)
        self.finger_orb.pack(side="left", padx=(0, 5))
        self.finger_orb_label = self._label(finger_line, "", bg=COLORS["bg"], fg=COLORS["text_soft"], font=FONT_UI_SMALL)
        self.finger_orb_label.pack(side="left")
        self.finger_status = self._label(finger_line, "GUIDE", bg=COLORS["bg"], fg=COLORS["muted_deep"], font=FONT_MONO_SMALL)
        self.finger_status.pack(side="left", padx=(6, 0))

    def _side_heading(self, parent: tk.Misc, title: str, status: str) -> tk.Frame:
        row = self._frame(parent, bg=COLORS["surface"])
        row.grid_columnconfigure(0, weight=1)
        self._label(row, title, bg=COLORS["surface"], fg=COLORS["text_soft"], font=("Segoe UI", 9, "bold"), anchor="w").grid(row=0, column=0, sticky="w")
        label = self._label(row, status, bg=COLORS["surface"], fg=COLORS["muted_deep"], font=FONT_MONO_SMALL, anchor="e")
        label.grid(row=0, column=1, sticky="e")
        if title == "練習狀態":
            self.session_status = label
        else:
            self.finger_status = label
        return row

    def _stat_row(self, parent: tk.Misc, label: str) -> tk.Label:
        row = self._frame(parent, bg=COLORS["surface"])
        row.pack(fill="x", padx=12, pady=(5, 0))
        self._label(row, label, bg=COLORS["surface"], fg=COLORS["muted"], font=FONT_UI_SMALL, anchor="w").pack(side="left")
        value = self._label(row, "0", bg=COLORS["surface"], fg=COLORS["text_soft"], font=FONT_MONO_SMALL, anchor="e")
        value.pack(side="right")
        return value

    def _draw_heatmap(self) -> None:
        canvas = getattr(self, "heatmap_canvas", None)
        if canvas is None or not canvas.winfo_exists():
            return
        self._hide_heatmap_tooltip()
        canvas.delete("all")

        columns = 7
        gap = 3
        width = max(canvas.winfo_width(), 166)
        height = max(canvas.winfo_height(), 190)
        cell = min(13, max(7, (width - 22 - gap * (columns - 1)) // columns))
        rows = max(1, (height - 16 + gap) // (cell + gap))
        total_width = columns * cell + (columns - 1) * gap
        total_height = rows * cell + (rows - 1) * gap
        start_x = max(7, (width - total_width) // 2)
        start_y = max(8, (height - total_height) // 2)

        today = self._local_today()
        current_week_start = today - timedelta(days=(today.weekday() + 1) % 7)
        first_week_start = current_week_start - timedelta(weeks=rows - 1)
        days = [first_week_start + timedelta(days=week * 7 + weekday) for week in range(rows) for weekday in range(columns)]
        daily_typed = self._current_daily_typed()
        max_count = max((daily_typed.get(day.isoformat(), 0) for day in days if day <= today), default=0)
        heat_colors = [COLORS["raised"], COLORS["accent_soft"], "#403866", "#6658a5", COLORS["accent"]]

        for index, day in enumerate(days):
            week, weekday = divmod(index, columns)
            x1 = start_x + weekday * (cell + gap)
            y1 = start_y + week * (cell + gap)
            count = daily_typed.get(day.isoformat(), 0)
            if day > today:
                color = COLORS["surface"]
            elif count <= 0 or max_count <= 0:
                color = heat_colors[0]
            else:
                level = min(4, max(1, int(count / max_count * 4)))
                color = heat_colors[level]
            item = canvas.create_rectangle(x1, y1, x1 + cell, y1 + cell, fill=color, outline="")
            if day <= today:
                canvas.tag_bind(item, "<Enter>", lambda event, day=day, count=count: self._show_heatmap_tooltip(event, day, count))
                canvas.tag_bind(item, "<Leave>", lambda _event: self._hide_heatmap_tooltip())

    def _show_heatmap_tooltip(self, event: tk.Event, day, count: int) -> None:
        self._hide_heatmap_tooltip()
        tooltip = tk.Toplevel(self.root)
        tooltip.overrideredirect(True)
        tooltip.configure(bg=COLORS["line"])
        self._label(
            tooltip,
            f"{day.isoformat()}\n{count} 字",
            bg=COLORS["line"],
            fg=COLORS["text"],
            font=FONT_MONO_SMALL,
            justify="center",
            padx=8,
            pady=5,
        ).pack()
        tooltip.update_idletasks()
        tooltip.geometry(f"+{event.x_root + 12}+{event.y_root + 12}")
        self.heatmap_tooltip = tooltip

    def _hide_heatmap_tooltip(self) -> None:
        if self.heatmap_tooltip is not None:
            self.heatmap_tooltip.destroy()
            self.heatmap_tooltip = None

    def _set_mode(self, mode: str) -> None:
        if self.mode == mode:
            return
        self.mode = mode
        self._save_settings()
        self._reset_practice()

    def _reset_practice(self, focus: bool = True) -> None:
        self.index = 0
        self.zhuyin_units = []
        self.zhuyin_stream = []
        self.zhuyin_characters = []
        self.zhuyin_char_index = 0
        self.zhuyin_key_index = 0
        self.english_queue = []
        self.zhuyin_queue = []
        self.last_english_fragment = None
        self.last_zhuyin_text = None
        self.typed = 0
        self.feedback = ""
        self.feedback_kind = "idle"
        self.wrong_code = None
        if self.wrong_after_id:
            self.root.after_cancel(self.wrong_after_id)
            self.wrong_after_id = None

        if self.mode == "english":
            self.target = ""
            self._ensure_english_buffer()
        else:
            self._ensure_zhuyin_buffer()

        self._render()
        if focus:
            self.root.focus_force()

    def _ensure_english_buffer(self) -> None:
        while len(self.target) < self.index + 540:
            fragment = self._next_english_fragment()
            self.target += (" " if self.target else "") + fragment

    def _next_english_fragment(self) -> str:
        if not self.english_queue:
            self.english_queue = list(dict.fromkeys(ENGLISH_FRAGMENTS))
            random.shuffle(self.english_queue)
            if len(self.english_queue) > 1 and self.english_queue[-1] == self.last_english_fragment:
                self.english_queue[0], self.english_queue[-1] = self.english_queue[-1], self.english_queue[0]
        fragment = self.english_queue.pop()
        self.last_english_fragment = fragment
        return fragment

    def _append_zhuyin_unit(self) -> None:
        text, syllables = self._next_zhuyin_sample()
        unit_index = len(self.zhuyin_units)
        unit = {"text": text, "syllables": syllables, "unit_index": unit_index}
        self.zhuyin_units.append(unit)
        for syllable_index, syllable in enumerate(syllables):
            tokens: list[dict] = []
            for symbol in syllable:
                mapping = ZHUYIN_TO_KEY.get(symbol)
                if not mapping:
                    continue
                display, code = mapping
                token = {
                    "code": code,
                    "display": display,
                    "symbol": symbol,
                    "unit_index": unit_index,
                    "syllable_index": syllable_index,
                    "commit": symbol in TONE_SYMBOLS,
                }
                tokens.append(token)
                self.zhuyin_stream.append(token)
            if not any(symbol in TONE_SYMBOLS for symbol in syllable):
                commit_token = {
                    "code": "Space",
                    "display": "SPACE",
                    "symbol": "一聲",
                    "unit_index": unit_index,
                    "syllable_index": syllable_index,
                    "commit": True,
                }
                tokens.append(commit_token)
                self.zhuyin_stream.append(commit_token)
            character = text[syllable_index] if syllable_index < len(text) else ""
            self.zhuyin_characters.append({
                "character": character,
                "unit_index": unit_index,
                "syllable_index": syllable_index,
                "tokens": tokens,
            })

    def _next_zhuyin_sample(self) -> tuple[str, list[str]]:
        if not self.zhuyin_queue:
            seen: set[str] = set()
            self.zhuyin_queue = []
            for text, syllables in ZHUYIN_SAMPLES:
                if text in seen:
                    continue
                seen.add(text)
                self.zhuyin_queue.append((text, list(syllables)))
            random.shuffle(self.zhuyin_queue)
            if len(self.zhuyin_queue) > 1 and self.zhuyin_queue[-1][0] == self.last_zhuyin_text:
                self.zhuyin_queue[0], self.zhuyin_queue[-1] = self.zhuyin_queue[-1], self.zhuyin_queue[0]
        text, syllables = self.zhuyin_queue.pop()
        self.last_zhuyin_text = text
        return text, syllables

    def _ensure_zhuyin_buffer(self) -> None:
        while len(self.zhuyin_characters) < self.zhuyin_char_index + 32:
            self._append_zhuyin_unit()

    def _current_zhuyin_character(self) -> dict | None:
        self._ensure_zhuyin_buffer()
        if self.zhuyin_char_index >= len(self.zhuyin_characters):
            return None
        return self.zhuyin_characters[self.zhuyin_char_index]

    def _current_zhuyin_token(self) -> dict | None:
        character = self._current_zhuyin_character()
        if not character or not character["tokens"]:
            return None
        position = min(self.zhuyin_key_index, len(character["tokens"]) - 1)
        token = character["tokens"][position]
        return {**token, "character": character["character"], "finger": FINGER_MAP.get(token["code"])}

    def _current_token(self) -> dict | None:
        if self.mode == "english":
            self._ensure_english_buffer()
            character = self.target[self.index]
            code = self._english_code(character)
            return {"code": code, "display": "SPACE" if character == " " else character.upper(), "raw": character, "finger": FINGER_MAP.get(code)}
        return self._current_zhuyin_token()

    @staticmethod
    def _english_code(character: str) -> str:
        if character == " ":
            return "Space"
        if character in string.ascii_lowercase:
            return f"Key{character.upper()}"
        return {
            ",": "Comma", ".": "Period", "'": "Quote", ";": "Semicolon", "/": "Slash", "-": "Minus",
            "=": "Equal", "[": "BracketLeft", "]": "BracketRight", "\\": "Backslash",
        }.get(character, "")

    def _render(self) -> None:
        is_zhuyin = self.mode == "zhuyin"
        self.english_button.configure(bg=COLORS["soft"] if not is_zhuyin else COLORS["surface"], fg=COLORS["text"] if not is_zhuyin else COLORS["muted"])
        self.zhuyin_button.configure(bg=COLORS["soft"] if is_zhuyin else COLORS["surface"], fg=COLORS["text"] if is_zhuyin else COLORS["muted"])
        self.mode_kicker.configure(text="ZHUYIN / ENG 鍵盤" if is_zhuyin else "ENGLISH / QWERTY")
        self.prompt_caption.configure(text="中文字句" if is_zhuyin else "")
        self.keyboard_note.configure(text="大千注音鍵位" if is_zhuyin else "QWERTY 鍵位")
        mode_name = "中文" if is_zhuyin else "英文"
        self.mode_stat.configure(text=mode_name)
        self.typed_stat_label.configure(text=f"{mode_name}累計字數")
        self.heatmap_title.configure(text=f"{mode_name}每日練習")
        if is_zhuyin:
            self._render_zhuyin_prompt()
        else:
            self._render_english_prompt()
        current = self._current_token()
        self._render_focus(current)
        self._render_keyboard(current)
        self.typed_stat.configure(text=str(self.total_typed_by_mode[self.mode]))
        self._draw_heatmap()
        status = "ACTIVE" if self.typed else "IDLE"
        self.session_status.configure(text=status, fg=COLORS["left"] if self.typed else COLORS["muted_deep"])
        self.finger_status.configure(text="GUIDE")
        self.feedback_label.configure(text=self.feedback, fg=COLORS["error"] if self.feedback_kind == "error" else COLORS["muted"])

    def _render_english_prompt(self) -> None:
        self.zhuyin_guide.grid_remove()
        self.prompt_text.configure(state="normal")
        self.prompt_text.delete("1.0", "end")
        start = max(0, self.index - 5)
        end = min(len(self.target), self.index + 78)
        for position in range(start, end):
            character = self.target[position]
            display = "·" if character == " " else character
            if position < self.index:
                tag = "typed"
            elif position == self.index:
                tag = "current_space" if character == " " else "current"
            else:
                tag = "future"
            self.prompt_text.insert("end", display, tag)
        self.prompt_text.configure(state="disabled")

    def _render_zhuyin_prompt(self) -> None:
        self.zhuyin_guide.grid()
        current = self._current_zhuyin_character()
        unit_index = current.get("unit_index", 0) if current else 0
        self.prompt_text.configure(state="normal")
        self.prompt_text.delete("1.0", "end")
        start = max(0, unit_index - 1)
        end = min(len(self.zhuyin_units), unit_index + 7)
        for position in range(start, end):
            unit = self.zhuyin_units[position]
            tag = "zh_typed" if position < unit_index else "zh_current" if position == unit_index else "zh_future"
            self.prompt_text.insert("end", unit["text"], tag)
        self.prompt_text.configure(state="disabled")

        for child in self.guide_symbols.winfo_children():
            child.destroy()
        for child in self.guide_keys.winfo_children():
            child.destroy()
        tokens = current["tokens"] if current else []
        active_index = min(self.zhuyin_key_index, len(tokens) - 1) if tokens else -1
        for position, token in enumerate(tokens):
            is_typed = position < self.zhuyin_key_index
            is_current = position == active_index
            symbol_fg = COLORS["text_soft"] if is_typed else COLORS["text"] if is_current else COLORS["muted"]
            symbol_bg = COLORS["right_soft"] if is_current else COLORS["raised"]
            key_fg = COLORS["right"] if is_current else COLORS["muted"]
            tk.Label(self.guide_symbols, text=token["symbol"], bg=symbol_bg, fg=symbol_fg, font=("Segoe UI", 12), padx=2).pack(side="left", padx=1)
            tk.Label(self.guide_keys, text=token["display"], bg=COLORS["raised"], fg=key_fg, font=FONT_MONO_SMALL, padx=2).pack(side="left", padx=1)

    def _render_focus(self, current: dict | None) -> None:
        current = current or {"display": "—", "finger": FINGERS["rightIndex"]}
        finger = current.get("finger") or FINGERS["rightIndex"]
        self.current_key.configure(
            text=current.get("display", "—"),
            bg=COLORS["left_soft"] if finger["hand"] == "left" else COLORS["thumb_soft"] if finger["hand"] == "thumb" else COLORS["right_soft"],
        )
        self.finger_name.configure(text=finger["name"])
        self.hand_name.configure(text=finger["hand_name"])
        self.finger_orb_label.configure(text=finger["name"])
        self._draw_finger_orb(finger)

    def _draw_finger_orb(self, finger: dict) -> None:
        self.finger_orb.delete("all")
        color = COLORS["left"] if finger["hand"] == "left" else COLORS["thumb"] if finger["hand"] == "thumb" else COLORS["right"]
        fill = COLORS["left_soft"] if finger["hand"] == "left" else COLORS["thumb_soft"] if finger["hand"] == "thumb" else COLORS["right_soft"]
        self.finger_orb.create_oval(4, 4, 30, 30, fill=fill, outline=color, width=1)
        self.finger_orb.create_oval(1, 1, 33, 33, outline=fill, width=3)
        self.finger_orb.create_text(17, 17, text=finger["letter"], fill=color, font=("Cascadia Mono", 8, "bold"))

    def _render_keyboard(self, current: dict | None) -> None:
        self._draw_keyboard(current_code=current.get("code") if current else None)

    def _draw_keyboard(self, current_code: str | None = None) -> None:
        if not hasattr(self, "keyboard_canvas"):
            return
        canvas = self.keyboard_canvas
        canvas.delete("all")
        self.key_items = {}
        width = max(canvas.winfo_width(), 470)
        gap = 3
        row_height = 22
        row_gap = 3
        left_padding = 10
        top_padding = 4
        for row_index, row in enumerate(KEYBOARD_ROWS):
            total_weight = sum(weight for _, weight in row)
            unit_width = (width - left_padding * 2 - gap * (len(row) - 1)) / total_weight
            x = left_padding
            y = top_padding + row_index * (row_height + row_gap)
            for code, weight in row:
                key_width = unit_width * weight
                finger = FINGER_MAP.get(code)
                fill = "#191c21"
                outline = COLORS["line"]
                if finger:
                    outline = COLORS["left"] if finger["hand"] == "left" else COLORS["thumb"] if finger["hand"] == "thumb" else COLORS["right"]
                    outline = self._blend(outline, COLORS["line"], 0.35)
                if code == current_code and finger:
                    fill = COLORS["left_soft"] if finger["hand"] == "left" else COLORS["thumb_soft"] if finger["hand"] == "thumb" else COLORS["right_soft"]
                    outline = COLORS["left"] if finger["hand"] == "left" else COLORS["thumb"] if finger["hand"] == "thumb" else COLORS["right"]
                if code == self.wrong_code:
                    fill = COLORS["error_soft"]
                    outline = COLORS["error"]
                rect = canvas.create_rectangle(x, y, x + key_width, y + row_height, fill=fill, outline=outline, width=1)
                label = canvas.create_text(x + key_width / 2, y + row_height / 2 - 1, text=KEY_LABELS.get(code, code), fill=COLORS["text"] if code == current_code else COLORS["muted"], font=FONT_MONO_SMALL)
                finger_id = canvas.create_text(x + key_width - 4, y + row_height - 4, text="", fill=COLORS["muted_deep"], font=("Segoe UI", 7), anchor="se")
                self.key_items[code] = (rect, label, finger_id)
                x += key_width + gap

    @staticmethod
    def _blend(primary: str, secondary: str, amount: float) -> str:
        def rgb(value: str) -> tuple[int, int, int]:
            value = value.lstrip("#")
            return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
        p = rgb(primary)
        s = rgb(secondary)
        mixed = tuple(round(p[index] * amount + s[index] * (1 - amount)) for index in range(3))
        return "#%02x%02x%02x" % mixed

    def _code_from_event(self, event: tk.Event) -> str:
        keysym = str(getattr(event, "keysym", "")).lower()
        if keysym in KEYSYM_TO_CODE:
            return KEYSYM_TO_CODE[keysym]
        if len(keysym) == 1 and keysym in string.ascii_lowercase:
            return f"Key{keysym.upper()}"
        if len(keysym) == 1 and keysym in string.digits:
            return f"Digit{keysym}"
        character = str(getattr(event, "char", "")).lower()
        punctuation = {
            " ": "Space", ",": "Comma", ".": "Period", "/": "Slash", "-": "Minus", "=": "Equal",
            "[": "BracketLeft", "]": "BracketRight", "\\": "Backslash", ";": "Semicolon", "'": "Quote", "`": "Backquote",
        }
        return punctuation.get(character, "")

    def _handle_key(self, event: tk.Event) -> str | None:
        if self.settings_window and self.settings_window.winfo_exists():
            return None
        if self.mode == "zhuyin":
            return self._handle_zhuyin_key(event)

        code = self._code_from_event(event)
        if not code:
            return None
        current = self._current_token()
        if not current or (code not in FINGER_MAP and code != current["code"]):
            return None
        if code == current["code"]:
            self.index += 1
            self._record_typed_character()
            self.feedback = ""
            self.feedback_kind = "idle"
            self._ensure_english_buffer()
        else:
            finger = current.get("finger") or FINGERS["rightIndex"]
            self._show_key_error(code, f"請用{finger['name']}按 {current['display']}")
        self._render()
        return "break"

    def _handle_zhuyin_key(self, event: tk.Event) -> str | None:
        code = self._code_from_event(event)
        if not code or code == "Enter":
            return None
        current = self._current_zhuyin_token()
        if not current:
            return None
        if code == current["code"]:
            character = self._current_zhuyin_character()
            if character and self.zhuyin_key_index >= len(character["tokens"]) - 1:
                self.zhuyin_char_index += 1
                self.zhuyin_key_index = 0
                self._record_typed_character()
                self._ensure_zhuyin_buffer()
            else:
                self.zhuyin_key_index += 1
            self.feedback = ""
            self.feedback_kind = "idle"
        else:
            if code not in FINGER_MAP:
                return None
            finger = current.get("finger") or FINGERS["rightIndex"]
            self._show_key_error(code, f"請用{finger['name']}按 {current['display']}")
        self._render()
        return "break"

    def _show_key_error(self, code: str, message: str) -> None:
        self.feedback = message
        self.feedback_kind = "error"
        self.wrong_code = code
        if self.wrong_after_id:
            self.root.after_cancel(self.wrong_after_id)
        self.wrong_after_id = self.root.after(220, self._clear_wrong)

    def _clear_wrong(self) -> None:
        self.wrong_code = None
        self.wrong_after_id = None
        self._render_keyboard(self._current_token())

    def _toggle_settings(self) -> None:
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.destroy()
            self.settings_window = None
            return
        window = tk.Toplevel(self.root)
        self.settings_window = window
        window.title("Typing Lab Settings")
        window.geometry("330x150")
        window.resizable(False, False)
        window.configure(bg=COLORS["raised"])
        window.transient(self.root)
        window.protocol("WM_DELETE_WINDOW", lambda: self._close_settings(window))
        head = self._frame(window, bg=COLORS["raised"])
        head.pack(fill="x", padx=15, pady=(14, 8))
        self._label(head, "PREFERENCES", bg=COLORS["raised"], fg=COLORS["muted"], font=FONT_MONO_SMALL, anchor="w").pack(anchor="w")
        self._label(head, "指法提示", bg=COLORS["raised"], fg=COLORS["text"], font=("Segoe UI", 14), anchor="w").pack(anchor="w", pady=(5, 0))
        tk.Frame(window, height=1, bg=COLORS["line"]).pack(fill="x", padx=15)
        note = self._border_frame(window, bg="surface")
        note.pack(fill="x", padx=15, pady=(12, 15))
        self._label(note, "i", bg=COLORS["surface"], fg=COLORS["accent"], font=FONT_MONO_SMALL, width=2).pack(side="left", padx=(8, 3), pady=8)
        self._label(note, "注音模式請切換至 ENG 英文鍵盤；一聲按 Space，其餘聲調按完即完成。", bg=COLORS["surface"], fg=COLORS["muted"], font=FONT_UI_SMALL, wraplength=250, justify="left").pack(side="left", padx=(0, 8), pady=8)

    def _close_settings(self, window: tk.Toplevel) -> None:
        if window.winfo_exists():
            window.destroy()
        self.settings_window = None

    def _close(self) -> None:
        self._hide_heatmap_tooltip()
        if self.save_after_id:
            self.root.after_cancel(self.save_after_id)
            self.save_after_id = None
        self._save_settings()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    TypingLabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
