from fastapi import FastAPI
from database.database import *
from login_functions import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

MAX_LEN_ALIAS = 16
MIN_LEN_ALIAS = 4
MAX_LEN_PASSWORD = 16
MIN_LEN_PASSWORD = 4
MAX_LEN_EMAIL = 30
MIN_LEN_EMAIL = 10
MAX_LEN_GAME_NAME =  16
MIN_LEN_GAME_NAME = 4
MIN_NUM_OF_PLAYERS = 5
MAX_NUM_OF_PLAYERS = 10
MIN_CARDS_IN_STACK = 3
MAX_BOX_FENIX_ORDER = 5
MAX_BOX_DEATH_EATERS = 6


app = FastAPI(
    title="Secret Voldemort",
    description="Ingenieria del Software 2020 - Desaproba2",
    version="0.1"
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/signup")
async def register_user(user_to_reg: UserTemp):
    invalid_fields = HTTPException(
            status_code=404,
            detail="field size is invalid"
        )
    if len(user_to_reg.alias) > MAX_LEN_ALIAS or \
       len(user_to_reg.alias) < MIN_LEN_ALIAS or \
       len(user_to_reg.password) > MAX_LEN_PASSWORD or \
       len(user_to_reg.password) < MIN_LEN_PASSWORD or \
       len(user_to_reg.email) > MAX_LEN_EMAIL or \
       len(user_to_reg.email) < MIN_LEN_EMAIL:
        raise invalid_fields
    elif email_exists(user_to_reg.email):
        raise HTTPException(
            status_code=404,
            detail="existing user"
        )
    else:
        new_user(user_to_reg.alias, user_to_reg.email,
                 get_password_hash(user_to_reg.password))
        return {"email": user_to_reg.email}

@app.post("/send_email")
async def send_email(user_email: str):
    user = get_user_by_email(user_email)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="The email was not found in our system"
        )
    else:
        if user.verified:
            raise HTTPException(
                status_code=404,
                detail="This email is already verified"
            )
        else:
            email = EmailSchema(email=[user_email])
            validate_token_expires = \
                timedelta(minutes=VALIDATE_TOKEN_EXPIRE_MINUTES)
            validate_token = create_token(
                data={"sub": user_email},
                expires_delta=validate_token_expires
            )
            alias = user.name
            html = generate_html(alias, validate_token)
            message = get_message(email, html)
            fm = FastMail(conf)
            await fm.send_message(message)
            return {"token_val": validate_token}

