__author__ = "n3rdkeller.de"
__license__ = "GPL"
__version__ = "0.9"
__email__ = "github@n3rdkeller.de"
__status__ = "Development"

# imports
import implementation
import ui
from random import shuffle, randint

# -----
# function
# -----
def ask_for_card(player: int) -> bool:
    '''
    Function to let the AI ask for a card_type
    Picks a player at random, then looks what card type it has most of and
    asks for that card.
    Returns True if the asked player had that card.
    '''
    asked_player = 255
    while asked_player != player:
        # picks a random player, which is not the ai itself
        asked_player = randint(0, ui.player_count - 1)
    card_decider = [0] # needed to decide which card type to ask for
    for card_type in range(7, 15):
        card_counter = 0
        for item in range(len(implementation.player_hands[player])):
            if card_type == 11:
                card_type = "J"
            if card_type == 12:
                card_type = "Q"
            if card_type == 13:
                card_type = "K"
            if card_type == 14:
                card_type = "A"
            if str(card_type) in implementation.player_hands[player][item]:
                # counts how often a card type is in the ai's hand
                card_counter += 1
        if card_counter > card_decider[0]:
            # saves the card type that exists the most
            card_decider = [card_counter, card_type]
    cards_to_ask_for = [] # needed to determin which specific card to ask for
    for card_color in ["H", "D", "C", "S"]:
        card = card_color + str(card_type)
        if not card in implementation.player_hands[player]:
            # adds only cards which are not owned by the ai
            cards_to_ask_for.append(card)
    shuffle(cards_to_ask_for)
    # returns one of the cards that could be asked for at random
    return implementation.ask_for_card(player, asked_player, cards_to_ask_for[0])

