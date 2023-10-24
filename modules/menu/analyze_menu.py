from modules import snap_base

def analyze_menu():
    while True:
        print("----- Analyzing Menu Menu -----")
        print("1. Analyze Location Patterns") 
        print("2. Analyze Cards Patterns")
        print("3. Analyze Location-Card Links")
        print("4. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Analyzing location patterns...")
            snap_base.analyze_location_patterns()  # Call your function here
            print("Analysis complete. Results saved to locations_results.json.")
        elif choice == '2':
            print("Analyzing cards patterns...")
            snap_base.analyze_card_patterns()  # Call your function here
            print("Analysis complete. Results saved to cards_results.json.")
        elif choice == '3':  # New condition for the new option
            print("Analyzing location-card links...")
            snap_base.analyze_location_card_link()
            print("Analysis complete. Results saved to links_results.json.")
        elif choice == '4':  # New condition for the new option
            return
        else:
            print("Invallid Choice.")
