import requests
import typer

from rich import print
from rich.console import Console
from rich.panel import Panel

from linkace_cli.cli.links import links_cli
from linkace_cli.cli.helpers import shared_ctx

app = typer.Typer()
app.add_typer(links_cli, name="link")

console = Console()


@app.callback()
def callback(
    api_url: str = typer.Option(..., help="e.g. http://example.com/api/v1/"),
    api_token: str = typer.Option(...)
):
    """
    Interact with the LinkAce API
    """
    shared_ctx['api_url'] = api_url
    shared_ctx['api_token'] = api_token


def main():
    try:
        app()
    except requests.exceptions.HTTPError as e:
        try:
            error = e.response.json()
            print(Panel(f"[red]{error['message']}[/red] \nErrors: {str(error['errors'])}", title="Error"))
        except Exception:
            print(Panel(str(e), title="Error"))


if __name__ == "__main__":
    main()
