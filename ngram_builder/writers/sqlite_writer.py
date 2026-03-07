from __future__ import annotations

import sqlite3
from collections import defaultdict
from pathlib import Path

from ngram_builder.models import NgramRow


def _write_one(rows: list[NgramRow], path: Path) -> None:
    conn = sqlite3.connect(path)
    try:
        conn.execute("DROP TABLE IF EXISTS ngrams")
        conn.execute("CREATE TABLE ngrams (ngram TEXT NOT NULL, count INTEGER NOT NULL, n INTEGER NOT NULL)")
        conn.executemany(
            "INSERT INTO ngrams (ngram, count, n) VALUES (?, ?, ?)",
            ((" ".join(row.ngram), row.count, len(row.ngram)) for row in rows),
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ngrams_n_count ON ngrams (n, count DESC)")
        conn.commit()
    finally:
        conn.close()


def write_sqlite(rows: list[NgramRow], output_path: Path, split_by_n: bool = False) -> None:
    if not split_by_n:
        _write_one(rows, output_path)
        return

    grouped: dict[int, list[NgramRow]] = defaultdict(list)
    for row in rows:
        grouped[len(row.ngram)].append(row)

    stem = output_path.stem
    suffix = output_path.suffix or ".sqlite"
    for n, subrows in sorted(grouped.items()):
        path = output_path.parent / f"{stem}.{n}gram{suffix}"
        _write_one(subrows, path)
