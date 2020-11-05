from pony.orm import *
from datetime import datetime
from collections import deque
import random

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
    finished_games = Set('FinishedGames')
    player_finished = Set('PlayerFinished')

#Players table
class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str)
    is_alive = Required(bool)
    loyalty = Optional(str) #str solo para probar, aca va un ENUM (o podriamos poner un str?)
    rol = Optional(str) #str solo para probar, aca va un ENUM (o podriamos poner un str?)
    user1 = Required('User')
    actualGame = Optional('Game')

#Finished games table
class FinishedGames(db.Entity):
    id = PrimaryKey(int, auto=True)
    game_name = Required(str)
    initial_date = Required(datetime)
    end_date = Required(datetime)
    win = Required(str)
    players_finished = Set('PlayerFinished')
    users = Set('User')

class PlayerFinished(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str)
    loyalty = Required(str)
    rol = Required(str)
    finish_game = Required('FinishedGames')
    user = Required('User')

#Games table
class Game(db.Entity):
    name = Required(str, unique=True)
    creation_date = Required(datetime) #datetime es un tipo de python, no de ponyorm
    initial_date = Optional(datetime)
    end_date = Optional(datetime)
    max_players = Required(int)
    creator = Required(str)
    players = Set('Player')
    turn = Optional('Turn')
    proclamation = Set('Proclamation')
    box = Set('Box')

#Turns table
class Turn(db.Entity):
    game = Required(Game)
    num_of_turn = Required(int)
    elect_marker = Required(int)
    previous_min = Optional(int)
    previous_dir = Optional(int)
    post_min = Optional(int)
    post_dir = Optional(int)
    elect_min = Optional(int)
    elect_dir = Optional(int)
    Pos_votes = Optional(int)
    Neg_votes = Optional(int)

class Proclamation(db.Entity):
    loyalty = Required(str)
    deck = Required(str)
    position = Required(int)
    actualGame = Optional('Game')

class Box(db.Entity):
    loyalty = Required(str)
    position = Required(int)
    spell = Optional(str)
    is_used = Required(bool)
    actualGame = Optional('Game')

db.generate_mapping(create_tables=True)
