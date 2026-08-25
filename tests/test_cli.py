"""
Tests for Octo Harness CLI interface.
"""

import pytest
from octo_harness.cli.main import create_parser, main


def test_cli_parser_help():
    parser = create_parser()
    with pytest.raises(SystemExit) as exc:
        parser.parse_args(["--help"])
    assert exc.value.code == 0


def test_cli_models_command():
    ret = main(["--mock", "models"])
    assert ret == 0


def test_cli_pulse_command():
    ret = main(["--mock", "pulse"])
    assert ret == 0


def test_cli_route_command():
    ret = main(["--mock", "route", "Explain Python generators in detail", "--strategy", "grok_primary"])
    assert ret == 0


def test_cli_cowork_command():
    ret = main(["--mock", "cowork", "Design a cache warming daemon"])
    assert ret == 0


def test_cli_consensus_command():
    ret = main(["--mock", "consensus", "What is the best DB for time series data?"])
    assert ret == 0
