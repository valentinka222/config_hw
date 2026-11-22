"""Ошибки трансляции учебного конфигурационного языка."""


class ConfigError(Exception):
    """Базовая ошибка трансляции."""


class ConfigSyntaxError(ConfigError):
    """Синтаксическая ошибка во входном тексте."""


class ConfigNameError(ConfigError):
    """Ошибка имен: ссылка на необъявленную константу."""
