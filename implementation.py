__author__ = "n3rdkeller.de"
__license__ = "GPL"
__version__ = "0.9"
__email__ = "github@n3rdkeller.de"
__status__ = "Development"

# imports
from random import shuffle
from copy import copy
import re
import ui

# global variables
deck = []
player_hands = []
sort_order = []

# -----
# functions
# -----
def init_deck():
    '''
    Initializes the deck (fills it with cards) and shuffles it.
    >>> test_cards()
    [32, [32, 12, 32, 0, 32, 0, 32, 0, 32, 0, 32, 0, 32, 0]]
    '''
    global deck
    global sort_order
    deck = []
    for i in range(7,15):
        if i < 11:
            deck.append("H" + str(i))
            deck.append("S" + str(i))
            deck.append("D" + str(i))
            deck.append("C" + str(i))
        elif i == 11:
            deck.append("H" + "J")
            deck.append("S" + "J")
            deck.append("D" + "J")
            deck.append("C" + "J")
        elif i == 12:
            deck.append("H" + "Q")
            deck.append("S" + "Q")
            deck.append("D" + "Q")
            deck.append("C" + "Q")
        elif i == 13:
            deck.append("H" + "K")
            deck.append("S" + "K")
            deck.append("D" + "K")
            deck.append("C" + "K")
        elif i == 14:
            deck.append("H" + "A")
            deck.append("S" + "A")
            deck.append("D" + "A")
            deck.append("C" + "A")
    sort_order = copy(deck)
    shuffle(deck)

def distr_cards(player_count: int):
    '''
    Distribute the cards to the given amount of players.
    >>> test_cards()
    [32, [32, 12, 32, 0, 32, 0, 32, 0, 32, 0, 32, 0, 32, 0]]
    '''
    global player_hands
    player_hands = []
    if player_count == 2:
        for i in range(player_count):
            player_hands.append(deck[-10:])
            del deck[-10:]
    else:
        card_count = len(deck) // player_count
        card_rest = len(deck) % player_count
        for i in range(player_count):
            player_hands.append(deck[-card_count:])
            del deck[-card_count:]
        if card_rest != 0:
            i = 0
            while len(deck) != 0:
                player_hands[i].append(deck[-1])
                del deck[-1]
                i += 1
    for i in range(player_count):
        ui.quartets_counter.append(0)

def test_cards() -> list:
    '''Function to test this module.'''
    init_deck()
    deck_len = len(deck)
    test_array = []
    for x in range(2,9):
        init_deck()
        test_array.append(len(deck))
        distr_cards(x)
        test_array.append(len(deck))
    return [deck_len,test_array]

def filter_quartets(player: int) -> list:
    '''Deletes all quartets the given player has in his hand,
    and returns them in a list of the quartets containing their cards.'''
    global player_hands
    quartets = []
    for card_type in range(7,15):
        is_quartet_counter = 0
        card_position =[]
        for item in range(len(player_hands[player])):
            if card_type == 11:
                card_type = "J"
            if card_type == 12:
                card_type = "Q"
            if card_type == 13:
                card_type = "K"
            if card_type == 14:
                card_type = "A"
            if str(card_type) in player_hands[player][item]:
                is_quartet_counter += 1
                card_position.append(item)
        if is_quartet_counter == 4:
            for i in range(len(card_position)):
                quartets.append(player_hands[player][card_position[i]])
    for i in range(len(quartets)):
        player_hands[player].remove(quartets[i])
    return quartets

def ask_for_card(asking_player: int, asked_player: int, card: str) -> bool:
    '''Function moves a card from one players hand to anothers'''
    if card in player_hands[asked_player]:
        # Appends the card to the asking players hand
        # and removes it from the asked players hand
        player_hands[asking_player].\
            append( player_hands[asked_player].\
                pop( player_hands[asked_player].\
                    index(card) ) )
        return True
    else:
        return False

def draw_card(player: int) -> str:
    '''
    Function to let a player draw a card if there are only 2 players
    '''
    drawn_card = deck.pop(-1)
    player_hands[player].append(drawn_card)
    return drawn_card