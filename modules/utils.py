from datetime import datetime
import json
import os


def check_and_create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return f"Folder '{folder_path}' has been created."
    else:
        return f"Folder '{folder_path}' already exists."
    
def read_player_json(file_path):
    try:
        if os.path.exists(file_path):
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        else:
            return {
                "Players" : []
            }
    except Exception as e:
        return {"error": str(e)}
    
def read_json(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        return {"error": str(e)}
    
def autocomplete_player_name(player_file, partial_name):
    matching_players = []
    players_base = read_player_json(player_file)
    players = players_base["Players"]
    
    # Filter matching players based on partial_name
    matching_players = [player['Name'] for player in players if player['Name'].lower().startswith(partial_name.lower())]
    
    return autocomplete_generic(matching_players, partial_name)
    
def autocomplete_card_name(base_file, partial_name):
    matching_cards = []
    base_data = read_json(base_file)
    for series in base_data.get('Cards', []):
        for series_name, cards in series.items():
            matching_cards.extend([card['Card'] for card in cards if card['Card'].lower().startswith(partial_name.lower())])
            
    return autocomplete_generic(matching_cards, partial_name)

def autocomplete_location_name(base_file, partial_name):
    matching_locations = []
    base_data = read_json(base_file)
    location_data = base_data.get('Locations', [])
    
    matching_locations = [loc['Location'] for loc in location_data if loc['Location'].lower().startswith(partial_name.lower())]

    return autocomplete_generic(matching_locations, partial_name)

def autocomplete_deck_name(decks, partial_name):
    matching_decks = []

    for deck in decks:
        matching_decks.append(deck["Name"])

    return autocomplete_generic(matching_decks, partial_name)


def autocomplete_generic(list_data, partial_name):
    if len(list_data) > 1:
        print('Multiple matches found. Please select one:')
        for i, loc in enumerate(list_data):
            print(f'{i + 1}. {loc}')
        selection = int(input('Enter your choice: ')) - 1
        return list_data[selection]
    elif list_data:
        return list_data[0]
    else:
        return partial_name

def get_cards_from_base(base_file):
    base_data = read_json(base_file)

    send_cards = []

    for series in base_data.get('Cards', []):
        for series_name, cards in series.items():
            for card in cards:
                send_cards.append(card['Card'])

    return send_cards

def save_player_to_players(player, player_file):
    players = read_player_json(player_file)

    players_list = players["Players"]

    set_players = []
    for check_player in players_list:
        if check_player["Id"] == player["Id"]:
            player["UpdatedTime"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            set_players.append(player)
            pass
        else:
            set_players.append(check_player)

    players["Players"] = set_players
    with open(player_file, "w") as f:
        json.dump(players, f)

def print_card_data_from_name(card_name, base_file):
    base_data = read_json(base_file)

    card_found = False
    for series in base_data.get('Cards', []):
        for series_name, cards in series.items():
            for card in cards:
                if card["Card"] == card_name:
                    card_found = True
                    print("---- Card Infromation ----")
                    print(f"Card Name : {card['Card']}")
                    print(f"Cost : {card['Cost']}")
                    print(f"Power : {card['Power']}")
                    print(f"Card Ability : {card['Card Ability']}")
                    print("--------------------------")
                    break
                
            if card_found:
                break
        if card_found:
                break
        
def get_cards_from_names(card_names, file_path):
    base_data = read_json(file_path)
    ret_Cards = []
    for c, card_name in enumerate(card_names):
        card_found = False
        for series in base_data.get('Cards', []):
            for series_name, cards in series.items():
                for card in cards:
                    if card["Card"] == card_name:
                        card_found = True
                        ret_Cards.append(card)
                        break

                if card_found:
                    break
            if card_found:
                    break
    return ret_Cards

def ask_for_player(player_file):
    """
    Ask the user to select a player from the available options.
    Returns the player_id of the selected player.
    """
    # Display available players and ask for selection
    while True:
        print("----- Player List -----")
        ct, players = list_players(player_file)  # Assume list_players is a function that returns count and list of players
        
        print("------------------------------")
        print(f"{ct + 1}. Back")
        
        choice = input("Enter your choice: ").strip()
        
        if choice.isdigit():
            choice = int(choice)
            if choice - 1 < ct:
                return players[choice - 1]
            elif choice == ct + 1:
                break  # Go back to the main menu
            else:
                return None
        else:
            selected_player = autocomplete_player_name(player_file, choice)
            for player in players:
                if player['Name'] == selected_player:
                    return player
            else:
                return None

def ask_for_decks(player_file, player_name):
    """
    Ask the user to select a deck from the available decks for the player.
    Returns the player_id of the selected player.
    """
    decks = None
    player_data = read_json(player_file)
    for player in player_data["Players"]:
        if player["Name"] == player_name:
            decks = player["Decks"]
            break

    if decks:
        while True:
            print(f"----- Player {player_name}'s Deck List -----")
            decks = list_decks(decks)
            ct = len(decks)

            print("------------------------------")
            print(f"{ct + 1}. Back")
        
            choice = input("Enter your choice: ").strip()
            if choice.isdigit():
                choice = int(choice)
                if choice - 1 < ct:
                    return decks[choice - 1]["Cards"]
                elif choice == ct + 1:
                    break  # Go back to the main menu
                else:
                    return None
            else:
                selected_deck = autocomplete_deck_name(decks, choice)
                for deck in decks:
                    if deck['Name'] == selected_deck:
                        return decks[choice - 1]["Cards"]
                else:
                    print("Invalid Deck.")
                    return None
    else:
        print("Invalid Player.")
        return None

def list_players(player_file):
    players_base = read_player_json(player_file)
    players = players_base["Players"]
    ct = len(players)
    for i, player in enumerate(players):
        print(f"{str(i + 1)}. {player['Name']}")

    return ct, players

def list_decks(decks):
    for i, deck in enumerate(decks):
        print(f"{str(i + 1)}. {deck['Name']}")

    return decks

def get_player_by_index(player_file, player_id):
    # Read existing players from players.json
    players = read_player_json(player_file)

    for i, player in enumerate(players["Players"]):
        if i == player_id - 1:
            return player["Name"]
    
    return None

def get_player_by_name(player_file, player_name):
    # Read existing players from players.json
    players = read_player_json(player_file)

    for i, player in enumerate(players["Players"]):
        if player["Name"] == player_name - 1:
            return player
    
    return None