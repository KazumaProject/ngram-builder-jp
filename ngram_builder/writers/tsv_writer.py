from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from tqdm import tqdm

from ngram_builder.models import NgramRow


def _write_one(rows: list[NgramRow], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write("ngram\tcount\n")
        for row in tqdm(rows, desc=f"Writing {path.name}", unit="row"):
            f.write(f"{' '.join(row.ngram)}\t{row.count}\n")


def write_tsv(rows: list[NgramRow], output_path: Path, split_by_n: bool = False) -> None:
    if not split_by_n:
        _write_one(rows, output_path)
        return

    grouped: dict[int, list[NgramRow]] = defaultdict(list)
    for row in tqdm(rows, desc="Grouping rows by n", unit="row"):
        grouped[len(row.ngram)].append(row)

    stem = output_path.stem
    suffix = output_path.suffix or ".tsv"
    for n, subrows in tqdm(sorted(grouped.items()), desc="Writing split TSV files", unit="file"):
        path = output_path.parent / f"{stem}.{n}gram{suffix}"
        _write_one(subrows, path)
