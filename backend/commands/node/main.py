"""
Defines commands to run CRUD operations against nodes
"""

import typer

from commands.node.input import app as input_app
from commands.node.llm import app as llm_app
from commands.node.prompt import app as prompt_app

app = typer.Typer()

app.add_typer(input_app, name="input")
app.add_typer(llm_app, name="llm")
app.add_typer(prompt_app, name="prompt")

