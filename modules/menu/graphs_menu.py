from datetime import datetime
import math
import random
import numpy as np
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from matplotlib.patheffects import withStroke

from modules.utils import ask_for_decks, ask_for_player, autocomplete_location_name, get_cards_from_names, get_player_by_name, read_json
from modules import snap_base
from modules.menu import player_menu


def graphs_menu():
    while True:
        print("----- Snap Data Graphs Menu -----")
        print('1. Create Total vs Collected Cards Pie Chart')
        print('2. Create Uncollected Cards by Series Pie Charts')
        print('3. Create Card-Location Compatibility Wavemap')
        print("4. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_collected_pie_chart()
        elif choice == '2':
            select_player_uncollected_series_pie_chart()
        elif choice == '3':  # New menu item
            select_player_card_location_heatmap()
        elif choice == '4':
            print("Returning to the main menu.")
            break

# Function to draw ASCII pie (Placeholder, the actual function will be implemented)
def draw_ascii_pie(percentage):
    pass

# Define the path effect
def path_effects_shadow(linewidth, alpha, color):
    return [withStroke(linewidth=linewidth, foreground=color, alpha=alpha)]

def select_player_card_location_heatmap():
    # 1. Prompt for Player name
    player_data = ask_for_player(player_menu.player_file)
    select_card_type_card_location_heatmap(player_data)
    
def select_card_type_card_location_heatmap(player_data):
    # 2. Ask for plot basis: "Collected" list or specific "Deck"
    while True:
        print(f"----- Select Player {player_data['Name']}' s Cards to use -----")
        print('1. Collection')
        print('2. Select Deck')
        print("3. Back")

        choice = input("Enter your choice: ")

        if choice == '1':
            selct_location_for_card_location_heatmap(player_data, player_data["Collected"])
        elif choice == '2':
            select_card_deck_card_location_heatmap(player_data)
        elif choice == '3':  # New menu item
            break
        else:
            print("Invalid Option")
    
def select_card_deck_card_location_heatmap(player_data):
    deck = ask_for_decks(player_menu.player_file, player_data["Name"])
    if deck:
        selct_location_for_card_location_heatmap(player_data, deck)
    else:
        print("Invalid Deck.")
    

def selct_location_for_card_location_heatmap(player_data, cards):
    location_name = autocomplete_location_name(snap_base.base_file, input("Enter the location name: "))
    create_card_location_wave_map(player_data, location_name, cards)

def create_card_location_wave_map(player_data, location_name, card_names, allow_interaction=False):
    # Fetch scores, energy, and power for each card
    scores, energy, power, labels = [], [], [], []
    cards_data = get_cards_from_names(card_names, snap_base.base_file)
    
    for card in cards_data:
        score = snap_base.calculate_compatibility_score(location_name, card["Card"])
        scores.append(score)
        energy.append(card['Cost'] + random.uniform(-0.3, 0.3))
        power.append(card['Power'] + random.uniform(-0.3, 0.3))
        labels.append(card['Card'])  # Assuming the name of the card is stored in 'Card'

    # Create the figure with an empty graph background
    fig = plt.figure(figsize=(15, 15))

    # Load and display background image on the whole figure
    img = mpimg.imread('assets/images/graph_background_border.png')
    img_ax = fig.add_axes([0, 0, 1, 1], frameon=False, xticks=[], yticks=[])
    img_ax.imshow(img, aspect='auto', extent=img_ax.get_xlim() + img_ax.get_ylim(), zorder=0)

    # Create a 3D subplot on top of the background with custom size and position
    ax = fig.add_axes([0.05, 0.05, 0.9, 0.9], projection='3d', frame_on=False)  # [left, bottom, width, height]

    # Plot the wave map with blue to light blue colors based on scores
    sc = ax.scatter(energy, power, scores, c=scores, cmap='Blues', marker='*', s=50)  # Set s=50 for larger points

    # Add titles and labels with path effects and white transparent color
    title = ax.set_title(f"{player_data['Name']} Card Map at {location_name}")
    title.set_path_effects(path_effects_shadow(3, 1, 'white'))  # Using the custom path effect


    ax.set_xlabel('Energy', fontsize=12).set_path_effects(path_effects_shadow(3, 1, 'white'))
    ax.set_zlabel('Score', fontsize=12).set_path_effects(path_effects_shadow(3, 1, 'white'))
    ax.set_ylabel('Power', fontsize=12).set_path_effects(path_effects_shadow(3, 1, 'white'))

    # Increase tick label size for better visibility
    ax.tick_params(axis='both', which='major', labelsize=10)

    # Draw lines from points to base and back of the graph
    for e, p, s in zip(energy, scores, power):
        ax.plot([e, e], [s, s], [min(scores), p], c='gray', linestyle='--', linewidth=0.8)
        ax.plot([e, e], [s, max(power)], [p, p], c='gray', linestyle='--', linewidth=0.8)

    # Add labels for the points if less than 13 items
    if len(labels) < 1300:
        for e, p, s, label in zip(energy, power, scores, labels):
            ax.text(e, p, s, label)

    # Set z-axis limits to min and max scores
    ax.set_xlim(min(energy), max(energy))
    ax.set_ylim(min(power), max(power))
    ax.set_zlim(min(scores), max(scores))

    # Save the wave map with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"Images/Card_Location_WaveMap_{player_data['Name']}_{timestamp}.png"

    # Save the image without a white border and stretch it vertically
    plt.savefig(filename, bbox_inches='tight', pad_inches=0, transparent=True)

    if allow_interaction:
        plt.show()

    # Save the image without a white border and stretch it vertically
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)

