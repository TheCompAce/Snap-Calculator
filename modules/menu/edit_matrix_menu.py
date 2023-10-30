import json


def edit_matrix_menu():
    while True:
        print("==== Edit Matrix Menu ====")
        print("1. Edit Location Matrix")
        print("2. Edit Card Matrix")
        print("3. Edit Location To Card Matrix")
        print("4. Edit Card To Card Link Matrix")
        print("5. Back")

        choice = input("Please enter your choice: ")

        if choice == '1':
            # Call the function to edit the Location Matrix
            edit_location_matrix_menu()
        elif choice == '2':
            # Call the function to edit the Card Matrix
            edit_card_matrix_menu()
        elif choice == '3':
            # Call the function to edit the Location To Card Matrix
            edit_location_to_card_matrix_menu()
        elif choice == '4':
            # Call the function to edit the Card To Card Link Matrix
            edit_card_to_card_link_matrix_menu()
        elif choice == '5':
            # Return to the main menu
            break
        else:
            print("Invalid choice. Please try again.")

def edit_location_matrix_menu():
    while True:
        print("==== Edit Location Matrix Menu ====")
        print("1. View Matrix")
        print("2. Add Item")
        print("3. Edit Item")
        print("4. Remove Item")
        print("5. Back")

        choice = input("Please enter your choice: ")

        if choice == '1':
            # Call the function to view the Location Matrix
            view_location_matrix()
        elif choice == '2':
            # Call the function to add an item to the Location Matrix
            add_item_to_location_matrix()
        elif choice == '3':
            # Call the function to edit an item in the Location Matrix
            edit_item_to_location_matrix()
        elif choice == '4':
            # Call the function to remove an item from the Location Matrix
            remove_item_from_location_matrix()
        elif choice == '5':
            # Return to the Edit Matrix menu
            break
        else:
            print("Invalid choice. Please try again.")

def view_location_matrix():
    # Read the existing data from system/matrix/location_matrix.json
    with open('system/matrix/location_matrix.json', 'r') as f:
        location_matrix = json.load(f)

    print("==== View Location Matrix ====")
    for item in location_matrix:
        print(f"Effect: {item['Effect']}, Pattern: {item['Pattern']}, Score: {item['Score']}")


def add_item_to_location_matrix():
    # Read the existing data from system/matrix/location_matrix.json
    with open('system/matrix/location_matrix.json', 'r') as f:
        location_matrix = json.load(f)

    # Ask for Effect id, Pattern, and Score
    effect_id = input("Enter the Effect id: ")
    
    # Check if Effect id already exists in the list of dictionaries
    if any(item['Effect'] == effect_id for item in location_matrix):
        print("Error: Effect id already exists.")
        return

    pattern = input("Enter the Pattern regEx: ")
    score = int(input("Enter the Score: "))  # Assuming score is an integer

    # Add the new entry to the location_matrix list
    new_entry = {"Effect": effect_id, "Pattern": pattern, "Score": score}
    location_matrix.append(new_entry)

    # Write the updated data back to system/matrix/location_matrix.json
    with open('system/matrix/location_matrix.json', 'w') as f:
        json.dump(location_matrix, f, indent=4)

    print(f"Successfully added {effect_id} to the Location Matrix.")

# Helper function to display a numerical list of items and return the selected Effect id
def select_effect_id_from_list():
    # Read the existing data from system/matrix/location_matrix.json
    with open('system/matrix/location_matrix.json', 'r') as f:
        location_matrix = json.load(f)

    print("==== Select an Effect id ====")
    for i, item in enumerate(location_matrix):
        print(f"{i+1}. Effect: {item['Effect']}, Pattern: {item['Pattern']}, Score: {item['Score']}")

    choice = int(input("Enter the number of the item you want to select: "))
    return location_matrix[choice-1]['Effect']

# Function to edit an item in the Location Matrix
def edit_item_to_location_matrix():
    # Get the Effect id to edit
    effect_id = select_effect_id_from_list()

    # Read the existing data from system/matrix/location_matrix.json
    with open('system/matrix/location_matrix.json', 'r') as f:
        location_matrix = json.load(f)

    # Find the item to edit
    item_to_edit = next(item for item in location_matrix if item['Effect'] == effect_id)

    # Ask for new Effect, Pattern, and Score (if left blank, use current value)
    new_effect = input(f"Enter the new Effect id (current: {item_to_edit['Effect']}): ") or item_to_edit['Effect']
    new_pattern = input(f"Enter the new Pattern (current: {item_to_edit['Pattern']}): ") or item_to_edit['Pattern']
    new_score = input(f"Enter the new Score (current: {item_to_edit['Score']}): ") or item_to_edit['Score']

    # Update the item
    item_to_edit['Effect'] = new_effect
    item_to_edit['Pattern'] = new_pattern
    item_to_edit['Score'] = int(new_score)  # Assuming score is an integer

    # Write the updated data back to system/matrix/location_matrix.json
    with open('system/matrix/location_matrix.json', 'w') as f:
        json.dump(location_matrix, f, indent=4)

    print(f"Successfully edited {new_effect} in the Location Matrix.")

