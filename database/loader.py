from fileinput import filename
import json
from typing import Type
from pony import orm
from pathlib import Path

from . import db


class LoadedResource(db.Entity):
  filename = orm.Required(str)


def load_resources(resource_dir, table):
  '''load static resources into our database and ensure they haven't been loaded before.
  parse the resources/ directory tree for a sub_dir and insert into the specific table.
  files must be json and have key-value pairs that map to what's expected by the database.
  Not much protection in here for mistakes in files, but not exposed to user input.

  Params:
    resource_dir (str): sub_dir directly below resources/ ie 'rp_questions'
    table (str): name of target table for bulk insertion ie 'RPQuestion'
  '''

  resource_path = Path(Path.cwd(), 'resources', resource_dir)
  files = list(resource_path.glob('**/*.json'))

  for file in files:
    with orm.db_session:
      if orm.select(f for f in db.LoadedResource if f.filename == file.name):
        continue

      data = json.load(open(file))
      for row in data['rows']:
        db.insert(table, **row)

      LoadedResource(filename=file.name)

