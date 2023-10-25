import json
import re
from heapq import nlargest
from collections import Counter

from modules.matrix.location_matrix import get_location_matrix
from modules.matrix.card_matrix import get_card_matrix
from modules.matrix.link_matrix import get_link_matrix
from modules.matrix.link_card_matrix import get_link_card_matrix
from modules.utils import read_json

ERR_NO_LOCATION = -10000
ERR_NO_CARD = -20000

location_context_captions = [
        {'Caption': 'here', 'ID': 1},
        {'Caption': 'next', 'ID': 2},
        {'Caption': 'this', 'ID': 3},
        {'Caption': 'turn', 'ID': 4}
    ]

location_context_spot_captions = [
    {'Context': 'Random Effects', 'ID': 1},
    {'Context': 'Location Change', 'ID': 2}
]

card_context_captions = [
        {'Caption': 'on reveal', 'ID': 1}, 
        {'Caption': 'ongoing', 'ID': 2}
    ]

base_file = "system/base.json"



def find_link_score(location_effects, card_effects, link_matrix):
    score = 0
    for location_effect in location_effects:
        for card_effect in card_effects:
            for link in link_matrix:
                if link['LocationContextID'] == location_effect and link['CardContextID'] == card_effect:
                    score += link['Score']
    return score

def calculate_link_score(location_name, card_name):
    base_data = read_json(base_file)

    link_matrix = get_link_matrix()
    location_matrix = get_location_matrix()
    card_matrix = get_card_matrix()

    location_data = base_data.get('Locations', [])
    card_data = []
    for series in base_data.get('Cards', []):
        for series_name, cards in series.items():
            card_data.extend(cards)
            
    # Find matching location
    location_match = next((item for item in location_data if item['Location'] == location_name), None)
    if not location_match:
        return 0  # Or some kind of error code
    
    # Find matching card
    card_match = next((item for item in card_data if item['Card'] == card_name), None)
    if not card_match:
        return 0  # Or some kind of error code
    
    location_effect_text = location_match.get('Effect', '').lower()
    card_effect_text = card_match.get('Card Ability', '').lower()

    # Identify effects present in this location
    location_effects = [item['Effect'] for item in location_matrix if re.search(item['Pattern'], location_effect_text, re.IGNORECASE)]

    # Identify effects present in this card
    card_effects = [item['Effect'] for item in card_matrix if re.search(item['Pattern'], card_effect_text, re.IGNORECASE)]

    # Calculate link score using the identified effects
    link_score = find_link_score(location_effects, card_effects, link_matrix)

    

    return link_score

def calculate_compatibility_score(location_name, card_name):
    """
    Calculate a compatibility score between a given Location and Card, taking into account term matrices,
    energy cost, and power of the cards.
    
    Parameters:
    location_name (str): The name of the location
    card_name (str): The name of the card
    
    Returns:
    int: The compatibility score between the given Location and Card, or an error code
    """
    compatibility_score = 0
    
    base_data = read_json(base_file)

    location_matrix = get_location_matrix()
    location_data = base_data.get('Locations', [])

    location_match = next((item for item in location_data if item['Location'] == location_name), None)

    card_matrix = get_card_matrix()
    card_match = None
    for series in base_data.get('Cards', []):
        for series_name, cards in series.items():
            card_match = next((item for item in cards if item['Card'] == card_name), None)
            if card_match:
                break
        if card_match:
            break

    if location_match:
        location_effect = location_match.get('Effect', '').lower()
        for term_data in location_matrix:
            pattern = term_data['Pattern']
            score = term_data['Score']
            
            match = re.search(pattern, location_effect, re.IGNORECASE)
            if match:
                compatibility_score += score
                if match and match.groups():
                    compatibility_score += (int(match.group(1)) / 100)

            if card_match:
                card_effect = card_match.get('Card Ability', '').lower()
                energy_cost = card_match.get('Cost', 0)
                power = card_match.get('Power', 0)
                
                # Considering the energy cost and power in the compatibility score
                compatibility_score += ((10 - energy_cost) / 100)  # Lower energy cost increases score
                compatibility_score += (power / 100)  # Higher power increases score
                compatibility_score += calculate_link_score(location_name, card_name)

                for term_data in card_matrix:
                    pattern = term_data['Pattern']
                    score = term_data['Score']
                    match = re.search(pattern, card_effect, re.IGNORECASE)
                    compatibility_score += score
                    if match and match.groups():
                        compatibility_score += (int(match.group(1)) / 100)

                return compatibility_score
            else:
                return ERR_NO_CARD
    else:
        return ERR_NO_LOCATION

