from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Iterable

from ngram_builder.models import NgramRow


def _write_one(rows: list[NgramRow], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write("ngram\tcount\tn\n")
        for row in rows:
            f.write(f"{' '.join(row.ngram)}\t{row.count}\t{len(row.ngram)}\n")


def write_tsv(rows: list[NgramRow], output_path: Path, split_by_n: bool = False) -> None:
    if not split_by_n:
        _write_one(rows, output_path)
        return

    grouped: dict[int, list[NgramRow]] = defaultdict(list)
    for row in rows:
        grouped[len(row.ngram)].append(row)

    stem = output_path.stem
    suffix = output_path.suffix or ".tsv"
    for n, subrows in sorted(grouped.items()):
        path = output_path.parent / f"{stem}.{n}gram{suffix}"
        _write_one(subrows, path)
