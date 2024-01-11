import pygame
import random
from network import Network
import os
from cards import *

# region Setup Stuff
pygame.font.init()
FPS = 6
width = 576
height = 960
card_size = (55, 77)
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Plunder Mobile")

# region colors
WHITE = (255, 255, 255)
BROWN = (88, 57, 39)
YELLOW = (255, 215, 0)
PURPLE = (186, 85, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BG_GREEN = (0, 100, 0)
BG_BLUE = (4, 231, 231)
GREY = (128, 128, 128)
OTHER_GREY = (50, 50, 50)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
# endregion

# region Card Backs
blue_back_load = pygame.image.load(os.path.join('Assets', 'Images', 'Card Art', 'blue.jpg'))
blue_back = pygame.transform.scale(blue_back_load, card_size)
red_back_load = pygame.image.load(os.path.join('Assets', 'Images', 'Card Art', 'red.jpg'))
red_card_back = pygame.transform.scale(red_back_load, card_size)
brown_card_back_load = pygame.image.load(os.path.join('Assets', 'Images', 'Card Art', 'brown.jpg'))
brown_card_back = pygame.transform.scale(brown_card_back_load, card_size)
green_card_back_load = pygame.image.load(os.path.join('Assets', 'Images', 'Card Art', 'green.jpg'))
green_card_back = pygame.transform.scale(green_card_back_load, card_size)
# endregion

# region Captains
gentleman_ld = pygame.image.load(os.path.join('Assets', 'Images', 'Captains', 'gentleman.png'))
gentleman = pygame.transform.scale(gentleman_ld, (60.5, 84.7))


# endregion
# endregion


# region Helper Functions
def get_other_player(p):
    players = [0, 1]
    players.remove(p)
    return players[0]


def draw_cards(deck, list_to_draw_to, number_of_cards):  # list_to_draw_to, deck - are client based variables.
    if len(deck) < number_of_cards:
        print(f"Deck ({deck}) didn't have enough cards.")
        pass
    else:
        print(f"Draw Cards function called. Drawing {number_of_cards} cards.")
        drawn_cards = random.sample(deck, number_of_cards)
        for card in drawn_cards:
            deck.remove(card)
            list_to_draw_to.append(card)


def update_after_draw_deck_to_hand(n):
    n.send(f"Deck Length,{str(len(client.deck))}")
    n.send(f"Hand Length,{str(len(client.hand))}")
    hand_card_pos = (516, 883)
    for card in client.hand:
        card.pos = hand_card_pos
        hand_card_pos = (hand_card_pos[0] - 55, hand_card_pos[1])
        card.update_hb()


def update_hand_cards_positions(hand):
    hand_card_pos = (516, 883)
    for card in hand:
        card.pos = hand_card_pos
        hand_card_pos = (hand_card_pos[0] - 55, hand_card_pos[1])
        card.update_hb()


def draw_text_box(text_to_write, colour, font_size, pos):
    font = pygame.font.SysFont("comicsans", font_size)
    text = font.render(text_to_write, 1, WHITE)
    box_width = round(text.get_width()) + (0.1 * round(text.get_width()))
    box_height = round(text.get_height()) + (0.1 * round(text.get_height()))
    x_pos = pos[0]
    y_pos = pos[1] - box_height
    pygame.draw.rect(win, colour, (x_pos, y_pos, box_width, box_height))
    # drawing the text position on rect. text, x position - (half width of button + half width of text), same with y
    win.blit(text, (x_pos + round(box_width / 2) - round(text.get_width() / 2),
                    y_pos + round(box_height / 2) - round(text.get_height() / 2)))


def draw_text_box_middle_centered(text_to_write, colour, font_size, pos):
    font = pygame.font.SysFont("comicsans", font_size)
    text = font.render(text_to_write, 1, WHITE)
    box_width = round(text.get_width()) + (0.1 * round(text.get_width()))
    box_height = round(text.get_height()) + (0.1 * round(text.get_height()))
    x_pos = pos[0] - round(text.get_width()) / 2
    y_pos = pos[1]
    pygame.draw.rect(win, colour, (x_pos, y_pos, box_width, box_height))
    # drawing the text position on rect. text, x position - (half width of button + half width of text), same with y
    win.blit(text, (x_pos + round(box_width / 2) - round(text.get_width() / 2),
                    y_pos + round(box_height / 2) - round(text.get_height() / 2)))


def draw_box_with_text(text_to_write, colour, font_size, pos, size):
    font = pygame.font.SysFont("comicsans", font_size)
    text = font.render(text_to_write, 1, WHITE)
    box_width = size[0]
    box_height = size[1]
    x_pos = pos[0]
    y_pos = pos[1]
    pygame.draw.rect(win, colour, (x_pos, y_pos, box_width, box_height))
    # drawing the text position on rect. text, x position - (half width of button + half width of text), same with y
    win.blit(text, (x_pos + round(box_width / 2) - round(text.get_width() / 2),
                    y_pos + round(box_height / 2) - round(text.get_height() / 2)))


def draw_inspected_card_on_screen(card):
    size = (319, 446.6)
    load = card_image_loads[card.name]
    image = pygame.transform.scale(load, size)
    position = (250, 200)
    win.blit(image, position)


def draw_stance_button(color, p):
    font = pygame.font.SysFont("comicsans", 18)
    text = font.render("Stance", 1, BLACK)
    if p == 0:
        posx = 516
        posy = 668
        win.blit(text, (515, 646))
    else:
        posx = 516
        posy = 172
        win.blit(text, (515, 150))
    pygame.draw.rect(win, color, (posx, posy, 55, 55))


def get_first_open_slot(p):
    for slot, card in client.players_active_slots[p].items():
        if card == "None":
            if slot != 's':
                return slot
    return "No Available Slots"


def draw_played_card_but_not_locked_in_yet_on_screen(cards_image, slot):
    slot = int(slot)
    if slot == 0:
        win.blit(cards_image, (105, 505))
    if slot == 1:
        win.blit(cards_image, (180, 505))
    if slot == 2:
        win.blit(cards_image, (255, 505))
    if slot == 3:
        win.blit(cards_image, (330, 505))
    if slot == 4:
        win.blit(cards_image, (405, 505))


def draw_box(reference_dict, slot, colour):
    pygame.draw.rect(win, colour, reference_dict[slot], 5)


# endregion


# region Client
class Client:
    def __init__(self):

        # region Game Variables
        self.tod = ["Day", "Night"]
        # endregion

        # region Homescreen Setup Variables
        self.hshp = 1
        self.hsatk = 1
        self.hsblock = 1
        self.hsplunder = 1
        self.hsexplore = 1
        # endregion

        # players
        self.p = 0
        self.other_p = 1

        # region Action Variables
        self.action_filled_for_turn = False
        self.players_active_stance = ["None", "None"]
        self.card_doing_damage_active = False
        self.player_deciding_on_action_list = [self.card_doing_damage_active, ]
        self.value_of_currently_active_effect = 0
        # endregion

        # region Game stuff? Eg. mouse pos
        self.current_mouse_position = None
        self.last_clicked_pos = None
        self.lockout = False
        self.game_initialization = True
        # endregion

        # region players variables
        self.player_deck_lengths = [1, 1]
        self.player_hand_lengths = [1, 1]

        self.players_attack_stats = [1, 1]
        self.players_block_stats = [1, 1]
        self.players_plunder_stats = [1, 1]
        self.players_explore_stats = [1, 1]
        self.players_max_hps = [1, 1]
        self.players_current_hps = [1, 1]

        self.players_base_max_hps = [1, 1]
        self.players_base_attack_stats = [1, 1]
        self.players_base_block_stats = [1, 1]
        self.players_base_plunder_stats = [1, 1]
        self.players_base_explore_stats = [1, 1]
        # endregion

        # region Players Combat Variables
        self.players_active_slots = [{'0': "None", '1': "None", '2': "None", '3': "None", '4': "None", 's': "None"},
                                     {'0': "None", '1': "None", '2': "None", '3': "None", '4': "None", 's': "None"}]
        self.current_slot_to_play_card_into = '0'

        self.actively_playing_slot_list = [False, False, False, False, False]

        self.current_active_card_effects_list = None
        self.current_active_card_popup_info = None
        self.current_effects_to_play_out = None
        self.card_activations_active = False
        # endregion

        # region Own stuff
        self.hand = []
        self.deck = []
        self.discard_pile = []
        self.active_moves_for_turn = []
        # endregion

        # region Clickable UI elements
        self.deck_box_self = pygame.Rect(470, 781, 65, 87)
        self.deck_box_opponent = pygame.Rect(30, 10, 65, 87)
        self.captain_box_self = pygame.Rect(240, 778, 90, 90)
        self.captain_box_opponent = pygame.Rect(240, 10, 90, 90)

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

        self.list_of_active_slot_card_positions_self = [(105, 505), (180, 505), (255, 505), (330, 505), (405, 505)]
        self.list_of_active_slot_card_positions_opponent = [(405, 378), (330, 378), (255, 378), (180, 378), (105, 378)]
        # endregion

        # region Inspectings
        self.inspecting_own_deck = False
        self.inspecting_own_captain = False
        self.inspecting_opponent_deck = False
        self.inspecting_opponent_captain = False
        self.card_being_inspected = None
        self.inspecting_card = False
        # endregion

        # region Variables to hold things, eg. selected card in hand
        self.selected_card_in_hand = None
        self.played_card_into_slot_not_locked_in_yet = False
        self.waiting_for_lock_or_cancel = False
        self.chose_card_effects_list = False
        # endregion

        # region Popup Variables
        self.popup_button_1 = None
        self.popup_button_2 = None
        self.popup_button_3 = None
        self.popup_button_4 = None
        self.play_card_popup = False
        # endregion

    def draw_popup(self, number_of_buttons, pos, button_text_1, button_text_2=None, button_text_3=None,
                   button_text_4=None):
        if number_of_buttons == 1:
            popup_size = (200, 100)
            if pos[0] > 376 and pos[1] > 860:
                pos_to_draw = ((pos[0] - 200), (pos[1] - 100))
            elif pos[0] > 376:
                pos_to_draw = ((pos[0] - 200), pos[1])
            elif pos[1] > 860:
                pos_to_draw = (pos[0], (pos[1] - 100))
            else:
                pos_to_draw = (pos[0], pos[1])
            pygame.draw.rect(win, GREY, pygame.Rect(pos_to_draw, popup_size))
            self.popup_button_1 = Button(button_text_1, 20, (pos_to_draw[0] + 25), (pos_to_draw[1] + 50), 65, 25,
                                         OTHER_GREY)
            self.popup_button_1.draw(win)

        elif number_of_buttons == 2:
            popup_size = (200, 100)
            if pos[0] > 376 and pos[1] > 860:
                pos_to_draw = ((pos[0] - 200), (pos[1] - 100))
            elif pos[0] > 376:
                pos_to_draw = ((pos[0] - 200), pos[1])
            elif pos[1] > 860:
                pos_to_draw = (pos[0], (pos[1] - 100))
            else:
                pos_to_draw = (pos[0], pos[1])
            pygame.draw.rect(win, GREY, pygame.Rect(pos_to_draw, popup_size))
            self.popup_button_1 = Button(button_text_1, 20, (pos_to_draw[0] + 25), (pos_to_draw[1] + 50), 65, 25,
                                         OTHER_GREY)
            self.popup_button_2 = Button(button_text_2, 20, (pos_to_draw[0] + 110), (pos_to_draw[1] + 50), 65, 25,
                                         OTHER_GREY)
            self.popup_button_1.draw(win)
            self.popup_button_2.draw(win)

        elif number_of_buttons == 4:
            popup_size = (200, 100)
            if pos[0] > 376 and pos[1] > 860:
                pos_to_draw = ((pos[0] - 200), (pos[1] - 100))
            elif pos[0] > 376:
                pos_to_draw = ((pos[0] - 200), pos[1])
            elif pos[1] > 860:
                pos_to_draw = (pos[0], (pos[1] - 100))
            else:
                pos_to_draw = (pos[0], pos[1])
            pygame.draw.rect(win, GREY, pygame.Rect(pos_to_draw, popup_size))
            self.popup_button_1 = Button(button_text_1, 20, (pos_to_draw[0] + 25), (pos_to_draw[1] + 12.5), 65, 25,
                                         OTHER_GREY)
            self.popup_button_2 = Button(button_text_2, 20, (pos_to_draw[0] + 110), (pos_to_draw[1] + 12.5), 65, 25,
                                         OTHER_GREY)
            self.popup_button_3 = Button(button_text_3, 20, (pos_to_draw[0] + 25), (pos_to_draw[1] + 62.5), 65, 25,
                                         OTHER_GREY)
            self.popup_button_4 = Button(button_text_4, 20, (pos_to_draw[0] + 110), (pos_to_draw[1] + 62.5), 65, 25,
                                         OTHER_GREY)
            self.popup_button_1.draw(win)
            self.popup_button_2.draw(win)
            self.popup_button_3.draw(win)
            self.popup_button_4.draw(win)


client = Client()


# endregion


# region Button Class
class Button:
    def __init__(self, text, font_size, x_pos, y_pos, width, height, color):
        self.text = text
        self.font_size = font_size
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x_pos, y_pos, width, height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x_pos, self.y_pos, self.width, self.height))
        font = pygame.font.SysFont("comicsans", self.font_size)
        text = font.render(self.text, 1, WHITE)
        # drawing the text position on rect. text, x position - (half width of button + half width of text), same with y
        win.blit(text, (self.x_pos + round(self.width / 2) - round(text.get_width() / 2),
                        self.y_pos + round(self.height / 2) - round(text.get_height() / 2)))

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False

    def update_text(self, new_text):
        self.text = new_text


