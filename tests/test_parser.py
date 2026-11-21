"""Тесты разбора: числа, словари, комментарии и ошибки."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from config_parser import ConfigSyntaxError, parse  # noqa: E402


class ParseValidTests(unittest.TestCase):
    """Корректные тексты разбираются без ошибок."""

    def test_numbers(self):
        """Целые числа со знаком и без."""
        for text in ["0", "7", "+5", "-12", "1000"]:
            with self.subTest(text=text):
                tree = parse(text)
                self.assertEqual(str(tree.children[0]), text)

    def test_empty_dict(self):
        """Пустой словарь."""
        for text in ["@{}", "@{ }"]:
            with self.subTest(text=text):
                dict_node = parse(text).children[0]
                self.assertEqual(dict_node.data, "dict")
                self.assertEqual(dict_node.children, [])

    def test_dict_with_entries(self):
        """Словарь с несколькими записями."""
        tree = parse("@{ a = 1; b = -2; c = 0; }")
        self.assertEqual(len(list(tree.find_data("entry"))), 3)

    def test_nested_dicts(self):
        """Словари внутри словарей."""
        tree = parse("@{ a = @{ b = @{ c = 1; }; }; }")
        self.assertEqual(len(list(tree.find_data("entry"))), 3)
        self.assertEqual(len(list(tree.find_data("dict"))), 3)

    def test_multiline_comment(self):
        """Многострочный комментарий перед значением."""
        tree = parse("{-\nмногострочный\nкомментарий\n-}\n42")
        self.assertEqual(str(tree.children[0]), "42")

    def test_comments_inside_dict(self):
        """Комментарии между записями и внутри записи."""
        tree = parse("@{ {- c1 -} a = {- c2 -} 1; {- c3 -} }")
        self.assertEqual(len(list(tree.find_data("entry"))), 1)

    def test_two_comments_stay_separate(self):
        """Два комментария не сливаются в один."""
        tree = parse("{- a -} 5 {- b -}")
        self.assertEqual(str(tree.children[0]), "5")


class ParseErrorTests(unittest.TestCase):
    """Некорректные тексты дают ConfigSyntaxError."""

    def test_invalid_texts(self):
        """Разные виды синтаксических ошибок."""
        bad_texts = [
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
        for text in bad_texts:
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