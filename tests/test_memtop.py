"""Base test suite for memtop.

The ``memtop`` script has no ``.py`` extension and carries a shebang plus a
PEP 723 metadata block at the top. Both are comments to Python, so the file
imports cleanly once its dependencies are present. We load it by path.
"""

import importlib.machinery
import importlib.util
from pathlib import Path

import pytest
from typer.testing import CliRunner

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "memtop"


def _load_memtop():
    loader = importlib.machinery.SourceFileLoader("memtop", str(SCRIPT_PATH))
    spec = importlib.util.spec_from_loader("memtop", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


memtop = _load_memtop()
runner = CliRunner()


def test_script_file_exists():
    assert SCRIPT_PATH.is_file()


def test_fmt_gib():
    assert memtop._fmt_gib(1024**3) == "1.0 GiB"
    assert memtop._fmt_gib(0) == "0.0 GiB"
    # 1.5 GiB
    assert memtop._fmt_gib(int(1.5 * 1024**3)) == "1.5 GiB"


@pytest.mark.parametrize(
    "pct,expected_color",
    [
        (10.0, "green"),
        (59.9, "green"),
        (60.0, "yellow"),
        (79.9, "yellow"),
        (80.0, "red"),
        (99.0, "red"),
    ],
)
def test_pct_color_thresholds(pct, expected_color):
    assert expected_color in memtop._pct_color(pct)


def test_ram_command_runs():
    result = runner.invoke(memtop.app, ["ram", "3"])
    assert result.exit_code == 0
    assert "RAM" in result.stdout
    assert "Top 3" in result.stdout


def test_help_runs():
    result = runner.invoke(memtop.app, ["--help"])
    assert result.exit_code == 0
    assert "ram" in result.stdout
    assert "cpu" in result.stdout
