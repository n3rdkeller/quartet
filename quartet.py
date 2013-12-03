__author__ = "n3rdkeller.de"
__license__ = "GPL"
__version__ = "0.9"
__email__ = "github@n3rdkeller.de"
__status__ = "Development"

# imports
import ui
import implementation
import ai

# global variables
victory = False

def main():
    ui.clear_screen()
    ui.print_mainmenu()
    implementation.init_deck()
    implementation.distr_cards(ui.player_count)
    global victory
    # Main part of game
    while not victory:
        # if the player is human:
        if ui.player_types[ui.current_player]: # HUMAN
            card_there = True
            before_asking = True
            while card_there:
                ui.clear_screen()
                ui.show_main_interface()
                # Saves detected quartets in a list. list can be empty
                quartets = implementation.filter_quartets(ui.current_player)
                # Prints the hand of the player in a nice layout
                print(ui.show_hand(implementation.player_hands[ui.current_player]))
                if not before_asking:
                    # Only shown if the player got a card from another player
                    print("Graaaaatz! You got the card you wanted!\n")
                if len(quartets) != 0:
                    # displaying the dropped quartet
                    # (it's already removed from implementation.player_hands)
                    print("You dropped a quartet:")
                    print(ui.show_hand(quartets))
                    ui.quartets_counter[ui.current_player] += 1
                    input("Press 'enter' to continue.\n")
                    ui.clear_screen()
                    ui.show_main_interface()
                    print(ui.show_hand(implementation.player_hands[ui.current_player]))
                if [] in implementation.player_hands:
                    # Detects end of game
                    victory = True
                    ui.victory()
                    break
                # card_there gets True, when the player successfully 
                # asked for a card
                card_there = ui.ask_for_cards()
                # Used earlier in an if-condition
                before_asking = False
            if victory:
                break
            print("\nYou did not get the card you asked for.")
            if len(implementation.deck) != 0:
                # Automaticly draws a card for the player if he failed to ask
                # for the right card and shows it to him
                print("But I got one from the deck for you:")
                print(ui.show_hand([implementation.draw_card(ui.current_player)]))
            input("Press 'enter' for next turn.\n")
            # switches the player
            if ui.current_player == ui.player_count - 1:
                ui.current_player = 0
                ui.turn_counter += 1
            else:
                ui.current_player += 1
            

        else: # AI
            while ai.ask_for_card(ui.current_player):
                # Asking for cards part for the ai.
                # Ai asks for cards in the while condition
                implementation.filter_quartets(ui.current_player)
                if [] in implementation.player_hands:
                    # tests for victory condition
                    victory = True
                    ui.victory()
                    break
            if victory:
                break
            if len(implementation.deck) != 0:
                # AI draws a card if it failed to ask for the right card
                implementation.draw_card(ui.current_player)
            # switches the player
            if ui.current_player == ui.player_count - 1:
                ui.current_player = 0
                ui.turn_counter += 1
            else:
                ui.current_player += 1

if __name__ == '__main__':
    main()