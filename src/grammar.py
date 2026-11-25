"""Грамматика учебного конфигурационного языка для Lark."""

GRAMMAR = r"""
start: definition* value

definition: "(" _DEF NAME value ")"

?value: number
      | dict
      | reference

number: NUMBER

dict: "@{" entry* "}"

entry: NAME "=" value ";"

reference: "$[" NAME "]"

_DEF: /def(?![a-z])/
NAME: /[a-z]+/
NUMBER: /[+-]?([1-9][0-9]*|0)/
COMMENT: /\{-[\s\S]*?-\}/

%ignore COMMENT
%ignore /\s+/
"""