@app.get("/validate/{token}")
async def validate_email(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BAD_TOKEN"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LINK_EXPIRES"
        )
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BAD_TOKEN"
        )
    else:
        set_user_verified(email)
    return {"Thanks for checking your email! email_user": email}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm =
                                 Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.email_address}, expires_delta=access_token_expires
    )
    return {"alias": user.name,
            "access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {current_user.email_address}

@app.post("/change_alias")
async def change_alias(current_user: User = Depends(get_current_user),
                        alias: Optional[str] = None):
    if not is_verified(current_user.email_address):
        raise HTTPException(
            status_code=401,
            detail="user not verified"
        )
    if get_user_by_email(current_user.email_address).name == alias:
        raise HTTPException(
            status_code=401,
            detail="the alias is the same as always"
        )
    if len(alias) > MAX_LEN_ALIAS or \
       len(alias) < MIN_LEN_ALIAS:
        raise HTTPException(
            status_code=401,
            detail="Alias must contain 4 - 16 characters.",
            )
    update_username(current_user.email_address, alias)
    return {"new_alias": get_user_by_email(current_user.email_address).name}


@app.get("/user_image")
async def get_user_image(current_user: User = Depends(get_current_user)):
    if current_user.photo == "":
        raise HTTPException(status_code=401, detail="no photo")
    return current_user.photo


@app.post("/upload_image")
async def save_image(photo: str,
                             current_user: User = Depends(get_current_user)):
    update_photo(current_user.email_address, photo)
    return {"photo updated succesfully"}


@app.post("/change_password")
async def change_password(old_password: str,
                          new_password: str,
                          confirm_new_password: str,
                          current_user: User = Depends(get_current_verified_user)):
    if old_password == new_password:
        raise HTTPException(
            status_code=404,
            detail="The old password is the same as the new password."
        )
    if (not new_password == confirm_new_password):
        raise HTTPException(
            status_code=404,
            detail="Passwords do not match."
        )
    invalid_fields = HTTPException(
        status_code=404,
        detail="Field size is invalid."
    )
    if len(new_password) > MAX_LEN_PASSWORD or \
       len(new_password) < MIN_LEN_PASSWORD or \
       len(confirm_new_password) > MAX_LEN_PASSWORD or \
       len(confirm_new_password) < MIN_LEN_PASSWORD:
        raise invalid_fields
    else:
        user = authenticate_user(current_user.email_address, old_password)
        if user == False:
            raise HTTPException(
                status_code=404,
                detail="The old password is not the current password."
            )
        update_password(get_password_hash(new_password),user.id)
        return{"Changed password."}

@app.get("/show_games")
async def game_list():
    games = get_games()
    return {"games_list": games}


@app.post("/newgame")
async def create_game(game: ConfigGame,
                      current_user: User = Depends(get_current_verified_user)):
    if game.max_players < MIN_NUM_OF_PLAYERS or \
       game.max_players > MAX_NUM_OF_PLAYERS:
        raise HTTPException(status_code=401,
                            detail="the number of players "
                                   "must be between 5 and 10"
                            )
    if game_exists(game.name):
        raise HTTPException(status_code=401, detail="Game already exists")
    if len(game.name) < MIN_LEN_GAME_NAME or len(game.name) > MAX_LEN_GAME_NAME:
        HTTPException(status_code=404,detail="field size is invalid")
    else:
        game_name = new_game(game.name,
                             game.max_players,
                             current_user.email_address)
        return {"name": game_name}


@app.get("/game/{game_name}")
async def join_url(game_name: str, current_user: User = Depends(get_current_verified_user)):
    if game_exists(game_name):
        if get_game_by_name(game_name).initial_date is not None and not is_user_in_game(current_user.email_address,
                                                                                        game_name):
            raise HTTPException(status_code=404,
                                detail="The game has already started"
                                )
        else:
            game = get_game_by_name(game_name)
            if not is_user_in_game(current_user.email_address, game_name):
                player_id = new_player(current_user.email_address)
                join_game(player_id, game_name)

        if num_of_players(game_name) <= game.max_players:
            list = get_player_list(game_name)
            list_dict = []
            for p in list:
                list_dict.append(player_to_dict(p.id))
            user_alias = get_user_by_email(
                current_user.email_address).name
            return {"alias": user_alias,
                    "game_name": game_name,
                    "max_players": game.max_players,
                    "players": list_dict,
                    "creator": game.creator,
                    "phase_game": get_phase_game(game_name)}
        else:
            raise HTTPException(status_code=404,
                                detail="The room is full"
                                )
    else:
        raise HTTPException(status_code=404,
                            detail="Game is not exists")

@app.get("/game/{game_name}/exit")
async def exit_game(game_name: str, current_user: User = Depends(get_current_user)):
    if game_exists(game_name):
        if get_game_by_name(game_name).initial_date is None:
            player_id = get_player_in_game_by_email(game_name,current_user.email_address)
            if is_the_creator_game(game_name,current_user.email_address):
                delete_all_player(game_name)
                set_phase_game(game_name,5)
            else:
                delete_player_from_game(game_name,player_id)
        else:
            raise HTTPException(status_code=404,
                                detail="Game is already started")
    else:
        raise HTTPException(status_code=404,
                            detail="Game is not exists")


@app.post("/start")
async def start_game(game_name: str):
    if  get_game_by_name(game_name) is None:
        raise HTTPException(status_code=404, detail="The game is not exist")
    if num_of_players(game_name) < MIN_NUM_OF_PLAYERS:
        raise HTTPException(status_code=403,
                            detail="There aren't enough players")
    set_game_started(game_name)
    set_phase_game(game_name,1)
    new_turn(game_name)
    new_deck(game_name)
    shuffle_cards(game_name)
    new_templates(game_name)
    number_players = num_of_players(game_name)
    config_boards(game_name, number_players)
    assing_loyalty_and_rol(game_name, number_players)
    player_list = get_player_list(game_name)
    player_dict = []
    for p in player_list:
        player_dict.append(player_to_dict(p.id))
    return {
        "players": player_dict
    }

@app.post("/set_minister")
async def select_post_min(game_name: str):
    if game_exists(game_name):
        if game_is_not_started(game_name):
            raise HTTPException(status_code=400, detail="game is not started")
        turn_id = get_turn_by_gamename(game_name)
        next_id_min = get_next_player_to_min(game_name)
        set_post_min(turn_id, next_id_min)
        player_min = player_to_dict(next_id_min)
        return{"minister" : player_min}
    else:
        raise HTTPException(status_code=400,detail="inexistent game")

@app.post("/next_turn")
async def next_turn_begin(game_name: str):
    if game_exists(game_name):
        if game_is_not_started(game_name):
            raise HTTPException(status_code=400, detail="game is not started")
        turn_id = get_turn_by_gamename(game_name)
        next_turn(turn_id)
        turn = get_turn(turn_id)
        if num_of_players_alive(game_name) > MIN_NUM_OF_PLAYERS:
            list_player = get_players_avaibles_to_elect_more_5players(game_name,turn_id)
            list_player_dict = []
            for p in list_player:
                list_player_dict.append(player_to_dict(p.id))
        else:
            list_player = get_players_avaibles_to_elect_less_5players(game_name,turn_id)
            list_player_dict = []
            for p in list_player:
                list_player_dict.append(player_to_dict(p.id))
        return {"players": list_player_dict}
    else:
        raise HTTPException(status_code=400,detail="inexistent game")


@app.put("/game")
async def dir_post(game_name: str, dir: int):
    if game_exists(game_name):
        if player_doesnt_exists(dir):
            raise HTTPException(status_code=400, detail="player doesn't exist")
        if game_is_not_started(game_name):
            raise HTTPException(status_code=400, detail="game is not started")
        set_phase_game(game_name,2)
        turn_id = get_turn_by_gamename(game_name)
        set_post_dir(turn_id, dir)
        dir_dict = player_to_dict(dir)
        return{"post_director": dir_dict,
               "post_minister": player_to_dict(get_post_min(turn_id))
              }
    else:
        raise HTTPException(status_code=400, detail="inexistent game")

@app.put("/game/{game_name}/vote")
async def vote_player(game_name: str, vote: bool,
                      current_user: User = Depends(get_current_verified_user)):
    player_id = get_player_in_game_by_email(game_name, current_user.email_address)
    if player_already_vote(player_id):
        raise HTTPException(status_code=401, detail="player already vote")
    turn_id = get_turn_by_gamename(game_name)
    if vote:
        set_vote_player(player_id, True)
        increment_pos_votes(turn_id)
    else:
        set_vote_player(player_id, False)
        increment_neg_votes(turn_id)
    if num_of_players_alive(game_name) == get_total_votes(turn_id):
        if get_status_vote(turn_id):
            if voldemort_is_director(turn_id) and \
            get_num_proclamations_death_eaters(game_name) >= 3:
                set_phase_game(game_name,5)
                finish_game_id = end_game_voldemort_director(game_name)
                return {finished_game_to_dict(finish_game_id)}
            set_phase_game(game_name,3)
            reset_votes_players(game_name)
            set_elect_min(turn_id, get_post_min(turn_id))
            set_elect_dir(turn_id, get_post_dir(turn_id))
            set_previous_min(turn_id, get_elect_min(turn_id))
            set_previous_dir(turn_id, get_elect_dir(turn_id))
            set_vote_to_zero(turn_id)
            return {"elect_min": player_to_dict(get_elect_min(turn_id)),
                    "elect_dir": player_to_dict(get_elect_dir(turn_id))}
        else:
            set_phase_game(game_name,1)
            reset_votes_players(game_name)
            increment_marker(turn_id)
            set_elect_dir(turn_id, None)
            set_elect_min(turn_id, None)
            set_previous_min(turn_id, get_post_min(turn_id))
            set_previous_dir(turn_id, get_post_dir(turn_id))
            set_vote_to_zero(turn_id)
            return {"status_vote": "there was no consensus, "
                                   "the election marker advances one place",
                    "mark_election": get_turn(turn_id).elect_marker}
    else:
        return{"cant_vote": get_total_votes(turn_id),
               "vote": vote,
               "vote_less": (num_of_players_alive(game_name) -
                             get_total_votes(turn_id))
              }

@app.get("/cards/draw_three_cards")
async def draw_three_cards(game_name: str):
    if game_exists(game_name):
        if game_is_not_started(game_name):
            raise HTTPException(status_code=400, detail="game is not started")
        list_of_cards_id = get_cards_in_game(game_name)
        cards_list = []
        for c in range(3):
            cards_list.append(card_to_dict(list_of_cards_id.pop()))
        return {"cards_list" : cards_list}
    else:
        raise HTTPException(status_code=400,detail="inexistent game")

@app.put("/cards/discard_min")
async def discard_card_min(card_id: int, game_name: str):
    if card_id in get_cards_in_game(game_name):
        set_phase_game(game_name,4)
        discard(card_id)
        card = card_to_dict(card_id)
        return {"card": card}
    else:
        raise HTTPException(status_code=404, detail="card not available")

@app.get("/cards/draw_two_cards")
async def draw_two_cards(game_name: str):
    if game_exists(game_name):
        if game_is_not_started(game_name):
            raise HTTPException(status_code=400, detail="game is not started")
        list_of_cards_id = get_cards_in_game(game_name)
        cards_list = []
        for c in range(2):
            cards_list.append(card_to_dict(list_of_cards_id.pop()))
        return {"cards_list" : cards_list}
    else:
        raise HTTPException(status_code=400,detail="inexistent game")

@app.put("/cards/discard_dir")
async def discard_card_dir(card_id: int, game_name: str):
    if card_id in get_cards_in_game(game_name):
        discard(card_id)
        card = card_to_dict(card_id)
        return {"card": card}
    else:
        raise HTTPException(status_code=404, detail="card not available")

@app.put("/cards/proclaim")
async def proclaim_card(card_id,game_name):
    if game_exists(game_name):
        if card_doesnt_exist(card_id):
            raise HTTPException(status_code=400,detail="inexistent card")
        if game_is_not_started(game_name):
            raise HTTPException(status_code=400, detail="game is not started")
        if (not card_belong_to_game(card_id,game_name)):
            raise HTTPException(status_code=400, detail="card doesnt belong to game")
        turn_id = get_turn_by_gamename(game_name)
        marker_to_zero(turn_id)
        proclaim(card_id)
        box_id = get_next_box(card_id,game_name)
        box = get_box(box_id)
        set_used_box(box_id)
        if (num_of_cards_in_steal_stack(game_name) < MIN_CARDS_IN_STACK):
            shuffle_cards(game_name)
        if (box.loyalty == "Fenix Order" and box.position == MAX_BOX_FENIX_ORDER) or \
                (box.loyalty == "Death Eaters" and box.position == MAX_BOX_DEATH_EATERS):
            set_phase_game(game_name, 5)
            finish_game_id = end_game(game_name,box.loyalty)
            return finished_game_to_dict(finish_game_id)
        if not box.spell == "":
            set_phase_game(game_name,6)
        else:
            set_phase_game(game_name, 1)
        return {
            "box": box_to_dict(box_id)
        }
    else:
        raise HTTPException(status_code=400,detail="inexistent game")

@app.get("/list_of_crucio")
async def list_of_crucio(game_name: str):
    if (not game_exists(game_name)):
        raise HTTPException(status_code=401,
                            detail="the game not exist")
    if game_is_not_started(game_name):
        raise HTTPException(status_code=401,
                            detail="game is not started")
    turn_id = get_turn_by_gamename(game_name)
    min_elect = get_elect_min(turn_id)
    # Get the list of live players
    players_list = get_player_list(game_name)
    player_before_bewitched = get_turn(turn_id).player_crucio
    list_available_players = \
        list(filter(lambda x: player_to_dict(x.id)["is_alive"] == 1
                        and x.id != min_elect
                        and x.id != player_before_bewitched, players_list))
    list_player_dict = []
    for p in list_available_players:
        list_player_dict.append(player_to_dict(p.id))
    return{"list_players": list_player_dict}

@app.get("/crucio")
async def crucio(game_name:str, victim: int):
    if (not game_exists(game_name)):
        raise HTTPException(status_code=400,
                            detail="the game not exist")
    if game_is_not_started(game_name):
        raise HTTPException(status_code=400,
                            detail="game is not started")
    if get_turn(get_turn_by_gamename(game_name)).player_crucio == victim:
        raise HTTPException(status_code=401,
                            detail="player already bewitched")
    player_dict = player_to_dict(victim)
    set_player_crucio(game_name, victim)
    return{"alias": player_dict["alias"], "loyalty": player_dict["loyalty"]}

@app.get("/avada_kedavra")
async def avada_kedavra(game_name: str, victim: int):
    if (not game_exists(game_name)):
        raise HTTPException(status_code=400,
                            detail="the game not exist")
    if game_is_not_started(game_name):
        raise HTTPException(status_code=400,
                            detail="game is not started")
    if (not player_belong_to_game(victim,game_name)):
        raise HTTPException(status_code=400,
                            detail="player doesnt belong to game or not exist")
    player_dict = player_to_dict(victim)
    if not player_dict["is_alive"]:
        raise HTTPException(status_code=401,
                            detail="This player already death")
    update_player_alive(victim)
    turn_id = get_turn_by_gamename(game_name)
    set_player_killed(turn_id, victim)
    if player_dict["rol"] == "Voldemort":
        set_phase_game(game_name, 5)
        return {"player_murdered": player_dict}
    else:
        set_phase_game(game_name, 1)
        return {"player_murdered": player_dict}

@app.get("/list_imperius")
async def list_imperius(game_name):
    turn_id = get_turn_by_gamename(game_name)
    min_elect = get_elect_min(turn_id)
    players_list = get_player_list(game_name)
    players_availables = list(filter(lambda p: p.is_alive and
                                            p.id != min_elect, players_list))
    list_player_dict = []
    for p in players_availables:
        list_player_dict.append(player_to_dict(p.id))
    return { "players_spellbinding": list_player_dict
    }

@app.post("/imperius")
async def imperius(game_name: str, new_min_id: int):
    if game_exists(game_name):
        if game_is_not_started(game_name):
            raise HTTPException(status_code=400, detail="game is not started")
        turn_id = get_turn_by_gamename(game_name)
        elect_min = get_elect_min(turn_id)
        if player_doesnt_exists(new_min_id) or player_doesnt_exists(elect_min):
            raise HTTPException(status_code=400, detail="new minister or old minister doesnt exists")
        set_min_imperius_old(turn_id, elect_min)
        set_min_imperius_new(turn_id, new_min_id)
        return {"ministers seted correctly"}
    else:
        raise HTTPException(status_code=400, detail="inexistent game")


@app.post("/finish_imperius")
async def finish_imperius(game_name: str):
    if game_exists(game_name):
        if game_is_not_started(game_name):
            raise HTTPException(status_code=400, detail="game is not started")
        turn_id = get_turn_by_gamename(game_name)
        turn = get_turn(turn_id)
        set_previous_min(turn_id, turn.imperius_minister_old)
        set_min_imperius_old_None(turn_id)
        set_min_imperius_new_None(turn_id)
        return {"imperius_finished"}
    else:
        raise HTTPException(status_code=400, detail="inexistent game")

@app.put("/expelliarmus")
async def expelliarmus(game_name: str, vote: bool):
    if get_num_proclamations_death_eaters(game_name) < 5:
        raise HTTPException(status_code=401,
                            detail="there are not enough proclamations")
    set_phase_game(game_name, 7)
    turn_id = get_turn_by_gamename(game_name)
    if vote:
        increment_pos_votes(turn_id)
    else:
        increment_neg_votes(turn_id)
    if get_total_votes(turn_id) == 2:
        if get_status_vote(turn_id):
            increment_marker(turn_id)
            set_vote_to_zero(turn_id)
            list_of_cards_id = get_cards_in_game(game_name)
            cards_list = []
            for c in range(2):
                cards_list.append(card_to_dict(list_of_cards_id.pop()))
            increment_marker(turn_id)
            discard(cards_list[0]["id"])
            discard(cards_list[1]["id"])
            set_phase_game(game_name, 1)
            reset_votes_players(game_name)
            return {"Se descartaron las cartas"}
        else:
            set_vote_to_zero(turn_id)
            set_phase_game(game_name, 3)
            reset_votes_players(game_name)
            return {"No se produjo expelliarmus"}
    else:
        return {"Se voto un expelliarmus tiene que decidir el ministro"}


@app.get("/caos")
async def caos(game_name: str):
    if (not game_exists(game_name)):
        raise HTTPException(status_code=401,
                            detail="the game not exist")
    if game_is_not_started(game_name):
        raise HTTPException(status_code=401,
                            detail="game is not started")
    # Get card
    list_of_cards_id = get_cards_in_game(game_name)
    cards_list = [card_to_dict(list_of_cards_id.pop())]
    # Proclaim
    card_id = cards_list[0]["id"]
    turn_id = get_turn_by_gamename(game_name)
    proclaim(card_id)
    box_id = get_next_box(card_id, game_name)
    box = get_box(box_id)
    set_used_box(box_id)
    if num_of_cards_in_steal_stack(game_name) < MIN_CARDS_IN_STACK:
        shuffle_cards(game_name)
    # In case the game ends
    if (box.loyalty == "Fenix Order" and box.position == MAX_BOX_FENIX_ORDER) or \
            (box.loyalty == "Death Eaters" and box.position == MAX_BOX_DEATH_EATERS):
        set_phase_game(game_name, 5)
        finish_game_id = end_game(game_name, box.loyalty)
        return finished_game_to_dict(finish_game_id)
    set_phase_game(game_name, 1)
    marker_to_zero(turn_id)
    # Limitations are eliminated
    set_elect_dir(turn_id, None)
    set_elect_min(turn_id, None)
    return {
        "box": box_to_dict(box_id)
    }

@app.get("/game_state")
async def get_game_state(game_name: str):
    num_fenix_orders_proclamed = get_num_proclamations_order_fenix(game_name)
    num_death_eaters_proclamed = get_num_proclamations_death_eaters(game_name)
    num_proclamations_availables = num_of_cards_in_steal_stack(game_name)
    num_proclamations_discarded = get_number_proclamations_discarded(game_name)
    election_marker = get_election_marker(game_name)
    return {
        "num_fenix_orders": num_fenix_orders_proclamed,
        "num_death_eaters": num_death_eaters_proclamed,
        "num_proclamations_avilables": num_proclamations_availables,
        "num_proclamations_discarted": num_proclamations_discarded,
        "election_marker": election_marker
    }



@app.get("/game_is_started")
async def game_is_started(game_name: str):
    if not game_is_not_started(game_name):
        return {"status": 'started'}
    else:
        return {"status": 'not started'}

@app.get("/postulated")
async def get_two_postulateds(game_name: str):
    turn_id = get_turn_by_gamename(game_name)
    post_min_id = get_post_min(turn_id)
    post_dir_id = get_post_dir(turn_id)
    post_min = player_to_dict(post_min_id)
    post_dir = player_to_dict(post_dir_id)
    return {
        "post_director": post_dir,
        "post_minister": post_min
    }

@app.get("/phase")
async def get_phase(game_name):
    if get_phase_game(game_name) == 0:
        players_list = get_player_list(game_name)
        list_players_dict = []
        for p in players_list:
            list_players_dict.append(player_to_dict(p.id))
        return {"phase_game": get_phase_game(game_name), "players_list": list_players_dict}
    if get_phase_game(game_name) == 6:
        box = get_last_box_used(game_name)
        return {"phase_game": get_phase_game(game_name), "spell": box.spell}
    else:
        return {"phase_game": get_phase_game(game_name),
        "player_murdered" : player_to_dict(get_turn(get_turn_by_gamename(game_name)).player_killed)}

@app.post("/phase")
async def set_phase(game_name: str, phase: int):
    set_phase_game(game_name, phase)

@app.get("/get_player")
async def get_player(game_name: str, current_user: User = Depends(get_current_user)):
    player_id = get_player_in_game_by_email(game_name,current_user.email_address)
    return {"player": player_to_dict(player_id)}

@app.get("/get_players")
async def get_players_in_game(game_name: str):
    players_list = get_player_list(game_name)
    list_player_dict = []
    for p in players_list:
        list_player_dict.append(player_to_dict(p.id))
    return {"players_list": list_player_dict}

@app.get("/dirmin_elect")
async def get_min_dir_elect(game_name: str):
    if game_exists(game_name):
        if game_is_not_started(game_name):
            raise HTTPException(status_code=400, detail="game is not started")
        turn_id = get_turn_by_gamename(game_name)
        elect_min_id = get_elect_min(turn_id)
        elect_dir_id = get_elect_dir(turn_id)
        player_min = player_to_dict(elect_min_id)
        player_dir = player_to_dict(elect_dir_id)
        return {"elect_min": player_min,
                "elect_dir": player_dir}
    else:
        raise HTTPException(status_code=400, detail="inexistent game")

@app.get("/player_murdered")
async def get_player_murdered(game_name: str):
    turn_id = get_turn_by_gamename(game_name)
    player_id = get_player_killed(turn_id)
    return {
        "player_murdered": player_to_dict(player_id)
    }