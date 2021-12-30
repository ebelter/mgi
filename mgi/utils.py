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
@click.argument("url", type=click.STRING, required=True, nargs=1)
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

@utils_db_cli.command(name="set", short_help="show the database URI")
@click.argument("uri", type=click.STRING, required=False, nargs=1)
def db_set_cmd(uri):
    """
    Show the Command to Set the Database URI

    This is set an an environment variable called SQLALCHEMY_DATABASE_URI, and must be set in your courrent environment. Please run the command output here.

    If no URI is given, an example will be used.
    """
    if uri is None:
        uri = "sqlite:///tests/data/db"
    print(f"export SQLALCHEMY_DATABASE_URI={uri}")

@utils_db_cli.command(name="show", short_help="show the database URI")
def db_show_cmd():
    """
    Show the Current DB URI

    This is set an an enivirnment variable called SQLALCHEMY_DATABASE_URI
    """
    print(f"{os.environ.get('SQLALCHEMY_DATABASE_URI', None)}")
