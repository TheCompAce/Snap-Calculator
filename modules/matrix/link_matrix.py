def get_link_matrix():
    """
    Returns a list of dictionaries containing linking rules between location and card contexts.
    
    Returns:
    list: The refined link matrix
    """
    link_matrix = [
        {'LocationContextID': 'destroy', 'CardContextID': 'destroyed', 'Score': 80},
        {'LocationContextID': 'energy_next_turn', 'CardContextID': 'ongoing', 'Score': 60},
        {'LocationContextID': 'power_increase', 'CardContextID': 'power_increase', 'Score': 70},
        {'LocationContextID': 'destroy_it', 'CardContextID': 'is_destroyed', 'Score': 50},
        {'LocationContextID': 'on_turn', 'CardContextID': 'turn', 'Score': 40},
        {'LocationContextID': 'end_the_game', 'CardContextID': 'power_increase', 'Score': 30},
        {'LocationContextID': 'cards_must_be_played', 'CardContextID': 'energy', 'Score': 50},
        {'LocationContextID': 'set_power', 'CardContextID': 'power_decrease', 'Score': 50},
        {'LocationContextID': 'add_random_card', 'CardContextID': 'random_card', 'Score': 40},
        {'LocationContextID': 'disable_effects', 'CardContextID': 'no_ability', 'Score': 50},
        {'LocationContextID': 'shuffle_into_deck', 'CardContextID': 'shuffle', 'Score': 40},
        {'LocationContextID': 'power_increase', 'CardContextID': 'ongoing', 'Score': 60},
        {'LocationContextID': 'draw_card', 'CardContextID': 'draw', 'Score': 50},
        {'LocationContextID': 'moves', 'CardContextID': 'moves', 'Score': 50}
    ]

    return link_matrix