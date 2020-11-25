from pony.orm import *
from datetime import datetime
from collections import deque
import random

db = pony.orm.Database()

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)


# Users table
class User(db.Entity):
    name = pony.orm.Required(str)
    email_address = pony.orm.Required(str, unique=True)  # SK
    password = pony.orm.Required(str)
    photo = pony.orm.Optional(str)
    verified = pony.orm.Required(bool)
    players = Set('Player')
    finished_games = Set('FinishedGames')


# Players table
class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    alias = Required(str)
    is_alive = Required(bool)
    loyalty = Optional(str)
    rol = Optional(str)
    vote = Optional(bool)
    user1 = Required(User)
    actualGame = Optional('Game')


# Finished games table
class FinishedGames(db.Entity):
    id = PrimaryKey(int, auto=True)
    game_name = Required(str)
    initial_date = Required(datetime)
    end_date = Required(datetime)
    win = Required(str)
    users = Set('User')


# Games table
class Game(db.Entity):
    name = Required(str, unique=True)
    creation_date = Required(datetime)
    initial_date = Optional(datetime)
    end_date = Optional(datetime)
    max_players = Required(int)
    creator = Required(str)
    phase = Required(int)
    players = Set('Player')
    turn = Optional('Turn')
    proclamation = Set('Proclamation')
    box = Set('Box')


# Turns table
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
    pos_expelliarmus = Optional(int)
    neg_expelliarmus = Optional(int)
    player_killed = Optional(int)
    imperius_minister_old = Optional(int)
    imperius_minister_new = Optional(int)
    player_crucio = Optional(int)

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


# Database functions

# Creates a new user
@pony.orm.db_session
def new_user(name, email_address, password):
    User(name=name, email_address=email_address, password=password,
         photo="", verified=True)


# given a email, returns the associate email
@pony.orm.db_session
def get_user_by_email(email_address):
    return (User.get(email_address=email_address))


# given a email, returns the verification bit
@pony.orm.db_session
def is_verified(email_address):
    return (User.get(email_address=email_address).verified)


# verify if certain email exists
@pony.orm.db_session
def email_exists(email_address):
    return (User.get(email_address=email_address) is not None)


@pony.orm.db_session
def update_username(email, nickname):
    user = get_user_by_email(email)
    user.name = nickname


# replace the old password with a new one
@pony.orm.db_session
def update_password(new_password, user_id):
    User[user_id].password = new_password


# creates a new game
@pony.orm.db_session
def new_game(name, max_players, email):
    game1 = Game(name=name, creation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 max_players=max_players, creator=email, phase=0)
    return game1.name


@pony.orm.db_session
def set_game_started(game_name):
    game = Game.get(name=game_name)
    game.initial_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@pony.orm.db_session
def game_is_not_started(game_name):
    game = Game.get(name=game_name)
    return (game.initial_date is None)


# verify if certain game exists
@pony.orm.db_session
def game_exists(name):
    return (Game.get(name=name) is not None)


# <precondition: user exists>

@pony.orm.db_session
def set_phase_game(game_name, n):
    game = get_game_by_name(game_name)
    game.phase = n


@pony.orm.db_session
def get_phase_game(game_name):
    game = get_game_by_name(game_name)
    return game.phase


@pony.orm.db_session
def new_player(email_address):
    user1 = get_user_by_email(email_address)
    player = Player(alias=user1.name, is_alive=True, user1=user1)
    commit()
    return player.id


@pony.orm.db_session
def player_doesnt_exists(player_id):
    try:
        Player[player_id]
        return False
    except:
        return True


@pony.orm.db_session
def set_player_killed(turn_id, player_id):
    turn = get_turn(turn_id)
    turn.player_killed = player_id


# the player returned can be None
@pony.orm.db_session
def get_player_killed(turn_id):
    return (get_turn(turn_id).player_killed)


# given a name, returns the associate game
@pony.orm.db_session
def get_game_by_name(name):
    g1 = Game.get(name=name)
    return (g1)


# <precondition: player and game exists>
@pony.orm.db_session
def join_game(player_id, game_name):
    g1 = get_game_by_name(game_name)
    g1.players.add(Player[player_id])


# <precondition: game exists>
@pony.orm.db_session
def num_of_players(game_name):
    return (len(get_player_list(game_name)))


@pony.orm.db_session
def num_of_players_alive(game_name):
    list_a = filter(lambda p: p.is_alive, get_player_list(game_name))
    return (len(list(list_a)))


# return true if the user is in the game
@pony.orm.db_session
def is_user_in_game(email_address, game_name):
    b = False
    for p in get_game_by_name(game_name).players:
        if p.user1.email_address == email_address:
            b = True
    return b


# delete a player
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


