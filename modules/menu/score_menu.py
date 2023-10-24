from modules.utils import autocomplete_card_name, autocomplete_location_name, check_and_create_folder
from modules import snap_base

def score_menu():
    check_and_create_folder("results")
    check_and_create_folder("player")

    while True:
        print("----- Scoring Values Menu -----")
        print("1. Get Location-Card Overall Score")
        print("2. Get Location-Card Linking Score")
        print("3. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            location_name = autocomplete_location_name(snap_base.base_file, input("Enter the location name: "))
            card_name = autocomplete_card_name(snap_base.base_file, input("Enter the card name: "))

            score = snap_base.calculate_compatibility_score(location_name, card_name)
            if score >= 0:
                print(f"The overall compatibility score between the location {location_name} and card {card_name} is {score}.")
            else:
                print("An error occurred while calculating the score.")
        elif choice == '2':
            location_name = autocomplete_location_name(snap_base.base_file, input("Enter the location name: "))
            card_name = autocomplete_card_name(snap_base.base_file, input("Enter the card name: "))
            score = snap_base.calculate_link_score(location_name, card_name)
            if score >= 0:
                print(f"The linking score between the location {location_name} and card {card_name} is {score}.")
            else:
                print("An error occurred while calculating the score.")
        elif choice == '3':
            return
        else:
            print("Invallid Choice.")