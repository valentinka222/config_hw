"""Трансляция текста конфигурации в числа и словари Python."""

from lark.exceptions import VisitError

from config_parser import parse
from config_transformer import ConfigTransformer
from errors import ConfigError


def translate(text: str):
    """Разбирает текст и вычисляет константы.

    Args:
        text: текст на учебном конфигурационном языке.

    Returns:
        Число (int) или словарь {имя: значение}.

    Raises:
        ConfigError: при синтаксической ошибке или необъявленной константе.
    """
    tree = parse(text)
    try:
        return ConfigTransformer().transform(tree)
    except VisitError as error:
        if isinstance(error.orig_exc, ConfigError):
            raise error.orig_exc from None
        raise
