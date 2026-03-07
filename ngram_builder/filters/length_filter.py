from __future__ import annotations

from ngram_builder.models import Token


class LengthFilter:
    def __init__(self, min_length: int | None, max_length: int | None) -> None:
        self._min = min_length
        self._max = max_length

    def keep(self, token: Token) -> bool:
        length = len(token.surface)
        if self._min is not None and length < self._min:
            return False
        if self._max is not None and length > self._max:
            return False
        return True
