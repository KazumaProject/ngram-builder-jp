from __future__ import annotations

import argparse

from ngram_builder.config import AppConfig
from ngram_builder.pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build configurable word-level n-gram dictionaries")

    parser.add_argument("--mode", choices=["streaming", "download", "local"], default="streaming")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--config-name", default=None)
    parser.add_argument("--split", default="train")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--local-path", default=None)
    parser.add_argument("--cache-dir", default=None)
    parser.add_argument("--save-local-dir", default=None)
    parser.add_argument("--force-redownload", action="store_true")

    parser.add_argument("--tokenizer", choices=["sudachi", "fugashi", "whitespace", "ginza"], default="sudachi")
    parser.add_argument("--sudachi-split-mode", choices=["A", "B", "C"], default="C")
    parser.add_argument("--ginza-model", default="ja_ginza")
    parser.add_argument("--ginza-batch-size", type=int, default=64)
    parser.add_argument("--ginza-n-process", type=int, default=1)
    parser.add_argument("--ginza-disable-ner", action="store_true")
    parser.add_argument("--token-form", choices=["surface", "lemma"], default="surface")

    parser.add_argument("--text-unit", choices=["document", "sentence"], default="sentence")
    parser.add_argument("--min-n", type=int, default=1)
    parser.add_argument("--max-n", type=int, default=3)
    parser.add_argument("--max-records", type=int, default=None)
    parser.add_argument("--max-ngrams", type=int, default=None)
    parser.add_argument("--max-ngrams-scope", choices=["overall", "per-n"], default="overall")
    parser.add_argument("--split-by-n", action="store_true")

    parser.add_argument("--drop-symbols", action="store_true")
    parser.add_argument("--drop-numbers", action="store_true")
    parser.add_argument("--allowed-pos", nargs="*", default=[])
    parser.add_argument("--blocked-pos", nargs="*", default=[])
    parser.add_argument("--min-token-length", type=int, default=None)
    parser.add_argument("--max-token-length", type=int, default=None)
    parser.add_argument(
        "--strip-chars",
        default="",
        help=(
            "Characters to remove from text before sentence splitting and tokenization. "
            "Example: --strip-chars '\"〈〉『』「」'"
        ),
    )

    parser.add_argument("--output-format", choices=["tsv", "sqlite"], default="tsv")
    parser.add_argument("--output", required=True)
    return parser


def parse_args() -> AppConfig:
    args = build_parser().parse_args()
    if args.min_n < 1:
        raise SystemExit("--min-n must be >= 1")
    if args.max_n < args.min_n:
        raise SystemExit("--max-n must be >= --min-n")
    if args.mode in {"streaming", "download"} and not args.dataset:
        raise SystemExit("--dataset is required for streaming/download mode")
    if args.mode == "local" and not args.local_path:
        raise SystemExit("--local-path is required for local mode")
    if args.ginza_batch_size < 1:
        raise SystemExit("--ginza-batch-size must be >= 1")
    if args.ginza_n_process < 1:
        raise SystemExit("--ginza-n-process must be >= 1")

    return AppConfig(
        mode=args.mode,
        dataset=args.dataset,
        config_name=args.config_name,
        split=args.split,
        text_column=args.text_column,
        local_path=args.local_path,
        cache_dir=args.cache_dir,
        save_local_dir=args.save_local_dir,
        force_redownload=args.force_redownload,
        tokenizer=args.tokenizer,
        sudachi_split_mode=args.sudachi_split_mode,
        ginza_model=args.ginza_model,
        ginza_batch_size=args.ginza_batch_size,
        ginza_n_process=args.ginza_n_process,
        ginza_disable_ner=args.ginza_disable_ner,
        token_form=args.token_form,
        text_unit=args.text_unit,
        min_n=args.min_n,
        max_n=args.max_n,
        max_records=args.max_records,
        max_ngrams=args.max_ngrams,
        max_ngrams_scope=args.max_ngrams_scope,
        split_by_n=args.split_by_n,
        drop_symbols=args.drop_symbols,
        drop_numbers=args.drop_numbers,
        allowed_pos=tuple(args.allowed_pos),
        blocked_pos=tuple(args.blocked_pos),
        min_token_length=args.min_token_length,
        max_token_length=args.max_token_length,
        strip_chars=args.strip_chars,
        output_format=args.output_format,
        output=args.output,
    )


def main() -> None:
    config = parse_args()
    run_pipeline(config)


if __name__ == "__main__":
    main()
