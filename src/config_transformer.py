"""Преобразование дерева разбора в числа и словари Python."""

from lark import Discard, Transformer

from errors import ConfigNameError


class ConfigTransformer(Transformer):
    """Превращает дерево разбора в числа и словари Python.

    Константы вычисляются на этапе трансляции: объявления запоминаются,
    а ссылки заменяются значениями.
    """

    def __init__(self):
        """Создает преобразователь с пустым набором констант."""
        super().__init__()
        self.constants = {}

    def start(self, items):
        """Корень дерева: после удаления объявлений остается значение."""
        return items[0]

    def definition(self, items):
        """Объявление (def имя значение): запоминает константу."""
        name, value = items
        self.constants[str(name)] = value
        return Discard

    def reference(self, items):
        """Ссылка $[имя]: заменяется значением константы."""
        name = str(items[0])
        if name not in self.constants:
            raise ConfigNameError(f"Константа '{name}' не объявлена")
        return self.constants[name]

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
