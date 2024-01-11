import pygame
import os

CARD_SIZE = (55, 77)

# region Card Loads
crusty_ld = pygame.image.load(os.path.join('Assets', 'Images', 'Cards', 'Crusty.png'))
clawshank_ld = pygame.image.load(os.path.join('Assets', 'Images', 'Cards', 'Clawshank.png'))
the_shoveler_ld = pygame.image.load(os.path.join('Assets', 'Images', 'Cards', 'The Shoveler.png'))
# endregion

card_image_loads = {
    'Clawshank': clawshank_ld,
    'Crusty': crusty_ld,
    'The Shoveler': the_shoveler_ld,
}

# region Images
clawshank = pygame.transform.scale(clawshank_ld, CARD_SIZE)
crusty = pygame.transform.scale(crusty_ld, CARD_SIZE)
the_shoveler = pygame.transform.scale(the_shoveler_ld, CARD_SIZE)
# endregion

card_images_dict = {
    'Clawshank': clawshank,
    'Crusty': crusty,
    'The Shoveler': the_shoveler,
}


class Card:
    all_instances = []

    def __init__(self, image, id_number, name, cost):
        self.image = image
        self.id_number = id_number
        self.id = id
        self.name = name
        self.cost = cost
        self.pos = (-1000, -1000)
        self.pos_for_opp = (-1000, -1000)
        self.hb = None
        self.hb_for_opp = None
        self.active = False
        Card.all_instances.append(self)

    def is_clicked(self, pos):
        if self.hb and self.hb.collidepoint(pos):
            return self
        else:
            return False

    def is_clicked_by_opp(self, pos):
        if self.hb_for_opp and self.hb_for_opp.collidepoint(pos):
            return self
        else:
            return False

    def update_hb(self):
        if self.pos:
            self.hb = self.image.get_rect(topleft=self.pos)
        else:
            self.hb = None
        if self.pos_for_opp:
            self.hb_for_opp = self.image.get_rect(topleft=self.pos_for_opp)
        else:
            self.hb_for_opp = None

    def __getstate__(self):
        state = self.__dict__.copy()
        # Exclude the unpickleable entries.
        state['image'] = None
        return state

    def __setstate__(self, state):
        # Restore instance attributes.
        self.__dict__.update(state)
        # Add the unpickleable entries back.
        self.image = card_images_dict[self.name]


class Crew(Card):
    def __init__(self, image, id_number, name, cost, max_health, damage, block, explore, plunder):
        super().__init__(image, id_number, name, cost)
        self.image = image
        self.id_number = id_number
        self.id = id
        self.name = name
        self.cost = cost
        self.pos = (-1000, -1000)
        self.pos_for_opp = (-1000, -1000)
        self.hb = None
        self.hb_for_opp = None
        self.max_health = max_health
        self.current_health = self.max_health
        self.damage = damage
        self.block = block
        self.explore = explore
        self.plunder = plunder
        self.effects_dict = {
            'The Shoveler': self.shoveler_effect,
            'Clawshank': self.shoveler_effect,
            'Crusty': self.shoveler_effect,
        }
        self.effect = self.effects_dict[self.name]

    def shoveler_effect(self):
        number_of_buttons = 1
        button_text_1 = "Deal Damage"
        button_text_2 = None
        button_text_3 = None
        button_text_4 = None
        pop_up_info = [number_of_buttons, button_text_1, button_text_2, button_text_3, button_text_4]
        effects_list = [[f"Damage:{self.damage}"]]
        return pop_up_info, effects_list


class Action(Card):
    def __init__(self, image, id_number, name, cost):
        super().__init__(image, id_number, name, cost)
        self.image = image
        self.id_number = id_number
        self.id = id
        self.name = name
        self.cost = cost
        self.pos = (-1000, -1000)
        self.pos_for_opp = (-1000, -1000)
        self.hb = None
        self.hb_for_opp = None


class Item(Card):
    def __init__(self, image, id_number, name, cost):
        super().__init__(image, id_number, name, cost)
        self.image = image
        self.id_number = id_number
        self.id = id
        self.name = name
        self.cost = cost
        self.pos = (-1000, -1000)
        self.pos_for_opp = (-1000, -1000)
        self.hb = None
        self.hb_for_opp = None


# image, idn, name, cost, amxhealth, damage, block, explore. plunder
c1 = Crew(clawshank, 1, "Clawshank", 3, 3, 3, 0, 0, 0)
c2 = Crew(clawshank, 2, "Clawshank", 3, 3, 3, 0, 0, 0)
c3 = Crew(crusty, 3, "Crusty", 2, 3, 3, 0, 0, 0)
c4 = Crew(crusty, 4, "Crusty", 2, 3, 3, 0, 0, 0)
c5 = Crew(the_shoveler, 5, "The Shoveler", 1, 3, 3, 0, 1, 0)
c6 = Crew(the_shoveler, 6, "The Shoveler", 1, 3, 3, 0, 1, 0)
c7 = Crew(clawshank, 7, "Clawshank", 3, 3, 3, 0, 0, 0)
c8 = Crew(clawshank, 8, "Clawshank", 3, 3, 3, 0, 0, 0)
c9 = Crew(crusty, 9, "Crusty", 2, 3, 3, 0, 0, 0)
c10 = Crew(crusty, 10, "Crusty", 2, 3, 3, 0, 0, 0)
c11 = Crew(the_shoveler, 11, "The Shoveler", 1, 3, 3, 0, 1, 0)
c12 = Crew(the_shoveler, 12, "The Shoveler", 1, 3, 3, 0, 1, 0)
