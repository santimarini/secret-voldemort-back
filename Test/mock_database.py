import sys
import os

# DATABASE_PATH = '/home/valentin/secvold/secret-voldemort-back/database'
DATABASE_PATH = '/home/joaquin/secret-voldemort-back/database'
# DATABASE_PATH = '/home/agusten/Pavilion/UNC/3erAño/IngenieriaDelSoftware/SecretVoldemort/Proyect/database'

sys.path.insert(1, DATABASE_PATH)

from database import *

new_user('user1', 'emailaddress1@gmail.com', 'password')
new_user('user2', 'emailaddress2@gmail.com', 'password')
new_user('user3', 'emailaddress3@gmail.com', 'password')
new_user('user4', 'emailaddress4@gmail.com', 'password')
new_user('user5', 'emailaddress5@gmail.com', 'password')
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

new_user('user1', 'emailaddress10@gmail.com', 'password')
new_user('user2', 'emailaddress20@gmail.com', 'password')
new_user('user3', 'emailaddress30@gmail.com', 'password')
new_user('user4', 'emailaddress40@gmail.com', 'password')
new_user('user5', 'emailaddress50@gmail.com', 'password')
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

player_id_1= new_player('emailaddress1@gmail.com')
player_id_2= new_player('emailaddress2@gmail.com')
player_id_3= new_player('emailaddress3@gmail.com')
player_id_4= new_player('emailaddress4@gmail.com')
player_id_5= new_player('emailaddress5@gmail.com')

# GameTest
new_game('game_name_test',5,'emailaddress1@gmail.com')
new_game('game_test_start',5,'emailaddress1@gmail.com')
join_game(player_id_1,'game_test_start')
join_game(player_id_2,'game_test_start')
join_game(player_id_3,'game_test_start')
join_game(player_id_4,'game_test_start')
join_game(player_id_5,'game_test_start')

#GameInitTest
new_game('game_init_test',5,'emailaddress1@gmail.com')
player_id_11= new_player('emailaddress1@gmail.com')
player_id_21= new_player('emailaddress2@gmail.com')
player_id_31= new_player('emailaddress3@gmail.com')
player_id_41= new_player('emailaddress4@gmail.com')
player_id_51= new_player('emailaddress5@gmail.com')
join_game(player_id_11,'game_init_test')
join_game(player_id_21,'game_init_test')
join_game(player_id_31,'game_init_test')
join_game(player_id_41,'game_init_test')
join_game(player_id_51,'game_init_test')

new_game('game_init_test_2',5,'emailaddress1@gmail.com')
player_id_12= new_player('emailaddress1@gmail.com')
player_id_22= new_player('emailaddress2@gmail.com')
player_id_32= new_player('emailaddress3@gmail.com')
player_id_42= new_player('emailaddress4@gmail.com')
player_id_52= new_player('emailaddress5@gmail.com')
join_game(player_id_12,'game_init_test_2')
join_game(player_id_22,'game_init_test_2')
join_game(player_id_32,'game_init_test_2')
join_game(player_id_42,'game_init_test_2')
join_game(player_id_52,'game_init_test_2')

new_game('game_init_test_3',5,'emailaddress1@gmail.com')
player_id_13= new_player('emailaddress1@gmail.com')
player_id_23= new_player('emailaddress2@gmail.com')
player_id_33= new_player('emailaddress3@gmail.com')
player_id_43= new_player('emailaddress4@gmail.com')
player_id_53= new_player('emailaddress5@gmail.com')
join_game(player_id_13,'game_init_test_3')
join_game(player_id_23,'game_init_test_3')
join_game(player_id_33,'game_init_test_3')
join_game(player_id_43,'game_init_test_3')
join_game(player_id_53,'game_init_test_3')

new_game('game_init_test_4',5,'emailaddress1@gmail.com')
player_id_14= new_player('emailaddress1@gmail.com')
player_id_24= new_player('emailaddress2@gmail.com')
player_id_34= new_player('emailaddress3@gmail.com')
player_id_44= new_player('emailaddress4@gmail.com')
player_id_54= new_player('emailaddress5@gmail.com')
join_game(player_id_14,'game_init_test_4')
join_game(player_id_24,'game_init_test_4')
join_game(player_id_34,'game_init_test_4')
join_game(player_id_44,'game_init_test_4')
join_game(player_id_54,'game_init_test_4')