# region Main Game Buttons
# text, font_size, x_pos, y_pos, width, height, color
op_atk_btn = Button(str(client.players_attack_stats[client.other_p]), 20, 290, 105, 60, 40, RED)
op_def_btn = Button(str(client.players_block_stats[client.other_p]), 20, 220, 105, 60, 40, BLUE)
op_explore_btn = Button(str(client.players_explore_stats[client.other_p]), 20, 195, 25, 40, 60, PURPLE)
op_plunder_btn = Button("P", 20, 340, 25, 40, 60, CYAN)
atk_btn = Button(str(client.players_attack_stats[client.p]), 20, 220, 733, 60, 40, RED)
def_btn = Button(str(client.players_block_stats[client.p]), 20, 290, 733, 60, 40, BLUE)
explore_btn = Button(str(client.players_explore_stats[client.p]), 20, 340, 793, 40, 60, PURPLE)
plunder_btn = Button("P", 20, 192, 793, 40, 60, CYAN)
end_turn_btn = Button("End Turn", 15, 290, 660, 100, 60, RED)
pass_btn = Button("Pass", 15, 180, 660, 100, 60, BG_BLUE)

# region Slot Buttons
slot_0_btn_a = Button("Lock In", 10, 105, 590, 55, 25, GREEN)
slot_0_btn_d = Button("Lock In", 10, 105, 590, 55, 25, GREY)
slot_0_btn_ca = Button("Cancel", 10, 105, 618, 55, 25, RED)
slot_0_btn_cd = Button("Cancel", 10, 105, 618, 55, 25, GREY)

