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
    user1 = Required(User)
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
    actualGame = Optional(Game)

class Box(db.Entity):
    loyalty = Required(str)
    position = Required(int)
    spell = Optional(str)
    is_used = Required(bool)
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

#set the initial_date of a game when is started
@pony.orm.db_session
def set_game_started(game_name):
    game = Game.get(name=game_name)
    game.initial_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

@pony.orm.db_session
def delete_all_player(game_name):
    for player in get_game_by_name(game_name).players:
        delete_player(player.id)

@pony.orm.db_session
def delete_all_box(game_name):
    for b in get_game_by_name(game_name).box:
        Box[b.id].delete()

@pony.orm.db_session
def delete_game(game_name):
    get_game_by_name(game_name).delete()

@pony.orm.db_session
def delete_turn(game_name):
    Turn[get_turn_by_gamename(game_name)].delete()

@pony.orm.db_session
def delete_all_proclamation(game_name):
    for p in get_game_by_name(game_name).proclamation:
        Proclamation[p.id].delete()

#return list of players in a specific game
@pony.orm.db_session
def get_player_list(game_name):
    list = []
    for p in get_game_by_name(game_name).players:
        player = Player[p.id]
        list.append(player)
    list.sort(key = lambda p: p.id)
    return list

#create a deck when game is starting, all cards are default "Available"
@pony.orm.db_session
def new_deck(game_name):
    game = get_game_by_name(game_name)
    mortifagos = 11
    ofenix = 6
    for i in range(mortifagos):
        proclam = Proclamation(loyalty="Death Eaters", deck="Available",
                     position=i+1, actualGame=game)
        game.proclamation.add(proclam)
    for i in range(ofenix):
        proclam = Proclamation(loyalty="Fenix Order", deck="Available",
                     position=i+12, actualGame=game)
        game.proclamation.add(proclam)

#shuffling cards, this function must be call when the game is starting and when
#need get three cards in the steal stack and this have less than three
@pony.orm.db_session
def shuffle_cards(game_name):
    cards = []
    for i in get_game_by_name(game_name).proclamation:
        if i.deck != "Proclaimed":
            i.deck = "Available"
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
        if ((i.deck != "Proclaimed") and (i.deck != "Discarded")):
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

#set a Proclamation as "Discarded" ie this card will be in "Discarded" deck
@pony.orm.db_session
def discard(id_card):
    card = Proclamation[id_card]
    card.deck = "Discarded"

#set a Proclamation as "Proclaimed" ie this card will be in the corresponding board
@pony.orm.db_session
def proclaim(id_card):
    card = Proclamation[id_card]
    card.deck = "Proclaimed"

#return number of cards in the steal stack
@pony.orm.db_session
def num_of_cards_in_steal_stack(game_name):
    n = 0
    for i in get_game_by_name(game_name).proclamation:
        if i.deck == "Available":
            n += 1
    return n

@pony.orm.db_session
def card_to_dict(card_id):
    c = Proclamation[card_id]
    dict_c = dict(id = c.id, loyalty = c.loyalty, deck = c.deck,
            position = c.position, adtualGame = c.actualGame.id)
    return dict_c

#transform a player object in a dict
@pony.orm.db_session
def player_to_dict(player_id):
    if player_id is None:
        return None
    else:
        p = Player[player_id]
        dict_p = dict(id = p.id, username = p.username, is_alive = p.is_alive,
                    loyalty = p.loyalty, rol = p.rol, user1 = p.user1.email_address,
                    actualGame = p.actualGame.name)
        return dict_p

#Creates a new turn
@pony.orm.db_session
def new_turn(game_name):
    t = Turn(game = get_game_by_name(game_name), num_of_turn = 0, elect_marker = 0, post_min = None)
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
def set_vote_to_zero(turn_id):
    turn = get_turn(turn_id)
    turn.Pos_votes = 0
    turn.Neg_votes = 0

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

@pony.orm.db_session  
def get_players_avaibles_to_elect_more_5players(game_name, turn_id):
    turn = get_turn(turn_id)
    if ((turn.elect_min is None) and (turn.elect_dir is None)):
        return list(filter(lambda p: p.is_alive and turn.post_min != p.id, get_player_list(game_name)))
    else:
        list_a = filter(lambda p: p.is_alive and turn.post_min != p.id and
                            turn.elect_dir != p.id and turn.elect_min != p.id,
                            get_player_list(game_name))
        return (list(list_a))