# Function to remove an item from the Location Matrix
def remove_item_from_location_matrix():
    # Get the Effect id to remove
    effect_id = select_effect_id_from_list()

    # Read the existing data from system/matrix/location_matrix.json
    with open('system/matrix/location_matrix.json', 'r') as f:
        location_matrix = json.load(f)

    # Remove the item with the selected Effect id
    location_matrix = [item for item in location_matrix if item['Effect'] != effect_id]

    # Write the updated data back to system/matrix/location_matrix.json
    with open('system/matrix/location_matrix.json', 'w') as f:
        json.dump(location_matrix, f, indent=4)

    print(f"Successfully removed {effect_id} from the Location Matrix.")

# Function to display the Card Matrix Menu
def edit_card_matrix_menu():
    while True:
        print("==== Edit Card Matrix Menu ====")
        print("1. View Matrix")
        print("2. Add Item")
        print("3. Edit Item")
        print("4. Remove Item")
        print("5. Back")

        choice = input("Please enter your choice: ")

        if choice == '1':
            view_card_matrix()
        elif choice == '2':
            add_item_to_card_matrix()
        elif choice == '3':
            edit_item_to_card_matrix()
        elif choice == '4':
            remove_item_from_card_matrix()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

# Helper function to select an Effect id from the list
def select_effect_id_from_list_card():
    with open('system/matrix/card_matrix.json', 'r') as f:
        card_matrix = json.load(f)
    for i, item in enumerate(card_matrix):
        print(f"{i+1}. Effect: {item['Effect']}, Pattern: {item['Pattern']}, Score: {item['Score']}")
    choice = int(input("Select the item number to edit: "))
    return card_matrix[choice-1]['Effect']

# Function to view the Card Matrix
def view_card_matrix():
    with open('system/matrix/card_matrix.json', 'r') as f:
        card_matrix = json.load(f)
    print("==== View Card Matrix ====")
    for item in card_matrix:
        print(f"Effect: {item['Effect']}, Pattern: {item['Pattern']}, Score: {item['Score']}")

# Function to add an item to the Card Matrix
def add_item_to_card_matrix():
    with open('system/matrix/card_matrix.json', 'r') as f:
        card_matrix = json.load(f)
    effect_id = input("Enter the Effect id: ")
    if any(item['Effect'] == effect_id for item in card_matrix):
        print("Error: Effect id already exists.")
        return
    pattern = input("Enter the Pattern regEx: ")
    score = int(input("Enter the Score: "))
    new_entry = {"Effect": effect_id, "Pattern": pattern, "Score": score}
    card_matrix.append(new_entry)
    with open('system/matrix/card_matrix.json', 'w') as f:
        json.dump(card_matrix, f, indent=4)
    print(f"Successfully added {effect_id} to the Card Matrix.")

# Function to edit an item in the Card Matrix
def edit_item_to_card_matrix():
    effect_id = select_effect_id_from_list_card()
    with open('system/matrix/card_matrix.json', 'r') as f:
        card_matrix = json.load(f)
    item_to_edit = next(item for item in card_matrix if item['Effect'] == effect_id)
    new_effect = input(f"Enter the new Effect id (current: {item_to_edit['Effect']}): ") or item_to_edit['Effect']
    new_pattern = input(f"Enter the new Pattern (current: {item_to_edit['Pattern']}): ") or item_to_edit['Pattern']
    new_score = input(f"Enter the new Score (current: {item_to_edit['Score']}): ") or item_to_edit['Score']
    item_to_edit['Effect'] = new_effect
    item_to_edit['Pattern'] = new_pattern
    item_to_edit['Score'] = int(new_score)
    with open('system/matrix/card_matrix.json', 'w') as f:
        json.dump(card_matrix, f, indent=4)
    print(f"Successfully edited {new_effect} in the Card Matrix.")

