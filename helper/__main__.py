import click
import parser
import pyperclip
from pathlib import Path
import msch as msch_
from msch import Schematic, Schematics
from jinja2 import Template
from textwrap import dedent

WEBSITE = "https://simonwoodburyforget.github.io/mindustry-modding/"

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
@click.option("-i", "--input", help="The input org file.")
@click.option("-t", "--template", help="The template org file.")
@click.option("-o", "--output", help="The rendered org file.")
def contents(input, template, output):
    """ Generate content table README. """
    template = Template(
        dedent('''
        * Overview
        
        Checkout the website here: {{ website }}
        
        Content Table:
        
        {{ content_table }}

        '''))

    with open(input, "r") as f:
        i = f.read()
        o = parser.build_content_tables(i)
        r = template.render(content_table=o,
                            website=WEBSITE)

    # TODO: load template from file

    with open(output, "w") as f:
        print(r, file=f)

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
