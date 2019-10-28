import click
import parser
import pyperclip

@click.group()
def cli():
    pass

@cli.command()
def java_to_table():
    """ Converts Mindustry attribute decelleration 
    into a Markdown table. """
    i = pyperclip.paste()
    o = parser.build_table(i)
    pyperclip.copy(o)
    click.echo(o)

@cli.command()
def to_defaults():
    """ Converts Mindustry attribute decelleration 
    into a Markdown table. """
    i = pyperclip.paste()
    o = parser.build_defaults(i)
    pyperclip.copy(o)
    click.echo(o)

    
cli()