def create_card_location_heatmap(player_data, location_name, card_names):
    # 1. Fetch scores for each card and location from data (Assume we have a function get_scores())
    scores = []
    for card in card_names:
        score = snap_base.calculate_compatibility_score(location_name, card)
        score_data = {
            "Name": card,
            "Score": score
        }
        scores.append(score_data)
    
    # 2. Create a 2D array to hold the scores (Assuming scores are in a list of dictionaries)
    score_values = [score['Score'] for score in scores]
    
    # 3. Generate the heatmap
    fig, ax = plt.subplots()
    
    # Load and display background image on the whole figure
    img = mpimg.imread('assets/images/graph_background.png')
    img_ax = fig.add_axes([0, 0, 1, 1], frameon=False, xticks=[], yticks=[])
    img_ax.imshow(img, aspect='auto', extent=img_ax.get_xlim() + img_ax.get_ylim(), zorder=0)
    
    cax = ax.matshow([score_values], cmap='coolwarm')
    
    # Add titles and labels with path effects
    title = plt.title(f"Card-Location Compatibility Heatmap for {player_data['Name']} at {location_name}")
    title.set_path_effects(path_effects_shadow(3, 1, 'white'))
    
    plt.xlabel('Cards').set_path_effects(path_effects_shadow(3, 1, 'white'))
    plt.ylabel('Location').set_path_effects(path_effects_shadow(3, 1, 'white'))
    
    plt.colorbar(cax, orientation='horizontal').set_label(label='Compatibility Score', size=15, weight='bold')
    
    # Add card names to the heatmap
    for i, (name, value) in enumerate(zip(card_names, score_values)):
        ax.text(i, 0, f"{name}\\n{value}", va='center', ha='center').set_path_effects(path_effects_shadow(3, 1, 'white'))
    
    # 4. Save the heatmap with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    plt.savefig(f"Images/Card_Location_Heatmap_{player_data['Name']}_{timestamp}.png")

    plt.show()


def create_collected_pie_chart():
    # Data Preparation
    base_data = read_json(snap_base.base_file)
    player_data = read_json(player_menu.player_file)
    all_cards = []
    for series in base_data.get('Cards', []):
        for series_name, cards in series.items():
            all_cards.extend(cards)
    total_cards = len(all_cards)
    collected_cards = len(player_data['Players'][0]['Collected'])  # Assuming 1st player

    # Load background image
    # Create the figure
    fig = plt.figure(figsize=(15, 15))

    # Load and display background image on the whole figure
    img = mpimg.imread('assets/images/graph_background.png')
    img_ax = fig.add_axes([0, 0, 1, 1], frameon=False, xticks=[], yticks=[])
    img_ax.imshow(img, aspect='auto', extent=img_ax.get_xlim() + img_ax.get_ylim(), zorder=0)

    # Create a pie chart on top of the background
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], frameon=False, xticks=[], yticks=[])

    # Add title to the pie chart with path effects for stroke
    title_obj = ax.set_title('Total vs Collected Cards', fontsize=20, fontweight='bold')
    title_obj.set_path_effects(path_effects_shadow(3, 1, 'white'))

    # Your existing pie chart code
    sizes = [collected_cards, total_cards - collected_cards]
    colors = [(0, 1, 1, 0.7), (1, 1, 1, 0.4)]
    labels = ['', '']
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, startangle=90, autopct='%1.1f%%', pctdistance=0.85)

    # Set the z-order for wedges
    for wedge, autotext in zip(wedges, autotexts):
        wedge.set_zorder(1)
        wedge.set_edgecolor("blue")
        font_size = 18  # Specify the font size
        for autotext in autotexts:
            autotext.set_fontsize(font_size)
        autotext.set_position((autotext.get_position()[0], autotext.get_position()[1] + 0.05))

    ax.set_title('Total vs Collected Cards', fontsize=20, fontweight='bold')
    

    # Draw ASCII pie
    draw_ascii_pie(collected_cards / total_cards)

    # Add a white background for the key (moved down)
    key_background_color = (1, 1, 1, 0.4)  # Same as the 'Total Area'
    key_size = 0.15  # This will make the key larger, adjust as needed
    key_background = Rectangle((-key_size/2, -1), key_size, 0.1, fc=key_background_color, zorder=2)
    ax.add_patch(key_background)

    legend_font_size = 14  # Specify the font size for the legend
    # Create key with percentages
    labels = [f'Collected ({collected_cards}/{total_cards})', f'Not Collected ({total_cards - collected_cards}/{total_cards})']
    title_font_size = 18  # Specify the font size for the legend title
    ax.legend(wedges, labels, title="Cards", loc="lower center", fontsize=legend_font_size, bbox_to_anchor=(0.5, 0), title_fontsize=title_font_size)


    # Save Pie Chart
    plt.savefig('Images/collected_pie.png')

    # Display Values with Percentage
    print(f'Total Cards: {total_cards}')
    print(f'Collected Cards: {collected_cards}')
    percentage_collected = (collected_cards / total_cards) * 100
    print(f'Percentage Collected: {percentage_collected:.2f}%')

