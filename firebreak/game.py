#!/usr/bin/env python3
from collections import namedtuple
from enum import Enum
from random import shuffle

class Color(Enum):
    RED = 91
    GREEN = 92
    BLUE = 93
    YELLOW = 94
    WHITE = 95
    RAINBOW = 96

Card = namedtuple('Card', ['color', 'rank'])

DEFAULT_COLORS = {Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.WHITE}
DEFAULT_COLOR_COMPOSITION = {
    1: 3,
    2: 2,
    3: 2,
    4: 2,
    5: 1,
}

class Board:
    def __init__(self, deck, max_clues=8, bombs=3):
        self.deck = deck
        self.max_clues = max_clues
        self.num_clues = max_clues
        self.num_bombs = bombs
        self.discards = {}
        self.zones = {color: 0 for color in self.deck.colors}

    def discard(self, card):
        self.discards[card] = self.discards.get(card, 0) + 1
        self.num_clues = min(self.max_clues, self.num_clues + 1)

    def play_card(self, card):
        if self.zones[card.color] == card.rank - 1:
            self.zones[card.color] += 1
            if card.rank == 5:
                self.num_clues = min(self.max_clues, self.num_clues + 1)
        else:
            self.num_bombs -= 1
            self.discards[card] = self.discards.get(card, 0) + 1

    def give_clue(self):
        assert self.num_clues > 0, "Tried to give a clue when there were no available clue tokens!"
        self.num_clues -= 1



class Deck:
    def __init__(self, colors=DEFAULT_COLORS, color_composition=DEFAULT_COLOR_COMPOSITION):
        self.colors = colors
        self.cards_remaining = 0
        self.card_counts = {}
        for color in self.colors:
            for rank, count in color_composition.items():
                self.card_counts[Card(color, rank)] = count
                self.cards_remaining += count

        self.__shuffled = [card_id for card_id, count in self.card_counts.items() for i in range(count)]
        shuffle(self.__shuffled)

    def draw_card(self):
        assert self.cards_remaining > 0, "Tried to draw from an empty deck."
        card_to_deal = self.__shuffled[self.cards_remaining - 1]
        self.card_counts[card_to_deal] -= 1
        self.cards_remaining -= 1
        return card_to_deal
