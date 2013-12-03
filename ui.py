__author__ = "n3rdkeller.de"
__license__ = "GPL"
__version__ = "0.9"
__email__ = "github@n3rdkeller.de"
__status__ = "Development"

# imports
import os
import sys
import re
import implementation
from copy import copy

# constants
NEW_GAME = 254
NEXT_TURN = 253
ERROR = 255
CARD_STYLE = ("+---+ ", "|", "| ")
AI_NAMES = ("Horst", "Dieter", "Manfred", "Timo", "Rolf", "Hans", "Andreas", \
            "Josef", "Uwe", "Tim", "Linus", "Alfred", "Björn", "Gerd", "Mario")


if sys.stdin.encoding.lower() == "cp850": # Windows Console
    HEARTS, DIAMONDS, CLUBS, SPADES = "\x03", "\x04", "\x05", "\x06"
    COLORS = {"clear": "", "bell": "", "yellow": "", "red": ""}
elif sys.stdin.encoding.lower() in ("utf-8"): # Unix
    HEARTS, DIAMONDS, CLUBS, SPADES = "\u2665", "\u2666", "\u2663", "\u2660"
    COLORS = {"clear": "\033[0m", "bell": "\a", \
          "yellow": "\033[1;33m", "red": "\033[1;31m"}
elif sys.stdin.encoding.lower() == "cp1252": # IDLE
    HEARTS, DIAMONDS, CLUBS, SPADES = "\u2665", "\u2666", "\u2663", "\u2660"
    COLORS = {"clear": "", "bell": "", "yellow": "", "red": ""}
else:
    HEARTS, DIAMONDS, CLUBS, SPADES = "H", "D", "C", "S"
    COLORS = {"clear": "", "bell": "", "yellow": "", "red": ""}


# global variables
player_count = None
player_names = []
player_types = [] # bool-list: Human (True), AI (False)
current_player = 0
quartets_counter = []
turn_counter = 1
# Same index in player_names, player_types and quartets_counter
# corresponds to the same player

# -----
# functions
# -----
def print_mainmenu():
    '''Prints out the main menu of the game.'''
    clear_screen()
    print(COLORS["yellow"] + "Welcome to our Quartet!" + COLORS["clear"])
    global player_count
    while True:
        player_count = ask_for_player_count()
        if player_count == ERROR:
            error_occured()
        else:
            break
    ask_for_player_names()

def ask_for_player_count() -> int:
    '''Asks the user for the player count.'''
    print("How many players? 2-8")
    player_count = input_int(8,2)
    if player_count == ERROR:
        return ERROR
    if player_count == NEW_GAME:
        restart_game()
    else:
        return player_count

