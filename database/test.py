from database import *


#new_user("valen","valen@gmail.com","asdasd","foto")
#new_user("valen","valen2@gmail.com","asdasd2","foto")
#new_user("valen","valen3@gmail.com","asdasd3","foto")
#print(get_user_by_email("valen@gmail.com").games)
#3 users added
#show(Game)

#new_game("game",5)
#new_deck("game")
print("---------------- Mezclamos Cartas -----------------------")
proclamaciones_mezcladas = shuffle_cards("game")
print(proclamaciones_mezcladas)
print("---------------- Obtenemos Cartas en su posicion en diferentes partes del juego -----------------------")
print(get_cards_in_game("game"))


cartas = get_cards_in_game("game")
primera = get_card_in_the_steal_stack(cartas.pop())
print("Primera carta: ")
print(primera)
segunda = get_card_in_the_steal_stack(cartas.pop())
print("Segunda carta: ")
print(segunda)
tercera = get_card_in_the_steal_stack(cartas.pop())
print("Tercera carta: ")
print(tercera)
print("---------------- Descartamos la primera y la tercera y luego proclamamos la segunda -----------------------")
print(card_to_dict(primera.id))
print(card_to_dict(segunda.id))
print(card_to_dict(tercera.id))
discard(primera.id)
discard(tercera.id)
proclam(segunda.id)
print("---------------- Obtenemos Cartas en su posicion en diferentes partes del juego -----------------------")
print(get_cards_in_game("game"))
print("---------------- si nos quedamos sin cartas en la pila del robo, mezclamos las deswcartas y las de la pila del robo -----------------------")
print(shuffle_cards("game"))


