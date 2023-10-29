import json
import re
from modules.matrix.get_matrix import get_matrix

def get_card_matrix():
    """
    Returns the refined card_matrix based on relevant gameplay terms, effects, patterns, and context values.
    
    Returns:
    list: The refined location_matrix
    """
    print("OK1")
    return get_matrix('system/matrix/card_matrix.json')
