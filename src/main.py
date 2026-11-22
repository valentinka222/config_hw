"""Точка входа: читает конфигурацию из stdin и пишет XML в файл."""

import argparse
import sys

from config_parser import ConfigSyntaxError, parse
from config_transformer import ConfigTransformer
from xml_writer import write_xml


def setup_streams() -> None:
    """Включает UTF-8 для ввода и вывода (русские комментарии и тексты)."""
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")


def parse_arguments() -> argparse.Namespace:
    """Разбирает аргументы командной строки.

    Returns:
        Объект с полем output: путь к выходному XML-файлу.
    """
    arg_parser = argparse.ArgumentParser(
        description="Преобразует конфигурацию из stdin в XML."
    )
    arg_parser.add_argument(
        "-o", "--output", required=True, help="путь к выходному XML-файлу"
    )
    return arg_parser.parse_args()


def main() -> int:
    """Читает текст из stdin, переводит его в XML и записывает в файл.

    Returns:
        Код завершения: 0 при успехе, 1 при ошибке.
    """
    args = parse_arguments()
    setup_streams()
    text = sys.stdin.read()
    try:
        value = ConfigTransformer().transform(parse(text))
        write_xml(value, args.output)
    except ConfigSyntaxError as error:
        print(error)
        return 1
    except OSError as error:
        print(f"Не удалось записать файл: {error}")
        return 1
    print(f"Результат записан в {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
