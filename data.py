import streamlit as st
import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
import heapq
from collections import defaultdict
from datetime import datetime
#SK-learn
# alpha = 0.1
# reg.fit(train[predictors], train["Share"])


#Dictionary for prices
prices_dict = {
    'Grilled Cheese Sandwich' : 8.99, 
    'Mac and Cheese' : 8.99, 
    'Pulled Pork' : 1.99, 
    'Grilled Chicken' : 1.99, 
    'Brisket' : 1.99, 
    'Bacon' : 1.99, 
    'Ham' : 1.99,
    'Garlic Bread' : 1.99,
    'Cheesy Garlic Bread' : 1.99,
    'Cheesecake' : 4.99,
    'Large Chocolate Chunk Cookie' : 4.99,
    'Doritos' : 1.99,
    'Cheetos' : 1.99,
    'Lays Barbecue' : 1.99,
    'Lays Classic' : 1.99,
    'Cheesy Broccoli' : 2.99,
    'Water' : 1.49,
    'Apple Juice' : 2.49,
    'Coke' : 1.99,
    'Dr. Pepper' : 1.99,
    'Sprite' : 1.99,
    'Diet Coke' : 1.99,
    'Powerade - Blue Mountain Berry Blast' : 1.99,
    'Minute Maid Lemonade' : 1.99,
    'XL Shirt' : 19.95,
    'Medium Shirt' : 19.95,
    'Shirt' : 19.95,
    'Small Shirt' : 19.95,
    '2X Shirt': 19.95,
    'Cheddar Mac' :  1.99,
    'Pepper Jack Mac' : 1.99,
    'Alfredo Mac' : 1.99,
    'Mac and Cheese Party Tray (Plus FREE Garlic Bread)' : 39.99
    }

#unique modifier counter dictionary
countItem_dict = {

    'Regular': 0,
    'Cheddar': 0,
    'Pulled Pork': 0,
    'Broccoli': 0,
    'Tomatoes': 0,
    'Breadcrumbs': 0,
    'BBQ': 0,
    'No Side': 0,
    'Water': 0,
    'Pepper Jack': 0,
    'Brisket': 0,
    'Corn': 0,
    'Mushrooms': 0,
    'Parmesan': 0,
    'No Drink': 0,
    'Alfredo': 0,
    'Jalapenos': 0,
    'Unlimited Fountain Drinks': 0,
    'No Toppings': 0,
    'Cheesy Broccoli': 0,
    'Cheesy Garlic Bread': 0,
    'No Meat': 0,
    'No Drizzle': 0,
    'Pepperjack': 0,
    'Bacon': 0,
    'Garlic Parmesan': 0,
    'Grilled Chicken': 0,
    'Bell Peppers': 0,
    'Hot Honey': 0,
    'Garlic Bread': 0,
    'Ranch': 0,
    'Cheesecake': 0,
    'Buffalo': 0,
    'Ham': 0,
    'Melted Cheddar': 0,
    'No Mac': 0,
    'Pesto': 0,
    'Sprite': 0,
    'Coke': 0,
    'Pepper Jack Mac': 0,
    'Pineapple': 0,
    'Melted Pepper Jack': 0,
    'MIX': 0,
    'Mix PJ And Cheddar': 0,
    'GLUTEN FREE': 0,
    'Melted Parmesan': 0,
    'Cheddar Mac': 0,
    'Alfredo Mac': 0,
    'Side Mac': 0,
    'Diet Coke': 0,
    'Onions': 0,
    'Onion': 0,
    'All Cheese!!!': 0,
    'I DO NOT NEED UTENSILS (Save waste!)': 0,
    'O J And BP On Side': 0,
    'Bacon On Side': 0,
    'Hot Honey On Half': 0,
    'MIXED Melted Cheese': 0,
    'Bbq On Side': 0,
    'Gluten-Free (ask store for safe toppings)': 0,
    'Hot Honey On Side': 0,
    'Bowl Alredo Bacon Breadcrumbs Bricholi Jalepnos Galic Parm': 0,
    'Bowl Chedder Chicken Jalepenos Bread Crumbs Buffalo Cheescake': 0,
    'Mac Alfredo Chick Every Addition But Brocli And Pinapple Gar Parm Ches Gar Bread Dr Pep': 0,
    'Apple Juice': 0,
    'Dr. Pepper': 0,
    'XL Shirt': 0,
    'Chips': 0,
    'Any Bag Of Chips': 0,
    'Shirt': 0,
    'Medium Shirt': 0
}

