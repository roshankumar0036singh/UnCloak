from typer.testing import CliRunner
from uncloak.cli import app

runner = CliRunner()

def test_scoreboard():
    result = runner.invoke(app, ["check", "--fixtures-dir", "tests/fixtures"])
    assert result.exit_code == 0
    assert "Score: 5/5" in result.stdout
