import json

def get_link_matrix():
    """
    Returns a list of dictionaries containing linking rules between location and card contexts.
    
    Returns:
    list: The refined link matrix
    """
    print("OK4")
    # Read the linking rules for gameplay mechanics from JSON file
    json_file_path = 'system/matrix/link_matrix.json'
    with open(json_file_path, 'r') as json_file:
        link_matrix = json.load(json_file)
    
    return link_matrix