def ask_for_player_names():
    '''Asks the user for the player names.'''
    while True:
        global player_names
        global player_count
        while True:
            # Player 1 can enter his name
            print("Please enter your name, Player 1:")
            player_name = input()
            # u"^([ \u00c0-\u01ffa-zA-Z'\-]){2,32}$|^[qr]$"
            # regex allows words of the length 2-32 with all kinds of utf-8
            # symbols, or just 'q' or 'r' for quit and new game
            # ISSUE: ONLY A GOOD OS KNOWS THE CHARACTERS: \u00c0-\u01ff
            # ELSE: CHANGE (TODO)
            re_pattern = re.compile(u"^([ \u00c0-\u01ffa-zA-Z'\-]){2,32}$|^[qr]$")
            if re_pattern.match(player_name):
                if player_name == "q":
                    quit_game()
                if player_name == "r":
                    restart_game()
                # Adds the capitalized playername to the player_names list
                # and adds True for human to the player_types list.
                player_names.append(player_name.title())
                player_types.append(True)
                break
            else:
                error_occured()
        print("Welcome, " + COLORS["yellow"] + player_names[0] + \
                        COLORS["clear"] + ", and have fun!")
        # u"^(([ \u00c0-\u01ffa-zA-Z'\-]){2,32})$|^[qrc]$" 
        # regex allows everything like the previous and adds the option
        # to type a single 'c' for 'ai from now on'
        re_pattern = re.compile(u"^(([ \u00c0-\u01ffa-zA-Z'\-]){2,32})$|^[qrc]$")
        ai_count = 0
        for i in range(1, player_count):
            # entering all player names:
            while True:
                print("Now, Player" + COLORS["yellow"] + " {0}".format(i + 1) + \
                        COLORS["clear"] + ", please enter your name " \
                        + "(or 'c' for ai from now on):")
                player_name = input()
                if (re_pattern.match(player_name)) and (player_name != "c"):
                    # Adds the capitalized playername to the player_names list
                    # and adds True for human to the player_types list.
                    player_names.append(player_name.title())
                    player_types.append(True)
                    print("Welcome, " + COLORS["yellow"] + player_names[i] + \
                            COLORS["clear"] + ", and have fun!")
                    break
                elif player_name == "c":
                    # counts the players left and makes them ai
                    ai_count = player_count - i
                    print("\nYou chose to play against " \
                        + "{0} computer opponents.".format(ai_count))
                    input("\nPress 'enter' to start the game.\n")
                    set_ai_names(ai_count)
                    break
                elif player_name == "q":
                    quit_game()
                elif player_name == "r":
                    restart_game()
                else:
                    error_occured()
            if ai_count != 0:
                break
        break

def set_ai_names(count: int): 
    global player_names
    ai_count = 0
    i = 0
    while ai_count < count:
        if not (AI_NAMES[i] in player_names):
            # Adds a AI name to the player_names list
            # and adds False for ai to the player_types list.
            player_names.append(AI_NAMES[i])
            player_types.append(False)
            ai_count += 1
        i += 1

def clear_screen():
    '''Clears the terminal window.'''
    # We do really not like Windows for this to be duty.
    if os.name == "posix":
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        os.system('cls')
    else:
        print(80 * "\n")

def show_main_interface():
    '''Displays the main interface'''
    clear_screen()
    print("Player:", player_names[current_player])
    print("Turn:", turn_counter, end = "    ")
    print("Quartets dropped:", quartets_counter[current_player], "\n")
    if player_count == 2:
        print("Opponent:")
    else:
        print("Opponents:")
    row_counter = 0
    # copy of player_names to prevent deletions:
    opponent_names = copy(player_names)
    # getting rid of the current player
    opponent_names.pop(current_player)
    for n in range(len(opponent_names)):
        # printing the opponents in a nice layout
        if (n + 1 < len(opponent_names)) & (row_counter < 3):
            print(opponent_names[n], " (", n, end = ") | ", sep = "")
            row_counter += 1
        else:
            print(opponent_names[n], " (", n, end = ")\n", sep = "")
            row_counter = 0
    print("\nOwn hand:")

def show_hand(hand: list) -> str:
    '''Returns a printable string of nice looking given cards.'''
    hand.sort(key=lambda x: implementation.sort_order.index(x))
    card_counter = len(hand)
    hand_string = (card_counter * CARD_STYLE[0]) + "\n"
    for i in range(card_counter):
        hand_string += CARD_STYLE[1] + " "
        if hand[i][0] == "C":
            hand_string += CLUBS
        elif hand[i][0] == "S":
            hand_string += SPADES
        elif hand[i][0] == "H":
            hand_string += HEARTS
        elif hand[i][0] == "D":
            hand_string += DIAMONDS
        else:
            return ERROR
        hand_string += " " + CARD_STYLE[2]
    hand_string += "\n"
    for i in range(card_counter):
        if hand[i][1:]=="10":
            hand_string += CARD_STYLE[1] + "1 0" + CARD_STYLE[2]
        else:
            hand_string += CARD_STYLE[1] + " " + hand[i][1] + " " \
                            + CARD_STYLE[2]
    hand_string += "\n" + (card_counter * CARD_STYLE[0]) + "\n"
    return hand_string

