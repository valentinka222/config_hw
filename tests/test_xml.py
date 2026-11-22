"""Тесты трансляции в XML: содержимое файла и работа из командной строки."""

import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from config_parser import parse  # noqa: E402
from config_transformer import ConfigTransformer  # noqa: E402
from xml_writer import write_xml  # noqa: E402


def translate(text: str) -> ET.Element:
    """Переводит текст в XML-файл и возвращает корневой элемент."""
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "result.xml"
        write_xml(ConfigTransformer().transform(parse(text)), str(path))
        return ET.parse(path).getroot()


class XmlContentTests(unittest.TestCase):
    """Содержимое XML для разных конструкций языка."""

    def test_number(self):
        """Число на верхнем уровне; плюс в записи пропадает."""
        for text, expected in [("42", "42"), ("+5", "5"), ("-3", "-3")]:
            with self.subTest(text=text):
                root = translate(text)
                self.assertEqual(root.tag, "config")
                self.assertEqual(root.find("number").text, expected)

    def test_dict_entries(self):
        """Словарь с записями: имена и значения."""
        root = translate("@{ port = 8080; debug = 0; }")
        entries = root.findall("dict/entry")
        self.assertEqual([e.get("name") for e in entries], ["port", "debug"])
        self.assertEqual(entries[0].find("number").text, "8080")

    def test_nested_dicts(self):
        """Вложенные словари."""
        root = translate("@{ a = @{ b = @{ c = 1; }; }; }")
        path = "dict/entry[@name='a']/dict/entry[@name='b']/dict/entry/number"
        self.assertEqual(root.find(path).text, "1")

    def test_empty_dict(self):
        """Пустой словарь дает пустой элемент dict."""
        root = translate("@{}")
        self.assertEqual(len(root.find("dict")), 0)

    def test_entry_order(self):
        """Порядок записей сохраняется."""
        root = translate("@{ z = 1; a = 2; m = 3; }")
        names = [e.get("name") for e in root.findall("dict/entry")]
        self.assertEqual(names, ["z", "a", "m"])

    def test_comments_are_dropped(self):
        """Комментарии в XML не попадают."""
        root = translate("{- c1 -} @{ {- c2 -} a = 1; }")
        self.assertEqual(len(root.findall("dict/entry")), 1)


class CommandLineTests(unittest.TestCase):
    """Запуск программы как отдельного процесса."""

    def run_tool(self, text: str, *args: str):
        """Запускает main.py с текстом на stdin."""
        command = [sys.executable, str(ROOT / "src" / "main.py"), *args]
        return subprocess.run(
            command, input=text, capture_output=True,
            text=True, encoding="utf-8",
        )

    def test_success(self):
        """Успешный запуск создает файл и возвращает 0."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sub" / "result.xml"
            result = self.run_tool("@{ a = 1; }", "-o", str(path))
            self.assertEqual(result.returncode, 0)
            self.assertTrue(path.exists())

    def test_syntax_error(self):
        """Синтаксическая ошибка: код 1, сообщение, файла нет."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "result.xml"
            result = self.run_tool("@{ a = ; }", "-o", str(path))
            self.assertEqual(result.returncode, 1)
            self.assertIn("Синтаксическая ошибка", result.stdout)
            self.assertFalse(path.exists())

    def test_no_output_key(self):
        """Без ключа -o программа завершается с кодом 2."""
        result = self.run_tool("42")
        self.assertEqual(result.returncode, 2)

    def test_unwritable_path(self):
        """Нельзя записать файл внутрь другого файла: код 1."""
        with tempfile.TemporaryDirectory() as folder:
            blocker = Path(folder) / "file.txt"
            blocker.write_text("x", encoding="utf-8")
            target = blocker / "result.xml"
            result = self.run_tool("42", "-o", str(target))
            self.assertEqual(result.returncode, 1)
            self.assertIn("Не удалось записать", result.stdout)


if __name__ == "__main__":
    unittest.main()
