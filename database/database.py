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
    proclamation = Set('Proclamation')

class Proclamation(db.Entity):
    loyalty = Required(str)
    deck = Required(str)
    position = Required(int)
    actualGame = Optional(Game)

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

#return list of players in a specific game
@pony.orm.db_session
def get_player_list(game_name):
    list = []
    for p in get_game_by_name(game_name).players:
        player = Player[p.id]
        list.append(player)
    return list

#transform a player object in a dict
@pony.orm.db_session
def player_to_dict(player_id):
    p = Player[player_id]
    dict_p = dict(id = p.id, username = p.username, is_alive = p.is_alive,
            loyalty = p.loyalty, rol = p.rol, user1 = p.user1.email_address,
            actualGame = p.actualGame.name)
    return dict_p

#create a deck when game is starting, all cards are default "Pila de robo"
@pony.orm.db_session
def new_deck(game_name):
    game = get_game_by_name(game_name)
    mortifagos = 11
    ofenix = 6
    for i in range(mortifagos):
        proclam = Proclamation(loyalty="Mortifagos", deck="Pila de robo",
                     position=i+1, actualGame=game)
        game.proclamation.add(proclam)
    for i in range(ofenix):
        proclam = Proclamation(loyalty="Orden del Fenix", deck="Pila de robo",
                     position=i+12, actualGame=game)
        game.proclamation.add(proclam)

#shuffling cards, this function must be call when the game is starting and when
#need get three cards in the steal stack and this have less than three
@pony.orm.db_session
def shuffle_cards(game_name):
    cards = []
    for i in get_game_by_name(game_name).proclamation:
        if i.deck != "Proclamada":
            cards.append(i)
    random.shuffle(cards)
    j = 1
    for i in cards:
        i.position = j
        j += 1
    cards.sort(key=lambda c: c.position, reverse=True)
    return cards

#return a list of ids cards in the steal stack
@pony.orm.db_session
def get_cards_in_game(game_name):
    cards = []
    cards_id = []
    for i in get_game_by_name(game_name).proclamation:
        if ((i.deck != "Proclamada") and (i.deck != "Descartada")):
            cards.append(i)
    cards.sort(key=lambda c: c.position, reverse=True)
    for i in cards:
        cards_id.append(i.id)
    return cards_id

#return a object Proclamation by id, this function must be call in the legislative session and
#when guess speel has invoke
@pony.orm.db_session
def get_card_in_the_steal_stack(id_card):
    return Proclamation[id_card]

#set a Proclamation as "Descartada" ie this card will be in "Descartdas" deck
@pony.orm.db_session
def discard(id_card):
    card = Proclamation[id_card]
    card.deck = "Descartada"

#set a Proclamation as "Proclamada" ie this card will be in the corresponding board
@pony.orm.db_session
def proclam(id_card):
    card = Proclamation[id_card]
    card.deck = "Proclamada"

#return number of cards in the steal stack
@pony.orm.db_session
def num_of_cards_in_steal_stack(game_name):
    n = 0
    for i in get_game_by_name(game_name).proclamation:
        if i.deck == "Pila de robo":
            n += 1
    return n

@pony.orm.db_session
def card_to_dict(card_id):
    c = Proclamation[card_id]
    dict_c = dict(id = c.id, loyalty = c.loyalty, deck = c.deck,
            position = c.position, adtualGame = c.actualGame.id)
    return dict_c
