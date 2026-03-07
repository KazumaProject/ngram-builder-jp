from __future__ import annotations

from ngram_builder.models import Token


class PosFilter:
    def __init__(self, allowed: tuple[str, ...], blocked: tuple[str, ...]) -> None:
        self._allowed = set(allowed)
        self._blocked = set(blocked)

    def keep(self, token: Token) -> bool:
        head = token.pos[0] if token.pos else ""
        if self._allowed and head not in self._allowed:
            return False
        if self._blocked and head in self._blocked:
            return False
        return True
