# pytest install trap on this machine - 2026-07-30

Dated additive note, 2026-07-30. Recorded after two sessions in a row got the wrong answer about whether this repo's test suite is runnable.

## The trap

`pytest` is installed on this machine, and `python3 -m pytest` still fails with `No module named pytest`. Both of these are true at once:

```bash
which pytest                        # /opt/homebrew/bin/pytest
pytest --version                    # pytest 9.1.1
python3 -c "import pytest"          # ModuleNotFoundError: No module named 'pytest'
```

Homebrew's `pytest` formula installs into its own isolated venv rather than into `/opt/homebrew/bin/python3`'s site-packages, so the `pytest` binary on `PATH` and the `python3` binary on `PATH` do not share a module namespace. Checking one tells you nothing about the other.

**Use the bare command, not the module form:**

```bash
cd /Users/juliandickie/code/humanise-copy && pytest -q
```

62 tests pass at 0.5.0. `python3 -m unittest discover -s tests -q` also works and gives the same 62, and is the fallback if `pytest` itself is ever missing from `PATH`.

## Why this is worth a note rather than just fixing it locally

A session on 27 July concluded "pytest is not installed" from `python3 -m pytest` failing, which was correct at the time. A session on 30 July, after pytest had been installed, made the same wrong inference from the same command and had to be corrected. The failure mode is that `python3 -m X` failing reads as "X is not installed" when on a Homebrew Python it can just as easily mean "X is installed somewhere the M flag can't see." Check `which <tool>` before concluding a tool is missing, not just the module form.
