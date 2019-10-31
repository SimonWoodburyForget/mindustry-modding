import click
import parser
import pyperclip
from pathlib import Path

@click.group()
def cli():
    pass

@cli.command()
def definitions():
    """ Converts Mindustry attribute decelleration 
    into a Markdown table. """
    i = pyperclip.paste()
    o = parser.build_definition_table(i)
    pyperclip.copy(o)
    click.echo(o)

@cli.command()
def defaults():
    """ Converts Mindustry attribute decelleration 
    into a Markdown table. """
    i = pyperclip.paste()
    o = parser.build_defaults_table(i)
    pyperclip.copy(o)
    click.echo(o)

@cli.command()
@click.argument("path")
def contents(path):
    """ Makes content table out of org file. """
    path = Path(path)
    with open(path, "r") as f:
        i = f.read()
    o = parser.build_content_tables(i)
    click.echo(o)

cli()
