from modules.menu.player_menu import player_file
from modules.utils import autocomplete_card_name, autocomplete_deck_name, autocomplete_location_name, get_cards_from_names, read_json, read_player_json
from modules import snap_base

base_data = read_json(snap_base.base_file)
all_cards = []

for series in base_data.get('Cards', []):
    for series_name, cards in series.items():
        all_cards.extend(cards)

def top_cards_menu():
    while True:
        print("----- Top Cards for Location Menu -----")
        print("1. Top Cards (All) for Location")
        print("2. Top Cards (Player) for Location ..")
        print("3. Top Cards (All) for Card")
        print("4. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            location_name = autocomplete_location_name(snap_base.base_file, input("Enter the location name: "))
            count = int(input("Enter the number of top cards you want: "))
            energy_level = int(input("Enter the energy level to filter by: "))
                    
            top_cards = snap_base.get_top_cards_for_location(location_name, all_cards, count, energy_level)
            
            if isinstance(top_cards, str):
                print(top_cards)
            else:
                print(f"The top {count} cards for location {location_name} are: {', '.join(top_cards)}")
        elif choice == '2':
            top_cards_player_menu()
        elif choice == '3':
            base_card = autocomplete_card_name(snap_base.base_file, input("Enter a card name: "))
            count = input("Enter the number of top cards you want: ")
            if count.isdigit():
                energy_level = int(input("Enter the energy level to filter by: "))
                top_cards = snap_base.get_top_cards_for_card(base_card, all_cards, count, energy_level)

                if isinstance(top_cards, str):
                    print(top_cards)
                else:
                    print(f"The top {count} cards for card {base_card} are: {', '.join(top_cards)}")
            else:
                print("Invalid Options.")
        elif choice == '4':
            print("Exiting the program.")
            break


def top_cards_player_menu():
    
    while True:
        
        print("----- Select Player for Top Card for Location Menu -----")

        ct, players = list_players()

        print("------------------------------")

        print(f"{ct + 1}. Back")
        choice = input("Enter your choice: ")

        if choice.isdigit():
            choice = int(choice)
            if choice - 1 < ct:
                player = players[ct - 1]
                top_player_menu(player)
                pass
            elif choice == ct + 1:
                break  # Go back to the main menu
            else:
                print("Invalid choice.")
    
def top_player_menu(player):
    while True:
        print(f"----- Top Cards of {player['Name']} for Location Menu -----")
        print("1. Top Collection Cards for Location")
        print("2. Top Deck Cards for Location")
        print("3. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            location_name = autocomplete_location_name(snap_base.base_file, input("Enter the location name: "))
            count = int(input("Enter the number of top cards you want: "))
            energy_level = int(input("Enter the energy level to filter by: "))
            
            real_cards = get_cards_from_names(player["Collected"], snap_base.base_file)

            top_cards = snap_base.get_top_cards_for_location(location_name, real_cards, count, energy_level)
            
            if isinstance(top_cards, str):
                print(top_cards)
            else:
                print(f"The top {count} cards for location {location_name} are: {', '.join(top_cards)}")
        elif choice == '2':
            top_player_deck_menu(player)
        elif choice == '3':
            break

def top_player_deck_menu(player):

    while True:
        decks = player["Decks"]
        print(f"----- Select the deck to for {player['Name']} Menu -----")
        list_decks(decks)

        ct = len(decks)
        print("------------------------------")
        print(f"{ct + 1}. Back")
        
        choice = input("Enter your choice: ").strip()
        
        if choice.isdigit():
            choice = int(choice)
            if choice - 1 < ct:
                check_deck_location(decks[choice - 1]["Cards"])
            elif choice == ct + 1:
                break  # Go back to the main menu
            else:
                print("Invalid choice.")
        else:
            selected_deck = autocomplete_deck_name(decks, choice)
            deck_found = False
            for deck in decks:
                if deck['Name'] == selected_deck:
                    check_deck_location(deck["Cards"])

            if not deck_found:
                print(f"Deck {selected_deck} not found.")
                break

def check_deck_location(cards):
    location_name = autocomplete_location_name(snap_base.base_file, input("Enter the location name: "))
    count = int(input("Enter the number of top cards you want: "))
    energy_level = int(input("Enter the energy level to filter by: "))
    
    real_cards = get_cards_from_names(cards, snap_base.base_file)

    top_cards = snap_base.get_top_cards_for_location(location_name, real_cards, count, energy_level)
    
    if isinstance(top_cards, str):
        print(top_cards)
    else:
        print(f"The top {count} cards for location {location_name} are: {', '.join(top_cards)}")

def list_decks(decks):
    for i, deck in enumerate(decks):
        print(f"{str(i + 1)}. {deck['Name']}")

def list_players():
    players_base = read_player_json(player_file)
    players = players_base["Players"]
    ct = len(players)
    for i, player in enumerate(players):
        print(f"{str(i + 1)}. {player['Name']}")

    return ct, players