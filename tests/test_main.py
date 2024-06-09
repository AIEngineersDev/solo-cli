from typer.testing import CliRunner
from solo_cli.main import app

runner = CliRunner()

def test_init():
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
    assert "llava-v1.5-7b-q4.llamafile downloaded successfully." in result.output

def test_quickstart():
    result = runner.invoke(app, ["quickstart"])
    assert result.exit_code == 0
