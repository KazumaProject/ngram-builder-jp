from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Iterator

from datasets import Dataset, IterableDataset, load_dataset

from ngram_builder.config import AppConfig


def load_records(config: AppConfig) -> Iterable[dict]:
    if config.mode in {"streaming", "download"}:
        return _load_hf_records(config)
    if config.mode == "local":
        return _load_local_records(config)
    raise ValueError(f"Unsupported mode: {config.mode}")


def _download_mode_value(config: AppConfig) -> str | None:
    if not config.force_redownload:
        return None
    return "force_redownload"


def _load_hf_records(config: AppConfig) -> Iterable[dict]:
    if not config.dataset:
        raise ValueError("--dataset is required for streaming/download mode")
    kwargs: dict = {
        "path": config.dataset,
        "name": config.config_name,
        "split": config.split,
        "streaming": config.mode == "streaming",
    }
    if config.cache_dir:
        kwargs["cache_dir"] = config.cache_dir
    if config.force_redownload:
        kwargs["download_mode"] = _download_mode_value(config)

    dataset = load_dataset(**kwargs)

    if config.mode == "download" and config.save_local_dir:
        save_path = Path(config.save_local_dir)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(dataset, Dataset):
            dataset.save_to_disk(str(save_path))
        else:
            materialized = Dataset.from_list(list(dataset))
            materialized.save_to_disk(str(save_path))
            dataset = materialized
    return dataset


def _load_local_records(config: AppConfig) -> Iterable[dict]:
    if not config.local_path:
        raise ValueError("--local-path is required for local mode")
    path = Path(config.local_path)
    if path.is_dir():
        try:
            from datasets import load_from_disk

            ds = load_from_disk(str(path))
            return ds
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Failed to load dataset directory: {path}") from exc

    suffix = path.suffix.lower()
    if suffix == ".txt":
        return _iter_txt(path, config.text_column)
    if suffix == ".jsonl":
        return _iter_jsonl(path)
    if suffix == ".json":
        return _iter_json(path)
    if suffix == ".csv":
        return _iter_csv(path)
    if suffix == ".parquet":
        ds = load_dataset("parquet", data_files=str(path), split="train")
        return ds
    raise ValueError(f"Unsupported local file type: {suffix}")


def _iter_txt(path: Path, text_column: str) -> Iterator[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line:
                yield {text_column: line}


def _iter_jsonl(path: Path) -> Iterator[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def _iter_json(path: Path) -> Iterator[dict]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        for row in data:
            yield row
        return
    raise ValueError("Local JSON file must contain a list of objects")


def _iter_csv(path: Path) -> Iterator[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield dict(row)
