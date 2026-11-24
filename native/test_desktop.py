import json
from pathlib import Path
import tempfile
import tkinter as tk
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from typing_lab import TypingLabApp


class TypingLabDesktopTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = self.enterContext(tempfile.TemporaryDirectory())
        self.settings_path = Path(directory) / "settings.json"
        self.enterContext(patch.object(TypingLabApp, "_settings_path", return_value=self.settings_path))
        self.enterContext(patch.object(TypingLabApp, "_next_english_fragment", return_value="abc test."))
        self.enterContext(patch.object(TypingLabApp, "_next_zhuyin_sample", return_value=("空", ["ㄎㄨㄥˋ"])))
        self.root = tk.Tk()
        self.root.withdraw()
        self.addCleanup(self.root.destroy)
        self.app = TypingLabApp(self.root)

    def press(self, keysym: str, character: str = "") -> None:
        self.app._handle_key(SimpleNamespace(keysym=keysym, char=character))

    def test_wrong_english_key_does_not_advance_or_count(self) -> None:
        self.press("z", "z")
        self.assertEqual(self.app.index, 0)
        self.assertEqual(self.app.total_typed_by_mode["english"], 0)
        self.assertEqual(self.app.feedback_kind, "error")
        self.press("a", "a")
        self.assertEqual(self.app.index, 1)
        self.assertEqual(self.app.total_typed_by_mode["english"], 1)

    def test_zhuyin_requires_tone_last_and_saves_separate_totals(self) -> None:
        self.press("a", "a")
        self.app._set_mode("zhuyin")
        self.press("4", "4")
        self.assertEqual(self.app.zhuyin_char_index, 0)
        self.assertEqual(self.app.feedback_kind, "error")

        for keysym, character in [("slash", "/"), ("j", "j"), ("d", "d")]:
            self.press(keysym, character)
        self.assertEqual(self.app.zhuyin_char_index, 0)
        self.press("4", "4")
        self.assertEqual(self.app.zhuyin_char_index, 1)
        self.app._save_settings()

        saved = json.loads(self.settings_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["mode"], "zhuyin")
        self.assertEqual(saved["total_typed_by_mode"], {"english": 1, "zhuyin": 1})


if __name__ == "__main__":
    unittest.main()
