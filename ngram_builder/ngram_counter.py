from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable

from ngram_builder.models import NgramRow


def update_counter(counter: Counter[tuple[str, ...]], values: list[str], min_n: int, max_n: int) -> None:
    size = len(values)
    if size == 0:
        return
    for n in range(min_n, max_n + 1):
        if size < n:
            continue
        for i in range(size - n + 1):
            counter[tuple(values[i : i + n])] += 1


def select_rows(counter: Counter[tuple[str, ...]], max_ngrams: int | None, scope: str) -> list[NgramRow]:
    if max_ngrams is None:
        items = counter.most_common()
        return [NgramRow(ngram=k, count=v) for k, v in items]

    if scope == "overall":
        items = counter.most_common(max_ngrams)
        return [NgramRow(ngram=k, count=v) for k, v in items]

    if scope == "per-n":
        groups: dict[int, Counter[tuple[str, ...]]] = defaultdict(Counter)
        for gram, count in counter.items():
            groups[len(gram)][gram] = count
        rows: list[NgramRow] = []
        for n in sorted(groups):
            for gram, count in groups[n].most_common(max_ngrams):
                rows.append(NgramRow(ngram=gram, count=count))
        return rows

    raise ValueError(f"Unsupported max_ngrams_scope: {scope}")
