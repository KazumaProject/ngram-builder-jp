from __future__ import annotations


def strip_chars(text: str, chars: str) -> str:
    if not text or not chars:
        return text
    table = str.maketrans("", "", chars)
    return text.translate(table)
