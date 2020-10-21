from pony.orm import *
from pydantic import EmailStr

db = pony.orm.Database()

# db.bind(provider='mysql', host='localhost', user='valentin', passwd='valentin', db='ponytest')
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)


class User(db.Entity):
    name = pony.orm.PrimaryKey(str)
    email_address = pony.orm.Required(str, unique=True) #SK  # quizas pueda usarla como SK y usar un int autoincremental de PK
    password = pony.orm.Required(str)
    photo = pony.orm.Optional(str)  # supongo que habria que guardar una url a la foto, no lo se
    verified = pony.orm.Required(bool)


db.generate_mapping(create_tables=True)


# no se si la definicion de funciones deberia ir dentro de la clase o no pero weno
@pony.orm.db_session
def new_user(name, email_address, password, photo):
    User(name=name, email_address=email_address, password=password,
         photo=photo, verified=False)

@pony.orm.db_session
def get_user_by_email(email_address):
    return(User.get(email_address=email_address))


# new_user("joaquin", "joaquin@joaquin.com", "fakehashedsecret", "photo")
# new_user("joaquinc", "joaquin2@joaquin.com", "fakehashedsecret", "photo")