#Sorting data into a list 
def load_data(file_name):
    with open(file_name, 'r') as file:
        # Read the file content, split by lines, and then split each line by commas
        data_list = [line.split(',') for line in file.read().split('\n')]
        
    # Remove the header and last empty line if they exist
    if data_list:
        data_list.pop(0)  # Remove header
    if data_list and not data_list[-1][0]:  # Check if the last line is empty
        data_list.pop(-1)
    
    return data_list

# Loading data for each month using the function into a list of lists
april_data_List = load_data('april_2024.csv')
august_data_List = load_data('august_2024.csv')
july_data_List = load_data('july_2024.csv')
june_data_List = load_data('june_2024.csv')
may_data_List = load_data('may_2024.csv')
october_data_List = load_data('october_2024.csv')
september_data_List = load_data('september_2024.csv')
# print(april_data_List)
# print(august_data_List)
# print(july_data_List)
# print(june_data_List)
# print(may_data_List)
# print(october_data_List)
# print(september_data_List)

allMonths_data = []
allMonths_data = april_data_List + may_data_List + june_data_List + july_data_List + august_data_List + september_data_List + october_data_List 
#print(allMonths_data)

#Order #,Sent Date,Modifier,Option Group Name,Parent Menu Selection,Order ID indexes 
Order_num = 0
Sent_Date = 1
Modifier = 2
Option_Group_Name = 3
Parent_Menu_Selection = 4
Order_ID_Indexes = 5

def count_modifiers(data_list, modifier_dict):
    for entry in data_list:
        item = entry[2].strip('"\'')  # Strip " and ' characters from item
        modifier_dict[item] = modifier_dict.get(item, 0) + 1

# Initialize dictionaries for each month
Modifier_april_dict = {}
Modifier_may_dict = {}
Modifier_june_dict = {}
Modifier_july_dict = {}
Modifier_august_dict = {}
Modifier_september_dict = {}
Modifier_october_dict = {}

# Count modifiers for each month by calling the function
count_modifiers(april_data_List, Modifier_april_dict)
count_modifiers(may_data_List, Modifier_may_dict)
count_modifiers(june_data_List, Modifier_june_dict)
count_modifiers(july_data_List, Modifier_july_dict)
count_modifiers(august_data_List, Modifier_august_dict)
count_modifiers(september_data_List, Modifier_september_dict)
count_modifiers(october_data_List, Modifier_october_dict)
# Optional print statements to verify each dictionary
#print(Modifier_april_dict)
#print(Modifier_may_dict)
#print(Modifier_june_dict)
#print(Modifier_july_dict)
#print(Modifier_august_dict)
#print(Modifier_september_dict)
#print(Modifier_october_dict)



def count_unique_parent_menu_selections(data_list):
    # Initialize the dictionary to store counts
    selection_count = {}

    # Loop through the list with an index up to the second-to-last element
    for i in range(len(data_list) - 1):
        # Get the current and next item for comparison, stripping spaces and specific characters
        current_item = data_list[i][4].strip(' ()"')
        next_item = data_list[i + 1][4].strip(' ()"')

        # Check if the current item is not empty and is not repeated in the next line
        if current_item and current_item != next_item:
            if current_item in selection_count:
                selection_count[current_item] += 1
            else:
                selection_count[current_item] = 1

    # Handle the last item separately, as it has no next item to compare
    last_item = data_list[-1][4].strip(' ()"')
    if last_item:  # Ensure last_item is not empty
        if last_item in selection_count:
            selection_count[last_item] += 1
        else:
            selection_count[last_item] = 1

    # Return the final dictionary
    return selection_count



# Example usage:
Parent_Menu_Selection_april_dict = count_unique_parent_menu_selections(april_data_List)
Parent_Menu_Selection_may_dict = count_unique_parent_menu_selections(may_data_List)
Parent_Menu_Selection_june_dict = count_unique_parent_menu_selections(june_data_List)
Parent_Menu_Selection_july_dict = count_unique_parent_menu_selections(july_data_List)
Parent_Menu_Selection_august_dict = count_unique_parent_menu_selections(august_data_List)
Parent_Menu_Selection_september_dict = count_unique_parent_menu_selections(september_data_List)
Parent_Menu_Selection_october_dict = count_unique_parent_menu_selections(october_data_List)

