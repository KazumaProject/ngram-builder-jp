from __future__ import annotations

from typing import Protocol

from ngram_builder.models import Token


class TokenFilter(Protocol):
    def keep(self, token: Token) -> bool:
        ...
