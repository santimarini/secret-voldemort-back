import sys
import os
sys.path.insert(1, '/home/valentin/secvold/secret-voldemort-back/database')
try:
    os.remove('/home/valentin/secvold/secret-voldemort-back/database/database.sqlite')
except OSError:
    pass
from database import *


new_user('user1', 'emailaddress1@gmail.com', 'password', 'photo')
new_user('user2', 'emailaddress2@gmail.com', 'password', 'photo')
new_user('user3', 'emailaddress3@gmail.com', 'password', 'photo')
new_user('user4', 'emailaddress4@gmail.com', 'password', 'photo')
new_user('user5', 'emailaddress5@gmail.com', 'password', 'photo')
#new_player('emailaddress1@gmail.com')
p2 = new_player('emailaddress2@gmail.com')
p3 = new_player('emailaddress3@gmail.com')
p4 = new_player('emailaddress4@gmail.com')
p5 = new_player('emailaddress5@gmail.com')
game_name = new_game('game_name',10,'emailaddress1@gmail.com')
join_game(p2, game_name)
join_game(p3, game_name)
join_game(p4, game_name)
join_game(p5, game_name)
set_game_started(game_name)
set_phase_game(game_name,1)
turn_id = new_turn(game_name)
set_elect_dir(turn_id,p2)
set_elect_min(turn_id,p3)
set_previous_min(turn_id,p4)
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

new_user('user1', 'emailaddress10@gmail.com', 'password', 'photo')
new_user('user2', 'emailaddress20@gmail.com', 'password', 'photo')
new_user('user3', 'emailaddress30@gmail.com', 'password', 'photo')
new_user('user4', 'emailaddress40@gmail.com', 'password', 'photo')
new_user('user5', 'emailaddress50@gmail.com', 'password', 'photo')
#pp2 = new_player('emailaddress20@gmail.com')
pp3 = new_player('emailaddress30@gmail.com')
pp4 = new_player('emailaddress40@gmail.com')
pp5 = new_player('emailaddress50@gmail.com')
game_name_not_started = new_game('game_name_not_started',10,'emailaddress20@gmail.com')
#join_game(pp2, game_name_not_started)
join_game(pp3, game_name_not_started)
join_game(pp4, game_name_not_started)
join_game(pp5, game_name_not_started)
new_turn(game_name_not_started)
