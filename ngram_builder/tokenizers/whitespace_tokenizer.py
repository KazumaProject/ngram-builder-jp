from __future__ import annotations

from ngram_builder.models import Token


class WhitespaceTokenizer:
    def tokenize(self, text: str) -> list[Token]:
        out: list[Token] = []
        for chunk in text.split():
            out.append(Token(surface=chunk, lemma=chunk, pos=tuple(), reading=None))
        return out
