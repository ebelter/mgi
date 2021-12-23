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
    create_db(url)
    print(f"Created DB with {url}")
utils_cli.add_command(create_db_cmd, name="create-db")