#print(Parent_Menu_Selection_april_dict)
#print(Parent_Menu_Selection_may_dict)
#print(Parent_Menu_Selection_june_dict)
#print(Parent_Menu_Selection_july_dict)
#print(Parent_Menu_Selection_august_dict)
#print(Parent_Menu_Selection_september_dict)
#print(Parent_Menu_Selection_october_dict)

def calculate_total_price(ParentMenuSelections, Modifier, prices_dict):
    total = 0

    # Calculate total for items in ParentMenuSelections
    for item, count in ParentMenuSelections.items():
        if item in prices_dict:
            total += count * prices_dict[item]

    # Calculate total for items in Modifier
    for item, count in Modifier.items():
        if item in prices_dict:
            total += count * prices_dict[item]

    return total

total_price_april = calculate_total_price(Parent_Menu_Selection_april_dict, Modifier_april_dict, prices_dict)
total_price_may = calculate_total_price(Parent_Menu_Selection_may_dict, Modifier_may_dict, prices_dict)
total_price_june = calculate_total_price(Parent_Menu_Selection_june_dict, Modifier_june_dict, prices_dict)
total_price_july = calculate_total_price(Parent_Menu_Selection_july_dict, Modifier_july_dict, prices_dict)
total_price_august = calculate_total_price(Parent_Menu_Selection_august_dict, Modifier_august_dict, prices_dict)
total_price_september = calculate_total_price(Parent_Menu_Selection_september_dict, Modifier_september_dict, prices_dict)
total_price_october = calculate_total_price(Parent_Menu_Selection_october_dict, Modifier_october_dict, prices_dict)
total_price = [total_price_april, total_price_may, total_price_june, total_price_july, total_price_august, total_price_september, total_price_october]
total_price_allMonths = total_price_april + total_price_may + total_price_june + total_price_july + total_price_august + total_price_september + total_price_october
#print(f'the total sales of all months: {total_price_allMonths}')
# print(f'total sales of april: {total_price_april}')
# print(f'total sales of may: {total_price_may}')
# print(f'total sales of june: {total_price_june}')
# print(f'total sales of july: {total_price_july}')
# print(f'total sales of august: {total_price_august}')
# print(f'total sales of september: {total_price_september}')
# print(f'total sales of october: {total_price_october}')
mostProfitableMonth = 'September'


def highest_profit_modifier(Modifier, prices_dict):
    # Dictionary to store the profit for given dictionary
    modifier_profit_dict = {}

    # Calculate profit for items in Modifier only
    for item, count in Modifier.items():
        if item in prices_dict:
            profit = count * prices_dict[item]
            modifier_profit_dict[item] = profit

    # Find the modifier item with the highest profit
    highest_profit_modifier = max(modifier_profit_dict, key=modifier_profit_dict.get)
    return highest_profit_modifier

top_profit_modifier_april = highest_profit_modifier(Modifier_april_dict, prices_dict)
top_profit_modifier_may = highest_profit_modifier(Modifier_may_dict, prices_dict)
top_profit_modifier_june = highest_profit_modifier(Modifier_june_dict, prices_dict)
top_profit_modifier_july = highest_profit_modifier(Modifier_july_dict, prices_dict)
top_profit_modifier_august = highest_profit_modifier(Modifier_august_dict, prices_dict)
top_profit_modifier_september = highest_profit_modifier(Modifier_september_dict, prices_dict)
top_profit_modifier_october = highest_profit_modifier(Modifier_october_dict, prices_dict)
# print(top_profit_modifier_april)
# print(top_profit_modifier_may)
# print(top_profit_modifier_june)
# print(top_profit_modifier_july)
# print(top_profit_modifier_august)
# print(top_profit_modifier_september)
# print(top_profit_modifier_october)


def rank_modifiers_by_popularity(Modifier):
    # Sort the Modifier items by count in descending order, limit to top 20
    sorted_modifiers = sorted(Modifier.items(), key=lambda item: item[1], reverse=True)[:20]
    
    # Create a ranking dictionary with rank labels and sales count as an array
    ranking_dict = {}
    for index, (name, sales) in enumerate(sorted_modifiers, start=1):
        if index == 1:
            rank = f"{index}st"
        elif index == 2:
            rank = f"{index}nd"
        elif index == 3:
            rank = f"{index}rd"
        else:
            rank = f"{index}th"
        
        # Store the name and sales as a list
        ranking_dict[rank] = [name, sales]
    
    return ranking_dict


