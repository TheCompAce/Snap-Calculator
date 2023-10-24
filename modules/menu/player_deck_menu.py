import json
import os
from modules.menu.player_deck_cards_menu import edit_deck_cards_menu
from modules.utils import autocomplete_deck_name, read_player_json

def deck_menu(player_name, player_file):

    while True:
        players = read_player_json(player_file)
        player_found = False
        decks = []
        for player in players["Players"]:
            if player["Name"] == player_name:
                player_found = True
                decks = player["Decks"]
                break
            
        if player_found:  
            print("----- Player Decks -----")
            list_decks(decks)  # Assume list_players is a function that returns count and list of players
            
            ct = len(decks)
            print("------------------------------")
            print(f"{ct + 1}. Add New Decks")
            print(f"{ct + 2}. Delete Decks")
            print(f"{ct + 3}. Back")
            
            choice = input("Enter your choice: ").strip()
            
            if choice.isdigit():
                choice = int(choice)
                if choice - 1 < ct:
                    edit_deck(player_file, player_name, decks[choice - 1]["Name"])
                elif choice == ct + 1:
                    add_new_deck(player_file, player_name) # Add Player
                elif choice == ct + 2:
                    delete_deck(player_file, player_name) # Delete Player
                elif choice == ct + 3:
                    break  # Go back to the main menu
                else:
                    print("Invalid choice.")
            else:
                selected_deck = autocomplete_deck_name(decks, choice)
                if selected_deck in [deck['Name'] for deck in decks]:
                    edit_deck(player_file, player_name, selected_deck)
                else:
                    add_new = input(f"Deck '{selected_deck}' not found. Would you like to add this player? (y/n): ").strip().lower()
                    if add_new == 'y':
                        add_new_deck(player_file, player_name, selected_deck)
        else:
            print("Invalid Player.")

def list_decks(decks):
    for i, deck in enumerate(decks):
        print(f"{str(i + 1)}. {deck['Name']}")

def add_new_deck(player_file, player_name, deck_name = None):
    if not deck_name:
        deck_name = input("What is the deck's name?")

    new_deck = {
        "Name": deck_name,
        "Cards": []
    }

    # Read existing players from players.json
    players = read_player_json(player_file)

    player_found = False
    for i, player in enumerate(players["Players"]):
        if player["Name"] == player_name:
            player_found = True
            # Add new player to players list
            player["Decks"].append(new_deck)
            players["Players"][i] = player

            # Update players.json with the new player
            with open(player_file, "w") as f:
                json.dump(players, f)

            print(f"New player {new_deck['Name']} added successfully!")

            edit_deck(player_file, player_name, deck_name)
            break

    if not player_found:
        print("Invalid Player.")

def delete_deck(player_file, player_name):
    # Read existing players from players.json
    players = read_player_json(player_file)

    player_found = False
    for i, player in enumerate(players["Players"]):
        if player["Name"] == player_name:
            player_found = True
    
            # Display existing players for selection
            for j, deck in enumerate(player["Decks"]):
                print(f"{j + 1}. {deck['Name']}")

            choice = input("Select the deck to delete: ")
            if choice.isdigit():
                choice = int(choice)
                
                # Validate the choice
                if 0 < choice <= len(player["Decks"]):
                    selected_deck = player["Decks"][choice - 1]
                    confirm = input(f"Are you sure you want to delete {selected_deck['Name']}? (y/n): ").strip().lower()
                    
                    if confirm == 'y':
                        # Remove the selected player
                        deleted_deck = player["Decks"].pop(choice - 1)

                        players["Players"][i] = player
                        
                        # Update players.json with the removed player
                        with open(player_file, "w") as f:
                            json.dump(players, f)
                            
                        print(f"Deck {deleted_deck['Name']} deleted successfully!")
                        break
                    else:
                        print("Deletion cancelled.")
                        break
                else:
                    print("Invalid choice. No deck deleted.")
                    break
            else:
                print("Invalid choice. No deck deleted.")
                break

    if not player_found:
        print("Invalid Player.")

def edit_deck(player_file, player_name, deck_name):
    new_name = input("Enter a new name for the deck (leave blank to keep the current name): ").strip()
    
    if new_name:
        # Read existing players from players.json
        players = read_player_json(player_file)
        
        # Find and update the player name
        for i, player in enumerate(players["Players"]):
            if player["Name"] == player_name:
                for j, deck in enumerate(player["Decks"]):
                    if deck["Name"] == deck_name:
                        deck["Name"] = new_name
                        players["Players"][i]["Decks"][j] = deck
                        break

                break
        
        # Update players.json with the new name
        with open(player_file, "w") as f:
            json.dump(players, f)
            
        print(f"Deck name updated to {new_name}.")
        edit_deck_cards_menu(player_file, player_name, new_name)
    else:
        print("Deck name remains unchanged.")
        edit_deck_cards_menu(player_file, player_name, deck_name)
