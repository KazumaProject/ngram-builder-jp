from __future__ import annotations

from collections import Counter
from typing import Iterable

from tqdm import tqdm

from ngram_builder.config import AppConfig
from ngram_builder.dataset_loader import load_records
from ngram_builder.filters.length_filter import LengthFilter
from ngram_builder.filters.number_filter import NumberFilter
from ngram_builder.filters.pos_filter import PosFilter
from ngram_builder.filters.symbol_filter import SymbolFilter
from ngram_builder.models import Token
from ngram_builder.ngram_counter import select_rows, update_counter
from ngram_builder.sentence_splitter import split_text
from ngram_builder.tokenizers.fugashi_tokenizer import FugashiTokenizer
from ngram_builder.tokenizers.ginza_bunsetu_tokenizer import GinzaBunsetuTokenizer
from ngram_builder.tokenizers.sudachi_tokenizer import SudachiTokenizer
from ngram_builder.tokenizers.whitespace_tokenizer import WhitespaceTokenizer
from ngram_builder.writers import write_rows


def build_tokenizer(config: AppConfig):
    if config.tokenizer == "ginza":
        return GinzaBunsetuTokenizer(model_name=config.ginza_model)
    if config.tokenizer == "sudachi":
        return SudachiTokenizer(split_mode=config.sudachi_split_mode)
    if config.tokenizer == "fugashi":
        return FugashiTokenizer()
    if config.tokenizer == "whitespace":
        return WhitespaceTokenizer()
    raise ValueError(f"Unsupported tokenizer: {config.tokenizer}")


def build_filters(config: AppConfig):
    filters = []
    if config.drop_symbols:
        filters.append(SymbolFilter())
    if config.drop_numbers:
        filters.append(NumberFilter())
    if config.allowed_pos or config.blocked_pos:
        filters.append(PosFilter(config.allowed_pos, config.blocked_pos))
    if config.min_token_length is not None or config.max_token_length is not None:
        filters.append(LengthFilter(config.min_token_length, config.max_token_length))
    return filters


def apply_filters(tokens: list[Token], filters) -> list[Token]:
    if not filters:
        return tokens
    out: list[Token] = []
    for token in tokens:
        if all(f.keep(token) for f in filters):
            out.append(token)
    return out


def pick_value(token: Token, token_form: str) -> str:
    if token_form == "surface":
        return token.surface
    if token_form == "lemma":
        return token.lemma or token.surface
    raise ValueError(f"Unsupported token_form: {token_form}")


def run_pipeline(config: AppConfig) -> None:
    records = load_records(config)
    tokenizer = build_tokenizer(config)
    filters = build_filters(config)
    counter: Counter[tuple[str, ...]] = Counter()

    processed = 0
    iterator = records
    for record in tqdm(iterator, desc="processing", unit="record"):
        text = record.get(config.text_column)
        if not isinstance(text, str) or not text.strip():
            continue

        units = split_text(text, config.text_unit)
        for unit in units:
            tokens = tokenizer.tokenize(unit)
            tokens = apply_filters(tokens, filters)
            values = [pick_value(token, config.token_form) for token in tokens if pick_value(token, config.token_form).strip()]
            update_counter(counter, values, config.min_n, config.max_n)

        processed += 1
        if config.max_records is not None and processed >= config.max_records:
            break

    rows = select_rows(counter, config.max_ngrams, config.max_ngrams_scope)
    write_rows(rows, config)