def select_player_uncollected_series_pie_chart():
    player = ask_for_player(player_menu.player_file)
    if player:
        create_uncollected_series_pie_chart(player)
    else:
        print ("Invalid Choice.")

def create_uncollected_series_pie_chart(selected_player):
    """
    Create a pie chart showing the distribution of uncollected cards by series for the selected player.
    """
    base_data = read_json(snap_base.base_file)

    # Extract data for the selected player and all cards
    collected_cards = selected_player['Collected']
    all_series = base_data['Cards']
    
    # Initialize data for the pie chart
    collected_by_series = {}
    
    # Calculate uncollected cards for each series
    for series in all_series:
        collected_in_series = 0
        series_name = list(series.keys())[0]
        total_cards_in_series = len(series[series_name])
        # collected_in_series = len([card for card in collected_cards if card in series[series_name]])
        for series_cards in series[series_name]:
            for card in collected_cards:
                if card == series_cards["Card"]:
                    collected_in_series += 1
                    break


        collected_by_series[series_name] = collected_in_series
    
    # Calculate the number of rows and columns for the grid
    num_series = len(collected_by_series)
    num_cols = 3  # You can adjust this based on your preferences
    num_rows = math.ceil(num_series / num_cols)

    # Create the figure
    fig = plt.figure(figsize=(15, 15))

    # Load and display background image on the whole figure
    img = mpimg.imread('assets/images/graph_background.png')
    img_ax = fig.add_axes([0, 0, 1, 1], frameon=False, xticks=[], yticks=[])
    img_ax.imshow(img, aspect='auto', extent=img_ax.get_xlim() + img_ax.get_ylim(), zorder=0)

    # Create the grid of subplots
    axs = fig.subplots(num_rows, num_cols).ravel()

    # Create pie charts for each series
    for idx, (series_name, uncollected_count) in enumerate(collected_by_series.items()):
        ax = axs[idx]

        # Update the total_cards_in_series variable for the current series
        total_cards_in_series = len([card for series in all_series for key, value in series.items() if key == series_name for card in value])
        print(f"For series {series_name}, total_cards_in_series: {total_cards_in_series}, uncollected_count: {uncollected_count}")
    
   
        # Pie chart data
        sizes = [uncollected_count, total_cards_in_series - uncollected_count]
        if sizes[0] < 0 or sizes[1] < 0:
            print(f"Warning: Negative sizes detected for series {series_name}. Sizes array: {sizes}")
            continue  # Skip this iteration and continue with the next series
    
        colors = [(0, 1, 1, 0.7), (1, 1, 1, 0.4)]
        labels = ['', '']
        wedges, _, _ = ax.pie(sizes, labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')

        # Styling (similar to your existing pie chart)
        for wedge in wedges:
            wedge.set_edgecolor("blue")

        # Increase Series caption font size to 20, make it bold, and add a white outline for shadow effect
        title_text = ax.set_title(series_name, fontsize=18, fontweight='bold', color='black', va='center', ha='center', 
                          path_effects=path_effects_shadow(4, 1, 'white'))
        

     # Remove any unused subplots
    for idx in range(num_series, num_cols * num_rows):
        axs[idx].axis('off')

    # Add a legend at the bottom center of the figure (common for all subplots)
    fig.legend(wedges, ['Collected', 'Uncollected'], title="Card Status", loc="lower center", fontsize='large', ncol=2)

    # Save the plot
    plt.savefig('Images/uncollected_series_pie.png')