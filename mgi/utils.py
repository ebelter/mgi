import click, os, re
from pathlib import Path
from sqlalchemy import create_engine

from mgi.models import db

@click.group(short_help="hopefully handy commands")
def utils_cli():
    pass

@click.command(short_help="create and deploy the database")
@click.argument("url", type=click.STRING)
def create_db_cmd(url):
    """
    Create and Deploy the DB Schema

    SQLite3: sqlite:///name.db
    """
    fn = re.sub(r"sqlite:///", "", url)
    if fn != url:
        if os.path.exists(fn):
            raise Exception(f"Database already exists: {fn}")
        Path(fn).touch()
    engine = create_engine(url)
    db.metadata.create_all(engine)
    print(f"Created DB with {url}")
utils_cli.add_command(create_db_cmd, name="create-db")
