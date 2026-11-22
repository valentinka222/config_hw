"""Тесты констант: вычисление значений и ошибки."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from errors import ConfigNameError, ConfigSyntaxError  # noqa: E402
from translator import translate  # noqa: E402

VALID_CASES = [
    ("(def x 5) $[x]", 5),
    ("(def x -4) $[x]", -4),
    ("(def p 80) @{ a = $[p]; }", {"a": 80}),
    ("(def d @{ k = 1; }) @{ a = $[d]; b = $[d]; }",
     {"a": {"k": 1}, "b": {"k": 1}}),
    ("(def a 1) (def b $[a]) $[b]", 1),
    ("(def p 5) (def d @{ x = $[p]; }) @{ r = $[d]; }",
     {"r": {"x": 5}}),
    ("(def v 7) @{ a = @{ b = $[v]; }; }", {"a": {"b": 7}}),
    ("{- c -}\n(  def   x   -3 )\n$[ x ]", -3),
    ("@{ def = 1; }", {"def": 1}),
]

UNDEFINED_CASES = [
    "$[x]",
    "@{ a = $[x]; }",
    "(def a $[b]) (def b 1) 5",
]

SYNTAX_CASES = [
    "(defx 1) 2",
    "(def x 1)",
    "(def X 1) 2",
    "@{ (def x 1); }",
    "$[x",
    "5 (def x 1)",
]


class ConstantTests(unittest.TestCase):
    """Вычисление констант и ошибки при их использовании."""

    def test_values(self):
        """Константы подставляются на место ссылок."""
        for text, expected in VALID_CASES:
            with self.subTest(text=text):
                self.assertEqual(translate(text), expected)

    def test_undefined_constant(self):
        """Ссылка на необъявленную константу дает ConfigNameError."""
        for text in UNDEFINED_CASES:
            with self.subTest(text=text):
                with self.assertRaises(ConfigNameError):
                    translate(text)

    def test_syntax_errors(self):
        """Неверная запись объявлений и ссылок дает ConfigSyntaxError."""
        for text in SYNTAX_CASES:
            with self.subTest(text=text):
                with self.assertRaises(ConfigSyntaxError):
                    translate(text)


if __name__ == "__main__":
    unittest.main()
