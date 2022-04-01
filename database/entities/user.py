from pony import orm
from .. import db


class User(db.Entity):
  name = orm.Required(str)
  rp_questions = orm.Set('RPQuestion')

  @classmethod
  def find_or_create_by_name(cls, value):
    user = cls.get(name=value)

    if user:
      return user

    return User(name=value)
