from __future__ import annotations

from sudachipy import Dictionary, SplitMode

from ngram_builder.models import Token


class SudachiTokenizer:
    def __init__(self, split_mode: str = "C") -> None:
        tokenizer = Dictionary().create()
        self._tokenizer = tokenizer
        self._split_mode = {
            "A": SplitMode.A,
            "B": SplitMode.B,
            "C": SplitMode.C,
        }[split_mode]

    def tokenize(self, text: str) -> list[Token]:
        out: list[Token] = []
        for m in self._tokenizer.tokenize(text, self._split_mode):
            pos = tuple(m.part_of_speech())
            lemma = m.dictionary_form() or None
            reading = m.reading_form() or None
            out.append(Token(surface=m.surface(), lemma=lemma, pos=pos, reading=reading))
        return out
