import typer
from rich import print
from rich.console import Console

from linkace_cli.api.search import Search
from linkace_cli.cli.helpers import shared_ctx
from linkace_cli.cli.links import print_links

search_cli = typer.Typer()
console = Console()


@search_cli.command()
def by_tag(
    exact: int = typer.Option(None, help="A numeric tag ID"),
    query: str = typer.Option(None, help="A search query for the tag name")
):
    """
    Search for links with tags
    """
    api = Search(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])

    if not exact and not query:
        print('[bold red]You have to supply either an exact match or a query[/bold red]')
        return

    with console.status("[bold green]Searching..."):
        if query:
            links = api.get_links_by_tag_query(query)
        else:
            links = api.get_links_by_tag_exact(exact)
    print_links(links)


@search_cli.command()
def by_list(
    exact: int = typer.Option(None, help="A numeric list ID"),
    query: str = typer.Option(None, help="A search query for the list name")
):
    """
    Search for links in lists
    """
    api = Search(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])

    if not exact and not query:
        print('[bold red]You have to supply either an exact match or a query[/bold red]')
        return

    with console.status("[bold green]Searching..."):
        if query:
            links = api.get_links_by_list_query(query)
        else:
            links = api.get_links_by_list_exact(exact)
    print_links(links)


@search_cli.command()
def by_query(
    query: str = typer.Option(...)
):
    """
    Search for tags by query
    """
    api = Search(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])
    with console.status("[bold green]Searching..."):
        links = api.get_links_by_query(query)
    print_links(links)
