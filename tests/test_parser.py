"""Тесты разбора: корректные и некорректные тексты."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from config_parser import ConfigSyntaxError, parse  # noqa: E402

VALID_TEXTS = [
    "0",
    "+5",
    "-12",
    "1000",
    "@{}",
    "@{ a = 1; b = -2; }",
    "@{ a = @{ b = @{ c = 1; }; }; }",
    "{-\nмногострочный\nкомментарий\n-}\n42",
    "@{ {- c1 -} a = {- c2 -} 1; {- c3 -} }",
    "{- a -} 5 {- b -}",
]

INVALID_TEXTS = [
    "",
    "007",
    "1.5",
    "+",
    "5 5",
    "@{ a = 1 }",
    "@{ a = 1;",
    "@{ a = 1; } }",
    "@{ A = 1; }",
    "@{ a1 = 1; }",
    "@{ a = ; }",
    "{- не закрыт 5",
]


class ParseTests(unittest.TestCase):
    """Разбор чисел, словарей и комментариев."""

    def test_valid_texts(self):
        """Корректные тексты разбираются без ошибок."""
        for text in VALID_TEXTS:
            with self.subTest(text=text):
                parse(text)

    def test_invalid_texts(self):
        """Некорректные тексты дают ConfigSyntaxError."""
        for text in INVALID_TEXTS:
            with self.subTest(text=text):
                with self.assertRaises(ConfigSyntaxError):
                    parse(text)

    def test_error_has_position(self):
        """Сообщение об ошибке содержит строку и столбец."""
        with self.assertRaises(ConfigSyntaxError) as context:
            parse("@{\n  a = ;\n}")
        self.assertIn("строка 2", str(context.exception))


if __name__ == "__main__":
    unittest.main()