slot_1_btn_a = Button("Lock In", 10, 180, 590, 55, 25, GREEN)
slot_1_btn_d = Button("Lock In", 10, 180, 590, 55, 25, GREY)
slot_1_btn_ca = Button("Cancel", 10, 180, 618, 55, 25, RED)
slot_1_btn_cd = Button("Cancel", 10, 180, 618, 55, 25, GREY)

slot_2_btn_a = Button("Lock In", 10, 255, 590, 55, 25, GREEN)
slot_2_btn_d = Button("Lock In", 10, 255, 590, 55, 25, GREY)
slot_2_btn_ca = Button("Cancel", 10, 255, 618, 55, 25, RED)
slot_2_btn_cd = Button("Cancel", 10, 255, 618, 55, 25, GREY)

slot_3_btn_a = Button("Lock In", 10, 330, 590, 55, 25, GREEN)
slot_3_btn_d = Button("Lock In", 10, 330, 590, 55, 25, GREY)
slot_3_btn_ca = Button("Cancel", 10, 330, 618, 55, 25, RED)
slot_3_btn_cd = Button("Cancel", 10, 330, 618, 55, 25, GREY)

slot_4_btn_a = Button("Lock In", 10, 405, 590, 55, 25, GREEN)
slot_4_btn_d = Button("Lock In", 10, 405, 590, 55, 25, GREY)
slot_4_btn_ca = Button("Cancel", 10, 405, 618, 55, 25, RED)
slot_4_btn_cd = Button("Cancel", 10, 405, 618, 55, 25, GREY)
# endregion

game_ui_buttons = [op_atk_btn, op_def_btn, op_explore_btn, op_plunder_btn,
                   atk_btn, def_btn, explore_btn, plunder_btn, slot_0_btn_d,
                   slot_0_btn_cd, slot_1_btn_d, slot_1_btn_cd, slot_2_btn_d,
                   slot_2_btn_cd, slot_3_btn_d, slot_3_btn_cd, slot_4_btn_d,
                   slot_4_btn_cd, end_turn_btn, pass_btn]

# region Play Card Effects Button
effect1_btn = Button("", 15, 70, 220, 100, 60, GREEN)
effect2_btn = Button("", 15, 180, 220, 100, 60, GREEN)
effect3_btn = Button("", 15, 290, 220, 100, 60, GREEN)
effect4_btn = Button("", 15, 400, 220, 100, 60, GREEN)
effect_button_list = [effect1_btn, effect2_btn, effect3_btn, effect4_btn]
# endregion
# endregion

# region Homescreen Buttons
homescreen_play_button = Button("Play", 40, 188, 810, 200, 100, GREEN)
hp1 = Button("1", 20, 121, 30, 40, 40, GREY)
hp2 = Button("2", 20, 166, 30, 40, 40, GREY)
hp3 = Button("3", 20, 211, 30, 40, 40, GREY)
hp4 = Button("4", 20, 256, 30, 40, 40, GREY)
hp5 = Button("5", 20, 301, 30, 40, 40, GREY)
hp6 = Button("6", 20, 346, 30, 40, 40, GREY)
hp7 = Button("7", 20, 391, 30, 40, 40, GREY)
hp8 = Button("8", 20, 436, 30, 40, 40, GREY)
hp9 = Button("9", 20, 481, 30, 40, 40, GREY)
hp10 = Button("10", 20, 526, 30, 40, 40, GREY)
hp11 = Button("11", 20, 121, 75, 40, 40, GREY)
hp12 = Button("12", 20, 166, 75, 40, 40, GREY)
hp13 = Button("13", 20, 211, 75, 40, 40, GREY)
hp14 = Button("14", 20, 256, 75, 40, 40, GREY)
hp15 = Button("15", 20, 301, 75, 40, 40, GREY)
hp16 = Button("16", 20, 346, 75, 40, 40, GREY)
hp17 = Button("17", 20, 391, 75, 40, 40, GREY)
hp18 = Button("18", 20, 436, 75, 40, 40, GREY)
hp19 = Button("19", 20, 481, 75, 40, 40, GREY)
hp20 = Button("20", 20, 526, 75, 40, 40, GREY)
hp_buttons = [hp1, hp2, hp3, hp4, hp5, hp6, hp7, hp8, hp9, hp10, hp11, hp12, hp13, hp14, hp15, hp16, hp17, hp18, hp19,
              hp20]
