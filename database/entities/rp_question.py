from pony import orm
from .. import db


class RPQuestion(db.Entity):
  prompt = orm.Required(str)
  users = orm.Set('User')
