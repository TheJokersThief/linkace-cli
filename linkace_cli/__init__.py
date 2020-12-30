import sys
import typer
from rich import print
from rich.console import Console

from linkace_cli import models
from linkace_cli.api.links import Links


app = typer.Typer()
links = typer.Typer()
app.add_typer(links, name="link")

console = Console()


shared_ctx = {}


@links.command()
def get(
    id: int = None,
    order_by: models.OrderBy = None,
    order_dir: models.OrderDir = None,
    fetch_tags: bool = typer.Option(False, help="By default, no tag info is returned when getting all links. This fetches tag info for every link which can slow things down."),
    max_results: int = typer.Option(sys.maxsize, help="The max number of links to display.")
):
    api = Links(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])

    with console.status("[bold green]Getting links..."):
        if id:
            links = [api.get(id=id)]
        else:
            links = api.get(order_by=order_by, order_dir=order_dir)

    # Get number of digits of the highest index we'll print, add 1 to account for full stop after number
    number_length = len(str(len(links))) + 1
    for index, link in enumerate(links[0:max_results]):
        padding = f"{'':<{number_length}}"
        index_str = f"{str(index + 1) + '.':<{number_length}}"
        print(
            f"[bold blue]{index_str}[/bold blue] [bold green]{link['title']}[/bold green] [{link['id']}]"
        )

        if link.get('url', None):
            print(f"{padding} [red]>[/red] [yellow]{link['url']}[/yellow]")

        if fetch_tags:
            link['tags'] = api.get(id=link['id'])['tags']

        if link.get('tags', None):
            tags = ", ".join([tag['name'] for tag in link['tags']])
            print(f"{padding} [red]#[/red] {tags}")

        if link.get('description', None):
            print(f"{padding} [red]+[/red] {link['description']}")

        print()


@links.command()
def create():
    pass


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
    app()


if __name__ == "__main__":
    main()
