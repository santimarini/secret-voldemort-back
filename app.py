from fastapi import FastAPI
from database.database import *
from login_functions import *
from fastapi.middleware.cors import CORSMiddleware

MAX_LEN_FIELD = 16
MIN_LEN_FIELD = 4
MAX_LEN_EMAIL = 30
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
    "http://localhost:3000"
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
    if len(user_to_reg.alias) > MAX_LEN_FIELD or \
       len(user_to_reg.alias) < MIN_LEN_FIELD or \
       len(user_to_reg.password) > MAX_LEN_FIELD or \
       len(user_to_reg.password) < MIN_LEN_FIELD or \
       len(user_to_reg.email) > MAX_LEN_EMAIL:
        raise invalid_fields
    if email_exists(user_to_reg.email):
        raise HTTPException(
            status_code=404,
            detail="existing user"
        )
    else:
        new_user(user_to_reg.alias, user_to_reg.email,
                 get_password_hash(user_to_reg.password), "photo")
        email = EmailSchema(email=[user_to_reg.email])
        validate_token_expires = timedelta(minutes=VALIDATE_TOKEN_EXPIRE_MINUTES)
        validate_token = create_token(
            data={"sub": user_to_reg.email}, expires_delta=validate_token_expires
        )
        html = generate_html(user_to_reg.alias,validate_token)
        message = get_message(email,html)
        fm = FastMail(conf)
        await fm.send_message(message)
        return {"email": user_to_reg.email}

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
    return {"Gracias por verificar tu email! email_user": email}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect alias or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.email_address}, expires_delta=access_token_expires
    )
    return {"alias": user.name, "photo": "photo",
            "access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {current_user.email_address}

@app.post("/newgame")
async def create_game(game: ConfigGame,
                      current_user: User = Depends(get_current_verified_user)):
    if game.max_players < MIN_NUM_OF_PLAYERS or game.max_players > MAX_NUM_OF_PLAYERS:
        raise HTTPException(status_code=401,
                            detail="the number of players must be between 5 and 10"
                            )
    if game_exists(game.name):
        raise HTTPException(status_code=401, detail="Game already exists")
    if len(game.name) < MIN_LEN_FIELD or len(game.name) > MAX_LEN_FIELD:
        HTTPException(status_code=404,detail="field size is invalid")
    else:
        game_name = new_game(game.name, game.max_players, current_user.email_address)
        return {"name": game_name}


@app.get("/game/{game_name}")
async def join_url(game_name: str, current_user: User = Depends(get_current_verified_user)):
    if game_exists(game_name):
        if get_game_by_name(game_name).initial_date is not None:
            raise HTTPException(status_code=404, detail="The game has already started")
        else:
            game = get_game_by_name(game_name)
            if not is_user_in_game(current_user.email_address, game_name):
                if num_of_players(game_name) < game.max_players:
                    player_id = new_player(current_user.email_address)
                    join_game(player_id, game_name)
                    list = get_player_list(game_name)
                    list_dict = []
                    for p in list:
                        list_dict.append(player_to_dict(p.id))
                    return {"alias": get_user_by_email(current_user.email_address).name,
                            "game_name": game_name,
                            "max_players": game.max_players,
                            "players": list_dict,
                            "creator": game.creator}
                else:
                    raise HTTPException(status_code=404, detail="The room is full")
            else:
                raise HTTPException(status_code=300, detail="Player already in the game")
    else:
        raise HTTPException(status_code=404, detail="Game is not exists")

@app.post("/start")
async def start_game(game_name: str):
    if num_of_players(game_name) < MIN_NUM_OF_PLAYERS:
        raise HTTPException(status_code=403, detail="There aren't enough players")
    set_game_started(game_name)
    set_phase_game(game_name,1)
    new_turn(game_name)
    new_deck(game_name)
    shuffle_cards(game_name)
    new_templates(game_name)
    np = num_of_players(game_name)
    if np == 5 or np == 6:
        config_template_6players(game_name)
    if np == 7 or np == 8:
        config_template_8players(game_name)
    if np == 9 or np == 10:
        config_template_10players(game_name)
    return {
        "game started!"
    }

@app.post("/next_turn")
async def new_turn_begin(game_name: str):
    turn_id = get_turn_by_gamename(game_name)
    next_turn(turn_id)
    turn = get_turn(turn_id)
    next_id_min = get_next_player_to_min(game_name, turn.previous_min)
    set_post_min(turn_id, next_id_min)
    player_min = player_to_dict(next_id_min)
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
    return {
        "minister": player_min,
        "players": list_player_dict
    }

@app.put("/game")
async def dir_post(game_name: str, dir: int):
    set_phase_game(game_name,2)
    turn_id = get_turn_by_gamename(game_name)
    set_post_dir(turn_id, dir)
    dir_dict = player_to_dict(dir)
    return{"post_director": dir_dict,
           "post_minister": player_to_dict(get_post_min(turn_id))
          }

@app.put("/game/{game_name}/vote")
async def vote_player(game_name: str, vote: bool):
    turn_id = get_turn_by_gamename(game_name)
    if vote:
        increment_pos_votes(turn_id)
    else:
        increment_neg_votes(turn_id)
    if num_of_players_alive(game_name) == get_total_votes(turn_id):
        if get_status_vote(turn_id):
            set_phase_game(game_name,3)
            marker_to_zero(turn_id)
            set_elect_min(turn_id, get_post_min(turn_id))
            set_elect_dir(turn_id, get_post_dir(turn_id))
            set_previous_min(turn_id, get_elect_min(turn_id))
            set_previous_dir(turn_id, get_elect_dir(turn_id))
            set_vote_to_zero(turn_id)
            return {"elect_min": player_to_dict(get_elect_min(turn_id)),
                    "elect_dir": player_to_dict(get_elect_dir(turn_id))}
        else:
            set_phase_game(game_name,1)
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
               "vote_less": (num_of_players_alive(game_name) - get_total_votes(turn_id))
              }