atk1 = Button("1", 20, 121, 155, 40, 40, GREY)
atk2 = Button("2", 20, 166, 155, 40, 40, GREY)
atk3 = Button("3", 20, 211, 155, 40, 40, GREY)
atk4 = Button("4", 20, 256, 155, 40, 40, GREY)
atk5 = Button("5", 20, 301, 155, 40, 40, GREY)
atk6 = Button("6", 20, 346, 155, 40, 40, GREY)
atk7 = Button("7", 20, 391, 155, 40, 40, GREY)
atk8 = Button("8", 20, 436, 155, 40, 40, GREY)
atk9 = Button("9", 20, 481, 155, 40, 40, GREY)
atk10 = Button("10", 20, 526, 155, 40, 40, GREY)
atk11 = Button("11", 20, 121, 200, 40, 40, GREY)
atk12 = Button("12", 20, 166, 200, 40, 40, GREY)
atk13 = Button("13", 20, 211, 200, 40, 40, GREY)
atk14 = Button("14", 20, 256, 200, 40, 40, GREY)
atk15 = Button("15", 20, 301, 200, 40, 40, GREY)
atk16 = Button("16", 20, 346, 200, 40, 40, GREY)
atk17 = Button("17", 20, 391, 200, 40, 40, GREY)
atk18 = Button("18", 20, 436, 200, 40, 40, GREY)
atk19 = Button("19", 20, 481, 200, 40, 40, GREY)
atk20 = Button("20", 20, 526, 200, 40, 40, GREY)
atk_buttons = [atk1, atk2, atk3, atk4, atk5, atk6, atk7, atk8, atk9, atk10, atk11, atk12, atk13, atk14, atk15, atk16,
               atk17, atk18, atk19, atk20]
block1 = Button("1", 20, 121, 280, 40, 40, GREY)
block2 = Button("2", 20, 166, 280, 40, 40, GREY)
block3 = Button("3", 20, 211, 280, 40, 40, GREY)
block4 = Button("4", 20, 256, 280, 40, 40, GREY)
block5 = Button("5", 20, 301, 280, 40, 40, GREY)
block6 = Button("6", 20, 346, 280, 40, 40, GREY)
block7 = Button("7", 20, 391, 280, 40, 40, GREY)
block8 = Button("8", 20, 436, 280, 40, 40, GREY)
block9 = Button("9", 20, 481, 280, 40, 40, GREY)
block10 = Button("10", 20, 526, 280, 40, 40, GREY)
block11 = Button("11", 20, 121, 325, 40, 40, GREY)
block12 = Button("12", 20, 166, 325, 40, 40, GREY)
block13 = Button("13", 20, 211, 325, 40, 40, GREY)
block14 = Button("14", 20, 256, 325, 40, 40, GREY)
block15 = Button("15", 20, 301, 325, 40, 40, GREY)
block16 = Button("16", 20, 346, 325, 40, 40, GREY)
block17 = Button("17", 20, 391, 325, 40, 40, GREY)
block18 = Button("18", 20, 436, 325, 40, 40, GREY)
block19 = Button("19", 20, 481, 325, 40, 40, GREY)
block20 = Button("20", 20, 526, 325, 40, 40, GREY)
block_buttons = [block1, block2, block3, block4, block5, block6, block7, block8, block9, block10, block11, block12,
                 block13, block14, block15, block16, block17, block18, block19, block20]
plunder1 = Button("1", 20, 121, 405, 40, 40, GREY)
plunder2 = Button("2", 20, 166, 405, 40, 40, GREY)
plunder3 = Button("3", 20, 211, 405, 40, 40, GREY)
plunder4 = Button("4", 20, 256, 405, 40, 40, GREY)
plunder5 = Button("5", 20, 301, 405, 40, 40, GREY)
plunder6 = Button("6", 20, 346, 405, 40, 40, GREY)
plunder7 = Button("7", 20, 391, 405, 40, 40, GREY)
plunder8 = Button("8", 20, 436, 405, 40, 40, GREY)
plunder9 = Button("9", 20, 481, 405, 40, 40, GREY)
plunder10 = Button("10", 20, 526, 405, 40, 40, GREY)
plunder11 = Button("11", 20, 121, 450, 40, 40, GREY)
plunder12 = Button("12", 20, 166, 450, 40, 40, GREY)
plunder13 = Button("13", 20, 211, 450, 40, 40, GREY)
plunder14 = Button("14", 20, 256, 450, 40, 40, GREY)
plunder15 = Button("15", 20, 301, 450, 40, 40, GREY)
plunder16 = Button("16", 20, 346, 450, 40, 40, GREY)
plunder17 = Button("17", 20, 391, 450, 40, 40, GREY)
plunder18 = Button("18", 20, 436, 450, 40, 40, GREY)
plunder19 = Button("19", 20, 481, 450, 40, 40, GREY)
plunder20 = Button("20", 20, 526, 450, 40, 40, GREY)
plunder_buttons = [plunder1, plunder2, plunder3, plunder4, plunder5, plunder6, plunder7, plunder8, plunder9, plunder10,
                   plunder11, plunder12, plunder13, plunder14, plunder15, plunder16, plunder17, plunder18, plunder19,
                   plunder20]
explore1 = Button("1", 20, 121, 530, 40, 40, GREY)
explore2 = Button("2", 20, 166, 530, 40, 40, GREY)
explore3 = Button("3", 20, 211, 530, 40, 40, GREY)
explore4 = Button("4", 20, 256, 530, 40, 40, GREY)
explore5 = Button("5", 20, 301, 530, 40, 40, GREY)
explore6 = Button("6", 20, 346, 530, 40, 40, GREY)
explore7 = Button("7", 20, 391, 530, 40, 40, GREY)
explore8 = Button("8", 20, 436, 530, 40, 40, GREY)
explore9 = Button("9", 20, 481, 530, 40, 40, GREY)
explore10 = Button("10", 20, 526, 530, 40, 40, GREY)
explore11 = Button("11", 20, 121, 575, 40, 40, GREY)
explore12 = Button("12", 20, 166, 575, 40, 40, GREY)
explore13 = Button("13", 20, 211, 575, 40, 40, GREY)
explore14 = Button("14", 20, 256, 575, 40, 40, GREY)
explore15 = Button("15", 20, 301, 575, 40, 40, GREY)
explore16 = Button("16", 20, 346, 575, 40, 40, GREY)
explore17 = Button("17", 20, 391, 575, 40, 40, GREY)
explore18 = Button("18", 20, 436, 575, 40, 40, GREY)
explore19 = Button("19", 20, 481, 575, 40, 40, GREY)
explore20 = Button("20", 20, 526, 575, 40, 40, GREY)
explore_buttons = [explore1, explore2, explore3, explore4, explore5, explore6, explore7, explore8, explore9, explore10,
                   explore11, explore12, explore13, explore14, explore15, explore16, explore17, explore18, explore19,
                   explore20]