@pony.orm.db_session
def get_players_avaibles_to_elect_less_5players(game_name, turn_id):
    turn = get_turn(turn_id)
    list_a = filter(lambda p: p.is_alive and turn.post_min != p.id,
                        get_player_list(game_name))
    return (list(list_a))

@pony.orm.db_session
def new_templates(game_name):
    game = get_game_by_name(game_name)
    for i in range(5):
        box = Box(loyalty="Fenix Order", position=i+1, is_used=False)
        game.box.add(box)
    for i in range(6):
        box = Box(loyalty="Death Eaters", position=i+1, is_used=False)
        game.box.add(box)

@pony.orm.db_session
def get_template_death_e(game_name):
    template_de = []
    for i in get_game_by_name(game_name).box:
        if i.loyalty == "Death Eaters":
            template_de.append(i)
    template_de.sort(key=lambda p: p.position)
    return template_de

@pony.orm.db_session
def get_template_order_f(game_name):
    template_de = []
    for i in get_game_by_name(game_name).box:
        if i.loyalty == "Fenix Order":
            template_de.append(i)
    template_de.sort(key=lambda p: p.position)
    return template_de

@pony.orm.db_session
def config_template_6players(game_name):
    template_de = get_template_death_e(game_name)
    template_de[2].spell = "Guess"
    template_de[3].spell = "Avada Kedavra"
    template_de[4].spell = "Avada Kedavra"

@pony.orm.db_session
def config_template_8players(game_name):
    template_de = get_template_death_e(game_name)
    template_de[1].spell = "Cruciatus"
    template_de[2].spell = "Imperius"
    template_de[3].spell = "Avada Kedavra"
    template_de[4].spell = "Avada Kedavra"

@pony.orm.db_session
def config_template_10players(game_name):
    template_de = get_template_death_e(game_name)
    template_de[0].spell = "Cruciatus"
    template_de[1].spell = "Cruciatus"
    template_de[2].spell = "Imperius"
    template_de[3].spell = "Avada Kedavra"
    template_de[4].spell = "Avada Kedavra"

@pony.orm.db_session
def get_next_box(card_id,game_name):
    card = Proclamation[card_id]
    if card.loyalty == "Fenix Order":
        template = get_template_order_f(game_name)
        for i in template:
            if (not i.is_used):
                box = i
                break
    else:
        template = get_template_death_e(game_name)
        for i in template:
            if (not i.is_used):
                box = i
                break
    return box.id

@pony.orm.db_session
def box_to_dict(box_id):
    b = Box[box_id]
    dict_b = dict(id = b.id, loyalty = b.loyalty, position = b.position,
                  spell = b.spell, is_used = b.is_used, actualGame = b.actualGame.id)
    return dict_b

@pony.orm.db_session
def set_used_box(box_id):
    Box[box_id].is_used = True

@pony.orm.db_session
def set_end_date(game_name):
    game = get_game_by_name(game_name)
    game.end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@pony.orm.db_session
def new_finished_game(game_name, loyalty_win):
    game = get_game_by_name(game_name)
    finish_game = FinishedGames(game_name=game_name, initial_date=game.initial_date,
                                end_date=game.end_date, win=loyalty_win)
    # Add id of user in finished_game
    for u in game.players.user1:
        finish_game.users.add(u)
    return finish_game.id

@pony.orm.db_session
def new_players_finished(game_name, finished_game_id):
    for p in get_player_list(game_name):
        player_fg = PlayerFinished(username=p.username, loyalty="Fenix",
                       rol="Hermione", finish_game=FinishedGames[finished_game_id],
                       user=p.user1)
        FinishedGames[finished_game_id].players_finished.add(player_fg)
    return finished_game_to_list_of_players(finished_game_id)

@pony.orm.db_session
def finished_game_to_dict(finished_game_id):
    finished_game = FinishedGames[finished_game_id]
    dict_finish_game = dict(id=finished_game.id ,game_name=finished_game.game_name, initial_date=finished_game.initial_date,
                            end_date=finished_game.end_date, win=finished_game.win,
                            list_user = list(map(lambda u: u.id,finished_game.users)),
                            list_player_finished = finished_game_to_list_of_players(finished_game_id))
    return dict_finish_game

@pony.orm.db_session
def finished_game_to_list_of_players(finish_game_id):
    finish_game = FinishedGames[finish_game_id]
    list_players_fg = list(map(lambda p: (p.username, p.rol, p.loyalty), finish_game.players_finished))
    return list_players_fg
