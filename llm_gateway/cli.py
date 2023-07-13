import click


@click.group(no_args_is_help=True)
def cli():
    pass


@cli.command("start")
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
def start(
    host=None,
    port=None,
):
    import uvicorn

    host = host or "127.0.0.1"
    port = 5000 if port is None else port
    uvicorn.run("llm_gateway.app:app", host=host, port=port, log_level="info")


if __name__ == "__main__":
    cli()
