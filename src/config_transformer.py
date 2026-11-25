"""Преобразование дерева разбора в числа и словари Python."""

from lark import Discard, Transformer, v_args

from errors import ConfigNameError


def name_error(line: int, message: str) -> ConfigNameError:
    """Создает ошибку имен с номером строки.

    Args:
        line: номер строки в исходном тексте.
        message: описание ошибки.

    Returns:
        Исключение, которое нужно выбросить через raise.
    """
    return ConfigNameError(f"Строка {line}: {message}")


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

    @v_args(meta=True)
    def definition(self, meta, items):
        """Объявление (def имя значение): запоминает константу."""
        name, value = items
        key = str(name)
        if key in self.constants:
            raise name_error(meta.line, f"константа '{key}' уже объявлена")
        self.constants[key] = value
        return Discard

    @v_args(meta=True)
    def reference(self, meta, items):
        """Ссылка $[имя]: заменяется значением константы."""
        name = str(items[0])
        if name not in self.constants:
            raise name_error(meta.line, f"константа '{name}' не объявлена")
        return self.constants[name]

    @v_args(meta=True)
    def entry(self, meta, items):
        """Запись «имя = значение»: тройка (имя, значение, строка)."""
        name, value = items
        return str(name), value, meta.line

    def dict(self, entries):
        """Словарь, собранный из записей; повтор ключа - ошибка."""
        result = {}
        for name, value, line in entries:
            if name in result:
                raise name_error(line, f"ключ '{name}' повторяется в словаре")
            result[name] = value
        return result

    def number(self, items):
        """Число из текста токена."""
        return int(items[0])
