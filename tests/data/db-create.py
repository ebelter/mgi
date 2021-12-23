#!/usr/bin/env python
import os, subprocess, sys
from mgi.utils import create_db

if len(sys.argv) == 1:
    fn = os.path.join(os.path.dirname(__file__), "db")
else:
    fn = os.path.abspath(sys.argv[1])
fn = os.path.abspath(fn)
url = "sqlite:///" + os.path.abspath(fn)
if os.path.exists(fn):
    os.remove(fn)
create_db(url)

sql_fn = os.path.join(os.path.dirname(__file__), "db.sql")
with open(sql_fn, "r") as f:
    # TODO mgi.utils.execute_sql(url, sql_fn)
    subprocess.check_call(["sqlite3", fn], stdin=f)
