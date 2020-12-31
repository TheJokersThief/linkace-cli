import os
import requests
import sys
import toml
import typer

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.traceback import install

from linkace_cli.cli.links import links_cli
from linkace_cli.cli.lists import lists_cli
from linkace_cli.cli.tags import tags_cli
from linkace_cli.cli.search import search_cli
from linkace_cli.cli.helpers import shared_ctx

app = typer.Typer()
app.add_typer(links_cli, name="link")
app.add_typer(lists_cli, name="list")
app.add_typer(tags_cli, name="tag")
app.add_typer(search_cli, name="search")

console = Console()
install()


@app.callback()
def callback(
    api_url: str = typer.Option(None, help="e.g. http://example.com/api/v1/"),
    api_token: str = typer.Option(None)
):
    """
    Interact with the LinkAce API
    """
    home = os.environ.get('HOME', '~/')

    if not os.path.exists(f"{home}/.config/linkace-cli"):
        os.makedirs(f"{home}/.config/linkace-cli")
    config_file = f"{home}/.config/linkace-cli/config.toml"

    config = None
    if os.path.isfile(config_file):
        with open(config_file) as file:
            config = toml.load(file)
            shared_ctx['api_url'] = config['api_url']
            shared_ctx['api_token'] = config['api_token']

    if not config and not api_url and not api_token:
        print(f'[bold red]Please either create a config file in {config_file} with the API URL and token or provide the --api-url and --api-token flags[/bold red]')
        sys.exit(1)

    if api_url:
        shared_ctx['api_url'] = api_url
    if api_token:
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
