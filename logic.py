import streamlit as st
import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

#Dictionary for prices
# prices_dict = {
#     'Grilled Cheese Sandwich' : 8.99, 
#     'Mac and Cheese' : 8.99, 
#     'Pulled Pork' : 1.99, 
#     'Grilled Chicken' : 1.99, 
#     'Brisket' : 1.99, 
#     'Bacon' : 1.99, 
#     'Ham' : 1.99,
#     'Garlic Bread' : 1.99,
#     'Cheesy Garlic Bread' : 1.99,
#     'Cheesecake' : 4.99,
#     'Large Chocolate Chunk Cookie' : 4.99,
#     'Doritos' : 1.99,
#     'Cheetos' : 1.99,
#     'Lays Barbecue' : 1.99,
#     'Lays Classic' : 1.99,
#     'Cheesy Broccoli' : 2.99,
#     'Water' : 1.49,
#     'Apple Juice' : 2.49,
#     'Coke' : 1.99,
#     'Dr. Pepper' : 1.99,
#     'Sprite' : 1.99,
#     'Diet Coke' : 1.99,
#     'Powerade - Blue Mountain Berry Blast' : 1.99,
#     'Minute Maid Lemonade' : 1.99,
#     'XL Shirt' : 19.95,
#     'Medium Shirt' : 19.95,
#     'Shirt' : 19.95,
#     'Small Shirt' : 19.95,
#     '2X Shirt': 19.95,
#     'Cheddar Mac' :  1.99,
#     'Pepper Jack Mac' : 1.99,
#     'Alfredo Mac' : 1.99,
     
#     }





# #unique modifier counter dictionary
# countItem_dict = {

#     'Regular': 0,
#     'Cheddar': 0,
#     'Pulled Pork': 0,
#     'Broccoli': 0,
#     'Tomatoes': 0,
#     'Breadcrumbs': 0,
#     'BBQ': 0,
#     'No Side': 0,
#     'Water': 0,
#     'Pepper Jack': 0,
#     'Brisket': 0,
#     'Corn': 0,
#     'Mushrooms': 0,
#     'Parmesan': 0,
#     'No Drink': 0,
#     'Alfredo': 0,
#     'Jalapenos': 0,
#     'Unlimited Fountain Drinks': 0,
#     'No Toppings': 0,
#     'Cheesy Broccoli': 0,
#     'Cheesy Garlic Bread': 0,
#     'No Meat': 0,
#     'No Drizzle': 0,
#     'Pepperjack': 0,
#     'Bacon': 0,
#     'Garlic Parmesan': 0,
#     'Grilled Chicken': 0,
#     'Bell Peppers': 0,
#     'Hot Honey': 0,
#     'Garlic Bread': 0,
#     'Ranch': 0,
#     'Cheesecake': 0,
#     'Buffalo': 0,
#     'Ham': 0,
#     'Melted Cheddar': 0,
#     'No Mac': 0,
#     'Pesto': 0,
#     'Sprite': 0,
#     'Coke': 0,
#     'Pepper Jack Mac': 0,
#     'Pineapple': 0,
#     'Melted Pepper Jack': 0,
#     'MIX': 0,
#     'Mix PJ And Cheddar': 0,
#     'GLUTEN FREE': 0,
#     'Melted Parmesan': 0,
#     'Cheddar Mac': 0,
#     'Alfredo Mac': 0,
#     'Side Mac': 0,
#     'Diet Coke': 0,
#     'Onions': 0,
#     'Onion': 0,
#     'All Cheese!!!': 0,
#     'I DO NOT NEED UTENSILS (Save waste!)': 0,
#     'O J And BP On Side': 0,
#     'Bacon On Side': 0,
#     'Hot Honey On Half': 0,
#     'MIXED Melted Cheese': 0,
#     'Bbq On Side': 0,
#     'Gluten-Free (ask store for safe toppings)': 0,
#     'Hot Honey On Side': 0,
#     'Bowl Alredo Bacon Breadcrumbs Bricholi Jalepnos Galic Parm': 0,
#     'Bowl Chedder Chicken Jalepenos Bread Crumbs Buffalo Cheescake': 0,
#     'Mac Alfredo Chick Every Addition But Brocli And Pinapple Gar Parm Ches Gar Bread Dr Pep': 0,
#     'Apple Juice': 0,
#     'Dr. Pepper': 0,
#     'XL Shirt': 0,
#     'Chips': 0,
#     'Any Bag Of Chips': 0,
#     'Shirt': 0,
#     'Medium Shirt': 0
# }
#number of orders per unique modifier stored into a dictionary for each month (completed)
Parent_Menu_Selection_october_dict = {} 
Parent_Menu_Selection_september_dict = {}
Parent_Menu_Selection_august_dict = {} 
Parent_Menu_Selection_april_dict = {} 
Parent_Menu_Selection_may_dict = {}
Parent_Menu_Selection_june_dict = {} 
Parent_Menu_Selection_july_dict = {} 





