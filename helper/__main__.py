import click
import parser
import pyperclip

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

    
cli()
