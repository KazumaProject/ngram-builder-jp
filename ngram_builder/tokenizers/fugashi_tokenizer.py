from __future__ import annotations

from ngram_builder.models import Token


class FugashiTokenizer:
    def __init__(self) -> None:
        try:
            import fugashi
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("fugashi is not installed. Install with: pip install -e .[fugashi]") from exc
        self._tagger = fugashi.Tagger()

    def tokenize(self, text: str) -> list[Token]:
        out: list[Token] = []
        for word in self._tagger(text):
            feat = getattr(word, "feature", None)
            lemma = None
            pos: tuple[str, ...] = tuple()
            reading = None
            if feat is not None:
                lemma = getattr(feat, "lemma", None) or None
                reading = getattr(feat, "pron", None) or getattr(feat, "kana", None) or None
                pos1 = getattr(feat, "pos1", None)
                pos2 = getattr(feat, "pos2", None)
                pos3 = getattr(feat, "pos3", None)
                pos4 = getattr(feat, "pos4", None)
                pos = tuple(p for p in (pos1, pos2, pos3, pos4) if p and p != "*")
            out.append(Token(surface=str(word), lemma=lemma, pos=pos, reading=reading))
        return out
