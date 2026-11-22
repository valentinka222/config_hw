"""Грамматика учебного конфигурационного языка для Lark."""

GRAMMAR = r"""
start: value

?value: NUMBER
      | dict

dict: "@{" entry* "}"

entry: NAME "=" value ";"

NAME: /[a-z]+/
NUMBER: /[+-]?([1-9][0-9]*|0)/
COMMENT: /\{-[\s\S]*?-\}/

%ignore COMMENT
%ignore /\s+/
"""
