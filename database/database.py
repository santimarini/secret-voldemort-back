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

#Players table
class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str)
    is_alive = Required(bool)
    loyalty = Optional(str) #str solo para probar, aca va un ENUM (o podriamos poner un str?)
    rol = Optional(str) #str solo para probar, aca va un ENUM (o podriamos poner un str?)
    user1 = Required(User)
    actualGame = Optional('Game')

#Finished games table
class Finishedgames(db.Entity):
    gameinfo = Required(str) #solo para probar, porque falta definir que informacion queremos guardar de una partida
    users = Set(User)

#Games table
class Game(db.Entity):
    name = Required(str, unique=True)
    creation_date = Required(datetime) #datetime es un tipo de python, no de ponyorm
    initial_date = Optional(datetime)
    end_date = Optional(datetime)
    max_players = Required(int)
    creator = Required(str)
    players = Set(Player)
    turn = Optional('Turn')

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
def new_game(name,max_players,email):
    game1 = Game(name=name,creation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 max_players=max_players, creator=email)
    return game1.name

@pony.orm.db_session
def set_game_started(game_name):
    game = Game.get(name=game_name)
    game.initial_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
    return(len(get_player_list(game_name)))

@pony.orm.db_session
def num_of_players_alive(game_name):
    list_a = filter(lambda p: p.is_alive, get_player_list(game_name))
    return(len(list(list_a)))

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

#return list of players in a specific game
@pony.orm.db_session
def get_player_list(game_name):
    list = []
    for p in get_game_by_name(game_name).players:
        player = Player[p.id]
        list.append(player)
    list.sort(key = lambda p: p.id)
    return list

#transform a player object in a dict
@pony.orm.db_session
def player_to_dict(player_id):
    p = Player[player_id]
    dict_p = dict(id = p.id, username = p.username, is_alive = p.is_alive,
            loyalty = p.loyalty, rol = p.rol, user1 = p.user1.email_address,
            actualGame = p.actualGame.name)
    return dict_p

#Creates a new turn
@pony.orm.db_session
def new_turn(game_name):
    t = Turn(game = get_game_by_name(game_name), num_of_turn = 0, elect_marker = 0)
    commit()
    return t.id

#return turn asociate a game_name
@pony.orm.db_session
def get_turn_by_gamename(game_name):
    return(get_game_by_name(game_name).turn.id)

@pony.orm.db_session
def next_turn(turn_id):
    Turn[turn_id].num_of_turn += 1

@pony.orm.db_session
def increment_marker(turn_id):
    Turn[turn_id].elect_marker += 1

@pony.orm.db_session
def marker_to_zero(turn_id):
    Turn[turn_id].elect_marker = 0

@pony.orm.db_session
def set_previous_min(turn_id,player_id):
    Turn[turn_id].previous_min = player_id

@pony.orm.db_session
def set_previous_dir(turn_id,player_id):
    Turn[turn_id].previous_dir = player_id

@pony.orm.db_session
def set_post_min(turn_id,player_id):
    Turn[turn_id].post_min = player_id

@pony.orm.db_session
def set_post_dir(turn_id,player_id):
    Turn[turn_id].post_dir = player_id

@pony.orm.db_session
def set_elect_min(turn_id,player_id):
    Turn[turn_id].elect_min = player_id

@pony.orm.db_session
def set_elect_dir(turn_id,player_id):
    Turn[turn_id].elect_dir = player_id

@pony.orm.db_session
def get_turn(turn_id):
    return(Turn[turn_id])


@pony.orm.db_session
def get_next_player_to_min(game_name, last_min):
    list_player_alive = list(filter(lambda p: p.is_alive, get_player_list(game_name)))
    n = len(list_player_alive)
    if last_min is None or (list_player_alive.index(Player[last_min]) == n-1):
        return list_player_alive[0].id
    else:
        return (list_player_alive[(list_player_alive.index(Player[last_min]) + 1)].id)

@pony.orm.db_session
def get_post_min(turn_id):
    return Turn[turn_id].post_min

@pony.orm.db_session
def get_post_dir(turn_id):
    return Turn[turn_id].post_dir

@pony.orm.db_session
def get_elect_min(turn_id):
    return Turn[turn_id].elect_min

@pony.orm.db_session
def get_elect_dir(turn_id):
    return Turn[turn_id].elect_dir

@pony.orm.db_session
def increment_pos_votes(turn_id):
    turn = get_turn(turn_id)
    if turn.Pos_votes is None:
        turn.Pos_votes = 1
    else:
        turn.Pos_votes = turn.Pos_votes + 1
    return turn.Pos_votes

@pony.orm.db_session
def increment_neg_votes(turn_id):
    turn = get_turn(turn_id)
    if turn.Neg_votes is None:
        turn.Neg_votes = 1
    else:
        turn.Neg_votes = turn.Neg_votes + 1
    return turn.Neg_votes

@pony.orm.db_session
def get_total_votes(turn_id):
    turn = get_turn(turn_id)
    if turn.Neg_votes is None:
        turn.Neg_votes = 0
    if turn.Pos_votes is None:
        turn.Pos_votes = 0
    return turn.Neg_votes + turn.Pos_votes

@pony.orm.db_session
def get_status_vote(turn_id):
    turn = get_turn(turn_id)
    return turn.Neg_votes < turn.Pos_votes