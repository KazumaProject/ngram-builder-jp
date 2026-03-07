from __future__ import annotations

import re

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？!?\n])")


def split_text(text: str, text_unit: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if text_unit == "document":
        return [text]
    if text_unit == "sentence":
        parts = _SENTENCE_SPLIT_RE.split(text)
        return [p.strip() for p in parts if p.strip()]
    raise ValueError(f"Unsupported text_unit: {text_unit}")
