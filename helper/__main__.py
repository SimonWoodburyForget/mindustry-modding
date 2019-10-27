import click
import parser


@click.group()
def cli():
    pass

@cli.command()
@click.argument("java")
def java_to_table(java):
    """ Converts Mindustry attribute decelleration 
    into a Markdown table. """
    click.echo(java)

cli()
