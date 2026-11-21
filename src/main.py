"""Точка входа: читает конфигурацию из stdin и разбирает ее."""

import sys

from config_parser import ConfigSyntaxError, parse


def setup_streams() -> None:
    """Включает UTF-8 для ввода и вывода (русские комментарии и тексты)."""
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    """Читает текст из стандартного ввода и печатает дерево разбора.

    Returns:
        Код завершения: 0 при успехе, 1 при ошибке.
    """
    setup_streams()
    text = sys.stdin.read()
    try:
        tree = parse(text)
    except ConfigSyntaxError as error:
        print(error)
        return 1
    print(tree.pretty())
    return 0


if __name__ == "__main__":
    sys.exit(main())