new_game('game_init_test_5',5,'emailaddress1@gmail.com')
player_id_15= new_player('emailaddress1@gmail.com')
player_id_25= new_player('emailaddress2@gmail.com')
player_id_35= new_player('emailaddress3@gmail.com')
player_id_45= new_player('emailaddress4@gmail.com')
player_id_55= new_player('emailaddress5@gmail.com')
join_game(player_id_15,'game_init_test_5')
join_game(player_id_25,'game_init_test_5')
join_game(player_id_35,'game_init_test_5')
join_game(player_id_45,'game_init_test_5')
join_game(player_id_55,'game_init_test_5')

new_game('game_init_test_6',5,'emailaddress1@gmail.com')
player_id_16= new_player('emailaddress1@gmail.com')
player_id_26= new_player('emailaddress2@gmail.com')
player_id_36= new_player('emailaddress3@gmail.com')
player_id_46= new_player('emailaddress4@gmail.com')
player_id_56= new_player('emailaddress5@gmail.com')
join_game(player_id_16,'game_init_test_6')
join_game(player_id_26,'game_init_test_6')
join_game(player_id_36,'game_init_test_6')
join_game(player_id_46,'game_init_test_6')
join_game(player_id_56,'game_init_test_6')

new_user('user12', 'user12@gmail.com', 'password')
set_user_verified("user12@gmail.com")

new_game('game_init_test_7',5,'emailaddress1@gmail.com')
player_id_17= new_player('emailaddress1@gmail.com')
player_id_27= new_player('emailaddress2@gmail.com')
player_id_37= new_player('emailaddress3@gmail.com')
player_id_47= new_player('emailaddress4@gmail.com')
player_id_57= new_player('emailaddress5@gmail.com')
join_game(player_id_17,'game_init_test_7')
join_game(player_id_27,'game_init_test_7')
join_game(player_id_37,'game_init_test_7')
join_game(player_id_47,'game_init_test_7')
join_game(player_id_57,'game_init_test_7')

new_game('game_init_test_8',5,'emailaddress1@gmail.com')
player_id_18= new_player('emailaddress1@gmail.com')
player_id_28= new_player('emailaddress2@gmail.com')
player_id_38= new_player('emailaddress3@gmail.com')
player_id_48= new_player('emailaddress4@gmail.com')
player_id_58= new_player('emailaddress5@gmail.com')
join_game(player_id_18,'game_init_test_8')
join_game(player_id_28,'game_init_test_8')
join_game(player_id_38,'game_init_test_8')
join_game(player_id_48,'game_init_test_8')
join_game(player_id_58,'game_init_test_8')

new_game('game_init_test_9',5,'emailaddress1@gmail.com')
player_id_19= new_player('emailaddress1@gmail.com')
player_id_29= new_player('emailaddress2@gmail.com')
player_id_39= new_player('emailaddress3@gmail.com')
player_id_49= new_player('emailaddress4@gmail.com')
player_id_59= new_player('emailaddress5@gmail.com')
join_game(player_id_19,'game_init_test_9')
join_game(player_id_29,'game_init_test_9')
join_game(player_id_39,'game_init_test_9')
join_game(player_id_49,'game_init_test_9')
join_game(player_id_59,'game_init_test_9')

new_game('game_init_test_10',5,'emailaddress1@gmail.com')
player_id_20= new_player('emailaddress1@gmail.com')
player_id_30= new_player('emailaddress2@gmail.com')
player_id_40= new_player('emailaddress3@gmail.com')
player_id_50= new_player('emailaddress4@gmail.com')
player_id_60= new_player('emailaddress5@gmail.com')
join_game(player_id_20,'game_init_test_10')
join_game(player_id_30,'game_init_test_10')
join_game(player_id_40,'game_init_test_10')
join_game(player_id_50,'game_init_test_10')
join_game(player_id_60,'game_init_test_10')

new_user('user11', 'emailaddress11@gmail.com', 'password')
new_user('user21', 'emailaddress21@gmail.com', 'password')
new_user('user31', 'emailaddress31@gmail.com', 'password')
new_user('user41', 'emailaddress41@gmail.com', 'password')
new_user('user51', 'emailaddress51@gmail.com', 'password')

