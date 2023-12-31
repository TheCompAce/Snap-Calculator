# Snap Calculator

## Introduction

Snap Calculator is a comprehensive tool designed to manage, analyze, and visualize card collections. Serving as a central hub, it integrates various functionalities such as:

- **Graphical Analysis:** Generate pie charts and graphs to visualize your collection.
- **Scoring System:** Evaluate the value and rarity of cards in your collection.
- **Top Cards Management:** Easily identify and manage the top cards in your collection.
- **Building Decks:** Automatically build decks for all locations, or just certain ones.
- **Player Menu:** Personalize settings and preferences for an individualized experience.

Whether you're a casual collector or a seasoned aficionado, Snap Calculator aims to simplify and enhance your card collecting journey.

## Features

Snap Calculator offers a variety of features to manage and analyze your card collection:

### Create Decks Automatically
- **Create Decks from you Collection:** Generate a deck for certain locations, or all locations, using you Collected cards.

### Get Scoring Values
- **Get Location-Card Overall Score:** Calculate an overall compatibility score between a given location and card.
- **Get Location-Card Linking Score:** Compute a score based on how well a card and location are linked.

### Create Analysis Files
- **Analyze Location Patterns:** Perform analysis on location patterns and save the results.
- **Analyze Cards Patterns:** Analyze card patterns and save the results.
- **Analyze Location-Card Links:** Analyze the links between locations and cards.

### Create Data Graphs
- **Create Total vs Collected Cards Pie Chart:** Generate a pie chart showing the total vs collected cards.
![Collected Pie Chart](assets/images/collected_pie.png)
- **Create Uncollected Cards by Series Pie Charts:** Generate pie charts depicting uncollected cards by series.
![Uncollected by Series Example](assets/images/uncollected_series_pie.png)
- **Create Card-Location Compatibility Wavemap:** Generate a heatmap showing the compatibility between cards and locations.
![Card score by Location for Collection Example](assets/images/collection_example.png)
![Card score by Location for Deck Example](assets/images/deck_example.png)


### Player Details Setup
- **Player List:** Manage and navigate through a list of players.
- **Add New Player:** Add new players to the list.
- **Delete Player:** Remove players from the list.
- **Edit Collection:** Navigate to the collection submenu to edit the player's collection.
- **Edit Decks:** Navigate to the deck submenu to edit the player's decks.
- **Player Decks:** Manage and navigate through a list of decks owned by the player.
- **Add New Decks:** Add new decks to the player's collection.
- **Delete Decks:** Remove decks from the player's collection.


## Matrix Setup

### How to Edit Matrix Files

#### Using the Edit Matrix Menu

1. **Main Edit Matrix Menu**: When you run the program, you'll encounter the main "Edit Matrix Menu." Here you can choose which matrix you'd like to edit.
    - **Options**: 
        - Edit Location Matrix
        - Edit Card Matrix
        - Edit Location To Card Matrix
        - Edit Card To Card Link Matrix
        - Back (to exit the menu)

2. **Sub-Menus**: After selecting a matrix to edit, you'll enter a sub-menu specific to that matrix. Each sub-menu has similar options:
    - **View Matrix**: Displays the current entries in the selected matrix.
    - **Add Item**: Allows you to add a new entry to the matrix.
    - **Edit Item**: Lets you edit an existing entry in the matrix.
    - **Remove Item**: Allows you to remove an entry from the matrix.
    - **Back**: Returns you to the main "Edit Matrix Menu."

##### Location Matrix Sub-Menu
- **Edit Location Matrix**: Once selected, you can view, add, edit, or remove entries related to gameplay effects and patterns at different locations.

##### Card Matrix Sub-Menu
- **Edit Card Matrix**: Here, you can manage entries related to card effects, patterns, and scores.

##### Location To Card Matrix Sub-Menu
- **Edit Location To Card Matrix**: This menu lets you manage how locations and cards are linked, with options to view, add, edit, or remove such links.

##### Card To Card Link Matrix Sub-Menu
- **Edit Card To Card Link Matrix**: This menu is for managing relationships between different card contexts. You can view, add, edit, or remove these relationships.

#### Navigating the Menus
- Follow the on-screen prompts to make your selection.
- When adding or editing an item, you'll be asked to input or select various fields depending on the matrix. These could be IDs, patterns, or scores.
- To exit any menu or sub-menu, select the "Back" option.

This way, you can easily manage and modify different aspects of your game mechanics without directly altering the code.

## Installation
- Install the dependencies by running `pip install -r requirements.txt`.

## Usage
- Run the project by executing `python snap.py`.

## Directories and Files
- **requirements.txt**: This is a text file that may contain important notes or configuration details.
- **snap.py**: This is a Python script that contains code for the project.
- **assets**: This is a directory that likely contains related files or modules.
- **modules**: This is a directory that likely contains related files or modules.
- **player**: This is a directory that likely contains related files or modules.
- **results**: This is a directory that likely contains related files or modules.
- **system**: This is a directory that likely contains related files or modules.
- **Tools**: This is a directory that likely contains related files or modules.
- **.gitignore**: This is a file of unknown type.
- **missing.txt**: This is a text file that may contain important notes or configuration details.

## Contributing
- You can contribute by joining our developers for this porject.
- You can also Venmo me donations to @BradfordBrooks79

## License
Copyright 2023 Bard Brooks

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