ranked_modifiers_april = rank_modifiers_by_popularity(Modifier_april_dict)
ranked_modifiers_may = rank_modifiers_by_popularity(Modifier_may_dict)
ranked_modifiers_june = rank_modifiers_by_popularity(Modifier_june_dict)
ranked_modifiers_july = rank_modifiers_by_popularity(Modifier_july_dict)
ranked_modifiers_august = rank_modifiers_by_popularity(Modifier_august_dict)
ranked_modifiers_september = rank_modifiers_by_popularity(Modifier_september_dict)
ranked_modifiers_october = rank_modifiers_by_popularity(Modifier_october_dict)
#print(ranked_modifiers_april)
#print(ranked_modifiers_may)
# print(ranked_modifiers_june)
# print(ranked_modifiers_july)
# print(ranked_modifiers_august)
# print(ranked_modifiers_september)
# print(ranked_modifiers_october)


from collections import defaultdict
from datetime import datetime




def count_orders_by_time(data_list):
    # Dictionary to store counts for each time of day within the month
    orders_by_time = defaultdict(int)

    for entry in data_list:
        # Extract Sent Date and Modifier from entry
        sent_date_str = entry[1]
        modifier = entry[3]
        
        # Check if sent_date_str is not empty and correctly formatted
        if sent_date_str:
            try:
                # Convert Sent Date to a datetime object to extract the hour
                sent_datetime = datetime.strptime(sent_date_str, '%Y-%m-%d %H:%M:%S')
                hour = sent_datetime.strftime('%H:00')  # Format as "HH:00" for grouping by hour
            except ValueError:
                print(f"Skipping entry with invalid date format: {sent_date_str}")
                continue
        else:
            print("Skipping entry with empty Sent Date.")
            continue
        
        # Count only entries with "Choose Your Drink" as the modifier
        if modifier == "Choose Your Drink":
            orders_by_time[hour] += 1

    return dict(orders_by_time)

# Example usage with a list of all monthly lists

april_orders_by_time = count_orders_by_time(april_data_List)
may_orders_by_time = count_orders_by_time(may_data_List)
june_orders_by_time = count_orders_by_time(june_data_List)
july_orders_by_time = count_orders_by_time(july_data_List)
august_orders_by_time = count_orders_by_time(august_data_List)
september_orders_by_time = count_orders_by_time(september_data_List)
october_orders_by_time = count_orders_by_time(october_data_List)

# print(april_orders_by_time)
# print(may_orders_by_time)
# print(june_orders_by_time)
# print(july_orders_by_time)
# print(august_orders_by_time)
# print(september_orders_by_time)
# print(october_orders_by_time)


#Most popular menu combinations


# def get_food_combination_counts(data_list):
#     # HashMap to store food combination counts
#     food_combination_counts = defaultdict(int)

#     # Variables to hold current order data
#     current_modifiers = []
#     current_parent_selection = None

#     # Process each entry in the data list
#     for entry in data_list:
#         # Ensure entry has exactly 6 elements before unpacking
#         if len(entry) != 6:
#             print(f"Skipping invalid entry: {entry}")
#             continue

#         # Unpack fields from each entry
#         order_num, sent_date, modifier, option_group, parent_menu, order_id = entry

#         # Check if this line marks the end of an order
#         if option_group == "Choose Your Drink":
#             # Sort modifiers for consistency and create key
#             combination_key = f"[{current_parent_selection}][{'|'.join(sorted(current_modifiers))}]"
            
#             # Increment the count in the hashmap
#             food_combination_counts[combination_key] += 1
            
#             # Reset for the next order
#             current_modifiers = []
#             current_parent_selection = None
#         else:
#             # Collect the current parent menu selection and modifier
#             current_parent_selection = parent_menu
#             current_modifiers.append(modifier)

#     return food_combination_counts

# april_order_combinations = get_food_combination_counts(april_data_List)
# may_order_combinations = get_food_combination_counts(may_data_List)
# june_order_combinations = get_food_combination_counts(june_data_List)
# july_order_combinations = get_food_combination_counts(july_data_List)
# august_order_combinations = get_food_combination_counts(august_data_List)
# september_order_combinations = get_food_combination_counts(september_data_List)
# october_order_combinations = get_food_combination_counts(october_data_List)

# print(april_order_combinations)
# # print(may_order_combinations)
# # print(june_order_combinations)
# # print(july_order_combinations)
# # print(august_order_combinations)
# # print(september_order_combinations)
# # print(october_order_combinations)