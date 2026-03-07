from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    surface: str
    lemma: str | None
    pos: tuple[str, ...]
    reading: str | None = None


@dataclass(frozen=True)
class NgramRow:
    ngram: tuple[str, ...]
    count: int