# return list of players in a specific game
@pony.orm.db_session
def get_player_list(game_name):
    list = []
    for p in get_game_by_name(game_name).players:
        player = Player[p.id]
        list.append(player)
    list.sort(key=lambda p: p.id)
    return list


@pony.orm.db_session
def get_player_ids_list(game_name):
    list = []
    for p in get_game_by_name(game_name).players:
        player = Player[p.id]
        list.append(player.id)
    return list

#create a deck when game is starting, all cards are default "Available"
@pony.orm.db_session
def new_deck(game_name):
    game = get_game_by_name(game_name)
    mortifagos = 11
    ofenix = 6
    for i in range(mortifagos):
        proclam = Proclamation(loyalty="Death Eaters", deck="Available",
                               position=i + 1, actualGame=game)
        game.proclamation.add(proclam)
    for i in range(ofenix):
        proclam = Proclamation(loyalty="Fenix Order", deck="Available",
                               position=i + 12, actualGame=game)
        game.proclamation.add(proclam)


# shuffling cards, this function must be call when the game is starting and when
# need get three cards in the steal stack and this have less than three
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


# return a list of ids cards in the steal stack
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


@pony.orm.db_session
def get_card_by_id(card_id):
    return Proclamation[card_id]


@pony.orm.db_session
def card_belong_to_game(card_id, game_name):
    game = get_game_by_name(game_name)
    card = get_card_by_id(card_id)
    return (card in game.proclamation)


# return a object Proclamation by id, this function must be call in the legislative session and
# when guess speel has invoke
@pony.orm.db_session
def get_card_in_the_steal_stack(id_card):
    return Proclamation[id_card]


# set a Proclamation as "Discarded" ie this card will be in "Discarded" deck
@pony.orm.db_session
def discard(id_card):
    card = Proclamation[id_card]
    card.deck = "Discarded"


@pony.orm.db_session
def card_doesnt_exist(card_id):
    try:
        Proclamation[card_id]
        return False
    except:
        return True


# set a Proclamation as "Proclaimed" ie this card will be in the corresponding board
@pony.orm.db_session
def proclaim(id_card):
    card = Proclamation[id_card]
    card.deck = "Proclaimed"


# return number of cards in the steal stack
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
    dict_c = dict(id=c.id, loyalty=c.loyalty, deck=c.deck,
                  position=c.position, adtualGame=c.actualGame.id)
    return dict_c


# transform a player object in a dict
@pony.orm.db_session
def player_to_dict(player_id):
    if player_id is None:
        return None
    else:
        p = Player[player_id]    
        dict_p = dict(id = p.id, alias = p.alias, is_alive = p.is_alive,
                    loyalty = p.loyalty, rol = p.rol, vote=p.vote,
                    user1 = p.user1.email_address,
                    actualGame = p.actualGame.name)
        return dict_p


# Creates a new turn
@pony.orm.db_session
def new_turn(game_name):
    t = Turn(game=get_game_by_name(game_name), num_of_turn=0, elect_marker=0, post_min=None)
    commit()
    return t.id


# return turn asociate a game_name
@pony.orm.db_session
def get_turn_by_gamename(game_name):
    return (get_game_by_name(game_name).turn.id)


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
def get_election_marker(game_name):
    game = get_game_by_name(game_name)
    return game.turn.elect_marker

@pony.orm.db_session
def set_previous_min(turn_id,player_id):
    Turn[turn_id].previous_min = player_id


@pony.orm.db_session
def set_previous_dir(turn_id, player_id):
    Turn[turn_id].previous_dir = player_id


@pony.orm.db_session
def set_post_min(turn_id, player_id):
    Turn[turn_id].post_min = player_id


@pony.orm.db_session
def set_post_dir(turn_id, player_id):
    Turn[turn_id].post_dir = player_id


@pony.orm.db_session
def set_elect_min(turn_id, player_id):
    Turn[turn_id].elect_min = player_id


@pony.orm.db_session
def set_elect_dir(turn_id, player_id):
    Turn[turn_id].elect_dir = player_id


@pony.orm.db_session
def get_turn(turn_id):
    return (Turn[turn_id])


@pony.orm.db_session
def get_next_player_to_min(game_name):
    t_id = get_turn_by_gamename(game_name)
    t = get_turn(t_id)
    if (t.imperius_minister_old == None) and (t.imperius_minister_new == None):
        last_min = t.previous_min
        list_player_alive = list(filter(lambda p: p.is_alive, get_player_list(game_name)))
        n = len(list_player_alive)
        if last_min is None or (list_player_alive.index(Player[last_min]) == n-1):
            return list_player_alive[0].id
        else:
            return (list_player_alive[(list_player_alive.index(Player[last_min]) + 1)].id)
    else:
        return (t.imperius_minister_new)
        
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
    list_a = filter(lambda p: p.is_alive and turn.post_min != p.id and
                            p.id != turn.elect_dir,
                    get_player_list(game_name))
    return (list(list_a))


