from typing import Annotated

import typer
from rich.console import Console

from uncloak import __version__

app = typer.Typer(help="Point it at a URL, get a working typed API client.")
console = Console()


def version_callback(value: bool) -> None:
    if value:
        console.print(
            f"[bold blue]uncloak[/bold blue] version: [green]{__version__}[/green]"
        )
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            is_eager=True,
            help="Print the version and exit",
        ),
    ] = False,
) -> None:
    pass


@app.command()
def generate(url: str) -> None:
    """
    Generate a client from a URL or HAR file.
    """
    console.print(
        f"[bold red]Not implemented:[/bold red] "
        f"uncloak generate for {url} is not yet implemented.",
        style="red",
    )
    raise typer.Exit(code=1)
