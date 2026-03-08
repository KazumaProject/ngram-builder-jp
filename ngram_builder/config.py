from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AppConfig:
    mode: str
    dataset: str | None
    config_name: str | None
    split: str
    text_column: str
    local_path: str | None
    cache_dir: str | None
    save_local_dir: str | None
    force_redownload: bool

    tokenizer: str
    sudachi_split_mode: str
    ginza_model: str
    token_form: str

    text_unit: str
    min_n: int
    max_n: int
    max_records: int | None
    max_ngrams: int | None
    max_ngrams_scope: str
    split_by_n: bool

    drop_symbols: bool
    drop_numbers: bool
    allowed_pos: tuple[str, ...]
    blocked_pos: tuple[str, ...]
    min_token_length: int | None
    max_token_length: int | None

    output_format: str
    output: str

    def output_path(self) -> Path:
        return Path(self.output)