@app.get("/cards/draw_three_cards")
async def draw_three_cards(game_name: str):
    if(num_of_cards_in_steal_stack(game_name) < MIN_CARDS_IN_STACK):
        shuffle_cards(game_name)
    list_of_cards_id = get_cards_in_game(game_name)
    cards_list = []
    for c in range(3):
        cards_list.append(card_to_dict(list_of_cards_id.pop()))
    return {"cards_list" : cards_list}

@app.put("/cards/discard_min")
async def discard_card_min(card_id: int, game_name: str):
    set_phase_game(game_name,4)
    discard(card_id)
    card = card_to_dict(card_id)
    return {"card": card}

@app.get("/cards/draw_two_cards")
async def draw_two_cards(game_name: str):
    list_of_cards_id = get_cards_in_game(game_name)
    cards_list = []
    for c in range(2):
        cards_list.append(card_to_dict(list_of_cards_id.pop()))
    return {"cards_list" : cards_list}

@app.put("/cards/discard_dir")
async def discard_card_dir(card_id: int):
    discard(card_id)
    card = card_to_dict(card_id)
    return {"card": card}

@app.put("/cards/proclaim")
async def proclaim_card(card_id,game_name):
    turn_id = get_turn_by_gamename(game_name)
    marker_to_zero(turn_id)
    proclaim(card_id)
    box_id = get_next_box(card_id,game_name)
    box = get_box(box_id)
    set_used_box(box_id)
    if (box.loyalty == "Fenix Order" and box.position == MAX_BOX_FENIX_ORDER) or \
            (box.loyalty == "Death Eaters" and box.position == MAX_BOX_DEATH_EATERS):
        set_phase_game(game_name, 5)
        finish_game_id = end_game(game_name,box.loyalty)
        return finished_game_to_dict(finish_game_id)
    else:
        set_phase_game(game_name, 1)
    return {
        "box": box_to_dict(box_id)
    }

@app.get("/postulated")
async def get_two(game_name: str):
    turn_id = get_turn_by_gamename(game_name)
    post_min_id = get_post_min(turn_id)
    post_dir_id = get_post_dir(turn_id)
    post_min = player_to_dict(post_min_id)
    post_dir = player_to_dict(post_dir_id)
    return {
        "post_director": post_dir,
        "post_minister": post_min
    }


@app.get("/game/is_started")
async def is_started(game_name: str):
    if not (game_name):
         return False
    game = get_game_by_name(game_name)
    return (game.initial_date is not None)

@app.get("/phase")
async def get_phase(game_name):
    return {"phase_game": get_phase_game(game_name)}



@app.get("/dirmin_elect")
async def get_min_dir_elect(game_name: str):
    turn_id = get_turn_by_gamename(game_name)
    elect_min_id = get_elect_min(turn_id)
    elect_dir_id = get_elect_dir(turn_id)
    email_min = get_user_email_by_id(elect_min_id)
    email_dir =  get_user_email_by_id(elect_dir_id)

    return {"elect_min": email_min,
            "elect_dir": email_dir}
