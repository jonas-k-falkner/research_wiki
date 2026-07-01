from __future__ import annotations

from unittest.mock import patch

import pytest

from wikitools.cli import main

_SUBCOMMANDS = ("lint", "toc", "extract", "import", "index", "search", "check")


def test_help_exits_zero(capsys):
    with patch("sys.argv", ["wiki", "--help"]), pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 0


def test_help_lists_all_subcommands(capsys):
    with patch("sys.argv", ["wiki", "--help"]), pytest.raises(SystemExit):
        main()
    out = capsys.readouterr().out
    for cmd in _SUBCOMMANDS:
        assert cmd in out, f"subcommand '{cmd}' missing from --help output"


def test_unknown_subcommand_exits_nonzero(capsys):
    with patch("sys.argv", ["wiki", "not-a-real-command"]), pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code != 0


def test_check_requires_subcommand(capsys):
    with patch("sys.argv", ["wiki", "check"]), pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code != 0