# Function to remove an item from the Card Matrix
def remove_item_from_card_matrix():
    effect_id = select_effect_id_from_list_card()
    with open('system/matrix/card_matrix.json', 'r') as f:
        card_matrix = json.load(f)
    card_matrix = [item for item in card_matrix if item['Effect'] != effect_id]
    with open('system/matrix/card_matrix.json', 'w') as f:
        json.dump(card_matrix, f, indent=4)
    print(f"Successfully removed {effect_id} from the Card Matrix.")

import json

def edit_location_to_card_matrix_menu():
    while True:
        print("==== Edit Location To Card Matrix Menu ====")
        print("1. View Matrix")
        print("2. Add Item")
        print("3. Edit Item")
        print("4. Remove Item")
        print("5. Back")
        
        choice = input("Please enter your choice: ")
        
        if choice == '1':
            view_location_to_card_matrix()
        elif choice == '2':
            add_item_to_location_to_card_matrix()
        elif choice == '3':
            edit_item_to_location_to_card_matrix()
        elif choice == '4':
            remove_item_from_location_to_card_matrix()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def select_context_id_from_list(context_type, json_file_path):
    with open(json_file_path, 'r') as f:
        matrix = json.load(f)
    print(f"==== Select {context_type} Context ID ====")
    for i, item in enumerate(matrix):
        print(f"{i + 1}. {item['Effect']}")
    choice = int(input("Select the Context ID: "))
    return matrix[choice - 1]['Effect']

# Function to view the Location To Card Matrix
def view_location_to_card_matrix():
    with open('system/matrix/link_matrix.json', 'r') as f:
        link_matrix = json.load(f)
    print("==== View Location To Card Matrix ====")
    for item in link_matrix:
        print(f"LocationContextID: {item['LocationContextID']}, CardContextID: {item['CardContextID']}, Score: {item['Score']}")

# Function to add an item to the Location To Card Matrix
def add_item_to_location_to_card_matrix():
    location_context_id = select_context_id_from_list("Location", 'system/matrix/location_matrix.json')
    card_context_id = select_context_id_from_list("Card", 'system/matrix/card_matrix.json')
    score = int(input("Enter the Score: "))

    new_entry = {"LocationContextID": location_context_id, "CardContextID": card_context_id, "Score": score}
    
    with open('system/matrix/link_matrix.json', 'r') as f:
        link_matrix = json.load(f)
    link_matrix.append(new_entry)
    
    with open('system/matrix/link_matrix.json', 'w') as f:
        json.dump(link_matrix, f, indent=4)
    print(f"Successfully added the new link to the Location To Card Matrix.")

# Function to edit an item in the Location To Card Matrix
def edit_item_to_location_to_card_matrix():
    with open('system/matrix/link_matrix.json', 'r') as f:
        link_matrix = json.load(f)
    
    print("==== Edit Item in Location To Card Matrix ====")
    for i, item in enumerate(link_matrix):
        print(f"{i + 1}. LocationContextID: {item['LocationContextID']}, CardContextID: {item['CardContextID']}, Score: {item['Score']}")
    
    choice = int(input("Select the item to edit: ")) - 1
    selected_item = link_matrix[choice]

    # Edit values
    print(f"Current LocationContextID: {selected_item['LocationContextID']}")
    new_location_context_id = input("Enter the new LocationContextID (leave blank to keep current): ")
    if new_location_context_id == "":
        new_location_context_id = selected_item['LocationContextID']
    else:
        # Validate new_location_context_id with existing LocationContextIDs in location_matrix.json
        new_location_context_id = select_context_id_from_list("Location", 'system/matrix/location_matrix.json')

    print(f"Current CardContextID: {selected_item['CardContextID']}")
    new_card_context_id = input("Enter the new CardContextID (leave blank to keep current): ")
    if new_card_context_id == "":
        new_card_context_id = selected_item['CardContextID']
    else:
        # Validate new_card_context_id with existing CardContextIDs in card_matrix.json
        new_card_context_id = select_context_id_from_list("Card", 'system/matrix/card_matrix.json')

    print(f"Current Score: {selected_item['Score']}")
    new_score = input("Enter the new Score (leave blank to keep current): ")
    if new_score == "":
        new_score = selected_item['Score']
    else:
        new_score = int(new_score)

    # Update the selected item
    selected_item['LocationContextID'] = new_location_context_id
    selected_item['CardContextID'] = new_card_context_id
    selected_item['Score'] = new_score

    # Write the updated data back to link_matrix.json
    with open('system/matrix/link_matrix.json', 'w') as f:
        json.dump(link_matrix, f, indent=4)
    print("Successfully edited the selected item.")

