# ngram-builder

A configurable CLI tool to build word-level n-gram dictionaries from Hugging Face datasets or local text files.

## Features

- Build unigram, bigram, trigram, or any `n` range
- Use Hugging Face datasets in `streaming` or cached `download` mode
- Read local text / jsonl / json / parquet / csv files with `--mode local`
- Default tokenizer: Sudachi
- Optional tokenizer backends: `fugashi`, `whitespace`
- Count by `surface` or `lemma`
- Split output by `n`
- Limit top results either `overall` or `per-n`
- Save a downloaded dataset to local files for later offline reuse
- Control Hugging Face cache directory and force redownload when needed
- Extension-friendly design for filters and tokenizers
- Remove unwanted characters before tokenization with `--strip-chars`

## Installation

### With uv

```bash
uv venv && source .venv/bin/activate && uv pip install -e .
```

Install with Sudachi support:

```bash
uv venv && source .venv/bin/activate && uv pip install -e '.[sudachi]'
```

### Optional fugashi backend

```bash
uv pip install -e .[fugashi]
```

## Basic usage

Build 1-gram through 3-gram from a Hugging Face dataset in streaming mode:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer sudachi --sudachi-split-mode C --token-form surface --text-unit sentence --min-n 1 --max-n 3 --max-records 10000 --drop-symbols --output-format tsv --output out/wiki_ngrams.tsv
```

This counts unigram, bigram, and trigram together and writes one TSV.

## Split output by n

Write separate files for 1-gram, 2-gram, and 3-gram:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer sudachi --sudachi-split-mode C --text-unit sentence --min-n 1 --max-n 3 --max-records 10000 --drop-symbols --split-by-n --output-format tsv --output out/wiki_ngrams.tsv
```

Output:

- `out/wiki_ngrams.1gram.tsv`
- `out/wiki_ngrams.2gram.tsv`
- `out/wiki_ngrams.3gram.tsv`

## Limit top results overall

Take top 100000 rows **across all n values**, then split files:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer sudachi --sudachi-split-mode C --text-unit sentence --min-n 1 --max-n 3 --max-records 10000 --drop-symbols --max-ngrams 100000 --max-ngrams-scope overall --split-by-n --output-format tsv --output out/wiki_ngrams.tsv
```

## Limit top results per n

Take top 100000 rows for each n independently:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer sudachi --sudachi-split-mode C --text-unit sentence --min-n 1 --max-n 3 --max-records 10000 --drop-symbols --max-ngrams 100000 --max-ngrams-scope per-n --split-by-n --output-format tsv --output out/wiki_ngrams.tsv
```

## Count by lemma instead of surface

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer sudachi --sudachi-split-mode C --token-form lemma --text-unit sentence --min-n 1 --max-n 3 --max-records 10000 --drop-symbols --output-format tsv --output out/wiki_ngrams_lemma.tsv
```

`surface` counts the exact form seen in text.
`lemma` counts dictionary-form-like normalized tokens when the tokenizer supports it.

## Cached download mode

Use Hugging Face cached download mode instead of streaming:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode download --cache-dir .cache/huggingface --tokenizer sudachi --text-unit sentence --min-n 1 --max-n 2 --max-records 5000 --drop-symbols --output-format tsv --output out/wiki_cached.tsv
```

If the dataset is already cached, the next run usually reuses the cache.

## Force redownload

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode download --cache-dir .cache/huggingface --force-redownload --tokenizer sudachi --text-unit sentence --min-n 1 --max-n 2 --max-records 5000 --drop-symbols --output-format tsv --output out/wiki_redownload.tsv
```

## Save dataset locally after download

Download once, save locally, and reuse later without the Hub:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode download --cache-dir .cache/huggingface --save-local-dir data/wiki_20240101 --tokenizer sudachi --text-unit sentence --min-n 1 --max-n 2 --max-records 5000 --drop-symbols --output-format tsv --output out/wiki_saved.tsv
```

This exports the resolved dataset split to `data/wiki_20240101`.

## Reuse local exported dataset

```bash
ngram-builder --mode local --local-path data/wiki_20240101 --text-column text --tokenizer sudachi --text-unit sentence --min-n 1 --max-n 2 --max-records 5000 --drop-symbols --output-format tsv --output out/wiki_local.tsv
```

## Use local JSONL file

```bash
ngram-builder --mode local --local-path data/articles.jsonl --text-column text --tokenizer sudachi --min-n 1 --max-n 3 --output-format tsv --output out/local_jsonl.tsv
```

## Use local text file

Each line is treated as one record.

```bash
ngram-builder --mode local --local-path data/plain.txt --text-column text --tokenizer whitespace --min-n 1 --max-n 2 --output-format tsv --output out/plain.tsv
```