list_of_button_lists = [hp_buttons, atk_buttons, block_buttons, plunder_buttons, explore_buttons]


# endregion
# endregion


# region Draw Functions
def draw_window(window, game=None, player=None):
    # store all draw functions into a dictionary with string keys
    windows = {
        'game': draw_game_window,
        'homescreen': draw_homescreen_window,
    }

    # grab whichever draw function is chosen
    draw_function = windows.get(window)

    if draw_function is not None:
        draw_function(game, player)
    else:
        print(f"No screen named '{window}' found.")


def draw_homescreen_window(game, p):
    win.fill(WHITE)

    # region Variables to Set
    font = pygame.font.SysFont("comicsans", 30)
    text = font.render(f"HP: {client.hshp}", 1, RED)
    win.blit(text, (10, 52.5))
    text = font.render(f"ATK: {client.hsatk}", 1, RED)
    win.blit(text, (10, 177.5))
    text = font.render(f"BLK: {client.hsblock}", 1, RED)
    win.blit(text, (10, 302.5))
    text = font.render(f"PLD: {client.hsplunder}", 1, RED)
    win.blit(text, (10, 427.5))
    text = font.render(f"EXP: {client.hsexplore}", 1, RED)
    win.blit(text, (10, 552.5))
    # endregion

    homescreen_play_button.draw(win)
    for list_of_buttons in list_of_button_lists:
        for button in list_of_buttons:
            button.draw(win)

    pygame.display.update()


