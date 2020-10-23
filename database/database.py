from pony.orm import *
from datetime import datetime

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
    players = Set('Player')
    finished_games = Set('Finishedgames')

class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str)
    is_alive = Required(bool)
    loyalty = Optional(str) #str solo para probar, aca va un ENUM (o podriamos poner un str?)
    rol = Optional(str) #str solo para probar, aca va un ENUM (o podriamos poner un str?)
    user1 = Required(User)
    actualGame = Optional('Game')

class Finishedgames(db.Entity):
    gameinfo = Required(str) #solo para probar, porque falta definir que informacion queremos guardar de una partida
    users = Set(User)

class Game(db.Entity):
    name = Required(str, unique=True)
    creation_date = Required(datetime) #datetime es un tipo de python, no de ponyorm
    initial_date = Optional(datetime)
    end_date = Optional(datetime)
    max_players = Required(int)
    players = Set(Player)

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

#given a email, returns the verification bit
@pony.orm.db_session
def is_verified(email_address):
    return(User.get(email_address=email_address).verified)

#verify if certain email exists
@pony.orm.db_session
def email_exists(email_address):
    return(User.get(email_address=email_address) is not None)

#creates a new game
@pony.orm.db_session
def new_game(name,max_players):
    game1 = Game(name=name,creation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),max_players=max_players)
    return game1.name


#verify if certain game exists
@pony.orm.db_session
def game_exists(name):
    return(Game.get(name=name) is not None)

#<precondition: user exists>

@pony.orm.db_session
def new_player(email_address):
    user1 = get_user_by_email(email_address)
    player = Player(username=user1.name,is_alive=True,user1=user1)
    commit()
    return player.id

#given a name, returns the associate game
@pony.orm.db_session
def get_game_by_name(name):
    g1 = Game.get(name=name)
    return(g1)

#<precondition: player and game exists>

@pony.orm.db_session
def join_game(player_id,game_name):
    g1 = get_game_by_name(game_name)
    g1.players.add(Player[player_id])

#<precondition: game exists>
@pony.orm.db_session
def num_of_players(game_name):
    return(count(get_game_by_name(game_name).players))

#return true if the user is in the game
@pony.orm.db_session
def is_user_in_game(email_address,game_name):
    b = False
    for p in get_game_by_name(game_name).players:
        if p.user1.email_address == email_address:
            b = True
    return b

#delete a player
@pony.orm.db_session
def delete_player(player_id):
    Player[player_id].delete()
    