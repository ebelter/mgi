import click, os, re
from pathlib import Path
from sqlalchemy import create_engine

from mgi.models import db

def create_db(url):
    engine = create_engine(url)
    db.metadata.create_all(engine)
    #with engine.connect() as con, open(sql_fn, "r") as f:
    #    for line in f.readlines():
    #        con.execute(statement, **line)
#-- create_db

@click.group(short_help="hopefully handy commands")
def utils_cli():
    pass

@utils_cli.group(name="db", short_help="tools for the database")
def utils_db_cli():
    pass

@utils_db_cli.command(name="create", short_help="create and deploy the database")
@click.argument("url", type=click.STRING)
def db_create_cmd(url):
    """
    Create and Deploy the DB Schema

    SQLite3: sqlite:///name.db

    Hopefully other URIs work!
    """
    fn = re.sub(r"sqlite:///", "", url)
    if fn != url:
        if os.path.exists(fn):
            raise Exception(f"Database already exists: {fn}")
        Path(fn).touch()
    create_db(url)
    print(f"Created DB with {url}")