## SQLite output

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer sudachi --text-unit sentence --min-n 1 --max-n 3 --max-records 10000 --drop-symbols --output-format sqlite --output out/wiki_ngrams.sqlite
```

## Filters

Drop symbols and numbers:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer sudachi --drop-symbols --drop-numbers --min-n 1 --max-n 2 --output-format tsv --output out/filtered.tsv
```

Block POS values:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer sudachi --blocked-pos 補助記号 助詞 助動詞 --min-n 1 --max-n 2 --output-format tsv --output out/blocked_pos.tsv
```

Allow only selected POS values:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer sudachi --allowed-pos 名詞 動詞 形容詞 --min-n 1 --max-n 2 --output-format tsv --output out/allowed_pos.tsv
```

Token length filter:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer sudachi --min-token-length 2 --max-token-length 20 --min-n 1 --max-n 2 --output-format tsv --output out/token_length.tsv
```

Remove specific quote / bracket characters before tokenization:

```bash
ngram-builder --mode local --local-path data/wiki_local_export --text-column text --tokenizer sudachi --token-form surface --text-unit sentence --min-n 1 --max-n 3 --max-records 20000 --strip-chars '"〈〉『』「」' --drop-symbols --split-by-n --max-ngrams 50000 --max-ngrams-scope per-n --output-format tsv --output out/wiki_clean.tsv
```

This removes only the listed characters and keeps the inner text.

Example:

- `"&" を 加える ことも` -> `& を 加える ことも`
- `ノアール 出版 〈絶版〉` -> `ノアール 出版 絶版`
- `『鏡が来た 高橋留美子短編集』収録。` -> `鏡が来た 高橋留美子短編集収録。`

## Local cache and offline workflow example

First run:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode download --cache-dir .cache/hf --save-local-dir data/wiki_local_export --tokenizer sudachi --text-unit sentence --min-n 1 --max-n 3 --max-records 20000 --drop-symbols --split-by-n --max-ngrams 50000 --max-ngrams-scope per-n --output-format tsv --output out/wiki.tsv

ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode download --cache-dir .cache/hf --save-local-dir data/wiki_local_export --tokenizer sudachi --text-unit lemma --min-n 1 --max-n 3 --max-records 20000 --drop-symbols --split-by-n --max-ngrams 50000 --max-ngrams-scope per-n --output-format tsv --output out/wiki.tsv 
```

Later offline run:

```bash
ngram-builder --mode local --local-path data/wiki_local_export --text-column text --tokenizer sudachi --token-form lemma --text-unit sentence --min-n 1 --max-n 3 --max-records 20000 --drop-symbols --split-by-n --max-ngrams 50000 --max-ngrams-scope per-n --output-format tsv --output out/wiki_offline.tsv

ngram-builder --mode local --local-path data/wiki_local_export --text-column text --tokenizer sudachi --token-form lemma --text-unit sentence --min-n 1 --max-n 3 --max-records 20000 --drop-symbols --split-by-n --max-ngrams 50000 --max-ngrams-scope per-n --output-format tsv --output out/wiki_offline.tsv
```

## CLI options summary

### Input

- `--mode {streaming,download,local}`
- `--dataset DATASET_NAME`
- `--config-name CONFIG_NAME`
- `--split SPLIT`
- `--text-column COLUMN_NAME`
- `--local-path PATH`
- `--cache-dir PATH`
- `--save-local-dir PATH`
- `--force-redownload`

### Tokenization

- `--tokenizer {sudachi,fugashi,whitespace}`
- `--sudachi-split-mode {A,B,C}`
- `--token-form {surface,lemma}`

### Counting

- `--text-unit {document,sentence}`
- `--min-n INT`
- `--max-n INT`
- `--max-records INT`
- `--max-ngrams INT`
- `--max-ngrams-scope {overall,per-n}`
- `--split-by-n`

### Filtering

- `--drop-symbols`
- `--strip-chars CHARS`
- `--drop-numbers`
- `--allowed-pos POS [POS ...]`
- `--blocked-pos POS [POS ...]`
- `--min-token-length INT`
- `--max-token-length INT`

### Output

- `--output-format {tsv,sqlite}`
- `--output PATH`

## Notes

- `--max-records` limits how many input records are processed.
- `--max-ngrams` limits the final ranked rows after counting.
- In `streaming` mode, the whole dataset is not materialized locally.
- In `download` mode, Hugging Face caching is reused when possible.
- `--save-local-dir` is the clearest way to avoid Hub access on later runs.

```bash
ngram_builder_jp % ngram-builder --mode local --local-path data/wiki_local_export --text-column text --tokenizer ginza --ginza-model ja_ginza --token-form surface --text-unit sentence --min-n 1 --max-n 3 --max-records 100 --drop-symbols --split-by-n --max-ngrams 50000 --max-ngrams-scope per-n --output-format tsv --output out/wiki_offline.tsv --strip-chars '"〈〉『』「」'
```
