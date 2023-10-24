from modules.menu.player_collection_menu import collection_menu
from modules.menu.player_deck_menu import deck_menu
def edit_player_menu(player_name, player_file):
    while True:
        print(f"----- Edit Player {player_name} -----")
        print("1. Edit Collection")
        print("2. Edit Decks")
        print("3. Back")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            # Call function to edit collection (to be implemented)
            collection_menu(player_name, player_file)
        elif choice == '2':
            # Call function to edit decks (to be implemented)
            deck_menu(player_name, player_file)
        elif choice == '3':
            break  # Go back to the previous menu
        else:
            print("Invalid choice. Please try again.")
