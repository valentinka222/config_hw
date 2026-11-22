"""Разбор текста учебного конфигурационного языка."""

from lark import Lark, Tree
from lark.exceptions import UnexpectedInput

from grammar import GRAMMAR


class ConfigSyntaxError(Exception):
    """Синтаксическая ошибка во входном тексте."""


PARSER = Lark(GRAMMAR, parser="lalr")


def parse(text: str) -> Tree:
    """Разбирает текст и возвращает дерево разбора.

    Args:
        text: текст на учебном конфигурационном языке.

    Returns:
        Дерево разбора Lark.

    Raises:
        ConfigSyntaxError: если текст не соответствует грамматике.
    """
    try:
        return PARSER.parse(text)
    except UnexpectedInput as error:
        raise ConfigSyntaxError(
            f"Синтаксическая ошибка: строка {error.line}, "
            f"столбец {error.column}\n{error.get_context(text)}"
        ) from error