def ask_for_cards() -> bool:
    card = ERROR
    card_already_ownd = 252
    while (card == ERROR) | (card == card_already_ownd):
        if (card != card_already_ownd):
            if player_count > 2:
                print("Who to ask (0 - {0}):".format(player_count - 2))
                asked_player = input_int(player_count - 2)
                if asked_player == ERROR:
                    error_occured()
                    continue
            else:
                asked_player = 0
            if asked_player >= current_player:
                asked_player += 1
        print("Which card are you asking for? (" \
            + HEARTS + " = H | " + SPADES + "︎ = S | " \
            + DIAMONDS + "︎ = D | " + CLUBS + " = C):")
        card = input_cards()
        if (card != ERROR) & (not (card in implementation.player_hands[current_player])):
            return implementation.ask_for_card(current_player, asked_player, card)
        elif (card != ERROR) & (card in implementation.player_hands[current_player]):
            print(COLORS["bell"] + "You already own that card!")
            card = card_already_ownd
        if card == ERROR:
            error_occured()

def victory():
    clear_screen()
    print(COLORS["red"] + "Game Over!" + COLORS["clear"] + "\n")
    print("Name" + (26 * " ") + "Dropped")
    print(40 * "-")
    for i in player_names:
        print(i + ((30 - len(i)) * " ") + str(quartets_counter[player_names.index(i)]))
    print()
    winners=[]
    for i in range(len(quartets_counter)):
        if quartets_counter[i] == max(quartets_counter):
            winners.append(player_names[i])
    if len(winners) == 1:
        print(COLORS["red"] + COLORS["bell"] + "{0} won!".format(winners[0])\
            + COLORS["clear"])
    else:
        print_string = COLORS["red"] + COLORS["bell"]
        for winner in winners:
            print_string += COLORS["yellow"] + winner + COLORS["red"] + ", "
        print_string += "\b\b" + " won!" + COLORS["clear"]
        print(print_string)

    choice = input("\nPress 'enter' to quit or type 'r' to restart.\n")
    if choice == "r":
        restart_game()
    else:
        quit_game()

def input_int(ubound: int, lbound: int = 0) -> int:
    '''Supporting function to get an input from the user.'''
    input_integer = input()
    # "^([" + str(lbound) + "-" + str(ubound) + "]|[qr])$"
    # regex allows numbers between the bounds and 'q' or 'r'
    re_pattern = re.compile("^([" + \
                    str(lbound) + "-" + str(ubound) \
                     + "]|[qr])$")
    if re_pattern.match(input_integer):
        if input_integer == "r":
            return NEW_GAME
        elif input_integer == "q":
            quit_game()
        else:
            return int(input_integer)
    else:
        return ERROR

def input_cards() -> str:
    '''Supporting function to get a string input from the user.
    It's used for the input of the card names and it's filtered by
    regular expressions.'''
    # We're going to do this with RegEx, let's try this one:
    # ^([HDCS])(7|8|9|10|[JQKA])$|^([qr])$
    # This should filter all correct card names out of the input string
    re_pattern = re.compile("^([HDCS])(7|8|9|10|[JQKA])$|^([qr])$")
    input_string = input()
    if input_string == "bigdaddy":
        # cheat to test what happens at the end of the game
        global current_player
        global quartets_counter
        quartets_counter[current_player] = 5
        quartets_counter[current_player + 1] = 5
        victory()
    if re_pattern.match(input_string):
        if input_string == "r":
            restart_game()
        elif input_string == "q":
            quit_game()
        else:
            return input_string
    else:
        return ERROR

def quit_game():
    print("Quitting game...")
    exit()

def error_occured():
    if sys.stdin.encoding.lower() in ("utf-8", "cp1252"):
        print("\033[A\033[2K\033[A\033[2K\033[A", end = "")
    print("An error occured. Please try again.")

def restart_game():
    '''Restarts the game from the beginning.'''
    python = sys.executable
    os.execl(python, python, * sys.argv)
