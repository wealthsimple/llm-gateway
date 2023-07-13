from typing import Optional

import click


def _llm_gateway_version() -> str:
    try:
        import pkg_resources

        return pkg_resources.get_distribution("llm-gateway").version
    except ImportError:
        return "0.0.0"


@click.group(no_args_is_help=True)
@click.version_option(version=_llm_gateway_version(), message="%(version)s")
def cli():
    """LLM-Gateway command line tool"""
    pass


@cli.command("up")
@click.option(
    "--host",
    type=str,
    help="Start the app at this host. Default: 127.0.0.1",
)
@click.option(
    "--port",
    type=int,
    help="Start the app at this port. Default: 5000",
)
def up(
    host: Optional[str] = None,
    port: Optional[int] = None,
) -> None:
    """Start LLM-Gateway Services"""
    import uvicorn

    host = host or "127.0.0.1"
    port = 5000 if port is None else port
    uvicorn.run("llm_gateway.app:app", host=host, port=port, log_level="info")


if __name__ == "__main__":
    cli()
