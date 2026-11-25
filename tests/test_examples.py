"""Тесты на примеры конфигураций из разных предметных областей."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from translator import translate

EXAMPLES = ROOT / "tests" / "examples"


def load(name: str):
    """Переводит файл примера и возвращает числа и словари Python."""
    text = (EXAMPLES / name).read_text(encoding="utf-8")
    return translate(text)


class ExampleTests(unittest.TestCase):
    """Константы подставлены, вложенность сохранена."""

    def test_server(self):
        """Пример: веб-сервер."""
        config = load("server.conf")
        self.assertEqual(
            config["server"], {"port": 80, "workers": 4, "timeout": 30}
        )
        self.assertEqual(config["proxy"]["retries"], 3)
        self.assertEqual(config["limits"]["connections"], 1000)

    def test_game(self):
        """Пример: параметры игры."""
        config = load("game.conf")
        self.assertEqual(
            config["hero"], {"hp": 100, "speed": 5, "armor": 10}
        )
        self.assertEqual(config["enemy"]["damage"], {"min": 5, "max": 15})
        self.assertEqual(config["world"]["gravity"], -10)

    def test_home(self):
        """Пример: умный дом."""
        config = load("home.conf")
        self.assertEqual(config["heating"]["bedroom"], 18)
        lamp = {"power": 60, "dimmer": 100}
        self.assertEqual(config["lighting"]["hall"], lamp)
        self.assertEqual(config["lighting"]["kitchen"]["main"], lamp)
        self.assertEqual(config["security"]["cameras"], 4)


if __name__ == "__main__":
    unittest.main()