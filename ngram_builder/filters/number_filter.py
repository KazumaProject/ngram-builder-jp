from __future__ import annotations

from ngram_builder.models import Token


class NumberFilter:
    def keep(self, token: Token) -> bool:
        if token.pos and token.pos[0] == "名詞" and len(token.pos) > 1 and token.pos[1] == "数詞":
            return False
        return not token.surface.isdigit()
