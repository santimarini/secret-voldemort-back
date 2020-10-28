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
            raise HTTPException(
                status_code=404,
                detail="The game has already started")
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
                    raise HTTPException(
                        status_code=404,
                        detail="The room is full")
            else:
                delete_player(player_id)
                raise HTTPException(
                    status_code=404,
                    detail="Player already in the game")
    else:
        raise HTTPException(
            status_code=404,
            detail="Game is not exists")

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
