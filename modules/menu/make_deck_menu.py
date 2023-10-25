from heapq import nlargest
from modules import snap_base
from modules.utils import autocomplete_location_name, print_card_data_from_name, ask_for_player, read_json, write_json, ask_for_decks, get_cards_from_base, get_cards_from_names, ask_for_decks
from modules.menu.player_menu import player_file
def deck_menu():
    while True:
        print("Welcome to the Deck Building Menu!")
        print("1. Build a deck based on specific locations")
        print("2. Build an overall best deck based on average scores by all Locations")
        print("3. Build an overall best deck based on average scores by card Links")
        print("4. Exit")
        
        choice = input("Please enter your choice: ")
        if choice == '1':
            build_deck_based_on_locations()
        elif choice == '2':
            build_deck_based_on_overall()
        elif choice == '3':
            build_deck_based_on_overall_cards()
        elif choice == '4':
            print("Exiting the Deck Building Menu.")
            break
        else:
            print("Invalid choice. Please try again.")

from modules.snap_base import calculate_link_score
from modules.utils import check_if_valid_location  # Import the scoring function from snap_base.py

def build_deck_based_on_overall_cards():
    player_name = ask_for_player(player_file)

    card_check_data = []
    if player_name:
        player_data = read_json(player_file)
        player_found = False
        
        for p, player in enumerate(player_data["Players"]):
            if player == player_name:
                card_names = player["Collected"]
                card_data = get_cards_from_names(card_names, snap_base.base_file)
                for card in card_data:
                    top_cards = snap_base.get_top_cards_for_card(card["Card"], card_data)
                    for top in  top_cards:
                        card_found = False
                        for check_card in card_check_data:
                            if check_card["Name"] == top:
                                card_found = True
                                break

                        if not card_found:
                            # set_card_data = get_cards_from_names(top, snap_base.base_file)
                            score = snap_base.calculate_cards_compatibility_score(card["Card"], top)
                            add_card = {
                                "Name" : top,
                                "Score": (score * (6 * (card["Cost"] / 6) * (card["Power"] / 20)))
                            }
                            card_check_data.append(add_card)
                base_scores = {}
                for card in card_check_data:
                    print(card["Score"])
                    base_scores[card["Name"]] = card["Score"]
                    
                deck_cards = nlargest(12, base_scores, key=base_scores.get)
                build_deck(player_name, deck_cards)
                break        
        if not player_found:
            print("Player name not found.")
    else:
        print("Player name not found.")

def build_deck_based_on_locations(location_list = None):
    player_name = ask_for_player(player_file)
    player_data = read_json(player_file)
    player_cards = []
    if player_name:
        player_found = False
        for p, player in enumerate(player_data["Players"]):
            if player == player_name:
                player_found = True
                player_cards = player["Collected"]
                pass

        if not player_found:
            print("Player not selected, deck not made.")
            return
        
        location_pass = False
        if not location_list:
            location_list = input("Enter a list of comma-separated locations: ").split(',')
        else:
            location_pass = True
            location_list = location_list.split(',')

        locations_bad = False
        bad_locations = []
        for i, location in enumerate(location_list):
            location_list[i] = autocomplete_location_name(snap_base.base_file, location, no_check=location_pass)
            if not check_if_valid_location(snap_base.base_file, location_list[i]):
                locations_bad = True
                bad_locations.append(location)
            
        if locations_bad:
            for bad_location in bad_locations:
                print(f"Location {bad_location} Not Found.")
            return None

        set_card_data = []

        for card in player_cards:
            location_scores = 0.0
            for location in location_list:
                location_scores += calculate_link_score(location, card)

            add_card_data = {
                "name" : card,
                "score": location_scores / len(location_list)
            }
            set_card_data.append(add_card_data)

        if len(add_card_data) > 0:
            top_12_cards = sorted(set_card_data, key=lambda x: x['score'], reverse=True)[:12]
            card_array = [obj["name"] for obj in top_12_cards]

            build_deck(player_name, card_array)
        else:
            print("Error finding cards.")
    else:
        print("Player name not set, Deck not saved.")

def build_deck_based_on_overall():
    base_data = read_json(snap_base.base_file)

    locations_names = ""
    for l, location in enumerate(base_data["Locations"]):
        if l == len(base_data["Locations"]) - 1:
            locations_names += location["Location"]
        else:
            locations_names += location["Location"] + ","

    build_deck_based_on_locations(locations_names)

def build_deck(player_name, cards):
    for card in cards:
        print_card_data_from_name(card, snap_base.base_file)

    player_data = read_json(player_file)

    add_check = input("Do you want to make a Deck out for this? (y/n)")

    if add_check == "y":
        deck_name = input("Enter the name for the deck? ")
        if deck_name != "":
            for p, player in enumerate(player_data["Players"]):
                if player == player_name:
                    deck_found = False
                    for d, deck in player["Decks"]:
                        if deck == deck_name:
                            deck_found = True
                            player["Decks"][d]["Cards"] = cards
                            print(f"Cards in Deck {deck_name} was overwritten.")
                            return

                    print(deck_found)

                    if not deck_found:
                        add_deck = {
                            "Name": deck_name,
                            "Cards": cards
                        }
                        player["Decks"].append(add_deck)

                    player_data["Players"][p] = player
                    write_json(player_data, player_file)

                    print(f"Deck {deck_name} was saved successfully.")
                    return
            
        else:
            print("No deck name entered, Deck not saved.")
            return
    else:
        print("Deck not saved.")
        return
    