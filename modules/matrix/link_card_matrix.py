def get_link_card_matrix():
    """
    Returns a list of dictionaries containing linking rules between location and card contexts.
    
    Returns:
    list: The refined link matrix
    """
    link_card_matrix = [
        # High importance due to Victory Condition
        {'BaseContextID': 'power_increase', 'CheckContextID': 'p_power', 'Score': 90},
        {'BaseContextID': 'p_power', 'CheckContextID': 'power_increase', 'Score': 90},

        # Destruction related
        {'BaseContextID': 'destroy', 'CheckContextID': 'destroyed', 'Score': 80},
        {'BaseContextID': 'destroyed', 'CheckContextID': 'destroy', 'Score': 80},
        {'BaseContextID': 'destroy', 'CheckContextID': 'destroyed_create', 'Score': 80},
        {'BaseContextID': 'destroyed_create', 'CheckContextID': 'destroy', 'Score': 80},

        # Draw mechanics
        {'BaseContextID': 'draw', 'CheckContextID': 'draws', 'Score': 75},
        {'BaseContextID': 'draws', 'CheckContextID': 'draw', 'Score': 75},

        # Energy mechanics
        {'BaseContextID': 'energy', 'CheckContextID': 'energy_value', 'Score': 70},
        {'BaseContextID': 'energy_value', 'CheckContextID': 'energy', 'Score': 70},

        # Gaining something
        {'BaseContextID': 'gain', 'CheckContextID': 'gains', 'Score': 65},
        {'BaseContextID': 'gains', 'CheckContextID': 'gain', 'Score': 65},

        # Cost related
        {'BaseContextID': 'cost_less', 'CheckContextID': 'cost_more', 'Score': -50},
        {'BaseContextID': 'cost_more', 'CheckContextID': 'cost_less', 'Score': -50},

        # Opponent interactions
        {'BaseContextID': 'opponent', 'CheckContextID': 'draw', 'Score': 55},
        {'BaseContextID': 'draw', 'CheckContextID': 'opponent', 'Score': 55},

        # Discarding
        {'BaseContextID': 'discard', 'CheckContextID': 'you_discarded', 'Score': 45},
        {'BaseContextID': 'you_discarded', 'CheckContextID': 'discard', 'Score': 45},

        # Yours and Opponent context
        {'BaseContextID': 'yours', 'CheckContextID': 'opponent', 'Score': -35},
        {'BaseContextID': 'opponent', 'CheckContextID': 'yours', 'Score': -35},
        
        # No ability
        {'BaseContextID': 'no_ability', 'CheckContextID': 'no_ability', 'Score': 0}
    ]



    return link_card_matrix