#Creating predictive model for sales
# arr = np.random.normal(1, 1, size=100)
# fig, ax = plt.subplots()
# ax.hist(arr, bins=20)

# st.pyplot(fig)


#Sorting data into a list 
april_data = open('april_2024.csv', 'r')
april_data_String = april_data.read()
april_data_List = april_data_String.split('\n')
for i in range(len(april_data_List)):
    april_data_List[i] = april_data_List[i].split(',') 
april_data_List.pop(0)
april_data_List.pop(len(april_data_List)-1)
#print(april_data_List)

august_data = open('august_2024.csv', 'r')
august_data_String = august_data.read()
august_data_List = august_data_String.split('\n')
for i in range(len(august_data_List)):
    august_data_List[i] = august_data_List[i].split(',') 
august_data_List.pop(0)
august_data_List.pop(len(august_data_List)-1)
#print(august_data_List)

july_data = open('july_2024.csv', 'r')
july_data_String = july_data.read()
july_data_List = july_data_String.split('\n')
for i in range(len(july_data_List)):
    july_data_List[i] = july_data_List[i].split(',') 
july_data_List.pop(0)
july_data_List.pop(len(july_data_List)-1)
#print(july_data_List)

june_data = open('june_2024.csv', 'r')
june_data_String = june_data.read()
june_data_List = june_data_String.split('\n')
for i in range(len(june_data_List)):
    june_data_List[i] = june_data_List[i].split(',') 
june_data_List.pop(0)
june_data_List.pop(len(june_data_List)-1)
#print(june_data_List)

may_data = open('may_2024.csv', 'r')
may_data_String = may_data.read()
may_data_List = may_data_String.split('\n')
for i in range(len(may_data_List)):
    may_data_List[i] = may_data_List[i].split(',') 
may_data_List.pop(0)
may_data_List.pop(len(may_data_List)-1)
#print(may_data_List)

october_data = open('october_2024.csv', 'r')
october_data_String = october_data.read()
october_data_List = october_data_String.split('\n')
for i in range(len(october_data_List)):
    october_data_List[i] = october_data_List[i].split(',')
october_data_List.pop(0) 
october_data_List.pop(len(october_data_List)-1)
#print(october_data_List)

september_data = open('september_2024.csv', 'r')
september_data_String = september_data.read()
september_data_List = september_data_String.split('\n')
for i in range(len(september_data_List)):
    september_data_List[i] = september_data_List[i].split(',') 
september_data_List.pop(0) 
september_data_List.pop(len(september_data_List)-1)
#print(september_data_List)

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

#allMonths_data[day number represented as an int][Specific piece of information you need ]


#number of orders per unique modifier stored into a dictionary for each month 
for entry in april_data_List:
    item = entry[2]
    if item in Parent_Menu_Selection_april_dict:
        Parent_Menu_Selection_april_dict[item] += 1
    else:
        Parent_Menu_Selection_april_dict[item] = 1
#print(Parent_Menu_Selection_april_dict)
for entry in may_data_List:
    item = entry[2]
    if item in Parent_Menu_Selection_may_dict:
        Parent_Menu_Selection_may_dict[item] += 1
    else:
        Parent_Menu_Selection_may_dict[item] = 1
#print(Parent_Menu_Selection_may_dict)
for entry in june_data_List:
    item = entry[2]
    if item in Parent_Menu_Selection_june_dict:
        Parent_Menu_Selection_june_dict[item] += 1
    else:
        Parent_Menu_Selection_june_dict[item] = 1
#print(Parent_Menu_Selection_june_dict)
for entry in july_data_List:
    item = entry[2]
    if item in Parent_Menu_Selection_july_dict:
        Parent_Menu_Selection_july_dict[item] += 1
    else:
        Parent_Menu_Selection_july_dict[item] = 1
#print(Parent_Menu_Selection_july_dict)
for entry in august_data_List:
    item = entry[2]
    if item in Parent_Menu_Selection_august_dict:
        Parent_Menu_Selection_august_dict[item] += 1
    else:
        Parent_Menu_Selection_august_dict[item] = 1
#print(Parent_Menu_Selection_august_dict)
for entry in september_data_List:
    item = entry[2]
    if item in Parent_Menu_Selection_september_dict:
        Parent_Menu_Selection_september_dict[item] += 1
    else:
        Parent_Menu_Selection_september_dict[item] = 1
#print(Parent_Menu_Selection_september_dict)
for entry in october_data_List:
    item = entry[2]
    if item in Parent_Menu_Selection_october_dict:
        Parent_Menu_Selection_october_dict[item] += 1
    else:
        Parent_Menu_Selection_october_dict[item] = 1
#print(Parent_Menu_Selection_october_dict)


#average time of business










#Predicting monthly sales for upcoming months


#chart shown on website 

