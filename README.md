# memtop

A tiny, single-file CLI that shows the top N processes by **RAM** or **CPU**, alongside a color-coded **memory and swap** summary.

It's a self-contained Python script with [PEP 723](https://peps.python.org/pep-0723/) inline dependencies, run via [uv](https://docs.astral.sh/uv/) — no virtualenv to manage, no `pip install`, no project setup. The dependencies live inside the file itself.

```
            Total       Used      Free   Available   Use%
 ─────────────────────────────────────────────────────────
  RAM    30.9 GiB   24.5 GiB   2.9 GiB     6.3 GiB    80%
  Swap    8.0 GiB    8.0 GiB   0.0 GiB           —   100%

                           Top 10 — RAM

     PID   User         Process                       RSS    RAM%
 ─────────────────────────────────────────────────────────────────
  222611   wfoschiera   next-server (v14.2.35)   3671 MiB   11.6%
   42980   root         bdsecd                   1089 MiB    3.4%
  424370   wfoschiera   python3 headroom.cli     1008 MiB    3.2%
   ...
```

## Features

- **Memory + swap summary** with color-coded usage (green / yellow / red).
- **`ram`** — top N processes sorted by resident memory (RSS).
- **`cpu`** — top N processes sorted by CPU usage, sampled over 1 second for accuracy. CPU% can exceed 100% on multi-core machines (per-core basis, like `top`).
- **Smart process names** — for generic interpreters (`node`, `python3`, `java`), shows the first meaningful command-line argument as a hint, so you can tell *which* node process is eating your RAM.
- Single file. Copy it anywhere uv is installed and it just runs.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (handles Python and dependencies automatically)
- Linux or macOS

uv transparently provisions a compatible Python and the script's dependencies (`psutil`, `rich`, `typer`) on first run, caching them for instant subsequent runs.

## Install

### Option A — quick (single file on your PATH)

```bash
# Download the script into a directory on your PATH
curl -fsSL https://raw.githubusercontent.com/wfoschiera/memtop/main/memtop \
  -o ~/.local/bin/memtop
chmod +x ~/.local/bin/memtop
```

Make sure `~/.local/bin` is on your `$PATH`. If it isn't, add this to your shell rc file:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Option B — clone the repo

```bash
git clone https://github.com/wfoschiera/memtop.git
cd memtop
ln -s "$PWD/memtop" ~/.local/bin/memtop   # symlink onto your PATH
```

The first run will download dependencies (~100 ms); every run after that is instant.

## Usage

```bash
memtop ram        # top 15 processes by RAM (default count)
memtop ram 5      # top 5 by RAM
memtop cpu        # top 15 by CPU (sampled over 1 s)
memtop cpu 20     # top 20 by CPU
memtop --help     # full help
```

### Flush a full swap (bonus tip)

`memtop` is handy for spotting why swap is full. To force the kernel to move swapped-out pages back into RAM (only when you have enough free RAM to absorb them):

```bash
sudo swapoff -a && sudo swapon -a
```

## How it works

The first line is a shebang:

```python
#!/usr/bin/env -S uv run --script
```

When you run `memtop`, the OS hands the file to `uv run --script`. uv reads the inline metadata block…

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["psutil", "rich", "typer"]
# ///
```

…builds (and caches) a throwaway environment with exactly those packages, and runs the script inside it. To Python, both the shebang and the metadata block are just comments.

## Contributing

Contributions are welcome — this started as a throwaway utility and is meant to grow.

1. **Fork** the repo and create a branch: `git checkout -b my-feature`.
2. Make your change in `memtop`. Keep it a single file unless there's a strong reason not to.
3. **Test locally**: `./memtop ram` and `./memtop cpu` should run cleanly.
4. If you add a dependency, add it to the `# /// script` block at the top of the file — not a `requirements.txt`.
5. Commit with a clear message and **open a pull request** describing what changed and why.

Ideas that would make good contributions:

- A `--json` / `--watch` output mode.
- Sort/filter by user, or exclude kernel threads.
- Per-process open file or thread counts.
- macOS-specific polish.

Please keep the dependency footprint small and the startup fast.

## License

[MIT](LICENSE) © William Foschiera
