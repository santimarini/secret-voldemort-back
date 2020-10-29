from fastapi import FastAPI
from database.database import *
from user import *
from loginfunctions import *
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
                 hash_password(user_to_reg.password), "photo")
        return {"email": user_to_reg.email}


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # return token to identify a specific user, it'll be the user's email for simplicity
    return {"access_token": user.email_address, "token_type": "bearer"}

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
    set_game_started(game_name)
    new_turn(game_name)
    #configuracion de tablero
    #asignacion de roles
    #asignacion de lealtades
    return {
        "game started!"
    }

@app.post("/new_turn")
async def new_turn_begin(game_name: str):
    turn_id = get_turn_by_gamename(game_name)
    next_turn(turn_id)
    ## Este endpoint podria recibir tambien un model hechizo y setear el min postulado
    turn = get_turn(turn_id)
    next_id_min = get_next_player_to_min(game_name, turn.previous_min)
    print(next_id_min)
    set_post_min(turn_id, next_id_min)
    player_min = player_to_dict(next_id_min)
    return {
        "ministro_postulado_actual": player_min
    }

@app.post("/pass_turn")
async def pass_turn(game_name: str):
    turn_id = get_turn_by_gamename(game_name)
    turn = get_turn(turn_id)
    actual_min_id = turn.post_min
    set_previous_min(turn_id, actual_min_id)
    return {
        "turno pasado!"
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
               "vote_less": (num_of_players_alive(game_name) - get_total_votes(turn_id))}

@app.put("/game/{game_name}/dir")
async def dir_post(game_name: str, dir: int):
    turn_id = get_turn_by_gamename(game_name)
    set_post_dir(turn_id, dir)
    dir_dict = player_to_dict(dir)
    return{"postulated_director": dir_dict,
           "postulated minister": player_to_dict(get_post_min(turn_id))}