@pony.orm.db_session
def new_templates(game_name):
    game = get_game_by_name(game_name)
    for i in range(5):
        box = Box(loyalty="Fenix Order", position=i + 1, is_used=False)
        game.box.add(box)
    for i in range(6):
        box = Box(loyalty="Death Eaters", position=i + 1, is_used=False)
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
    template_fo = []
    for i in get_game_by_name(game_name).box:
        if i.loyalty == "Fenix Order":
            template_fo.append(i)
    template_fo.sort(key=lambda p: p.position)
    return template_fo


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
def get_next_box(card_id, game_name):
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
    dict_b = dict(id=b.id, loyalty=b.loyalty, position=b.position,
                  spell=b.spell, is_used=b.is_used, actualGame=b.actualGame.id)
    return dict_b


@pony.orm.db_session
def get_box(box_id):
    return (Box[box_id])


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
    for p in game.players:
        finish_game.users.add(p.user1)
    return finish_game.id


@pony.orm.db_session
def finished_game_to_dict(finished_game_id):
    finished_game = FinishedGames[finished_game_id]
    dict_finish_game = dict(id=finished_game.id, game_name=finished_game.game_name,
                            initial_date=finished_game.initial_date,
                            end_date=finished_game.end_date, win=finished_game.win,
                            list_user=list(map(lambda u: u.email_address, finished_game.users)))
    return dict_finish_game


@pony.orm.db_session
def finished_game_to_list_of_players(finish_game_id):
    finish_game = FinishedGames[finish_game_id]
    list_players_fg = list(map(lambda p: (p.alias, p.rol, p.loyalty), finish_game.players_finished))
    return list_players_fg


@pony.orm.db_session
def get_user_email_by_id(player_id):
    player_email = Player[player_id].user1.email_address
    return player_email


@pony.orm.db_session
def end_game(game_name, loyalty):
    set_end_date(game_name)
    finish_game_id = new_finished_game(game_name, loyalty)
    delete_all_box(game_name)
    delete_all_proclamation(game_name)
    delete_all_player(game_name)
    delete_turn(game_name)
    return finish_game_id

@pony.orm.db_session
def is_card_discard(card_id):
    card = Proclamation[card_id]
    return (card.deck == "Discarded")


@pony.orm.db_session
def set_user_verified(user_email):
    user = get_user_by_email(user_email)
    user.verified = True


list_roles_death_eaters = ["Voldemort", "Bellatrix", "Draco", "Dolores Umbridge"]
list_roles_fenix_order = ["Harry Potter", "Hermione", "Ronald", "Dumbledore", "Sirius Black", "Hagrid"]


@pony.orm.db_session
def assign_roles_6players(game_name):
    player_list = get_player_list(game_name)
    random.shuffle(player_list)
    number_players = num_of_players(game_name)
    for i in range(2):
        player_list[i].loyalty = "Death Eaters"
        player_list[i].rol = list_roles_death_eaters[i]
    if number_players == 5:
        for i in range(3):
            player_list[i + 2].loyalty = "Fenix Order"
            player_list[i + 2].rol = list_roles_fenix_order[i]
    else:
        for i in range(4):
            player_list[i + 2].loyalty = "Fenix Order"
            player_list[i + 2].rol = list_roles_fenix_order[i]


@pony.orm.db_session
def assign_roles_8players(game_name):
    player_list = get_player_list(game_name)
    random.shuffle(player_list)
    number_players = num_of_players(game_name)
    for i in range(3):
        player_list[i].loyalty = "Death Eaters"
        player_list[i].rol = list_roles_death_eaters[i]
    if number_players == 7:
        for i in range(4):
            player_list[i + 3].loyalty = "Fenix Order"
            player_list[i + 3].rol = list_roles_fenix_order[i]
    else:
        for i in range(5):
            player_list[i + 3].loyalty = "Fenix Order"
            player_list[i + 3].rol = list_roles_fenix_order[i]


@pony.orm.db_session
def assign_roles_10players(game_name):
    player_list = get_player_list(game_name)
    random.shuffle(player_list)
    number_players = num_of_players(game_name)
    for i in range(4):
        player_list[i].loyalty = "Death Eaters"
        player_list[i].rol = list_roles_death_eaters[i]
    if number_players == 9:
        for i in range(5):
            player_list[i + 4].loyalty = "Fenix Order"
            player_list[i + 4].rol = list_roles_fenix_order[i]
    else:
        for i in range(6):
            player_list[i + 4].loyalty = "Fenix Order"
            player_list[i + 4].rol = list_roles_fenix_order[i]


