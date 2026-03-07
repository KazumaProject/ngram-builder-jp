from pathlib import Path

from ngram_builder.writers.sqlite_writer import write_sqlite
from ngram_builder.writers.tsv_writer import write_tsv


def write_rows(rows, config) -> None:
    output_path = Path(config.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if config.output_format == "tsv":
        write_tsv(rows, output_path, split_by_n=config.split_by_n)
        return
    if config.output_format == "sqlite":
        write_sqlite(rows, output_path, split_by_n=config.split_by_n)
        return
    raise ValueError(f"Unsupported output_format: {config.output_format}")