# Function to remove an item from the Location To Card Matrix
def remove_item_from_location_to_card_matrix():
    with open('system/matrix/link_matrix.json', 'r') as f:
        link_matrix = json.load(f)
    
    print("==== Remove Item from Location To Card Matrix ====")
    for i, item in enumerate(link_matrix):
        print(f"{i + 1}. LocationContextID: {item['LocationContextID']}, CardContextID: {item['CardContextID']}, Score: {item['Score']}")
    
    choice = int(input("Select the item to remove: ")) - 1
    removed_item = link_matrix.pop(choice)
    
    # Write the updated data back to link_matrix.json
    with open('system/matrix/link_matrix.json', 'w') as f:
        json.dump(link_matrix, f, indent=4)
    print(f"Successfully removed {removed_item['LocationContextID']} - {removed_item['CardContextID']} from the Location To Card Matrix.")

# Function to display the Edit Card To Card Link Matrix Menu
def edit_card_to_card_link_matrix_menu():
    while True:
        print("==== Edit Card To Card Link Matrix Menu ====")
        print("1. View Matrix")
        print("2. Add Item")
        print("3. Edit Item")
        print("4. Remove Item")
        print("5. Back")

        choice = input("Please enter your choice: ")

        if choice == '1':
            # Function to view the Card To Card Link Matrix
            view_card_to_card_link_matrix()
        elif choice == '2':
            # Function to add an item to the Card To Card Link Matrix
            add_item_to_card_to_card_link_matrix()
        elif choice == '3':
            # Function to edit an item in the Card To Card Link Matrix
            edit_item_to_card_to_card_link_matrix()
        elif choice == '4':
            # Function to remove an item from the Card To Card Link Matrix
            remove_item_from_card_to_card_link_matrix()
        elif choice == '5':
            # Return to the Edit Matrix menu
            break
        else:
            print("Invalid choice. Please try again.")

# Function to view the Card To Card Link Matrix
def view_card_to_card_link_matrix():
    with open('system/matrix/link_card_matrix.json', 'r') as f:
        link_card_matrix = json.load(f)
    
    print("==== View Card To Card Link Matrix ====")
    for item in link_card_matrix:
        print(f"BaseContextID: {item['BaseContextID']}, CheckContextID: {item['CheckContextID']}, Score: {item['Score']}")

# Function to add an item to the Card To Card Link Matrix
def add_item_to_card_to_card_link_matrix():
    base_id = select_context_id_from_list("Card", 'system/matrix/card_matrix.json')
    check_id = select_context_id_from_list("Card", 'system/matrix/card_matrix.json')
    score = int(input("Enter the Score: "))
    new_entry = {"BaseContextID": base_id, "CheckContextID": check_id, "Score": score}
    
    with open('system/matrix/link_card_matrix.json', 'r+') as f:
        data = json.load(f)
        data.append(new_entry)
        f.seek(0)
        json.dump(data, f, indent=4)

# Function to edit an item in the Card To Card Link Matrix
def edit_item_to_card_to_card_link_matrix():
    with open('system/matrix/link_card_matrix.json', 'r+') as f:
        data = json.load(f)
        
    for idx, item in enumerate(data):
        print(f"{idx + 1}. BaseContextID: {item['BaseContextID']}, CheckContextID: {item['CheckContextID']}, Score: {item['Score']}")
    
    choice = int(input("Select an item to edit: ")) - 1
    selected_item = data[choice]
    
    new_base_id = input(f"Enter new BaseContextID (current: {selected_item['BaseContextID']}): ")
    new_check_id = input(f"Enter new CheckContextID (current: {selected_item['CheckContextID']}): ")
    new_score = input(f"Enter new Score (current: {selected_item['Score']}): ")
    
    if new_base_id:
        selected_item['BaseContextID'] = new_base_id
    if new_check_id:
        selected_item['CheckContextID'] = new_check_id
    if new_score:
        selected_item['Score'] = int(new_score)
        
    data[choice] = selected_item
    
    with open('system/matrix/link_card_matrix.json', 'w') as f:
        json.dump(data, f, indent=4)

# Function to remove an item from the Card To Card Link Matrix
def remove_item_from_card_to_card_link_matrix():
    with open('system/matrix/link_card_matrix.json', 'r+') as f:
        data = json.load(f)
        
    for idx, item in enumerate(data):
        print(f"{idx + 1}. BaseContextID: {item['BaseContextID']}, CheckContextID: {item['CheckContextID']}, Score: {item['Score']}")
    
    choice = int(input("Select an item to remove: ")) - 1
    removed_item = data.pop(choice)
    
    with open('system/matrix/link_card_matrix.json', 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"Successfully removed item with BaseContextID: {removed_item['BaseContextID']}, CheckContextID: {removed_item['CheckContextID']}")

