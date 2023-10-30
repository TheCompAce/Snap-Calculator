import json
from modules import snap_base
from modules.menu.graphs_menu import graphs_menu
from modules.menu.make_deck_menu import deck_menu
from modules.menu.score_menu import score_menu
from modules.menu.top_cards_menu import top_cards_menu
from modules.utils import check_and_create_folder, autocomplete_location_name, autocomplete_card_name, read_json
from modules.menu import player_menu
from  modules.menu.analyze_menu import analyze_menu

def main_menu():
    check_and_create_folder("results")
    check_and_create_folder("player")
    check_and_create_folder("Images")

    while True:
        print("----- Snap Calculator Menu -----")
        print("1. Get Scoring Values")
        print("2. Get Top Cards")
        print("3. Create Data Graphs")
        print("4. Create Analysis Files Menu") 
        print("5. Player Detials Setup")
        print("6. Edit Matrix")
        print("7. Build Decks")        
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            score_menu()
        elif choice == '2':
            top_cards_menu()
        elif choice == '3':
            graphs_menu()
        elif choice == '4':
            analyze_menu()
        elif choice == '5':
            player_menu.player_setup_menu()
        elif choice == '6':
            pass
        elif choice == '7':
            deck_menu()
        elif choice == '8':
            print("Exiting the program.")
            break

