import click

from app.database import recreate_db


@click.command()
@click.option('--recreate', is_flag=True)
@click.option('--testing', is_flag=True)
def cli_handler(recreate: bool, testing: bool) -> None:
    if recreate:
        recreate_db(testing)
