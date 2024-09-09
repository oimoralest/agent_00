"""
Defines CLI tool to create agents
"""
import typer

from commands.agent.main import app as agent_app
from commands.node.main import app as node_app
from commands.project.main import app as project_app

app = typer.Typer()

app.add_typer(agent_app, name="agent")
app.add_typer(node_app, name="node")
app.add_typer(project_app, name="project")

if __name__  == "__main__":
    app()
