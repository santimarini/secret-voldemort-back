from pony.orm import *

db = pony.orm.Database()

# db.bind(provider='mysql', host='localhost', user='valentin', passwd='valentin', db='ponytest')
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

#Users table
class User(db.Entity):
    name = pony.orm.Required(str)
    email_address = pony.orm.Required(str, unique=True) #SK
    password = pony.orm.Required(str)
    photo = pony.orm.Optional(str)  # supongo que habria que guardar una url a la foto, no lo se
    verified = pony.orm.Required(bool)

db.generate_mapping(create_tables=True)

#Database functions

#Creates a new user
@pony.orm.db_session
def new_user(name, email_address, password, photo):
    User(name=name, email_address=email_address, password=password,
         photo=photo, verified=True)

#given a email, returns the associate email
@pony.orm.db_session
def get_user_by_email(email_address):
    return(User.get(email_address=email_address))

#verify if certain email exists
@pony.orm.db_session
def email_exists(email_address):
    return(User.get(email_address=email_address) is not None)