def get_top_cards_for_location(location_name, cards = [], count=5, energy_level=6):
    """
    Get the top 'count' cards for a given location based on compatibility scores.
    
    Parameters:
    location_name (str): The name of the location
    count (int): The number of top cards to return
    
    Returns:
    list or str: List of top 'count' card names for the given location or error message
    """
    filtered_cards = [card for card in cards if card["Cost"] <= energy_level]
    
    scores = {}
    for card in filtered_cards:
        card_name = card['Card']
        score = calculate_compatibility_score(location_name, card_name)
        
        if score == ERR_NO_LOCATION:
            return f"Location '{location_name}' not found."
        
        if score >= 0:  # Only consider cards with a valid score
            scores[card_name] = score
    
    # Get the top 'count' cards
    top_cards = nlargest(count, scores, key=scores.get)
    
    return top_cards

def analyze_location_patterns():
    base_data = read_json(base_file)

    location_matrix = get_location_matrix()
    location_data = base_data.get('Locations', [])
    # List of location effects from the locations JSON
    location_effects = [location['Effect'] for location in location_data]
    
    # Initialize a frequency Counter to count occurrences of each pattern
    pattern_frequency = Counter()
    
    # Scan each location effect and tally pattern occurrences
    for effect in location_effects:
        for pattern_dict in location_matrix:
            pattern = pattern_dict['Pattern']
            if re.search(pattern, effect, re.IGNORECASE):
                pattern_frequency[pattern] += 1

    # Sort the frequency dictionary by occurrences
    sorted_frequency = dict(sorted(pattern_frequency.items(), key=lambda item: item[1], reverse=True))
    
    # Save the sorted frequency dictionary to results.json
    with open('results/locations_matrix_freq_results.json', 'w') as f:
        json.dump(sorted_frequency, f, indent=4)

def analyze_card_patterns():
    base_data = read_json(base_file)

    card_matrix = get_card_matrix()
    series_data = base_data.get('Cards', [])
    
    # Initialize a frequency Counter to count occurrences of each pattern
    pattern_frequency = Counter()
    
    for series in series_data:
        for series_name, cards in series.items():
            # List of card effects from the cards JSON
            card_effects = [card['Card Ability'] for card in cards]
            
            # Scan each card effect and tally pattern occurrences
            for effect in card_effects:
                for pattern_dict in card_matrix:
                    pattern = pattern_dict['Pattern']
                    if re.search(pattern, effect, re.IGNORECASE):
                        pattern_frequency[pattern] += 1

    # Sort the frequency dictionary by occurrences
    sorted_frequency = dict(sorted(pattern_frequency.items(), key=lambda item: item[1], reverse=True))
    
    # Save the sorted frequency dictionary to cards_results.json
    with open('results/cards_matrix_freq_results.json', 'w') as f:
        json.dump(sorted_frequency, f, indent=4)

def analyze_location_card_link():
    base_data = read_json(base_file)
    all_locations = base_data.get('Locations', [])
    all_cards = []

    for series in base_data.get('Cards', []):
        for series_name, cards in series.items():
            all_cards.extend(cards)

    # Initialize a dictionary to store the link scores between each location and card pair
    link_scores = {}

    for location in all_locations:
        location_name = location['Location']
        link_scores[location_name] = {}
        
        for series in base_data.get('Cards', []):
            for series_name, cards in series.items():
                for card in cards:
                    card_name = card['Card']
                    link_score = calculate_compatibility_score(location_name, card_name)
                    
                    # Only consider valid link scores
                    if link_score >= 0:
                        link_scores[location_name][card_name] = link_score

    # Save the link scores to a JSON file
    with open('results/links_results.json', 'w') as f:
        json.dump(link_scores, f, indent=4)
