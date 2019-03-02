#!/usr/bin/env python3

import unittest

from firebreak.game import Deck, Color, Card, DEFAULT_COLORS, Board

class TestGame(unittest.TestCase):
    def test_deck(self):
        unique_deck = Deck(color_composition={i:1 for i in range(1, 6)})
        seen = set()
        while unique_deck.cards_remaining:
            card = unique_deck.draw_card()
            self.assertNotIn(card, seen) # There should be no duplicates
            seen.add(card)
        # Expect to see one of every card
        self.assertEqual(seen, {Card(c, r) for c in DEFAULT_COLORS for r in range(1, 6)})
        # Expect to see an error if we draw from an empty deck.
        with self.assertRaises(Exception):
            unique_deck.draw_card()

    def test_default_deck(self):
        ''' This hard-codes some basic assumptions about the standard deck (no rainbows) '''
        default_deck = Deck()
        self.assertEqual(default_deck.cards_remaining, 50)
        self.assertEqual(default_deck.card_counts[Card(Color.BLUE, 1)], 3)
        self.assertEqual(default_deck.card_counts[Card(Color.RED, 4)], 2)
        self.assertEqual(default_deck.card_counts[Card(Color.WHITE, 5)], 1)

        yellow2 = Card(Color.YELLOW, 2)
        card_drawn = None
        while card_drawn != yellow2:
            card_drawn = default_deck.draw_card()

        self.assertEqual(default_deck.card_counts[yellow2], 1)

        card_drawn = None
        while card_drawn != yellow2:
            card_drawn = default_deck.draw_card()

        self.assertEqual(default_deck.card_counts[yellow2], 0)

    def test_board(self):
        # instantiate an instance of a Board
        clues = 8
        bombs = 3
        bored_cat = Board(Deck(), max_clues=clues, bombs=bombs)

        self.assertEqual(bored_cat.num_clues, clues)

        # clues
        for i in range(clues):
            bored_cat.give_clue()

        self.assertEqual(bored_cat.num_clues, 0)

        with self.assertRaises(Exception):
            bored_cat.give_clue()

        bored_cat.play_card(Card(Color.WHITE, 1))
        bored_cat.play_card(Card(Color.WHITE, 2))
        bored_cat.play_card(Card(Color.WHITE, 3))
        bored_cat.play_card(Card(Color.WHITE, 4))
        bored_cat.play_card(Card(Color.WHITE, 5))

        self.assertEqual(bored_cat.num_clues, 1)

        bored_cat.give_clue()
        self.assertEqual(bored_cat.num_clues, 0)

        # Discards
        for i in range(clues):
            bored_cat.discard(Card(Color.WHITE, 1))
            self.assertEqual(bored_cat.num_clues, i+1)

        bored_cat.discard(Card(Color.WHITE, 1))
        self.assertEqual(bored_cat.num_clues, bored_cat.max_clues)

        # bombs
        self.assertEqual(bored_cat.num_bombs, bombs)

        for i in range(bombs):
            while bored_cat.num_bombs != 0:
                bored_cat.play_card(Card(Color.WHITE, 3))

        self.assertEqual(bored_cat.num_bombs, 0)

