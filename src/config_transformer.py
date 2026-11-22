"""Преобразование дерева разбора в числа и словари Python."""

from lark import Transformer


class ConfigTransformer(Transformer):
    """Превращает дерево разбора в числа и словари Python."""

    def start(self, items):
        """Корень дерева: единственное значение программы."""
        return items[0]

    def entry(self, items):
        """Запись «имя = значение»: пара (имя, значение)."""
        name, value = items
        return str(name), value

    def dict(self, entries):
        """Словарь, собранный из пар (имя, значение)."""
        return {name: value for name, value in entries}

    def NUMBER(self, token):
        """Число из текста токена."""
        return int(token)
