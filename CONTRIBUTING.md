# Contributing

Thanks for helping improve these demos. They're teaching material, so the best changes keep them short, correct and easy to follow.

## Ground rules

- Keep each demo a single, self-contained script that matches the code shown in the session.
- Keep pin numbers and defaults in line with the [wiring guide](docs/wiring.md).
- Add or update tests for every change in behaviour.
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Set up

You need Python 3.11 or newer on Linux or macOS. On Windows, use WSL.

```bash
git clone https://github.com/sakar-rahulkatiyar/Beyond_the_laptop_session.git
cd Beyond_the_laptop_session
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install   # runs the checks on every commit
```

## Run the checks

CI runs these on every push and pull request. Run them before you open one:

```bash
ruff check .
ruff format --check .
mypy
pytest
shellcheck scripts/*.sh
```

The tests use gpiozero's mock pins, so you don't need a Raspberry Pi. If you change how a demo talks to hardware, please also try it on a real Pi.

## Style

- Python is linted and formatted with [Ruff](https://docs.astral.sh/ruff/), configured in `pyproject.toml`.
- Every function has type hints and a Google-style docstring; mypy runs in strict mode.
- Shell scripts start with `#!/usr/bin/env bash` and `set -euo pipefail`, and pass ShellCheck.
- Comments and docs use plain English that a first-year student can follow.

## Commits and pull requests

- Write commit messages in the [Conventional Commits](https://www.conventionalcommits.org/) style, for example `fix: debounce the button by default`.
- Keep each pull request to one topic. Say what changed and how you tested it.
- Add a line to `CHANGELOG.md` under **Unreleased**.
