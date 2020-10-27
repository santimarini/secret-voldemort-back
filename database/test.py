from database import *


#new_user("valen","valen@gmail.com","asdasd","foto")
#new_user("valen","valen2@gmail.com","asdasd2","foto")
#new_user("valen","valen3@gmail.com","asdasd3","foto")
#print(get_user_by_email("valen@gmail.com").games)
#3 users added
#show(Game)


new_user("valen","valen@gmail.com","pass","foto")
new_user("valen","valen2@gmail.com","pass","foto")
print(new_game("partida1",5,"valen@gmail.com"))
print(game_exists("partida1"))
pid = new_player("valen@gmail.com")
pid2 = new_player("valen2@gmail.com")
tid = new_turn("partida1",pid)
print(get_turn(tid).num_of_turn)
next_turn(tid)
print(get_turn(tid).num_of_turn)
print("------------------------------")
print(get_turn(tid).elect_dir)
set_elect_dir(tid,pid2)
print(get_turn(tid).num_of_turn)
#print(pid)
#print(pid2)
#print("--------------")
#join_game(pid,"partida1")
#print(is_player_in_game(pid,"partida1"))
#print(is_player_in_game(pid2,"partida1"))