# region Main Game Window Draw Function
def draw_game_window(game, p):
    other_p = get_other_player(p)
    win.fill(WHITE)

    if not game.connected():
        # region Drawing Loading
        win.fill(WHITE)
        font = pygame.font.SysFont("comicsans", 40)
        # true argument makes it bold
        text = font.render("Waiting for Player 2", 1, RED, True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        pygame.display.update()
        # endregion

    else:

        # region bottom level game constants
        # region opponents stuff
        # deck
        pygame.draw.rect(win, BLACK, client.deck_box_opponent, 5)
        # gold amount
        draw_box_with_text(str(game.players_gold_amounts[other_p]), YELLOW, 20, (30, 105), (65, 65))
        # chest
        draw_box_with_text(str(game.players_chest_amounts[other_p]), YELLOW, 20, (470, 10), (65, 87))
        # other player
        # pygame.draw.rect(win, BROWN, client.captain_box_opponent)
        win.blit(gentleman, (240, 10))
        # other player hp
        draw_box_with_text(str(client.players_current_hps[other_p]), RED, 20, (300, 10), (30, 30))
        # their card for deck
        if client.player_deck_lengths[other_p] > 0:
            win.blit(red_card_back, (35, 15))
        # endregion
        # region Your Stuff
        # box for hand
        pygame.draw.rect(win, BLACK, (0, 878, 576, 82), 5)
        # chest
        draw_box_with_text(str(game.players_chest_amounts[p]), YELLOW, 20, (30, 781), (65, 87))
        # deck
        pygame.draw.rect(win, BLACK, client.deck_box_self, 5)
        # gold amount
        draw_box_with_text(str(game.players_gold_amounts[p]), YELLOW, 20, (470, 710), (65, 65))
        # player icon
        # pygame.draw.rect(win, BROWN, client.captain_box_self)
        win.blit(gentleman, (240, 778))
        # player hp
        draw_box_with_text(str(client.players_current_hps[p]), RED, 20, (300, 778), (30, 30))
        # your card for deck
        if client.player_deck_lengths[p] > 0:
            win.blit(blue_back, (475, 786))
        # instructions for buttons
        font = pygame.font.SysFont("comicsans", 20)
        text = font.render("Attack", 1, RED)
        win.blit(text, (110, 780))
        text = font.render("Block", 1, BLUE)
        win.blit(text, (390, 780))
        text = font.render("Plunder", 1, CYAN)
        win.blit(text, (110, 810))
        text = font.render("Explore", 1, PURPLE)
        win.blit(text, (390, 810))
        # endregion

        # region UI Setups
        for btn in game_ui_buttons:
            btn.draw(win)

        if client.current_slot_to_play_card_into == '0':
            slot_0_btn_a.draw(win)
            slot_0_btn_ca.draw(win)
        if client.current_slot_to_play_card_into == '1':
            slot_1_btn_a.draw(win)
            slot_1_btn_ca.draw(win)
        if client.current_slot_to_play_card_into == '2':
            slot_2_btn_a.draw(win)
            slot_2_btn_ca.draw(win)
        if client.current_slot_to_play_card_into == '3':
            slot_3_btn_a.draw(win)
            slot_3_btn_ca.draw(win)
        if client.current_slot_to_play_card_into == '4':
            slot_4_btn_a.draw(win)
            slot_4_btn_ca.draw(win)

        if not game.players_turn[p]:
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render("Waiting for opponent to act", 1, RED)
            win.blit(text, (100, 150))

        # font = pygame.font.SysFont("comicsans", 60)
        # text = font.render(client.tod[1], 1, GREY)
        # win.blit(text, (30, 150))
        # endregion

        # region Active Cards UI
        # region boxes around card slots - green if active one
        for slot, box in client.active_slot_dict_self.items():
            if slot == game.card_currently_activating[p]:
                draw_box(client.active_slot_dict_self, slot, GREEN)
            else:
                draw_box(client.active_slot_dict_self, slot, BLACK)
        for slot, box in client.active_slot_dict_opponent.items():
            if slot == game.card_currently_activating[other_p]:
                draw_box(client.active_slot_dict_opponent, slot, GREEN)
            else:
                draw_box(client.active_slot_dict_opponent, slot, BLACK)
        # endregion

        if client.played_card_into_slot_not_locked_in_yet:
            draw_played_card_but_not_locked_in_yet_on_screen(client.selected_card_in_hand.image, client.current_slot_to_play_card_into)
        for slot, card in game.players_active_slots[p].items():
            if card != 'None':
                win.blit(card.image, client.list_of_active_slot_card_positions_self[int(slot)])
        for slot, card in game.players_active_slots[other_p].items():
            if card != 'None':
                if not card.active:
                    win.blit(red_card_back, client.list_of_active_slot_card_positions_opponent[int(slot)])
                else:
                    win.blit(card.image, client.list_of_active_slot_card_positions_opponent[int(slot)])
        # endregion

        # region Cards Hand
        for card in client.hand:
            win.blit(card.image, card.pos)
        # endregion

        # region Card Effects to Play UI
        if client.current_effects_to_play_out:  # holds a list of effects that the card will do.
            n_of_effects = len(client.current_effects_to_play_out)
            for i in range(n_of_effects):
                effect_button_list[i].update_text(client.current_effects_to_play_out[i].split(":")[0])
                effect_button_list[i].draw(win)
        else:
            if any(client.actively_playing_slot_list):
                client.draw_popup(client.current_active_card_popup_info[0], (300, 700),
                                  client.current_active_card_popup_info[1],
                                  button_text_2=client.current_active_card_popup_info[2],
                                  button_text_3=client.current_active_card_popup_info[3],
                                  button_text_4=client.current_active_card_popup_info[4])
        # endregion

        # region Popups
        if client.play_card_popup:
            client.draw_popup(2, client.last_clicked_pos, "Play", "Cancel")
        # endregion

        # region Inspectings
        # opponents
        if client.inspecting_opponent_captain:
            draw_text_box(str(client.player_hand_lengths[other_p]), GREY, 30, client.current_mouse_position)
        if client.inspecting_opponent_deck:
            draw_text_box(str(client.player_deck_lengths[other_p]), GREY, 30, client.current_mouse_position)
        # own
        if client.inspecting_own_captain:
            draw_text_box(str(client.player_hand_lengths[p]), GREY, 30, client.current_mouse_position)
        if client.inspecting_own_deck:
            draw_text_box(str(len(client.deck)), GREY, 30, client.current_mouse_position)
        if client.inspecting_card:
            draw_inspected_card_on_screen(client.card_being_inspected)
        # endregion

        pygame.display.update()


# endregion
# endregion


# region Main Game Function
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    # connecting to network, getting back that number that represents what player they are.
    # Running n.connect() behind the scenes
    client.p = int(n.getP())
    p = client.p
    client.other_p = get_other_player(client.p)
    other_p = client.other_p
    print(f"You are player {client.p}")

    # setting up the starting window to draw as the game window.
    window = 'game'

    # region Game Initialization
    n.send(f"Starting Stats,{client.hshp},{client.hsatk},{client.hsblock},{client.hsplunder},{client.hsexplore}")
    if p == 0:
        client.deck = [c1, c2, c3, c4, c5, c6]
    else:
        client.deck = [c7, c8, c9, c10, c11, c12]
    starting_deck_ids = []
    for card in client.deck:
        starting_deck_ids.append(str(card.id_number))
    n.send(f"Starting Deck:{starting_deck_ids}")

    draw_cards(client.deck, client.hand, 5)
    update_after_draw_deck_to_hand(n)

    while client.game_initialization:
        clock.tick(FPS)
        try:
            game = n.send("get")
        except:
            loading = False
            print("Couldn't get game")
            break

        if game.connected():
            pygame.time.delay(2000)

            # region Updating from Server Initial Chosen Stats
            client.players_base_max_hps = game.players_base_maxhps
            client.players_base_attack_stats = game.players_base_atks
            client.players_base_block_stats = game.players_base_blocks
            client.players_base_plunder_stats = game.players_base_plunders
            client.players_base_explore_stats = game.players_base_explores
            client.players_current_hps = game.players_current_hps
            client.players_max_hps = client.players_base_max_hps
            client.players_attack_stats = client.players_base_attack_stats
            client.players_block_stats = client.players_base_block_stats
            client.players_plunder_stats = client.players_base_plunder_stats
            client.players_explore_stats = client.players_base_explore_stats
            # endregion

            # base stats
            op_atk_btn.update_text(str(client.players_attack_stats[other_p]))
            op_def_btn.update_text(str(client.players_block_stats[other_p]))
            op_explore_btn.update_text(str(client.players_explore_stats[other_p]))
            atk_btn.update_text(str(client.players_attack_stats[p]))
            def_btn.update_text(str(client.players_block_stats[p]))
            explore_btn.update_text(str(client.players_explore_stats[p]))

            # other things we want updated b4 loading in
            client.player_deck_lengths = game.deck_lengths
            client.player_hand_lengths = game.hand_lengths

            pygame.time.delay(2000)
            client.game_initialization = False
    # endregion

    while run:
        clock.tick(FPS)
        try:
            # every frame we pull to game status from the server. (everything in game class)
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        # region Pygame Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # region for test button (end turn)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if end_turn_btn.is_clicked(pos):
                    print(game.players_active_slots)
            # endregion

            # region Mouse Clicks
            if not client.lockout and game.players_turn[p]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # region Mouse Clicks - Popups
                    if client.play_card_popup and client.popup_button_1 and client.popup_button_1.is_clicked(pos):  # play
                        print(f"Played card: {client.selected_card_in_hand.name}")
                        client.waiting_for_lock_or_cancel = True
                        client.hand.remove(client.selected_card_in_hand)
                        client.selected_card_in_hand.pos = client.list_of_active_slot_card_positions_self[
                            int(client.current_slot_to_play_card_into)]
                        client.selected_card_in_hand.update_hb()
                        client.last_clicked_pos = None
                        client.play_card_popup = False
                        client.played_card_into_slot_not_locked_in_yet = True

                        client.players_active_slots[p][
                            client.current_slot_to_play_card_into] = client.selected_card_in_hand
                    elif client.play_card_popup and client.popup_button_2 and client.popup_button_2.is_clicked(pos):  # cancel
                        client.last_clicked_pos = None
                        client.play_card_popup = False
                        client.selected_card_in_hand = None

                    if any(client.actively_playing_slot_list) and client.popup_button_1 and client.popup_button_1.is_clicked(pos):  # the first option for the card activation (only button if there is only 1 choice)
                        client.current_effects_to_play_out = client.current_active_card_effects_list[0]  # client.current_effects_to_play_out fills with a list of effects to play out
                        client.chose_card_effects_list = True
                        client.current_active_card_effects_list = None
                        client.actively_playing_slot_list = [False, False, False, False, False]  # emptying the list
                    # endregion

                    # region Mouse Clicks - Cards in Hand
                    if not client.waiting_for_lock_or_cancel and not client.chose_card_effects_list and not any(client.player_deciding_on_action_list):
                        for card in client.hand:
                            if card.is_clicked(pos):
                                print(f"Clicked card: {card}")
                                client.current_slot_to_play_card_into = get_first_open_slot(p)
                                if client.current_slot_to_play_card_into != "No Available Slots":  # conditions for playing a card here. <---
                                    client.selected_card_in_hand = card
                                    client.last_clicked_pos = pos
                                    client.play_card_popup = True
                    # endregion

                    # region Active Cards
                    for slot, card in game.players_active_slots[other_p].items():
                        if client.card_doing_damage_active:
                            if card != "None":  # if there is something in there
                                if card.is_clicked_by_opp(pos):
                                    if isinstance(card, Crew):  # if that something is a crew
                                        damage = client.value_of_currently_active_effect
                                        client.value_of_currently_active_effect = 0
                                        card.current_health -= damage
                                        client.card_doing_damage_active = False
                                        if card.current_health <= 0:
                                            n.send(f"Active Card Slot to Discard:{other_p}:{slot}")
                                            # maybe have to run server update here
                                            card.pos = None
                                            card.pos_for_opp = None
                                            card.update_hb()
                                            card.active = False
                                        if not client.current_effects_to_play_out:  # if there are no effects to play out left
                                            print(f"No more stuff to play out")
                                            n.send(f"Finished Activations:{game.card_currently_activating[p]}")
                                            client.current_active_card_popup_info = None
                                            client.card_activations_active = False
                                            # update the server to deal with multithreading
                                            try:
                                                game = n.send("get")
                                            except:
                                                run = False
                                                print("Couldn't get game")
                                                break
                        # endregion
                    # endregion

                    # region Mouse Clicks - Game Buttons
                    if not any(client.player_deciding_on_action_list):
                        if client.current_effects_to_play_out and effect1_btn and effect1_btn.is_clicked(pos):  # corresponds to the first effect in the list of current_effects_to_play_out
                            client.chose_card_effects_list = False
                            effect_to_play_out = client.current_effects_to_play_out[0]
                            effect_type = effect_to_play_out.split(":")[0]
                            client.value_of_currently_active_effect = int(effect_to_play_out.split(":")[1])
                            if effect_type == "Damage":
                                # set state where captain or any active crew cards can be selected
                                client.card_doing_damage_active = True
                                # get rid of the button and effect from the list
                                client.current_effects_to_play_out.pop(0)

                    # if atk_btn.is_clicked(pos):
                    #     if not client.action_filled_for_turn:  # conditions
                    #         client.players_active_stance[p] = "Attack"
                    #         server_message = f"Stance,Attack:"
                    #         client.active_moves_for_turn.insert(0, server_message)
                    #         client.action_filled_for_turn = True
                    #         print(f"Clicked on Attack, did the stuff.")
                    # if def_btn.is_clicked(pos):
                    #     if not client.action_filled_for_turn:  # conditions
                    #         client.players_active_stance[p] = "Block"
                    #         server_message = f"Stance,Block:"
                    #         client.active_moves_for_turn.insert(0, server_message)
                    #         client.action_filled_for_turn = True
                    #         print(f"Clicked on Block, did the stuff.")

                    if not client.waiting_for_lock_or_cancel and not client.chose_card_effects_list and not any(client.player_deciding_on_action_list):
                        if pass_btn.is_clicked(pos):
                            if game.players_turn[p] and not client.played_card_into_slot_not_locked_in_yet:  # conditions
                                # send to server that we passed
                                n.send("Pass")

                    # region Lockin/Cancel Buttons Under Active Cards
                    if not client.chose_card_effects_list and not any(client.player_deciding_on_action_list):
                        if slot_0_btn_a.is_clicked(pos) and client.current_slot_to_play_card_into == '0':  # lockin
                            update_after_draw_deck_to_hand(n)
                            n.send(f"Played Card:{client.current_slot_to_play_card_into}:{client.selected_card_in_hand.id_number}")  # instruct:slot:card_id
                            client.played_card_into_slot_not_locked_in_yet = False
                            client.selected_card_in_hand = None
                            client.waiting_for_lock_or_cancel = False
                        elif slot_0_btn_ca.is_clicked(pos) and client.current_slot_to_play_card_into == '0':  # cancel
                            client.hand.append(client.selected_card_in_hand)
                            update_hand_cards_positions(client.hand)
                            client.players_active_slots[p][client.current_slot_to_play_card_into] = "None"
                            client.selected_card_in_hand = None
                            client.played_card_into_slot_not_locked_in_yet = False
                            client.waiting_for_lock_or_cancel = False
                        if slot_1_btn_a.is_clicked(pos) and client.current_slot_to_play_card_into == '1':  # lockin
                            update_after_draw_deck_to_hand(n)
                            n.send(
                                f"Played Card:{client.current_slot_to_play_card_into}:{client.selected_card_in_hand.id_number}")  # instruct:slot:card_id
                            client.played_card_into_slot_not_locked_in_yet = False
                            client.selected_card_in_hand = None
                            client.waiting_for_lock_or_cancel = False
                        elif slot_1_btn_ca.is_clicked(pos) and client.current_slot_to_play_card_into == '1':  # cancel
                            client.hand.append(client.selected_card_in_hand)
                            update_hand_cards_positions(client.hand)
                            client.players_active_slots[p][client.current_slot_to_play_card_into] = "None"
                            client.selected_card_in_hand = None
                            client.played_card_into_slot_not_locked_in_yet = False
                            client.waiting_for_lock_or_cancel = False
                        if slot_2_btn_a.is_clicked(pos) and client.current_slot_to_play_card_into == '2':  # lockin
                            update_after_draw_deck_to_hand(n)
                            n.send(
                                f"Played Card:{client.current_slot_to_play_card_into}:{client.selected_card_in_hand.id_number}")  # instruct:slot:card_id
                            client.played_card_into_slot_not_locked_in_yet = False
                            client.selected_card_in_hand = None
                            client.waiting_for_lock_or_cancel = False
                        elif slot_2_btn_ca.is_clicked(pos) and client.current_slot_to_play_card_into == '2':  # cancel
                            client.hand.append(client.selected_card_in_hand)
                            update_hand_cards_positions(client.hand)
                            client.players_active_slots[p][client.current_slot_to_play_card_into] = "None"
                            client.selected_card_in_hand = None
                            client.played_card_into_slot_not_locked_in_yet = False
                            client.waiting_for_lock_or_cancel = False
                        if slot_3_btn_a.is_clicked(pos) and client.current_slot_to_play_card_into == '3':  # lockin
                            update_after_draw_deck_to_hand(n)
                            n.send(
                                f"Played Card:{client.current_slot_to_play_card_into}:{client.selected_card_in_hand.id_number}")  # instruct:slot:card_id
                            client.played_card_into_slot_not_locked_in_yet = False
                            client.selected_card_in_hand = None
                            client.waiting_for_lock_or_cancel = False
                        elif slot_3_btn_ca.is_clicked(pos) and client.current_slot_to_play_card_into == '3':  # cancel
                            client.hand.append(client.selected_card_in_hand)
                            update_hand_cards_positions(client.hand)
                            client.players_active_slots[p][client.current_slot_to_play_card_into] = "None"
                            client.selected_card_in_hand = None
                            client.played_card_into_slot_not_locked_in_yet = False
                            client.waiting_for_lock_or_cancel = False
                        if slot_4_btn_a.is_clicked(pos) and client.current_slot_to_play_card_into == '4':  # lockin
                            update_after_draw_deck_to_hand(n)
                            n.send(
                                f"Played Card:{client.current_slot_to_play_card_into}:{client.selected_card_in_hand.id_number}")  # instruct:slot:card_id
                            client.played_card_into_slot_not_locked_in_yet = False
                            client.selected_card_in_hand = None
                            client.waiting_for_lock_or_cancel = False
                        elif slot_4_btn_ca.is_clicked(pos) and client.current_slot_to_play_card_into == '4':  # cancel
                            client.hand.append(client.selected_card_in_hand)
                            update_hand_cards_positions(client.hand)
                            client.players_active_slots[p][client.current_slot_to_play_card_into] = "None"
                            client.selected_card_in_hand = None
                            client.played_card_into_slot_not_locked_in_yet = False
                            client.waiting_for_lock_or_cancel = False
                    # endregion
                    # endregion

                    # region Base UI (eg. captain card)
                    if client.card_doing_damage_active:
                        if client.captain_box_opponent.collidepoint(pos):
                            damage = client.value_of_currently_active_effect
                            client.value_of_currently_active_effect = 0
                            game.players_current_hps[other_p] -= damage
                            print(f"Hit captain. Captains new hp: {game.players_current_hps[other_p]}")
                            client.card_doing_damage_active = False

                            # now we say if all the effects are done we can pass it to other_p to do their next card.
                            if not client.current_effects_to_play_out:  # if there are no effects to play out left
                                n.send(f"Finished Activations:{game.card_currently_activating[p]}")
                                client.current_active_card_popup_info = None
                                client.card_activations_active = False
                                # update the server to deal with multithreading
                                try:
                                    game = n.send("get")
                                except:
                                    run = False
                                    print("Couldn't get game")
                                    break
                    # endregion
            # endregion

            # region Keys Pressed/Inspecting
            keys = pygame.key.get_pressed()  # Get the state of all keys
            if keys[pygame.K_i]:  # Check if 'i' is being held down
                pos = pygame.mouse.get_pos()
                client.current_mouse_position = pos
                card_lists_to_check = [client.hand]
                found = False
                for list in card_lists_to_check:
                    for card in list:
                        if card.is_clicked(pos):
                            client.card_being_inspected = card
                            client.inspecting_card = True
                            found = True
                            break
                        else:
                            client.card_being_inspected = None
                            client.inspecting_card = False
                    if found:
                        break

                # decks
                # ours
                if client.deck_box_self.collidepoint(pos):
                    client.inspecting_own_deck = True
                else:
                    client.inspecting_own_deck = False
                if client.captain_box_self.collidepoint(pos):
                    client.inspecting_own_captain = True
                else:
                    client.inspecting_own_captain = False
                # opponents
                if client.deck_box_opponent.collidepoint(pos):
                    client.inspecting_opponent_deck = True
                else:
                    client.inspecting_opponent_deck = False
                if client.captain_box_opponent.collidepoint(pos):
                    client.inspecting_opponent_captain = True
                else:
                    client.inspecting_opponent_captain = False

            # if no longer inspecting, turn inspecting variables off
            elif not keys[pygame.K_i]:
                client.inspecting_own_deck = False
                client.inspecting_own_captain = False
                client.inspecting_opponent_deck = False
                client.inspecting_opponent_captain = False
                client.card_being_inspected = None
                client.inspecting_card = False
            # endregion
        # endregion

        # region End of Round Card Activation
        if not client.card_activations_active:
        # if not any(client.actively_playing_slot_list):
            if game.card_currently_activating[p]:
                slot_activating = game.card_currently_activating[p]
                card_trying_to_activate = game.players_active_slots[p][slot_activating]
                if game.players_gold_amounts[p] >= card_trying_to_activate.cost:
                    n.send(f"Spent Gold:{card_trying_to_activate.cost}")
                    client.card_activations_active = True
                    client.actively_playing_slot_list[int(slot_activating)] = True
                    client.current_active_card_popup_info, client.current_active_card_effects_list = game.players_active_slots[p][slot_activating].effect()
                else:
                    n.send(f"Not Enough Gold for Card")
        # endregion

        # region Updating Server Info
        # region Players Infos
        client.player_deck_lengths = game.deck_lengths
        client.player_hand_lengths = game.hand_lengths
        # endregion

        # region Actions Stuff
        if game.actions_submitted[p] and game.actions_submitted[other_p]:
            pygame.time.delay(2000)
            # send our actions.
            actions_to_send = "Turn Actions:"
            for action in client.active_moves_for_turn:
                actions_to_send += action
            n.send(actions_to_send)
            # turn this off, so it doesn't try to do it again
            n.send("Submitting Actions")

        client.players_active_slots = game.players_active_slots
        # endregion
        # endregion

        draw_window(window, game, p)


# endregion


# region Menu Function
def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in hp_buttons:
                    if button.is_clicked(pos):
                        client.hshp = int(button.text)
                for button in atk_buttons:
                    if button.is_clicked(pos):
                        client.hsatk = int(button.text)
                for button in block_buttons:
                    if button.is_clicked(pos):
                        client.hsblock = int(button.text)
                for button in plunder_buttons:
                    if button.is_clicked(pos):
                        client.hsplunder = int(button.text)
                for button in explore_buttons:
                    if button.is_clicked(pos):
                        client.hsexplore = int(button.text)
                if homescreen_play_button.is_clicked(pos):
                    run = False

        draw_window('homescreen')

    main()


# endregion


while True:
    menu_screen()
