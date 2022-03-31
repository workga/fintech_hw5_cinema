from app.cli import cli_handler
from app.logger import init_logger

if __name__ == '__main__':
    init_logger()
    # ignore pylint, because it doesn't know about click's parameters
    cli_handler()  # pylint: disable=no-value-for-parameter
