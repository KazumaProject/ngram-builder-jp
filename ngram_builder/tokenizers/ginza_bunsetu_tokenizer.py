from __future__ import annotations

from typing import Iterable

from ngram_builder.models import Token


class GinzaBunsetuTokenizer:
    def __init__(self, model_name: str = "ja_ginza") -> None:
        try:
            import ginza  # type: ignore
            import spacy
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "GiNZA is not installed. Install with: pip install -e .[ginza]"
            ) from exc

        try:
            self._nlp = spacy.load(model_name)
        except OSError as exc:  # pragma: no cover
            raise RuntimeError(
                f"spaCy model '{model_name}' is not installed. Install with: pip install -U ginza {model_name}"
            ) from exc

        self._ginza = ginza

    def tokenize(self, text: str) -> list[Token]:
        doc = self._nlp(text)
        out: list[Token] = []
        for span in self._ginza.bunsetu_spans(doc):
            surface = span.text.strip()
            if not surface:
                continue
            root = span.root
            lemma = "".join(self._lemma_for_token(token) for token in span).strip() or None
            reading = "".join(self._reading_for_token(token) for token in span).strip() or None
            pos = tuple(part for part in (root.pos_, root.tag_) if part)
            out.append(Token(surface=surface, lemma=lemma, pos=pos, reading=reading))
        return out

    @staticmethod
    def _lemma_for_token(token) -> str:
        lemma = getattr(token, "lemma_", None)
        return lemma if lemma not in (None, "", "*") else token.text

    @staticmethod
    def _reading_for_token(token) -> str:
        morph = getattr(token, "morph", None)
        if morph is None:
            return token.text
        readings = morph.get("Reading")
        if readings:
            return readings[0]
        return token.text
