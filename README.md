# ngram-builder

A configurable CLI tool to build Japanese n-gram dictionaries from Hugging Face datasets or local text sources.

## What changed in this version

This version switches the recommended Japanese tokenizer from plain Sudachi token output to **GiNZA bunsetsu API**.

Why:

- Sudachi token-level n-grams often produce fragmented patterns like `さ れ て い た`
- GiNZA provides **bunsetsu spans** (`ginza.bunsetu_spans(...)`), which are much closer to natural Japanese phrase units ([official docs](https://github.com/megagonlabs/ginza/blob/develop/docs/index.md), [bunsetu API overview](https://github.com/megagonlabs/ginza/blob/develop/docs/bunsetu_api.md))
- GiNZA standard model installation is officially `pip install -U ginza ja_ginza` ([official README](https://github.com/megagonlabs/ginza/blob/develop/README.md?plain=1))

## Features

- Build unigram through any `n` range
- Use Hugging Face datasets in `streaming` or cached `download` mode
- Read local text / jsonl / json / parquet / csv files with `--mode local`
- Recommended tokenizer: **GiNZA bunsetsu API**
- Optional tokenizer backends: `sudachi`, `fugashi`, `whitespace`
- Count by `surface` or `lemma`
- Split output by `n`
- Limit top results either `overall` or `per-n`
- Save a downloaded dataset to local files for later offline reuse
- Control Hugging Face cache directory and force redownload when needed

## Installation

### With uv

```bash
uv venv && source .venv/bin/activate && uv pip install -e .
```

### Install GiNZA bunsetsu support

Official GiNZA standard model installation is `pip install -U ginza ja_ginza`. ([official README](https://github.com/megagonlabs/ginza/blob/develop/README.md?plain=1))

With this project:

```bash
uv pip install -e '.[ginza]'
```

If you prefer pip directly:

```bash
pip install -U ginza ja_ginza
```

### Optional fugashi backend

```bash
uv pip install -e .[fugashi]
```

## Recommended usage: natural Japanese phrase n-grams

Build bunsetsu-level n-grams with GiNZA from Hugging Face data:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer ginza --ginza-model ja_ginza --token-form surface --text-unit sentence --min-n 1 --max-n 3 --max-records 10000 --drop-symbols --output-format tsv --output out/wiki_phrase.tsv
```

This is the main difference from the previous version:

- old approach: Sudachi token-level n-grams
- new recommended approach: **GiNZA bunsetsu-level n-grams**

## Split output by n

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer ginza --ginza-model ja_ginza --token-form surface --text-unit sentence --min-n 1 --max-n 3 --max-records 10000 --drop-symbols --split-by-n --output-format tsv --output out/wiki_phrase.tsv
```

Output:

- `out/wiki_phrase.1gram.tsv`
- `out/wiki_phrase.2gram.tsv`
- `out/wiki_phrase.3gram.tsv`

## Limit top results overall

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer ginza --ginza-model ja_ginza --token-form surface --text-unit sentence --min-n 1 --max-n 3 --max-records 10000 --drop-symbols --max-ngrams 100000 --max-ngrams-scope overall --split-by-n --output-format tsv --output out/wiki_phrase.tsv
```

## Limit top results per n

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer ginza --ginza-model ja_ginza --token-form surface --text-unit sentence --min-n 1 --max-n 3 --max-records 10000 --drop-symbols --max-ngrams 100000 --max-ngrams-scope per-n --split-by-n --output-format tsv --output out/wiki_phrase.tsv
```

## Count by lemma at bunsetsu level

```bash
ngram-builder --mode local --local-path data/wiki_local_export --text-column text --tokenizer ginza --ginza-model ja_ginza --token-form lemma --text-unit sentence --min-n 1 --max-n 3 --max-records 5000 --drop-symbols --output-format tsv --output out/wiki_phrase_lemma.tsv
```

With GiNZA bunsetsu mode:

- `surface` joins the surface forms inside each bunsetsu span
- `lemma` joins the token lemmas inside each bunsetsu span

## Cached download mode

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode download --cache-dir .cache/hf --save-local-dir data/wiki_local_export --tokenizer ginza --ginza-model ja_ginza --token-form surface --text-unit sentence --min-n 1 --max-n 3 --max-records 20000 --drop-symbols --split-by-n --max-ngrams 50000 --max-ngrams-scope per-n --output-format tsv --output out/wiki.tsv
```

## Offline local reuse

```bash
ngram-builder --mode local --local-path data/wiki_local_export --text-column text --tokenizer ginza --ginza-model ja_ginza --token-form surface --text-unit sentence --min-n 1 --max-n 3 --max-records 20000 --drop-symbols --split-by-n --max-ngrams 50000 --max-ngrams-scope per-n --output-format tsv --output out/wiki_offline.tsv

```

## Use Sudachi token-level mode explicitly

If you still want the old token-level behavior:

```bash
ngram-builder --mode local --local-path data/wiki_local_export --text-column text --tokenizer sudachi --sudachi-split-mode C --token-form surface --text-unit sentence --min-n 1 --max-n 3 --max-records 5000 --drop-symbols --output-format tsv --output out/wiki_sudachi.tsv
```

## SQLite output

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer ginza --ginza-model ja_ginza --token-form surface --text-unit sentence --min-n 1 --max-n 3 --max-records 10000 --drop-symbols --output-format sqlite --output out/wiki_phrase.sqlite
```

## Filters

Drop symbols and numbers:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer ginza --ginza-model ja_ginza --drop-symbols --drop-numbers --min-n 1 --max-n 2 --output-format tsv --output out/filtered.tsv
```

Block POS values:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer ginza --ginza-model ja_ginza --blocked-pos PUNCT 助動詞 --min-n 1 --max-n 2 --output-format tsv --output out/blocked_pos.tsv
```

Allow only selected POS values:

```bash
ngram-builder --dataset hpprc/wikipedia-20240101 --split train --text-column text --mode streaming --tokenizer ginza --ginza-model ja_ginza --allowed-pos NOUN VERB ADJ ADV --min-n 1 --max-n 2 --output-format tsv --output out/allowed_pos.tsv
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

- `--tokenizer {ginza,sudachi,fugashi,whitespace}`
- `--ginza-model MODEL_NAME`
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
- GiNZA v5.1+ requires installing both `ginza` and a model package such as `ja_ginza` or `ja_ginza_electra`. ([official docs](https://github.com/megagonlabs/ginza/blob/develop/docs/index.md))
