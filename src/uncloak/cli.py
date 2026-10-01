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
def generate(url: str, output: str = "client.py") -> None:
    """
    Generate a client from a URL or HAR file.
    """
    import datetime

    from uncloak.analyzer import extract_params
    from uncloak.emitter import emit_client
    from uncloak.filters import filter_captures
    from uncloak.har import load_har
    from uncloak.models import Contract
    from uncloak.ranker import group_by_endpoint, rank_candidates
    from uncloak.recorder import record_har
    from uncloak.schema import infer_array_path, infer_schema

    console.print(f"Recording HAR for {url}...")
    har_path = "temp_capture.har"

    # Simple check if it's a local HAR file vs a URL
    if url.endswith(".har"):
        har_path = url
    else:
        record_har(url, har_path)

    console.print("Processing captures...")
    captures = load_har(har_path)
    filtered = filter_captures(captures)

    candidates = group_by_endpoint(filtered)
    ranked = rank_candidates(candidates)

    if not ranked:
        console.print("[bold red]Error:[/bold red] No valid API endpoints found.")
        raise typer.Exit(1)

    best = ranked[0]
    endpoint = extract_params(best)
    schema = infer_schema(best.captures)

    contract = Contract(
        version=1,
        uncloak_version=__version__,
        generated_at=datetime.datetime.now().isoformat(),
        endpoint=endpoint,
        response_schema=schema,
        fields={},
        array_path=infer_array_path(schema),
    )

    code = emit_client(contract, "ApiClient")
    with open(output, "w", encoding="utf-8") as f:
        f.write(code)

    console.print(f"[bold green]Success![/bold green] Generated {output}")
