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
        game_name = new_game(game.name, game.max_players)
        player_id = new_player(game.email)
        print(player_id)
        join_game(player_id, game_name)
        return {"name": game_name}

# Entry of url to join the game
@app.post("/game/{game_name}")
async def join_url(game_name: str, email: str):
    if game_exists(game_name):
        game = get_game_by_name(game_name)
        player_id = new_player(email)
        if not is_user_in_game(email, game_name):
            if num_of_players(game_name) < game.max_players:
                join_game(player_id, game_name)
                return {"username": get_user_by_email(email).name}
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