@pony.orm.db_session
def config_boards(game_name, n_players):
    if n_players == 5 or n_players == 6:
        config_template_6players(game_name)
    if n_players == 7 or n_players == 8:
        config_template_8players(game_name)
    if n_players == 9 or n_players == 10:
        config_template_10players(game_name)


@pony.orm.db_session
def assing_loyalty_and_rol(game_name, n_players):
    if n_players == 5 or n_players == 6:
        assign_roles_6players(game_name)
    if n_players == 7 or n_players == 8:
        assign_roles_8players(game_name)
    if n_players == 9 or n_players == 10:
        assign_roles_10players(game_name)


@pony.orm.db_session
def game_to_dict(game):
    dict_g = dict(id=game.id, name=game.name, players=num_of_players(game.name),
                  max_players=game.max_players
                  )
    return dict_g


@pony.orm.db_session
def update_photo(user_email, photo):
    user = get_user_by_email(user_email)
    user.photo = photo
    commit()


@pony.orm.db_session
def update_player_alive(player_id):
    Player[player_id].is_alive = False


@pony.orm.db_session
def player_belong_to_game(player_id, game_name):
    if player_doesnt_exists(player_id):
        return False
    else:
        game = get_game_by_name(game_name)
        player = Player[player_id]
        return (player in game.players)


@pony.orm.db_session
def get_games():
    list_game = Game.select(lambda g: g.initial_date is None)[:]
    dict_g = []
    for g in list(filter(lambda g: g.max_players > num_of_players(g.name), list_game)):
        dict_g.append(game_to_dict(g))
    return dict_g


@pony.orm.db_session
def save_user_image(email, photo_link):
    user = get_user_by_email(email)
    user.photo = photo_link


@pony.orm.db_session
def get_player_in_game_by_email(game_name, email):
    user = get_user_by_email(email)
    print(user)
    game = get_game_by_name(game_name)
    print(game)
    player_id = 0
    for p in user.players:
        if p.actualGame.id == game.id:
            player_id = p.id
            break
    print(player_id)
    return player_id

@pony.orm.db_session
def set_vote_player(player_id: int, vote: Optional(bool)):
    Player[player_id].vote = vote

@pony.orm.db_session
def reset_votes_players(game_name):
    game = get_game_by_name(game_name)
    for p in game.players:
        p.vote = None

@pony.orm.db_session
def get_last_box_used(game_name):
    template = get_template_death_e(game_name)
    i = 0
    for b in template:
        if (b.is_used):
            i += 1
        else:
            break
    if i < 0:
        return template[0]
    else:
        return template[i-1]

@pony.orm.db_session
def set_min_imperius_old(turn_id: int,old_min_id: int):
    t = get_turn(turn_id)
    t.imperius_minister_old = old_min_id

@pony.orm.db_session
def set_min_imperius_new(turn_id: int,new_min_id: int):
    t = get_turn(turn_id)
    t.imperius_minister_new = new_min_id

@pony.orm.db_session
def set_min_imperius_new_None(turn_id: int):
    t = get_turn(turn_id)
    t.imperius_minister_new = None

@pony.orm.db_session
def is_the_creator_game(game_name, email):
    game = get_game_by_name(game_name)
    return game.creator == email


@pony.orm.db_session
def delete_player_from_game(game_name,player_id):
    g = get_game_by_name(game_name)
    p = Player[player_id]
    g.players.remove(p)
    delete_player(player_id)

@pony.orm.db_session
def get_number_proclamations_discarded(game_name):
    game = get_game_by_name(game_name)
    n = 0
    for p in game.proclamation:
        if p.deck == "Discarded":
            n += 1
    return n

@pony.orm.db_session
def get_num_proclamations_order_fenix(game_name):
    template_fo = get_template_order_f(game_name)
    n = 0
    for b in template_fo:
        if b.is_used:
            n += 1
    return n

@pony.orm.db_session
def get_num_proclamations_death_eaters(game_name):
    template_de = get_template_death_e(game_name)
    n = 0
    for b in template_de:
        if b.is_used:
            n += 1
    return n

@pony.orm.db_session
def delete_all_player(game_name):
    game = get_game_by_name(game_name)
    for player in game.players:
        game.players.remove(player)
        delete_player(player.id)

@pony.orm.db_session
def set_player_crucio(game_name, player_id):
    get_turn(get_turn_by_gamename(game_name)).player_crucio = player_id

@pony.orm.db_session
def set_min_imperius_old_None(turn_id: int):
    t = get_turn(turn_id)
    t.imperius_minister_old = None

@pony.orm.db_session
def voldemort_is_director(turn_id):
    turn = Turn[turn_id]
    player = Player[turn.post_dir]
    return player.rol == "Voldemort"

@pony.orm.db_session
def player_already_vote(player_id):
    player = Player[player_id]
    return player.vote is not None