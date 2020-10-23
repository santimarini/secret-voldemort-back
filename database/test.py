from database import *


#new_user("valen","valen@gmail.com","asdasd","foto")
#new_user("valen","valen2@gmail.com","asdasd2","foto")
#new_user("valen","valen3@gmail.com","asdasd3","foto")
#print(get_user_by_email("valen@gmail.com").games)
#3 users added
#show(Game)


new_user("valen","valen@gmail.com","pass","foto")
new_user("valen","valen2@gmail.com","pass","foto")
print(new_game("partida1",5))
print(game_exists("partida1"))
pid = new_player("valen@gmail.com")
pid2 = new_player("valen2@gmail.com")
print(pid)
print(pid2)
print("--------------")
join_game(pid,"partida1")
print(is_player_in_game(pid,"partida1"))
print(is_player_in_game(pid2,"partida1"))
