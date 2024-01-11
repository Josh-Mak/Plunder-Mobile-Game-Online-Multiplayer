from cards import *
import pygame

def get_other_player(p):
    players = [0, 1]
    players.remove(p)
    other_player = players[0]
    return other_player


class Game:
    def __init__(self, id):

        # region players info
        self.hand_lengths = [0, 0]
        self.deck_lengths = [0, 0]
        self.players_starting_decks = [[], []]
        self.players_discard_piles = [[], []]
        self.players_current_hps = [1, 1]
        self.players_base_maxhps = [1, 1]
        self.players_base_atks = [1, 1]
        self.players_base_blocks = [1, 1]
        self.players_base_plunders = [1, 1]
        self.players_base_explores = [1, 1]

        self.players_chest_amounts = [0, 0]
        self.players_gold_amounts = [3, 3]
        # endregion

        # region Gameplay Variables
        self.players_turn = [True, False]
        self.player_round_starter = [True, False]
        self.player_passed_last_turn = [False, False]
        # endregion

        # region Actions
        self.actions_submitted = [False, False]
        self.players_actions = ["", ""]
        self.players_current_blocking = [0, 0]
        self.players_current_attacking = [0, 0]
        self.players_active_stance = ["None", "None"]
        self.players_active_slots = [{'0': "None", '1': "None", '2': "None", '3': "None", '4': "None", 's': "None"},
                                     {'0': "None", '1': "None", '2': "None", '3': "None", '4': "None", 's': "None"}]
        self.card_currently_activating = [None, None]
        self.slots_that_have_activated_this_round = [[False, False, False, False, False], [False, False, False, False, False]]
        # endregion

        # region Active Slot Box Dicts
        self.active_slot_dict_self = {"0": pygame.Rect(100, 500, 65, 87),
                                      "1": pygame.Rect(175, 500, 65, 87),
                                      "2": pygame.Rect(250, 500, 65, 87),
                                      "3": pygame.Rect(325, 500, 65, 87),
                                      "4": pygame.Rect(400, 500, 65, 87),
                                      "s": pygame.Rect(475, 500, 65, 87)}

        self.active_slot_dict_opponent = {"0": pygame.Rect(400, 373, 65, 87),
                                          "1": pygame.Rect(325, 373, 65, 87),
                                          "2": pygame.Rect(250, 373, 65, 87),
                                          "3": pygame.Rect(175, 373, 65, 87),
                                          "4": pygame.Rect(100, 373, 65, 87),
                                          "s": pygame.Rect(25, 373, 65, 87)}
        # endregion

        # server variables
        self.ready = False
        # stands for the games id (numeric) so each game client as its own id
        self.id = id

    # a simple function to tell us when player is connected to server or not.
    def connected(self):
        return self.ready

    def process_actions(self):
        p0_list_of_actions_str = self.players_actions[0].split("|")
        del p0_list_of_actions_str[-1]
        for action in p0_list_of_actions_str:
            if "Attacking Damage" in action:
                attack_value_str = action.split(",")[1]
                attack_value = int(attack_value_str)
                self.players_current_attacking[0] = attack_value
            elif "Blocking Damage" in action:
                blocking_value_str = action.split(",")[1]
                blocking_value = int(blocking_value_str)
                self.players_current_blocking[0] = blocking_value

        p1_list_of_actions_str = self.players_actions[1].split("|")
        del p1_list_of_actions_str[-1]
        for action in p1_list_of_actions_str:
            if "Attacking Damage" in action:
                attack_value_str = action.split(",")[1]
                attack_value = int(attack_value_str)
                self.players_current_attacking[1] = attack_value
            elif "Blocking Damage" in action:
                blocking_value_str = action.split(",")[1]
                blocking_value = int(blocking_value_str)
                self.players_current_blocking[1] = blocking_value

    # copy for p1,

    def fill_deck_from_id_list(self, id_list, deck_list):
        for id in id_list:
            for card in Card.all_instances:
                if id == card.id_number:
                    deck_list.append(card)

    def end_of_round_effects(self):
        if self.player_round_starter[0]:
            self.players_turn[0] = True
            self.players_turn[1] = False
            p_first = 0
            p_second = 1
        else:
            self.players_turn[0] = False
            self.players_turn[1] = True
            p_first = 1
            p_second = 0
        i = 0
        while not any(self.card_currently_activating):  # while both are None
            slot_ns = str(i)
            if self.players_active_slots[p_first][slot_ns] != "None":
                card = self.players_active_slots[p_first][slot_ns]
                self.card_currently_activating[p_first] = slot_ns
                card.active = True
            elif self.players_active_slots[p_first][slot_ns] == "None":
                self.slots_that_have_activated_this_round[p_first][int(slot_ns)] = True
            elif self.players_active_slots[p_second][slot_ns] != "None":
                card = self.players_active_slots[p_second][slot_ns]
                self.card_currently_activating[p_second] = slot_ns
                card.active = True
            elif self.players_active_slots[p_second][slot_ns] == "None":
                self.slots_that_have_activated_this_round[p_second][int(slot_ns)] = True
            i += 1
            if i == 5:
                print(f"No slots filled for either player, need to do stances.")
                break

    def get_card_from_idn(self, idn):
        for card in Card.all_instances:
            if card.id_number == idn:
                return card

    def get_next_activating_slot(self, p, slot_n_just_played):
        other_p = get_other_player(p)
        if self.player_round_starter[p]:
            next_slot_n = slot_n_just_played
            if self.players_active_slots[other_p][str(next_slot_n)] != "None":  # if they have something in the slot:
                return str(next_slot_n)
            else:
                return None
        else:
            next_slot_n = slot_n_just_played + 1
            if next_slot_n < 5:
                if self.players_active_slots[other_p][str(next_slot_n)] != "None":  # if they have something in the slot:
                    return str(next_slot_n)
                else:
                    return None
            else:
                return None

    def update_card_position(self, slot, p):  # slot string of a number
        self.players_active_slots[p][slot].pos = (self.active_slot_dict_self[slot].topleft[0] + 5, self.active_slot_dict_self[slot].topleft[1] + 5)
        self.players_active_slots[p][slot].pos_for_opp = (self.active_slot_dict_opponent[slot].topleft[0] + 5, self.active_slot_dict_opponent[slot].topleft[1] + 5)
        self.players_active_slots[p][slot].update_hb()
