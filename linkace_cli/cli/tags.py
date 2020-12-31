import sys
import toml
import typer
from rich import print
from rich.console import Console

from linkace_cli import models
from linkace_cli.api.tags import Tags
from linkace_cli.cli.helpers import interactive_editor, shared_ctx

tags_cli = typer.Typer()
console = Console()


def print_tags(tags: list):
    """
    Prints a list of tag models in a consistent and (hopefully) pretty way
    """
    # Get number of digits of the highest index we'll print, add 1 to account for full stop after number
    number_length = len(str(len(tags))) + 1
    for index, link in enumerate(tags):
        index_str = f"{str(index + 1) + '.':<{number_length}}"
        print(
            f"[bold blue]{index_str}[/bold blue] [bold green]{link['name']}[/bold green] [{link['id']}]"
        )


@tags_cli.command()
def get(
    id: int = None,
    order_by: models.OrderBy = None,
    order_dir: models.OrderDir = None,
    max_results: int = typer.Option(sys.maxsize, help="The max number of tags to display.")
):
    """
    Get all tags or, if --id is provided, get the details of just one tag.
    """
    api = Tags(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])

    with console.status("[bold green]Getting tags..."):
        if id:
            tags = [api.get(id=id)]
        else:
            tags = api.get(order_by=order_by, order_dir=order_dir)

    print_tags(tags[0:max_results])


@tags_cli.command()
def create(
    interactive: bool = typer.Option(False, help="Interactively create a tag, uses your chosen EDITOR"),
    name: str = None,
    is_private: bool = False,
):
    """
    Create a new tag with the info provided. Use the --interactive flag to open your environment's
    $EDITOR. Any info provided via flags will prefill values in the interactive mode.
    """
    api = Tags(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])

    obj = {
        "name": name,
        "is_private": is_private,
    }

    if interactive or not name:
        edited_str = interactive_editor('tag.toml', prefill_data=obj)
        obj = toml.loads(edited_str)

    with console.status("[bold green]Creating tag..."):
        resp = api.create(obj)

    obj = models.Tag().load(resp)
    print_tags([obj])


@tags_cli.command()
def delete(
    id: int = typer.Option(...)
):
    """
    Delete a tag with the given ID
    """
    api = Tags(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])
    with console.status("[bold green]Deleting Tag..."):
        api.delete(id)
    print("[bold green]Tag deleted successfully[/bold green]")


@tags_cli.command()
def update(
    id: int = typer.Option(...),
    interactive: bool = typer.Option(False, help="Interactively update a tag, uses your chosen EDITOR"),
    name: str = None,
    is_private: bool = False,
):
    """
    Update a tag with the info provided. Use the --interactive flag to open it in your environment's
    $EDITOR. Any info provided via flags will prefill values in the interactive mode.
    """
    api = Tags(base_url=shared_ctx['api_url'], api_token=shared_ctx['api_token'])

    with console.status("[bold green]Getting tag info..."):
        obj = api.get(id=id)

    provided_info = {
        "name": name,
        "is_private": is_private,
    }
    # Merge provided values
    for key, val in provided_info.items():
        if val:
            obj[key] = val

    obj = {key: obj[key] for key in provided_info.keys()}

    if interactive:
        edited_str = interactive_editor('tag.toml', prefill_data=obj)
        obj = toml.loads(edited_str)

    with console.status("[bold green]Updating tag..."):
        resp = api.update(id, obj)

    obj = models.Tag().load(resp)
    print_tags([obj])
