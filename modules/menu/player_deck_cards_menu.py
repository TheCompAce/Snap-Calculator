import json
from modules.utils import autocomplete_generic, print_card_data_from_name, read_player_json, get_cards_from_base, save_player_to_players, autocomplete_card_name
from modules.snap_base import base_file

def edit_deck_cards_menu(player_file, player_name, deck_name):
    run_loop = True
    while run_loop:
        players = read_player_json(player_file)
        player_found = False
        decks = []
        for player in players["Players"]:
            if player["Name"] == player_name:
                player_found = True
                decks = player["Decks"]
                break
            
        if player_found:
            for deck in decks:
                if deck["Name"] == deck_name:
                    cards = deck["Cards"]

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
                            add_card(player_name, player_file, deck_name)
                        elif choice == len(cards) + 2:
                            delete_card(player_name, player_file, deck_name)
                        elif choice == len(cards) + 3:
                            run_loop = False
                        else:
                            print("Invalid choice. Please try again.")
                    else:
                        selected_card = autocomplete_generic(cards, choice)
                        if selected_card in [card for card in cards]:
                            show_card(selected_card)
                        else:
                            add_new = input(f"Card '{selected_card}' not found. Would you like to add this card? (y/n): ").strip().lower()
                            if add_new == 'y':
                                add_card(player_name, player_file, deck_name, selected_card)
                else:
                    print("Deck not found!")
                    run_loop = False
        else:
            print("Player not found!")
            run_loop = False

def show_card(card):
    print_card_data_from_name(card, base_file)

# Add a new card to the deck
def add_card(player_name, player_file, deck_name, card_name = None):
    if not card_name:
        card_name = autocomplete_card_name(base_file, input("Enter the name of the card you want to add: ").strip())
    
    player_file = player_file
    players = read_player_json(player_file)
    cards = get_cards_from_base(base_file)

    player_found = False
    for i, player in enumerate(players["Players"]):
        if player["Name"] == player_name:
            player_found = True
            deck_found = False
            for d, deck in enumerate(player["Decks"]):
                if deck["Name"] == deck_name:
                    deck_found = True

                    if card_name in deck:
                        print(f"You already have the card {card_name}.")
                    elif card_name not in cards:
                        print(f"{card_name} is not a valid game card.")
                    else:
                        player["Decks"][d]["Cards"].append(card_name)
                        save_player_to_players(player, player_file)
                        print(f"Card {card_name} added to your collection!")
                    break

            if not deck_found:
                print("Deck not found!")
                
    if not player_found:
        print("Player not found!")


# Delete a specific card from the collection and save to players.json
def delete_card(player_name, player_file, deck_name):
    # Read existing players from players.json
    players = read_player_json(player_file)
    
    player_found = False
    for p, player in enumerate(players["Players"]):
        if player["Name"] == player_name:
            player_found = True
            for d, deck in enumerate(player["Decks"]):
                if deck["Name"] == deck_name:
                    card = autocomplete_deck_cards_name(deck["Cards"], input("Enter the Card's name :"))
                    if card in deck["Cards"]:
                        confirm = input(f"Are you sure you want to delete {card}? (y/n): ").strip().lower()
                        if confirm == 'y':
                            # Remove the card from the collection
                            deck["Cards"].remove(card)

                            players["Players"][p]["Decks"][d] = deck
                            
                            # Save the updated collection back to players.json
                            save_player_to_players(player, player_file)
                            
                            print(f"Card {card} deleted from your collection!")
                        else:
                            print(f"Card {card} was not saved to your collection!")
                    else:
                        print(f"Card {card} not found in your collection.")
                    break
            if not player_found:
                print("Deck not found!")
            
    if not player_found:
        print("Player not found!")

def autocomplete_deck_cards_name(cards, partial_name):
    matching_cards = []

    for card in cards:
        if card.lower().startswith(partial_name.lower()):
            matching_cards.append(card)

    return autocomplete_generic(matching_cards, partial_name)
    pass