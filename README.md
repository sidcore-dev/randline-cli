# randline-cli

A small, dependency-free command-line tool that picks N random lines from
a file or stdin, without replacement, using true single-pass reservoir
sampling.

## Why

The obvious way to grab random lines — read everything into a list, then
`random.sample` it — requires the whole input to fit in memory. `randline-cli`
uses reservoir sampling (Algorithm R) instead: it streams through the input
exactly once, keeping only `n` candidates in memory at any time, so it works
correctly even on inputs too large to load twice (or even once) into RAM.

## Install

```bash
pip install .
```

This installs a `randline-cli` command on your PATH.

## Usage

```bash
$ printf 'apple\nbanana\ncherry\ndate\nelderberry\n' | randline-cli -n 2 --seed 1
banana
elderberry
```

Read from a file instead of stdin:

```bash
randline-cli access.log -n 10
```

Reproducible output with `--seed`:

```bash
randline-cli big-file.txt -n 5 --seed 42
randline-cli big-file.txt -n 5 --seed 42   # same 5 lines, same order
```

### Options

| Flag             | Description                                          |
|------------------|-------------------------------------------------------|
| `file`           | Path to read lines from (default: stdin)              |
| `-n`, `--number` | Number of lines to pick (default: 1)                   |
| `--seed`         | Random seed, for reproducible output                   |

### Behavior notes

- If the input has fewer than `n` lines, every line is printed (in the
  order it appeared).
- Selection is genuinely without replacement — no line is ever picked twice.
- Without `--seed`, output varies run to run, as expected for random sampling.

### Exit codes

- `0` — completed successfully
- `2` — the input file couldn't be read, or `-n` was negative

## Development

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## License

All rights reserved. This code is public for viewing and reference only —
no license is granted to use, copy, modify, or redistribute it. See
[LICENSE](LICENSE) for details.