player_id_80= new_player('emailaddress11@gmail.com')
player_id_81= new_player('emailaddress21@gmail.com')
player_id_82= new_player('emailaddress31@gmail.com')
player_id_83= new_player('emailaddress41@gmail.com')
player_id_84= new_player('emailaddress51@gmail.com')
new_game('game_init_test_15',5,'emailaddress1@gmail.com')
join_game(player_id_80,'game_init_test_15')
join_game(player_id_81,'game_init_test_15')
join_game(player_id_82,'game_init_test_15')
join_game(player_id_83,'game_init_test_15')
join_game(player_id_84,'game_init_test_15')

player_id_aa1= new_player('emailaddress11@gmail.com')
player_id_aa2= new_player('emailaddress21@gmail.com')
player_id_aa3= new_player('emailaddress31@gmail.com')
player_id_aa4= new_player('emailaddress41@gmail.com')
player_id_aa5= new_player('emailaddress51@gmail.com')
new_game('game_init_aa1',5,'emailaddress11@gmail.com')
join_game(player_id_aa1,'game_init_aa1')
join_game(player_id_aa2,'game_init_aa1')
join_game(player_id_aa3,'game_init_aa1')
join_game(player_id_aa4,'game_init_aa1')
join_game(player_id_aa5,'game_init_aa1')

player_id_aa6= new_player('emailaddress11@gmail.com')
player_id_aa7= new_player('emailaddress21@gmail.com')
player_id_aa8= new_player('emailaddress31@gmail.com')
player_id_aa9= new_player('emailaddress41@gmail.com')
player_id_aa10= new_player('emailaddress51@gmail.com')
new_game('game_init_aa2',5,'emailaddress11@gmail.com')
join_game(player_id_aa6,'game_init_aa2')
join_game(player_id_aa7,'game_init_aa2')
join_game(player_id_aa8,'game_init_aa2')
join_game(player_id_aa9,'game_init_aa2')
join_game(player_id_aa10,'game_init_aa2')

player_id_aa11= new_player('emailaddress11@gmail.com')
player_id_aa12= new_player('emailaddress21@gmail.com')
player_id_aa13= new_player('emailaddress31@gmail.com')
player_id_aa14= new_player('emailaddress41@gmail.com')
player_id_aa15= new_player('emailaddress51@gmail.com')
new_game('game_init_aa3',5,'emailaddress11@gmail.com')
join_game(player_id_aa11,'game_init_aa3')
join_game(player_id_aa12,'game_init_aa3')
join_game(player_id_aa13,'game_init_aa3')
join_game(player_id_aa14,'game_init_aa3')
join_game(player_id_aa15,'game_init_aa3')

player_id_aa16= new_player('emailaddress11@gmail.com')
player_id_aa17= new_player('emailaddress21@gmail.com')
player_id_aa18= new_player('emailaddress31@gmail.com')
player_id_aa19= new_player('emailaddress41@gmail.com')
player_id_aa20= new_player('emailaddress51@gmail.com')
new_game('game_init_aa4',5,'emailaddress11@gmail.com')
join_game(player_id_aa16,'game_init_aa4')
join_game(player_id_aa17,'game_init_aa4')
join_game(player_id_aa18,'game_init_aa4')
join_game(player_id_aa19,'game_init_aa4')
join_game(player_id_aa20,'game_init_aa4')
=======
player_id_a1= new_player('emailaddress11@gmail.com')
player_id_a2= new_player('emailaddress21@gmail.com')
player_id_a3= new_player('emailaddress31@gmail.com')
player_id_a4= new_player('emailaddress41@gmail.com')
player_id_a5= new_player('emailaddress51@gmail.com')
new_game('game_init_test_a1',5,'emailaddress1@gmail.com')
join_game(player_id_a1,'game_init_test_a1')
join_game(player_id_a2,'game_init_test_a1')
join_game(player_id_a3,'game_init_test_a1')
join_game(player_id_a4,'game_init_test_a1')
join_game(player_id_a5,'game_init_test_a1')

player_id_a6= new_player('emailaddress11@gmail.com')
player_id_a7= new_player('emailaddress21@gmail.com')
player_id_a8= new_player('emailaddress31@gmail.com')
player_id_a9= new_player('emailaddress41@gmail.com')
player_id_a10= new_player('emailaddress51@gmail.com')
new_game('game_init_test_a2',5,'emailaddress11@gmail.com')
join_game(player_id_a6,'game_init_test_a2')
join_game(player_id_a7,'game_init_test_a2')
join_game(player_id_a8,'game_init_test_a2')
join_game(player_id_a9,'game_init_test_a2')
join_game(player_id_a10,'game_init_test_a2')
