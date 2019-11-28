'''This script assumes it's running from Python3.8

The major dependencies are at the top, and the minor dependencies
are within the commands, such that not all dependencies are required
to simply run a subcommand.
'''

import click

from pathlib import Path
from textwrap import dedent
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

WEBSITE = "https://simonwoodburyforget.github.io/mindustry-modding/"

@click.group()
def cli():
    pass

@cli.command()
def definitions():
    """ Converts Mindustry attribute decelleration 
    into a Markdown table. """
    import parser
    import pyperclip
    i = pyperclip.paste()
    o = parser.build_definition_table(i)
    pyperclip.copy(o)
    click.echo(oe)

@cli.command()
def defaults():
    """ Converts Mindustry attribute decelleration 
    into a Markdown table. """
    import parser
    import pyperclip
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
    from jinja2 import Template
    import parser
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
    import msch as msch_
    from msch import Schematic, Schematics
    schems = msch_.load(msch_text)
    schems = Schematics(schems.width,
                        schems.height,
                        schems.tags,
                        [ Schematic(new, *s[1:]) if s.name == old else s
                          for s in schems.tiles ])
    click.echo(msch_.dump(schems, True))

@cli.command()
@click.option("-i", "--input", default='index.org', help="path to template index.org file")
@click.option("-o", "--output", default='index.tmp.org', help="path to output index.org file")
@click.option("-l", "--logs", default='helper/change-log.yaml' ,help="path to commit logs yaml file")
def build_index(input, output, logs):
    '''Build index out of index.org template.'''
    from github import Github
    import humanize
    from jinja2 import Template
    import yaml

    @dataclass
    class Log:
        hash: str
        notes: List[str]
        date: datetime
        message: str

        def date_fmt(self):
            return humanize.naturalday(self.date)

    with open(Path.home() / ".github-token") as f:
        token = f.read()
    g = Github(token)
    repo = g.get_repo("Anuken/Mindustry")
    def from_commit(x):
        sha, notes = x
        commit = repo.get_commit(sha=sha)
        return Log(sha,
                   notes,
                   commit.commit.author.date,
                   commit.commit.message)
    with open(logs) as f:
        logs = yaml.safe_load(f.read())
    logs = [ from_commit(x) for x in logs.items() ]
    logs = reversed(sorted(logs, key=lambda x: x.date))

    with open(input) as f:
        template = Template(f.read())
    with open(output, 'w') as f:
        print(template.render(change_log=logs), file=f)

    
if __name__ == '__main__':
    cli()
