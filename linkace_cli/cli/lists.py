import sys
import toml
import typer
from rich import print
from rich.console import Console

from linkace_cli import models
from linkace_cli.api.lists import Lists
from linkace_cli.cli.helpers import interactive_editor, shared_ctx

lists_cli = typer.Typer()
console = Console()


def print_lists(lists: list):
    """
    Prints a list of link models in a consistent and (hopefully) pretty way
    """
    # Get number of digits of the highest index we'll print, add 1 to account for full stop after number
    number_length = len(str(len(lists))) + 1
    for index, link in enumerate(lists):
        padding = f"{'':<{number_length}}"
        index_str = f"{str(index + 1) + '.':<{number_length}}"
        print(
            f"[bold blue]{index_str}[/bold blue] [bold green]{link['name']}[/bold green] [{link['id']}]"
        )

        if link.get('description', None):
            print(f"{padding} [red]+[/red] {link['description']}")
        # Add a newline after every list
        print()


@lists_cli.command()
def get(
    id: int = None,
    order_by: models.OrderBy = None,
    order_dir: models.OrderDir = None,
    max_results: int = typer.Option(sys.maxsize, help="The max number of lists to display.")
):
    """
    Get all lists or, if --id is provided, get the details of just one link.
    """
    api = Lists(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])

    with console.status("[bold green]Getting links..."):
        if id:
            lists = [api.get(id=id)]
        else:
            lists = api.get(order_by=order_by, order_dir=order_dir)

    print_lists(lists[0:max_results])


@lists_cli.command()
def create(
    interactive: bool = typer.Option(False, help="Interactively create a link, uses your chosen EDITOR"),
    name: str = None,
    description: str = None,
    is_private: bool = False,
):
    """
    Create a new link with the info provided. Use the --interactive flag to open your environment's
    $EDITOR. Any info provided via flags will prefill values in the interactive mode.
    """
    api = Lists(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])

    obj = {
        "name": name,
        "description": description,
        "is_private": is_private,
    }

    if interactive or not name:
        edited_str = interactive_editor('list.toml', prefill_data=obj)
        obj = toml.loads(edited_str)

    with console.status("[bold green]Creating list..."):
        resp = api.create(obj)

    obj = models.List().load(resp)
    print_lists([obj])


@lists_cli.command()
def delete(
    id: int = typer.Option(...)
):
    """
    Delete a link with the given ID
    """
    api = Lists(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])
    with console.status("[bold green]Deleting List..."):
        api.delete(id)
    print("[bold green]List deleted successfully[/bold green]")


@lists_cli.command()
def update(
    id: int = typer.Option(...),
    interactive: bool = typer.Option(False, help="Interactively update a list, uses your chosen EDITOR"),
    name: str = None,
    description: str = None,
    is_private: bool = False,
):
    """
    Update a list with the info provided. Use the --interactive flag to open it in your environment's
    $EDITOR. Any info provided via flags will prefill values in the interactive mode.
    """
    api = Lists(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])

    with console.status("[bold green]Getting list info..."):
        obj = api.get(id=id)

    provided_info = {
        "name": name,
        "description": description,
        "is_private": is_private,
    }
    # Merge provided values
    for key, val in provided_info.items():
        if val:
            obj[key] = val

    obj = {key: obj[key] for key in provided_info.keys()}

    if interactive:
        edited_str = interactive_editor('list.toml', prefill_data=obj)
        obj = toml.loads(edited_str)

    with console.status("[bold green]Updating list..."):
        resp = api.update(id, obj)

    obj = models.List().load(resp)
    print_lists([obj])
