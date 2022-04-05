import click

from app.database import recreate_db
from app.logger import init_logger


@click.command()
@click.option('--recreate', is_flag=True)
@click.option('--testing', is_flag=True)
def cli_handler(recreate: bool, testing: bool) -> None:
    if recreate:
        recreate_db(testing)


if __name__ == '__main__':
    init_logger()
    # ignore pylint, because it doesn't know about click's parameters
    cli_handler()  # pylint: disable=no-value-for-parameter
