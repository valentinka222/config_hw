"""Запись результата трансляции в XML-файл."""

import xml.etree.ElementTree as ET
from pathlib import Path


def build_element(value) -> ET.Element:
    """Строит XML-элемент для числа или словаря.

    Args:
        value: число (int) или словарь {имя: значение}.

    Returns:
        Элемент number или dict с вложенными элементами entry.
    """
    if isinstance(value, dict):
        element = ET.Element("dict")
        for name, item in value.items():
            entry = ET.SubElement(element, "entry", name=name)
            entry.append(build_element(item))
        return element
    number = ET.Element("number")
    number.text = str(value)
    return number


def write_xml(value, path: str) -> None:
    """Записывает значение в XML-файл, создавая нужные папки.

    Args:
        value: число или словарь, результат трансляции.
        path: путь к выходному файлу.

    Raises:
        OSError: если файл не удалось записать.
    """
    root = ET.Element("config")
    root.append(build_element(value))
    ET.indent(root)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(
        str(target), encoding="utf-8", xml_declaration=True
    )
