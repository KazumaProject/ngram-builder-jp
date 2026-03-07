from __future__ import annotations

import re

from ngram_builder.models import Token

_SYMBOL_ONLY_RE = re.compile(r"^[\W_]+$", re.UNICODE)


class SymbolFilter:
    def keep(self, token: Token) -> bool:
        if token.pos and token.pos[0] == "補助記号":
            return False
        return not _SYMBOL_ONLY_RE.match(token.surface)
