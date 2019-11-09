import click
import parser
import pyperclip
from pathlib import Path
import msch as msch_
from msch import Schematic, Schematics

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

@cli.command()
@click.argument("msch-text")
@click.option("--old", prompt="New blocks name")
@click.option("--new", prompt="Old blocks name")
def msch(msch_text, old, new):
    """ Replaces one block with another within a schematic. """
    schems = msch_.load(msch_text)
    schems = Schematics(schems.width,
                        schems.height,
                        schems.tags,
                        [ Schematic(new, *s[1:]) if s.name == old else s
                          for s in schems.tiles ])
    click.echo(msch_.dump(schems, True))

if __name__ == '__main__':
    cli()
