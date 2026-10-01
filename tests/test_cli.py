import pytest
from typer.testing import CliRunner
from uncloak.cli import app
from uncloak import __version__

runner = CliRunner()

def test_cli_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout

def test_cli_generate_not_implemented():
    result = runner.invoke(app, ["generate", "https://example.com"])
    assert result.exit_code != 0
    assert "not implemented" in result.stdout.lower()
