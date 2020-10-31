from fastapi import FastAPI
from database.database import *
from pydantic_models import *
from login_functions import *
from fastapi.middleware.cors import CORSMiddleware


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

# Register user
@app.post(
    "/signup",
    status_code=status.HTTP_200_OK
)
async def register_user(user_to_reg: UserTemp):

    if email_exists(user_to_reg.email):
        raise HTTPException(
            status_code=404,
            detail="existing user"
        )
    else:
        new_user(user_to_reg.username, user_to_reg.email,
                 get_password_hash(user_to_reg.password), "photo")
        return {"email": user_to_reg.email}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email_address}, expires_delta=access_token_expires
    )
    return {"access_token": user.email_address, "token_type": "bearer"}  # deberia ir access_token

@app.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return {current_user.email_address}

@app.post("/newgame")
async def create_game(game: ConfigGame):
    if not is_verified(game.email):
        raise HTTPException(status_code=401, detail="No verified email ")
    if game_exists(game.name):
        raise HTTPException(status_code=401, detail="Game already exists")
    else:
        game_name = new_game(game.name, game.max_players, game.email)
        return {"name": game_name }

# Entry of url to join the game
@app.post("/game/{game_name}")
async def join_url(game_name: str, email: str):
    if game_exists(game_name):
        game = get_game_by_name(game_name)
        if game.initial_date is not None:
            raise HTTPException(status_code=404, detail="The game has already started")
        else:
            player_id = new_player(email)
            if not is_user_in_game(email, game_name):
                if num_of_players(game_name) < game.max_players:
                    join_game(player_id, game_name)
                    list = get_player_list(game_name)
                    list_dict = []
                    for p in list:
                        list_dict.append(player_to_dict(p.id))
                    return {"username": get_user_by_email(email).name,
                            "game_name": game_name,
                            "max_players": game.max_players,
                            "players": list_dict,
                            "creator": game.creator}
                else:
                    raise HTTPException(status_code=404, detail="The room is full")
            else:
                delete_player(player_id)
                raise HTTPException(status_code=404, detail="Player already in the game")
    else:
        raise HTTPException(status_code=404, detail="Game is not exists")

@app.post("/start")
async def start_game(game_name: str):
    if num_of_players(game_name) < 5:
        raise HTTPException(status_code=403, detail="There aren't enough players")
    set_game_started(game_name)
    new_turn(game_name)
    new_deck(game_name)
    shuffle_cards(game_name)
    new_templates(game_name)
    np = num_of_players(game_name)
    print(np)
    if np == 5 or np == 6:
        print("5 o 6 jugadores")
        config_template_6players(game_name)
    if np == 7 or np == 8:
        print("7 o 8 jugadores")
        config_template_8players(game_name)
    if np == 9 or np == 10:
        print("9 o 10 jugadores")
        config_template_10players(game_name)
    #asignacion de roles
    #asignacion de lealtades
    return {
        "game started!"
    }

@app.post("/next_turn")
async def new_turn_begin(game_name: str):
    turn_id = get_turn_by_gamename(game_name)
    next_turn(turn_id)
    ## Este endpoint podria recibir tambien un model hechizo y setear el min postulado
    turn = get_turn(turn_id)
    next_id_min = get_next_player_to_min(game_name, turn.previous_min)
    set_post_min(turn_id, next_id_min)
    player_min = player_to_dict(next_id_min)
    if num_of_players_alive(game_name) > 5:
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
    turn_id = get_turn_by_gamename(game_name)
    set_post_dir(turn_id, dir)
    dir_dict = player_to_dict(dir)
    return{"post_director": dir_dict,
           "post_minister": player_to_dict(get_post_min(turn_id))
          }

@app.put("/game/{game_name}/vote")
async def vote_player(game_name: str, vote: bool):
    turn_id = get_turn_by_gamename(game_name)
    # update the votes
    if vote:
        increment_pos_votes(turn_id)
    else:
        increment_neg_votes(turn_id)
    if num_of_players_alive(game_name) == get_total_votes(turn_id):
        # most positive votes
        if get_status_vote(turn_id):
            marker_to_zero(turn_id)
            set_elect_min(turn_id, get_post_min(turn_id))
            set_elect_dir(turn_id, get_post_dir(turn_id))
            set_previous_min(turn_id, get_elect_min(turn_id))
            set_previous_dir(turn_id, get_elect_dir(turn_id))
            set_vote_to_zero(turn_id)
            return {"elect_min": player_to_dict(get_elect_min(turn_id)),
                    "elect_dir": player_to_dict(get_elect_dir(turn_id))}
            # most negative votes
        else:
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
  
@app.get("/cards/draw")
async def draw_cards(game_name: str):
    if(num_of_cards_in_steal_stack(game_name) < 3):
        shuffle_cards(game_name)
    list_of_cards_id = get_cards_in_game(game_name)
    cards_list = []
    for c in range(3):
        cards_list.append(card_to_dict(list_of_cards_id.pop()))
    return {"cards_list" : cards_list}

@app.get("/cards/discard")
async def discard_card(card_id: int):
    discard(card_id)
    card = card_to_dict(card_id)
    return {"Proclamation": card}

@app.put("/cards/proclaim")
async def proclaim_card(card_id,game_name):
    turn_id = get_turn_by_gamename(game_name)
    marker_to_zero(turn_id)
    proclaim(card_id)
    box = get_next_box(card_id,game_name)
    set_used_box(box)
    return {
        "box": box_to_dict(box)
    }

@app.post("/game/{game_name}/finished")
async def finished_game(game_name: str, loyalty_win: str):
    set_end_date(game_name)
    finish_game_id = new_finished_game(game_name, loyalty_win)
    new_players_finished(game_name ,finish_game_id)
    return finished_game_to_dict(finish_game_id)

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

@app.post("/game/box")
async def delete_boxs(game_name: str):
    for b in get_game_by_name(game_name).box:
        delete_box(b.id)