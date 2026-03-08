from __future__ import annotations

import ginza
import spacy

from ngram_builder.models import Token


class GinzaTokenizer:
    def __init__(
        self,
        model_name: str = "ja_ginza",
        batch_size: int = 64,
        n_process: int = 1,
        disable_ner: bool = False,
    ) -> None:
        self.batch_size = batch_size
        self.n_process = n_process
        disable = ["ner"] if disable_ner else []
        self._nlp = spacy.load(model_name, disable=disable)

    def tokenize(self, text: str) -> list[Token]:
        docs = self._nlp.pipe([text], batch_size=self.batch_size, n_process=self.n_process)
        doc = next(docs, None)
        if doc is None:
            return []

        out: list[Token] = []
        for span in ginza.bunsetu_spans(doc):
            span_text = span.text.strip()
            if not span_text:
                continue
            root = span.root
            lemma = root.lemma_ if root.lemma_ and root.lemma_ != "-PRON-" else root.text
            pos = tuple(p for p in root.tag_.split("-") if p) or ((root.pos_,) if root.pos_ else tuple())
            out.append(Token(surface=span_text, lemma=lemma, pos=pos, reading=None))
        return out
