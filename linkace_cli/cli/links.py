import sys
import toml
import typer
from rich import print
from rich.console import Console

from linkace_cli import models
from linkace_cli.api.links import Links
from linkace_cli.cli.helpers import interactive_editor, shared_ctx

links_cli = typer.Typer()
console = Console()


def print_links(links: list):
    # Get number of digits of the highest index we'll print, add 1 to account for full stop after number
    number_length = len(str(len(links))) + 1
    for index, link in enumerate(links):
        padding = f"{'':<{number_length}}"
        index_str = f"{str(index + 1) + '.':<{number_length}}"
        print(
            f"[bold blue]{index_str}[/bold blue] [bold green]{link['title']}[/bold green] [{link['id']}]"
        )

        if link.get('url', None):
            print(f"{padding} [red]>[/red] [yellow]{link['url']}[/yellow]")

        if link.get('tags', None):
            tags = ", ".join([tag['name'] for tag in link['tags']])
            print(f"{padding} [red]#[/red] {tags}")

        if link.get('description', None):
            print(f"{padding} [red]+[/red] {link['description']}")
        # Add a newline after every link
        print()


@links_cli.command()
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

            if fetch_tags:
                # Make individual requests to fetch tag data
                fetched_links = []
                for link in links[0:max_results]:
                    link['tags'] = api.get(id=link['id'])['tags']
                    fetched_links.append(link)
                links = fetched_links

    print_links(links[0:max_results])


@links_cli.command()
def create(
    interactive: bool = typer.Option(False, help="Interactively create a link, uses your chosen EDITOR"),
    title: str = None,
    url: str = None,
    description: str = None,
    tags: str = typer.Option(None, help="Comma-separated tags"),
    lists: str = typer.Option(None, help="Comma-separated lists"),
    is_private: bool = False,
    check_disabled: bool = False
):
    api = Links(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])

    link = {
        "title": title,
        "url": url,
        "description": description,
        "tags": tags,
        "lists": lists,
        "is_private": is_private,
        "check_disabled": check_disabled,
    }

    if interactive or not (title and url):
        edited_str = interactive_editor('link.toml', prefill_data=link)
        link = toml.loads(edited_str)

    with console.status("[bold green]Creating link..."):
        resp = api.create(link)

    link = models.Link().load(resp)
    print_links([link])


@links_cli.command()
def delete(
    id: int
):
    api = Links(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])
    with console.status("[bold green]Deleting link..."):
        api.delete(id)
    print("[bold green]Link deleted successfully[/bold green]")


@links_cli.command()
def update(
    id: int = typer.Option(...),
    interactive: bool = typer.Option(False, help="Interactively create a link, uses your chosen EDITOR"),
    title: str = None,
    url: str = None,
    description: str = None,
    tags: str = typer.Option(None, help="Comma-separated tags"),
    lists: str = typer.Option(None, help="Comma-separated lists"),
    is_private: bool = False,
    check_disabled: bool = False
):
    api = Links(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])

    with console.status("[bold green]Getting link info..."):
        link = api.get(id=id)

    provided_info = {
        "title": title,
        "url": url,
        "description": description,
        "tags": tags,
        "lists": lists,
        "is_private": is_private,
        "check_disabled": check_disabled,
    }
    # Merge provided values
    for key, val in provided_info.items():
        if val:
            link[key] = val

    link['tags'] = ", ".join([tag['name'] for tag in link['tags']])
    link['lists'] = ", ".join([alist['name'] for alist in link['lists']])

    if interactive:
        edited_str = interactive_editor('link.toml', prefill_data=link)
        link = toml.loads(edited_str)

    with console.status("[bold green]Creating link..."):
        resp = api.update(id, link)

    link = models.Link().load(resp)
    print_links([link])
