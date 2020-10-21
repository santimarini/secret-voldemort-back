from pony.orm import *

db = Database()

#db.bind(provider='mysql', host='localhost', user='valentin', passwd='valentin', db='ponytest')
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

class User(db.Entity):
    name = Required(str)
    email_address = PrimaryKey(str)#quizas pueda usarla como SK y usar un int autoincremental de PK
    password = Required(str)
    photo = Optional(str) #supongo que habria que guardar una url a la foto, no lo se
    is_logged = Required(bool) #es mejor utilizar un boleano que implementar un tipo nuevo, ya que eso implica mucho trabajo
    verified = Required(bool)

db.generate_mapping(create_tables=True)

#no se si la definicion de funciones deberia ir dentro de la clase o no pero weno

@db_session
def new_user(name,email_address,password,photo):
    User(name=name, email_address=email_address, password=password, photo=photo, is_logged=False, verified=False)

@db_session
def login(email_address):
    User[email_address].is_logged = True
