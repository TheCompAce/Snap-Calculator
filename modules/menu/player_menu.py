import json
import os
import uuid
from modules.menu.player_edit_menu import edit_player_menu
from modules.utils import check_and_create_folder, get_player_by_index, list_players, read_player_json, autocomplete_player_name
player_file = "player/players.json"

def player_setup_menu():
    check_and_create_folder("player")
    while True:
        print("----- Player List -----")
        ct, players = list_players(player_file)  # Assume list_players is a function that returns count and list of players
        
        print("------------------------------")
        print(f"{ct + 1}. Add New Player")
        print(f"{ct + 2}. Delete Player")
        print(f"{ct + 3}. Back")
        
        choice = input("Enter your choice: ").strip()
        
        if choice.isdigit():
            choice = int(choice)
            if choice - 1 < ct:
                edit_player(get_player_by_index(player_file, choice))
            elif choice == ct + 1:
                add_new_player() # Add Player
            elif choice == ct + 2:
                delete_player() # Delete Player
            elif choice == ct + 3:
                break  # Go back to the main menu
            else:
                print("Invalid choice.")
        else:
            selected_player = autocomplete_player_name(player_file, choice)
            if selected_player in [player['Name'] for player in players]:
                edit_player(selected_player)
            else:
                add_new = input(f"Player '{selected_player}' not found. Would you like to add this player? (y/n): ").strip().lower()
                if add_new == 'y':
                    add_new_player(selected_player)


def add_new_player(player_name = None):
    if not player_name:
        player_name = input("What is the player's name?")

    unique_id = str(uuid.uuid4())

    new_player = {
        "Id": unique_id,
        "Name": player_name,
        "Collected": [],
        "Decks": []
    }

    # Read existing players from players.json
    players = read_player_json(player_file)

    # Add new player to players list
    players["Players"].append(new_player)

    # Update players.json with the new player
    with open(player_file, "w") as f:
        json.dump(players, f)

    print(f"New player {new_player['Name']} added successfully!")

    edit_player(player_name)

def delete_player():
    # Read existing players from players.json
    players = read_player_json(player_file)
    
    # Display existing players for selection
    for i, player in enumerate(players["Players"]):
        print(f"{i + 1}. {player['Name']}")

    choice = input("Select the player to delete: ")
    if choice.isdigit():
        choice = int(choice)
        
        # Validate the choice
        if 0 < choice <= len(players["Players"]):
            selected_player = players["Players"][choice - 1]
            confirm = input(f"Are you sure you want to delete {selected_player['Name']}? (y/n): ").strip().lower()
            
            if confirm == 'y':
                # Remove the selected player
                deleted_player = players["Players"].pop(choice - 1)
                
                # Update players.json with the removed player
                with open(player_file, "w") as f:
                    json.dump(players, f)
                    
                print(f"Player {deleted_player['Name']} deleted successfully!")
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid choice. No player deleted.")
    else:
        print("Invalid choice. No player deleted.")


def edit_player(player_name):
    new_name = input("Enter a new name for the player (leave blank to keep the current name): ").strip()
    
    if new_name:
        # Read existing players from players.json
        players = read_player_json(player_file)
        
        # Find and update the player name
        for player in players["Players"]:
            if player["Name"] == player_name:
                player["Name"] = new_name
                break
        
        # Update players.json with the new name
        with open(player_file, "w") as f:
            json.dump(players, f)
            
        print(f"Player name updated to {new_name}.")
        edit_player_menu(new_name, player_file)
    else:
        print("Player name remains unchanged.")
        edit_player_menu(player_name, player_file)


