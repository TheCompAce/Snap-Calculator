import json
from modules.utils import print_card_data_from_name, read_player_json, get_cards_from_base, save_player_to_players, autocomplete_card_name
from modules.snap_base import base_file

def collection_menu(player_name, player_file):
    while True:
        players = read_player_json(player_file)
        player_found = False
        cards = []
        for player in players["Players"]:
            if player["Name"] == player_name:
                player_found = True
                cards = player["Collected"]
                break
            
        if player_found:
            print("----- Collection List -----")

            for i, card in enumerate(cards):
                print(f"{i + 1}. {card}")
            print("---------------------------")
            print(f"{len(cards) + 1}. Add Card")
            print(f"{len(cards) + 2}. Delete Card")
            print(f"{len(cards) + 3}. Back")
            
            choice = input("Enter your choice: ").strip()
            
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(cards):
                    card = cards[i -1]
                    show_card(card)
                elif choice == len(cards) + 1:
                    add_card(player_name, player_file)
                elif choice == len(cards) + 2:
                    delete_card(player_name, player_file)
                elif choice == len(cards) + 3:
                    break  # Go back to the edit_player_menu
                else:
                    print("Invalid choice. Please try again.")
            else:
                selected_card = autocomplete_card_name(base_file, choice)
                if selected_card in [card for card in cards]:
                    show_card(selected_card)
                else:
                    add_new = input(f"Card '{selected_card}' not found. Would you like to add this card? (y/n): ").strip().lower()
                    if add_new == 'y':
                        add_card(player_name, player_file, selected_card)
        else:
            print("Player not found!")
            break

def show_card(card):
    print_card_data_from_name(card, base_file)

# Add a new card to the collection
def add_card(player_name, player_file, card_name = None):
    if not card_name:
        card_name = autocomplete_card_name(base_file, input("Enter the name of the card you want to add: ").strip())
    
    player_file = player_file
    players = read_player_json(player_file)
    cards = get_cards_from_base(base_file)

    player_found = False
    for player in players["Players"]:
        if player["Name"] == player_name:
            player_found = True

            if card_name in player["Collected"]:
                print(f"You already have the card {card_name}.")
            elif card_name not in cards:
                print(f"{card_name} is not a valid game card.")
            else:
                player["Collected"].append(card_name)
                save_player_to_players(player, player_file)
                print(f"Card {card_name} added to your collection!")
            break
                
    if not player_found:
        print("Player not found!")


# Delete a specific card from the collection and save to players.json
def delete_card(player_name, player_file):
    # Read existing players from players.json
    players = read_player_json(player_file)
    
    player_found = False
    for player in players["Players"]:
        if player["Name"] == player_name:
            player_found = True
            card = autocomplete_card_name(base_file, input("Enter the Card's name :"))
            if card in player["Collected"]:
                confirm = input(f"Are you sure you want to delete {card}? (y/n): ").strip().lower()
                if confirm == 'y':
                    # Remove the card from the collection
                    player["Collected"].remove(card)
                    
                    # Save the updated collection back to players.json
                    save_player_to_players(player, player_file)
                    
                    print(f"Card {card} deleted from your collection!")
                else:
                    print(f"Card {card} was not saved to your collection!")
            else:
                print(f"Card {card} not found in your collection.")
            break
            
    if not player_found:
        print("Player not found!")

