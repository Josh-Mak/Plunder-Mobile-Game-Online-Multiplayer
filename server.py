import socket
from _thread import *
import pickle
from game import Game

server = "10.0.0.12"
port = 5050

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

# stores the ip addresses of connected clients
connected = set()
# store our games with ids
games = {}
# keeps count of are current id so we know what game to do stuff with.
idCount = 0


def get_other_player(p):
    players = [0, 1]
    players.remove(p)
    other_player = players[0]
    return other_player


string_numbers = ["0", "1", "2", "3", '4', "5", "6", "7", "8", "9"]
def threaded_client(conn, p, gameId):
    global idCount
    # sends the connected client what player they are (o or 1)
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(2048*4).decode()

            # every time we run while loop, check if the game still exists
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if "Deck Length" in data:
                        str_deck_length = data.split(",")[1].strip()
                        int_deck_length = int(str_deck_length)
                        game.deck_lengths[p] = int_deck_length
                    elif "Hand Length" in data:
                        str_hand_length = data.split(",")[1].strip()
                        int_hand_length = int(str_hand_length)
                        game.hand_lengths[p] = int_hand_length
                    elif "Starting Stats" in data:
                        str_stats = data.split(",")
                        game.players_base_maxhps[p] = int(str_stats[1])
                        game.players_current_hps[p] = int(str_stats[1])
                        game.players_base_atks[p] = int(str_stats[2])
                        game.players_base_blocks[p] = int(str_stats[3])
                        game.players_base_plunders[p] = int(str_stats[4])
                        game.players_base_explores[p] = int(str_stats[5])
                    elif "Starting Deck" in data:
                        str_list = data.split(":")[1]
                        card_ids_list = []
                        for l in str_list:
                            if l in string_numbers:
                                card_ids_list.append(int(l))
                        game.fill_deck_from_id_list(card_ids_list, game.players_starting_decks[p])
                    elif "Played Card" in data:
                        slot_number = data.split(":")[1]
                        card_idn_str = data.split(":")[2]
                        card_idn = int(card_idn_str)
                        played_card = game.get_card_from_idn(card_idn)
                        game.players_active_slots[p][slot_number] = played_card
                        game.update_card_position(slot_number, p)
                        game.players_turn[p] = False
                        game.players_turn[get_other_player(p)] = True
                        game.player_passed_last_turn[get_other_player(p)] = False
                    elif "Active Card Slot to Discard" in data:
                        player_who_lost_card = data.split(":")[1]
                        player_who_lost_card = int(player_who_lost_card)
                        slot_that_was_lost = data.split(":")[2]
                        card_lost = game.players_active_slots[player_who_lost_card][slot_that_was_lost]
                        game.players_discard_piles[player_who_lost_card].append(card_lost)
                        game.players_active_slots[player_who_lost_card][slot_that_was_lost] = "None"
                    elif "Pass" in data:
                        game.player_passed_last_turn[p] = True
                        if game.player_passed_last_turn[get_other_player(p)]:
                            # trigger end of turn playout thing
                            game.player_passed_last_turn = [False, False]
                            game.end_of_round_effects()
                        else:
                            game.players_turn[p] = False
                            game.players_turn[get_other_player(p)] = True
                    elif "Finished Activations" in data:
                        game.card_currently_activating[p] = None
                        slot_just_activated = data.split(":")[1]
                        int_slot_just_activated = int(slot_just_activated)
                        game.slots_that_have_activated_this_round[p][int_slot_just_activated] = True
                        next_slot = game.get_next_activating_slot(p, int_slot_just_activated)
                        if next_slot:  # next_slot will be None if there's nothing in the next slot to activate
                            game.card_currently_activating[get_other_player(p)] = next_slot
                            game.players_active_slots[get_other_player(p)][next_slot].active = True
                            game.players_turn[p] = False
                            game.players_turn[get_other_player(p)] = True
                    elif "Not Enough Gold for Card" in data:
                        slot_just_activated = game.card_currently_activating[p]
                        int_slot_just_activated = int(slot_just_activated)
                        game.card_currently_activating[p] = None
                        game.slots_that_have_activated_this_round[p][int_slot_just_activated] = True
                        card_that_failed = game.players_active_slots[p][slot_just_activated]
                        card_that_failed.active = False
                        game.players_discard_piles[p].append(card_that_failed)  # move from active to discard pile
                        game.players_active_slots[p][slot_just_activated] = "None"  # replace active with None
                        next_slot = game.get_next_activating_slot(p, int_slot_just_activated)
                        if next_slot:  # next_slot will be None if there's nothing in the next slot to activate
                            game.card_currently_activating[get_other_player(p)] = next_slot
                            game.players_active_slots[get_other_player(p)][next_slot].active = True
                            game.players_turn[p] = False
                            game.players_turn[get_other_player(p)] = True
                    elif "Spent Gold" in data:
                        gold_amount = data.split(":")[1]
                        gold_amount = int(gold_amount)
                        game.players_gold_amounts[p] -= gold_amount
                    elif "Actions Ready" in data:
                        game.actions_submitted[p] = True
                    elif "Turn Actions:" in data:
                        str_actions = data.split(":")[2].strip()
                        game.players_actions[p] = str_actions
                        print(f"Set player {p}'s actions to: {str_actions}")
                        str_stance_ = data.split(":")[1].strip()
                        str_stance = str_stance_.split(",")[1].strip()
                        print(f"Set player {p}'s stance to: {str_stance}")
                        game.players_active_stance[p] = str_stance
                        if game.players_actions[get_other_player(p)] and game.players_active_stance[get_other_player(p)] != "None":
                            game.process_actions()
                    elif "Attacking Damage" in data:
                        str_damage = data.split(",")[1].strip()
                        damage = int(str_damage)
                    elif "Submitting Actions" in data:
                        game.actions_submitted[p] = False
                    # if not one of our things
                    elif data != "get":
                        print(f"ERROR: Data was not something server is familiar with. Data: {data}")

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        print("Closing Game", gameId)
        del games[gameId]
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    # p standing for the current player
    p = 0
    # every 2 people that connect to the server, we increase gameId by 1.
    gameId = (idCount - 1)//2
    # true if player is player 0. This means we need to create a new game. Checking if an odd number basically.
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    # if we dont need to create a new game
    else:
        # game is ready to start playing
        games[gameId].ready = True
        # player = 1 (b/c they are the 2nd player)
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))