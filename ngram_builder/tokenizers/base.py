from __future__ import annotations

from typing import Protocol

from ngram_builder.models import Token


class TokenizerProtocol(Protocol):
    def tokenize(self, text: str) -> list[Token]:
        ...
