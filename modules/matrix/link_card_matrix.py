import json
import re
from modules.matrix.get_matrix import get_matrix

def get_link_card_matrix():
    """
    Returns a list of dictionaries containing linking rules between location and card contexts.
    
    Returns:
    list: The refined link matrix
    """
    print("Ok2")
    # Read the linking rules for gameplay mechanics from JSON file
    json_file_path = 'system/matrix/link_card_matrix.json'
    with open(json_file_path, 'r') as json_file:
        link_matrix = json.load(json_file)

    return link_matrix
