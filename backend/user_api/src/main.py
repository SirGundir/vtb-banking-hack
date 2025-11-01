import click
import uvicorn
import yaml

import app_instance


@click.command(name='run_server')
def runserver():
    """Start API server."""
    server_config = dict(
        port=8000,
        host='0.0.0.0',
        lifespan='on'
    )
    server_config['reload'] = True
    server_config['log_level'] = 'info'
    uvicorn.run("app_instance:app", **server_config)


@click.command(name='dump_docs')
def dump_docs():
    with open('openapi/openapi.yaml', 'w') as f:
        yaml.dump(app_instance.app.openapi(), f, sort_keys=False)


@click.group()
def cli():
    """Initialize CLI."""


cli.add_command(runserver)
cli.add_command(dump_docs)

if __name__ == '__main__':
    cli()
