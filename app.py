import streamlit as st
import numpy as np
import pandas as pd
# import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
# import data
import plotly.express as px
import streamlit as st
from openai import OpenAI
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
import random
import time
from pytrends.request import TrendReq
import matplotlib.dates as mdates

#This line talks to the other file, call variables or functions from the other file using dot notation 

#make sure to save the other file before running this one 

# Logo top left
st.sidebar.markdown(
    f"<h1 style='color: #F5B84E; font-size: 48px;'>RoniBot's Analytics</h1>",
    unsafe_allow_html=True
)

image_path = "ronisMacbarIcon.png"
TopleftIcon_path= "TopleftIcon.jpg"
st.sidebar.image(TopleftIcon_path, use_container_width=False, width=150)

# Sidebar navigation

page = st.sidebar.radio("Select a Page:", [
    "🏠 Home",
    "📊 Parent Menu Order Totals",
    "⭐ Modifiers by Popularity",
    "📅 Total Sales per Month",
    "⏰ Sales Throughout the Day",
    "📈 Ronis Cstat Internet Trends",
    "🤖 Talk to RoniBot"
])

# Show a loading message when switching pages

loading_messages = [
    "🍲 Cooking up some data magic...",
    "🍜 Stirring the macaroni...",
    "🧀 Gathering the cheese...",
    "🔢 Crunching numbers...",
    "🔥 Heating up the stats...",
    "🥄 Mixing in the modifiers...",
    "🔍 Preparing your insights..."
]
if page != "🤖 Talk to RoniBot":
    with st.spinner(random.choice(loading_messages)):
        time.sleep(3)  # Simulate loading time (adjust the duration as needed)



# Customizable parameters
fig_width = 8  # Width of the figure
fig_height = 6  # Height of the figure
bar_color = '#F5B84E'  # Color of the bars
background_color = '#000000'  # Background color of the plot
font_color = 'white'  # Color of the font for labels and title
label_offset = 400  # Distance of the labels from the bars (adjust for better positioning)

# Define content for each page based on st.session_state["page"]
if page == "🏠 Home":
    # Title Page Content
    st.markdown(
        """
        <h1 style='color: #F5B84E;'>Welcome to RoniBot's data Dashboard!</h1>
        """,
        unsafe_allow_html=True
    )
    st.subheader("Explore Insights, Data, and More!")
    st.write("""
    Here, you can dive into data visualizations, explore 
    menu insights, and view AI-driven predictions by talking to RoniBot to help understand trends and make informed decisions.
    Select an option from the sidebar to get started!
    """)


   
    # Optional: Add an image or logo for the home page
    st.image(image_path, caption="Roni's Mac Bar - Where flavor meets data!", use_container_width=True)

    st.subheader("Data Sets Utilized:")
        # List of file paths and labels
    file_paths = {
        "April 2024 Data": "april_2024.csv",
        "May 2024 Data": "may_2024.csv",
        "June 2024 Data": "june_2024.csv",
        "July 2024 Data": "july_2024.csv",
        "August 2024 Data": "august_2024.csv",
        "September 2024 Data": "september_2024.csv",
        "October 2024 Data": "october_2024.csv"
    }

    # Dropdown to select the month
    selected_label = st.selectbox("Select a Month for Download:", list(file_paths.keys()))
    selected_file = file_paths[selected_label]

    # Load the selected CSV file
    try:
        df = pd.read_csv(selected_file, encoding='ISO-8859-1')

        # Display a download button for the selected file
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name=selected_file,
            mime="text/csv"
        )
    except UnicodeDecodeError:
        st.error(f"Could not read {selected_label} due to encoding issues.")

    # Add any other introductory text or insights
    st.write("""
             




    Developed for the Roni's Challenge for TamuDatathon 2024
    """)
    
if page == "📊 Parent Menu Order Totals":
    # Customizable variables
    pie_colors = ["#F5B84E", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494", "#b3b3b3"]
    edge_color = 'white'  # Border color of each pie slice for contrast
    font_size_percentage = 8
    font_size_label = 10
    font_size_legend = 10
    legend_position = "lower left"
    legend_bbox_to_anchor = (-0.3, -0.1)

    # Background and text colors
    background_color = 'black'
    text_color = 'white'

    # Dictionary mapping month names to their respective parent menu selection data
    parent_menu_data = {
        "April": data.Parent_Menu_Selection_april_dict,
        "May": data.Parent_Menu_Selection_may_dict,
        "June": data.Parent_Menu_Selection_june_dict,
        "July": data.Parent_Menu_Selection_july_dict,
        "August": data.Parent_Menu_Selection_august_dict,
        "September": data.Parent_Menu_Selection_september_dict,
        "October": data.Parent_Menu_Selection_october_dict
    }

    # Dropdown selection for the month
    selected_month = st.selectbox("Select a month to view parent menu selections", list(parent_menu_data.keys()))

    # Get the selected month's data
    selected_data = parent_menu_data[selected_month]

    # Convert the dictionary to a DataFrame and sort by frequency in descending order
    df = pd.DataFrame(list(selected_data.items()), columns=["Menu Item", "Frequency"])

    # Calculate total frequency to determine percentage thresholds
    total_frequency = df["Frequency"].sum()

    # Separate out items with <1% frequency and aggregate them into an "Other" category
    df["Percentage"] = (df["Frequency"] / total_frequency) * 100
    main_items = df[df["Percentage"] >= 1]
    other_items = df[df["Percentage"] < 1]

    # Calculate the "Other" category and add it to main_items if it exists
    other_total_frequency = other_items["Frequency"].sum()
    if other_total_frequency > 0:
        other_row = pd.DataFrame({
            "Menu Item": ["Other"],
            "Frequency": [other_total_frequency],
            "Percentage": [(other_total_frequency / total_frequency) * 100]
        })
        main_items = pd.concat([main_items, other_row], ignore_index=True)

    # Display the sorted table
    st.markdown(
        f"""
        <h1 style='color: #F5B84E;'>Parent Menu Selection Data for {selected_month}</h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"""
    ### Insights on Parent Menu Order Totals for {selected_month}

    This chart shows the popularity of each Parent Menu item in {selected_month}, helping identify high-demand categories 
    for better stock and preparation planning. Tracking these totals over time allows us to adjust menu offerings and highlight 
    popular items to enhance customer experience.

    Ask RoniBot for more information
    """)

    st.write("### Data Table of Parent Menu Selections")
    st.dataframe(main_items[["Menu Item", "Frequency", "Percentage"]].sort_values(by="Frequency", ascending=False))

    # Pie Chart
    st.write("### Pie Chart of Parent Menu Selections")

    # Prepare labels, hiding "Other" from the pie chart labels
    labels = [label if label != "Other" else '' for label in main_items["Menu Item"]]

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor(background_color)  # Set the figure background color
    ax.set_facecolor(background_color)  # Set the plot background color

    # Create the pie chart, scaling for readability and hiding labels below 10%
    wedges, texts, autotexts = ax.pie(
        main_items["Frequency"],
        labels=labels,
        colors=pie_colors,
        autopct=lambda pct: f'{pct:.1f}%' if pct >= 10 else '',
        startangle=90,
        wedgeprops={'edgecolor': edge_color}
    )

    # Customize labels and percentage text colors and font sizes
    for text in texts:
        text.set_color(text_color)
        text.set_fontsize(font_size_label)
    for autotext in autotexts:
        autotext.set_color(text_color)
        autotext.set_fontsize(font_size_percentage)

    # Customize legend text color to white
    legend = ax.legend(wedges, main_items["Menu Item"], title="Menu Items", loc=legend_position, 
                    bbox_to_anchor=legend_bbox_to_anchor, fontsize=font_size_legend)
    legend.get_title().set_color(text_color)  # Legend title color
    for text in legend.get_texts():
        text.set_color(text_color)  # Set legend item text color to white

    # Customize title appearance and text color
    ax.set_title(f"Data displayed for {selected_month}", color='#F5B84E')
    plt.tight_layout()  # Adjust layout to fit everything properly
    

    # Display the plot
    st.pyplot(fig)
    

elif page == "⭐ Modifiers by Popularity":
    # Dictionary mapping month names to their respective ranked modifier data
    month_data = {
        "April": data.ranked_modifiers_april,
        "May": data.ranked_modifiers_may,
        "June": data.ranked_modifiers_june,
        "July": data.ranked_modifiers_july,
        "August": data.ranked_modifiers_august,
        "September": data.ranked_modifiers_september,
        "October": data.ranked_modifiers_october
    }

    # Dropdown selection for the month
    selected_month = st.selectbox("Select a month to view top modifiers", list(month_data.keys()))

    st.markdown(f"""
    ### Insights on Modifier Popularity for {selected_month}

    This chart shows the top 20 modifiers selected by customers in {selected_month}, helping estimate demand 
    and reduce waste from oversupply. Tracking modifier trends over time also reveals seasonal preferences, 
    enabling adjustments to align with changing customer demand.

    Ask RoniBot for more information
    """)

    # Get the selected month's data
    selected_data = month_data[selected_month]

    # Convert the dictionary to a DataFrame with appropriate columns for the chart
    ranked_modifiers_df = pd.DataFrame(
        [(rank, item[0], item[1]) for rank, item in selected_data.items()],
        columns=["Rank", "Modifier Name", "Frequency"]
    )

    # Create a horizontal bar chart using matplotlib with customizable size
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    bars = ax.barh(ranked_modifiers_df["Modifier Name"], ranked_modifiers_df["Frequency"], color=bar_color)

    # Set labels and title with customizable font color
    ax.set_xlabel("Frequency", color=font_color)
    ax.set_ylabel("Modifier", color=font_color)
    ax.set_title(f"Top 20 Modifiers by Total Frequency Chosen ({selected_month})", color=font_color)
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest frequency at the top

    # Set colors for ticks and background
    ax.tick_params(axis='x', colors=font_color)
    ax.tick_params(axis='y', colors=font_color)
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    # Add labels to each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(width - label_offset, (bar.get_y() + bar.get_height() / 2) - 0.05, 
                f'{width}', va='center', color=font_color)

    # Display the chart in Streamlit
    st.markdown(
        f"""
        <h1 style='color: #F5B84E;'>Top 20 Modifiers by Popularity {selected_month}</h1>
        """,
        unsafe_allow_html=True
    )

    st.pyplot(fig)

    
elif page == "📅 Total Sales per Month":
    
        # Example `total_price` array
    total_price = data.total_price
    months = ['April', 'May', 'June', 'July', 'August', 'September', 'October']

    # Create a line chart with `matplotlib`
    fig, ax = plt.subplots()
    ax.plot(months, total_price, marker='o', color='#F5B84E', linestyle='-')
    ax.set_title("Total Monthly Sales", color='white')
    ax.set_xlabel("Month", color='white')
    ax.set_ylabel("Sales (USD)", color='white')

    # Set colors for ticks and background
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    fig.patch.set_facecolor('#000000')
    ax.set_facecolor('#000000')

    # Display the chart in Streamlit
    st.markdown(
        """
        <h1 style='color: #F5B84E;'>Total Monthly Sales Per Month</h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"""
    ### Insights on Monthly Sales

    This chart provides an overview of total sales through the months, helping to identify high and low sales periods 
    for more effective resource allocation. Tracking monthly sales trends allows for better inventory planning and 
    targeted marketing to align with seasonal demand patterns.
                
    Ask RoniBot for more information          
    """)

    st.pyplot(fig)

    # #Predicted model
    # future_months = ['November', 'December', 'January', 'February', 'March', 'April', 'May']
    # future_month_numbers = [11, 12, 1, 2, 3, 4, 5] 

    # months = np.array([4, 5, 6, 7, 8, 9, 10])  # Months 
    # sales = np.array(total_price)

    # model = LinearRegression()
    # model.fit(months.reshape(-1, 1), sales)

    # future_months_array = np.array(future_month_numbers).reshape(-1, 1)
    # future_sales_predictions = model.predict(future_months_array)

    # fig2, ax2 = plt.subplots(figsize = (10, 6))
    # ax2.plot(future_months_array, future_sales_predictions, marker = 'o', color='red', linestyle = '-')
    
    # #Titles
    # ax2.set_title("Predicted Monthly Sales", color='white')
    # ax2.set_xlabel("Month", color='white')
    # ax2.set_ylabel("Predicted Sales (USD)", color='white')
    
    # # X ticks for past and future months
    # all_months = np.concatenate([months, future_months_array.flatten()])
    # all_month_labels = np.concatenate([np.arange(4, 11), future_months])

    # # Set tick locations and tick labels
    # ax2.set_xticks(all_months)
    # ax2.set_xticklabels(np.concatenate([np.arange(4, 11), future_months]), color='white')

    # # Set background color
    # fig2.patch.set_facecolor('#000000')
    # ax2.set_facecolor('#000000')

    # ax2.tick_params(axis='x', colors='white')
    # ax2.tick_params(axis='y', colors='white')

    # st.pyplot(fig2)
    ################################################################################################
    # #Titles
    # ax.set_xlabel('Month')
    # ax.set_ylabel('Predicted Sales (USD)')
    # ax.set_title('Sales Forecast')

    # # Create a line chart with `matplotlib`
    # fig, ax = plt.subplots()
    # ax.plot(pred_months, total_price, marker='o', color='blue', linestyle='-')
    # ax.set_title("Predicted Monthly Sales", color='white')
    # ax.set_xlabel("Month", color='white')
    # ax.set_ylabel("Predicted Sales (USD)", color='white')

    # # Set colors for ticks and background
    # ax.tick_params(axis='x', colors='white')
    # ax.tick_params(axis='y', colors='white')
    # fig.patch.set_facecolor('#000000')
    # ax.set_facecolor('#000000')

    # # Display the chart in Streamlit
    # st.pyplot(fig)

    # ######

    # future_months = ['November', 'December', 'January']  # Future months to predict

    # # Assuming that 'total_price' corresponds to months 11 through 1.
    

    # # Step 2: Train the linear regression model using historical data
    

    # # Step 3: Predict future sales for 'future_month_numbers'
    

    # # Step 4: Plot the regression line and predictions
    # fig2, ax = plt.subplots(figsize=(10, 6))

    # # Plot the past data
    # ax.plot(months, sales, color='blue', marker='o', label='Historical Data')

    # # Plot the predicted future data
    # ax.plot(future_months_array, future_sales_predictions, color='red', label='Predicted Sales')

    # # Annotate the months
    # for i, txt in enumerate(future_months):
    #     ax.annotate(f"{future_sales_predictions[i][0]:.2f}", (future_months_array[i], future_sales_predictions[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='red')

    # # Add labels and title
    
    # ax.set_xticks(np.concatenate([months.flatten(), future_months_array.flatten()]))
    # ax.set_xticklabels(np.concatenate([np.arange(4, 11), future_months]))  # Use numbers for months (4-10 for historical, names for future)

    # # Show legend
    # ax.legend()

    # # Display the plot using Streamlit
    # st.pyplot(fig)



    #     # Create a DataFrame for total sales per month, rounding sales to 2 decimal places
    # sales_data = pd.DataFrame({
    #         "Month": months,
    #         "Total Sales (USD)": [round(sale, 2) for sale in total_price]
    #     })

    #     # Apply consistent color scheme to the entire DataFrame using `Styler`
    # styled_sales_data = sales_data.style.set_properties(**{
    #         'background-color': '#000000',    # Set background color for cells
    #         'color': '#F5B84E',               # Set text color
    #         'border-color': '#F5B84E'         # Set border color for cells
    #     }).set_table_styles([{
    #         'selector': 'th',
    #         'props': [('color', 'white'), ('background-color', '#000000')]
    #     }]).format({"Total Sales (USD)": "{:.2f}"})

    #     # Display the styled table in Streamlit using `st.write`
    # st.write(styled_sales_data)


elif page == "⏰ Sales Throughout the Day":

    
    # Set the hex color and styling parameters
    line_color = "#F5B84E"
    bg_color = "black"
    text_color = "white"

    # Dropdown to select the month
    selected_month = st.selectbox("Select a Month:", ["April", "May", "June", "July", "August", "September", "October"])


    st.markdown(
            f"""
            <h1 style='color: #F5B84E;'>Total Sales Throughout {selected_month}</h1>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown(f"""
    ### Insights on Order Frequency by Time of Day for {selected_month}

    This chart shows order distribution across the day in {selected_month}, highlighting peak and off-peak hours to 
    help optimize staff scheduling and inventory. Tracking these trends allows us to plan promotions, anticipate busy 
    times, and better align resources with demand patterns throughout the day.

    Ask RoniBot for more information
    """)


    # Mapping of month names to their corresponding data dictionaries in the data module
    month_data_map = {
        "April": data.april_orders_by_time,
        "May": data.may_orders_by_time,
        "June": data.june_orders_by_time,
        "July": data.july_orders_by_time,
        "August": data.august_orders_by_time,
        "September": data.september_orders_by_time,
        "October": data.october_orders_by_time,
    }

    # Retrieve the selected month's data
    selected_data = month_data_map[selected_month]

    # Sort the data by time for plotting
    sorted_times = sorted(selected_data.keys())
    sorted_counts = [selected_data[time] for time in sorted_times]

    # Plotting the line graph with customized colors
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_times, sorted_counts, color=line_color, marker='o')
    plt.xlabel("Time of Day (Hour)", color=text_color)
    plt.ylabel("Count of Orders", color=text_color)
    plt.title(f"Orders by Time of Day for {selected_month}", color=text_color)
    plt.xticks(rotation=45, color=text_color)
    plt.yticks(color=text_color)
    plt.grid(True, color=line_color, linestyle='--', linewidth=0.5)
    plt.gca().set_facecolor(bg_color)  # Set plot background to black
    plt.gcf().patch.set_facecolor(bg_color)  # Set figure background to black

    # Display the plot in Streamlit
    st.pyplot(plt)

    
elif page == "📈 Ronis Cstat Internet Trends":
        # Initialize pytrends
    pytrends = TrendReq(hl='en-US', tz=360)

    # Set the line color and background/text colors
    line_color = "#F5B84E"
    bg_color = "black"
    text_color = "white"

    st.markdown(
    f"<h1 style='color: #F5B84E;'>Google Trends Data Graph Generator</h1>",
    unsafe_allow_html=True
    )
    # Text input for user to enter a keyword
    st.text('Example keywords: Ronis, Macaroni, Food at College Station')
    keyword = st.text_input("Enter a keyword to see its Google Trends over time:")
    

    # Generate and display the trend graph if a keyword is entered
    if keyword:
        try:
            # Build payload for the entered keyword
            pytrends.build_payload([keyword], cat=0, timeframe='today 5-y', geo='', gprop='')

            # Retrieve interest over time data
            data = pytrends.interest_over_time()

            if not data.empty:
                # Drop the 'isPartial' column for cleaner data
                data = data.drop(labels=['isPartial'], axis='columns')
                
                # Resample data to monthly frequency using the average value for each month
                monthly_data = data[keyword].resample('M').mean()

                # Plot the data with specified styles
                plt.figure(figsize=(10, 5))
                plt.plot(monthly_data.index, monthly_data, color=line_color, linewidth=2, marker='o')
                plt.title(f"Google Trends Interest Over Time for '{keyword}'", color=text_color)
                plt.xlabel("Date (Yearly)", color=text_color)
                plt.ylabel("Interest", color=text_color)
                plt.xticks(color=text_color)
                plt.yticks(color=text_color)
                
                # Set x-axis to show only the year
                plt.gca().xaxis.set_major_locator(mdates.YearLocator())  # Display ticks only at the start of each year
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
                
                # Set the grid and background colors
                plt.grid(True, color=line_color, linestyle='--', alpha=0.5)
                plt.gca().set_facecolor(bg_color)  # Set plot background to black
                plt.gcf().patch.set_facecolor(bg_color)  # Set figure background to black

                # Display the keyword's data as a line chart in Streamlit
                st.pyplot(plt)
                plt.close()
            else:
                st.write(f"No data found for '{keyword}'.")

        except Exception as e:
            # Display any error that occurs during processing
            st.error(f"An error occurred: {e}")


    st.markdown(f"""
    ### Interest Value Explained
    In Google Trends, the y-axis labeled "Interest" shows a term’s popularity over time on a scale from 0 to 100. 
    A value of 100 is the peak popularity, 50 indicates half of the peak interest, and 0 represents very low or no search activity.

    ### Insights on Google Trends Data
    This chart shows search interest trends for a keyword, helping identify high-interest periods for marketing adjustments. 
    By tracking trends over time, we can anticipate shifts in consumer preferences and plan inventory, staffing, and promotions accordingly.
                
    Ask RoniBot for more information
    """)
elif page == "🤖 Talk to RoniBot":
    st.markdown(
        """
        <h1 style='color: #F5B84E;'>Welcome to RoniBot 🤖🧀</h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
        ### Speak to RoniBot for insights and analysis of the sales according to the datasets provided
        Ask RoniBot "What are some data sets you can provide me?" to get started
                

        
    """)

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
          # Add an initial system message to guide the assistant
        #how to act prompts
        st.session_state.messages = [{"role": "system", "content": "You are RoniBot, an AI assistant for Roni's Mac Bar. Answer questions based on sales and menu insights, and provide analysis when asked. If unsure, respond with 'I would need more information to provide an accurate answer.', If prompted to do a calculation, always use the data that I am about to give you and output the calculation in your response."}]
        #prompts for modifiers  
        st.session_state.messages += [{"role": "system", "content": "If I ask you What datasets you could provide, please only say Parent menu order totals, Total Modifiers purchased per month, Total sales by month, sales throughout the day, however also say: RoniBot will try my best!"}]
        st.session_state.messages += [{"role": "system", "content": "I will give you dictionaries of datasets through these prompts, please remember this data for me"}]
        st.session_state.messages += [{"role": "system", "content": "This is April's data set in this format: modifier : counts {'Regular': 4910, 'Cheddar': 3236, 'Pulled Pork': 496, 'Broccoli': 1300, 'Tomatoes': 853, 'Breadcrumbs': 3145, 'BBQ': 1201, 'No Side': 3046, 'Water': 639, 'Pepper Jack': 916, 'Brisket': 1924, 'Corn': 1008, 'Mushrooms': 1314, 'Parmesan': 3360, 'No Drink': 3542, 'Alfredo': 819, 'Jalapenos': 920, 'Unlimited Fountain Drinks': 935, 'No Toppings': 488, 'Cheesy Broccoli': 1, 'Cheesy Garlic Bread': 1520, 'No Meat': 898, 'No Drizzle': 957, 'Pepperjack': 1, 'Bacon': 1196, 'Garlic Parmesan': 1938, 'Grilled Chicken': 1656, 'Bell Peppers': 840, 'Hot Honey': 592, 'Garlic Bread': 597, 'Ranch': 968, 'Cheesecake': 272, 'Buffalo': 831, 'Ham': 129, 'Melted Cheddar': 225, 'No Mac': 134, 'Pesto': 496, 'Sprite': 41, 'Coke': 165, 'Pepper Jack Mac': 61, 'Pineapple': 262, 'Melted Pepper Jack': 95, 'MIX': 23, 'Mix PJ And Cheddar': 1, 'GLUTEN FREE': 1, 'Melted Parmesan': 50, 'Cheddar Mac': 152, 'Alfredo Mac': 35, 'Side Mac': 63, 'Diet Coke': 38, 'Onions': 1502, 'Onion': 1, 'All Cheese!!!': 1, 'I DO NOT NEED UTENSILS (Save waste!)': 14, 'O J And BP On Side': 1, 'Bacon On Side': 1, 'Hot Honey On Half': 1, 'MIXED Melted Cheese': 1, 'Bbq On Side': 1, 'Gluten-Free (ask store for safe toppings)': 39, 'Hot Honey On Side': 1, 'Bowl Alredo Bacon Breadcrumbs Bricholi Jalepnos Galic Parm': 1, 'Bowl Chedder Chicken Jalepenos Bread Crumbs Buffalo Cheescake': 1, 'Mac Alfredo Chick Every Addition But Brocli And Pinapple Gar Parm Ches Gar Bread Dr Pep': 1, 'Apple Juice': 64, 'Dr. Pepper': 10, 'XL Shirt': 1, 'Chips': 1, 'Any Bag Of Chips': 66, 'Shirt': 1, 'Medium Shirt': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "This is May's data set in this format: modifier : counts {'Melted Cheddar': 277, 'No Mac': 201, 'Brisket': 1698, 'Broccoli': 1151, 'Mushrooms': 879, 'Ranch': 919, 'Cheesy Garlic Bread': 1498, 'No Drink': 2927, 'Regular': 4576, 'Alfredo': 686, 'Grilled Chicken': 1535, 'Onions': 1367, 'Jalapenos': 1037, 'Bell Peppers': 887, 'Parmesan': 2950, 'Buffalo': 721, 'Any Bag Of Chips': 110, 'Cheddar': 3070, 'Breadcrumbs': 2763, 'BBQ': 1247, 'Cheesecake': 307, 'Unlimited Fountain Drinks': 1528, 'Pepper Jack': 923, 'No Meat': 871, 'No Toppings': 596, 'No Drizzle': 933, 'Garlic Bread': 543, 'Bacon': 1208, 'No Side': 2859, 'Tomatoes': 774, 'Garlic Parmesan': 1702, 'Pesto': 559, 'Corn': 1103, 'Pulled Pork': 534, 'Melted Pepper Jack': 132, 'Hot Honey': 504, 'Ham': 198, 'Water': 376, 'Cheddar Mac': 175, 'Gluten-Free (ask store for safe toppings)': 43, 'Alfredo Mac': 42, 'Melted Parmesan': 60, 'Pineapple': 274, 'Doritos': 10, 'Apple Juice': 79, 'I DO NOT NEED UTENSILS (Save waste!)': 159, 'Pepper Jack Mac': 59, 'No Cheese On Top And No Oven': 1, 'MIX': 49, 'MIXED Melted Cheese': 5, 'No Butter': 1, 'Medium Shirt': 2, 'Dr. Pepper': 73, 'Coke': 27, 'Texas BBQ (Pepper Jack': 3, 'TEST ORDER DO NOT MAKE!!!!!!!!': 1, 'Sprite': 49, 'Side Mac': 74, 'Lays Classic': 9, 'Diet Coke': 34, 'Brystol': 1, 'Piper': 3, 'James': 1, 'Powerade - Blue Mountain Berry Blast': 22, 'NO CHEESE': 2, 'No Noodles': 1, 'Chicken Bacon Ranch (Cheddar': 3, 'Fanta Orange': 14, 'Minute Maid Lemonade': 9, 'Mixed Cheese Side Mac': 1, 'No Shred No Oven': 1, 'Cheetos': 7, 'Barq's Root Beer': 49, 'Classic Mac (Cheddar': 2, 'This is a test order. Do not prepare the food.': 1, '': 1, 'No ice with drink': 1, 'no ice': 1, 'Can I get the hot honey on the side separate pleas': 1, 'Large Shirt': 2, 'Small Shirt': 2, 'Lays Barbecue': 3, 'plz hella broccoli ': 1, 'Garlic Bread (Feeds 10)': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "This is June's data set in this format: modifier : counts {'Regular': 2046, 'Cheddar': 1398, 'No Meat': 368, 'Corn': 433, 'Parmesan': 1207, 'Breadcrumbs': 1071, 'BBQ': 574, 'Garlic Parmesan': 667, 'Hot Honey': 220, 'Cheesy Garlic Bread': 648, 'No Drink': 1242, 'Brisket': 791, 'Onions': 617, 'Bell Peppers': 381, 'No Side': 1294, 'Unlimited Fountain Drinks': 832, 'Melted Parmesan': 30, 'Alfredo Mac': 26, 'Grilled Chicken': 684, 'Mushrooms': 451, 'No Drizzle': 515, 'Pulled Pork': 251, 'Bacon': 555, 'Pesto': 229, 'No Toppings': 343, 'Pepper Jack': 393, 'Ranch': 384, 'Garlic Bread': 266, 'Melted Cheddar': 161, 'No Mac': 138, 'Alfredo': 346, 'Broccoli': 496, 'Pineapple': 113, 'Cheesecake': 156, 'Water': 138, 'Cheddar Mac': 70, 'Buffalo': 277, 'Dr. Pepper': 53, 'Diet Coke': 30, 'Barq's Root Beer': 29, 'Any Bag Of Chips': 86, 'Sprite': 40, 'Gluten-Free (ask store for safe toppings)': 43, 'Ham': 106, 'Powerade - Blue Mountain Berry Blast': 11, 'Coke': 14, 'I DO NOT NEED UTENSILS (Save waste!)': 97, 'Apple Juice': 25, 'would it be possible to get extra cheese and sauce': 1, 'if available add tomato and jalapeño': 1, 'Melted Pepper Jack': 63, 'Pepper Jack Mac': 23, 'MIX': 43, 'Side Mac': 63, 'Cheetos': 9, 'Lays Barbecue': 6, 'Doritos': 5, 'Jalapenos': 412, 'Tomatoes': 275, 'Need utensils': 1, 'MIXED Melted Cheese': 2, 'Fanta Orange': 3, 'Extra broccoli and mushrooms please': 1, 'Minute Maid Lemonade': 7, 'Please put the barbecue sauce on the side if possible': 1, 'bbq sauce and hot honey on the side please': 1, 'Lays Classic': 3, 'NO CHEESE': 2, 'May I get extra BBQ sauce?': 1, 'Extra mushrooms': 1, 'Classic Mac (Cheddar': 1, 'Ectra buffalo if you can': 1, 'Extra buffalo': 1, 'I want Alfredo cheese TOO if that's possible': 1, 'All Vegetarian': 1, 'Buffalo Chicken (Cheddar': 1, 'Ranch and buffalo on the side': 1, 'Garlic Bread (Feeds 10)': 2, 'Extra BBQ Sauce on the side please': 1, 'cheddar AND alfredo if possible :)': 1, 'extra BBQ sauce please': 1, 'Texas BBQ (Pepper Jack': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "This is July's data set in this format: modifier : counts {'Regular': 2465, 'Alfredo': 564, 'Grilled Chicken': 805, 'Broccoli': 506, 'Onions': 770, 'Jalapenos': 562, 'Tomatoes': 400, 'Pesto': 260, 'No Side': 1615, 'No Drink': 1605, 'Cheddar': 1661, 'Corn': 505, 'Bell Peppers': 502, 'Breadcrumbs': 1324, 'BBQ': 720, 'Cheesecake': 94, 'Unlimited Fountain Drinks': 787, 'Pepper Jack': 615, 'Pulled Pork': 338, 'Brisket': 934, 'Mushrooms': 560, 'Parmesan': 1457, 'Ranch': 425, 'Hot Honey': 261, 'Cheesy Garlic Bread': 751, 'Water': 143, 'Melted Cheddar': 146, 'No Mac': 117, 'No Meat': 381, 'No Drizzle': 560, 'Sprite': 30, 'Buffalo': 337, 'Garlic Parmesan': 737, 'Melted Pepper Jack': 66, 'Pineapple': 148, 'Garlic Bread': 258, 'No Toppings': 357, 'Bacon': 634, 'Cheddar Mac': 70, 'Barq's Root Beer': 32, 'Side Mac': 58, 'Doritos': 14, 'Diet Coke': 28, 'Dr. Pepper': 72, 'I DO NOT NEED UTENSILS (Save waste!)': 183, 'Cheetos': 8, 'Melted Parmesan': 26, 'Powerade - Blue Mountain Berry Blast': 21, 'Coke': 30, 'Any Bag Of Chips': 75, 'Ham': 129, 'Lays Barbecue': 4, 'Lays Classic': 10, 'Gluten-Free (ask store for safe toppings)': 28, 'MIX': 325, 'Fanta Orange': 5, 'Apple Juice': 39, 'Minute Maid Lemonade': 25, 'Extra cheese sauce': 1, 'Pepper Jack Mac': 30, 'Avery': 1, 'Sarah': 1, 'Alfredo Mac': 24, 'Chicken Alfredo (Alfredo': 1, 'Have a great day!': 1, 'Classic Mac (Cheddar': 3, 'extra bell pepper and pesto please ': 1, 'Garden Mac (Cheddar': 1, 'bacon on the side': 1, 'fuck me up bowl please ??': 1, 'barbecue sauce on the side please ': 2, 'pesto on the side please ': 1, 'could I please do cheddar and pepper jack ': 1, 'If possible': 3, 'all three cheese please': 1, 'all three cheeses please ': 1, 'extra cheese please!': 1, 'Can I have all of the cheeses please': 1, 'can I have pepper jack if available? if no cheddar': 1, 'if possible': 1, 'I want cheddar Mac over Alfredo if available.': 1, 'I want f me up bowl. Couldn't choose all cheeses.': 1, 'Extra extra BBQ sauce please.': 2, 'can y'all do extra cheese/sauce please? Thank you!': 1, 'extra cheese and sauce please! Thank you!': 1, 'Please also add pepper jack cheese if possible! Thank you :) ': 1, '2X Shirt': 1, 'can I get all 3 cheeses (f me up)': 1, 'Please put BBQ on side and not in bowl': 1, 'Please put Buffalo sauce on side and not in bowl': 1, 'buffalo sauce on the side': 1, 'Include utensils': 1, 'Add alfredo and pepper jack cheese as well!': 2, 'half cheddar and half alfredo please': 1, 'can I get all 3 sauces (f me up :)': 1, 'plz hella broccoli ': 1, 'can you make it a fuck me up please': 1, 'Texas BBQ (Pepper Jack': 1, 'Buffalo Chicken (Cheddar': 1, 'Chicken Bacon Ranch (Cheddar': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "This is August's data set in this format: modifier : counts {'Regular': 3736, 'Alfredo': 950, 'Ham': 171, 'Parmesan': 2256, 'Ranch': 728, 'Garlic Bread': 390, 'No Drink': 2375, 'Please do not bake this one. Ranch on the side.': 1, 'Pepper Jack': 1008, 'Pulled Pork': 356, 'Onions': 1171, 'BBQ': 969, 'Cheddar': 2771, 'Corn': 950, 'Tomatoes': 671, 'No Side': 2687, 'Water': 398, 'Brisket': 1384, 'Breadcrumbs': 2103, 'Bell Peppers': 763, 'MIX': 868, 'Jalapenos': 813, 'Pineapple': 217, 'Hot Honey': 457, 'Bacon': 953, 'No Drizzle': 854, 'Cheesy Garlic Bread': 983, 'Melted Cheddar': 229, 'Cheddar Mac': 126, 'I DO NOT NEED UTENSILS (Save waste!)': 178, 'Broccoli': 894, 'Mushrooms': 860, 'Garlic Parmesan': 1252, 'Melted Parmesan': 43, 'Pepper Jack Mac': 29, 'No Mac': 180, 'No Toppings': 503, 'Grilled Chicken': 1341, 'Buffalo': 537, 'Unlimited Fountain Drinks': 1146, 'Pesto': 486, 'No Meat': 681, 'Any Bag Of Chips': 70, 'Cheesecake': 137, 'Buffalo Chicken (Cheddar': 3, 'Texas BBQ (Pepper Jack': 4, 'Garden Mac (Cheddar': 3, 'Chicken Bacon Ranch (Cheddar': 3, 'Classic Mac (Cheddar': 6, 'Apple Juice': 54, 'Sprite': 57, 'Minute Maid Lemonade': 26, 'Alfredo Mac': 35, 'Barq's Root Beer': 34, 'Cheetos': 8, 'Dr. Pepper': 54, 'Doritos': 11, 'Lays Classic': 5, 'Fanta Orange': 8, 'Melted Pepper Jack': 87, 'Gluten-Free (ask store for safe toppings)': 70, 'Lays Barbecue': 7, 'Side Mac': 59, 'Powerade - Blue Mountain Berry Blast': 32, '': 2, 'Diet Coke': 49, 'MIXED Melted Cheese': 4, 'Coke': 24, 'Small Shirt': 1, 'Garlic Bread (Feeds 10)': 1, 'Extra cheese and sauce please! Thank you!! :D': 1, 'all sauces on side except garlic Parm on Mac': 1, 'no shredded cheese': 1, 'NO CHEESE': 2, 'Cheddar cheese- not Alfredo. There was not an option to select cheddar listed. Please put drizzles in cup on the side': 1, 'sauce on side': 1, 'Broccoli on the side please. NOT on on Mac': 1, 'i need utensils': 1, 'can I have double bbq sauce please': 1, '2X Shirt': 1, 'Chicken Alfredo (Alfredo': 2, 'Large Chocolate Chunk Cookie': 27, '    can I get extra corn bell pepper and bread cr ': 1, 'Please add utensils': 1, 'Can you mix alfredo and pepper jack please?': 1, 'Very light drizzle please': 1, 'extra hit hot honey please!': 1, 'extra broccoli please': 1, 'extra bbq sauce please ': 1, 'extra garlic parm sauce ': 1, 'Please but the sauce on the side': 1, 'Please put the sauce on the side': 1, 'Could i get a blend of cheddar and afredo': 1, 'extra corn bell pepper ': 1, 'can you mix Alfredo and pepper jack together?': 1, 'Can you mix pepper jack and cheddar?': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "This is Septembers's data set in this format: modifier : counts {'Regular': 4301, 'Cheddar': 3195, 'Brisket': 1547, 'Broccoli': 1028, 'Breadcrumbs': 2578, 'Garlic Parmesan': 1604, 'Cheesy Garlic Bread': 947, 'Unlimited Fountain Drinks': 1427, 'Bacon': 1023, 'Corn': 1157, 'No Drizzle': 956, 'Grilled Chicken': 1471, 'No Side': 3238, 'Water': 269, 'Melted Cheddar': 244, 'No Mac': 179, 'No Meat': 927, 'Tomatoes': 854, 'BBQ': 1106, 'Any Bag Of Chips': 80, 'Pepper Jack': 1267, 'Alfredo': 1123, 'MIX': 1080, 'No Toppings': 501, 'Ranch': 894, 'No Drink': 2780, 'Parmesan': 2770, 'Pulled Pork': 388, 'Bell Peppers': 1045, 'Buffalo': 648, 'Onions': 1388, 'Mushrooms': 968, 'Large Chocolate Chunk Cookie': 70, 'Garlic Bread': 397, 'Side Mac': 61, 'Diet Coke': 42, 'Jalapenos': 1050, 'Powerade - Blue Mountain Berry Blast': 35, 'Alfredo Mac': 51, 'Pesto': 570, 'Cheddar Mac': 117, 'Hot Honey': 532, 'Gluten-Free (ask store for safe toppings)': 82, 'Ham': 170, 'Melted Parmesan': 51, 'Pepper Jack Mac': 40, 'I DO NOT NEED UTENSILS (Save waste!)': 215, 'Dr. Pepper': 83, 'Pineapple': 311, 'Barq's Root Beer': 53, 'Sprite': 78, 'Melted Pepper Jack': 85, 'Fanta Orange': 11, 'Cheesecake': 199, 'Apple Juice': 45, 'Minute Maid Lemonade': 32, 'Lays Barbecue': 13, 'Buffalo Chicken (Cheddar': 4, 'Coke': 37, 'extra extra corn bell peppers extra broccoli     ': 1, 'Cheetos': 9, 'Extra hot honey please!': 1, 'XL Shirt': 1, 'Can I get cheddar as well in the cheese option ': 1, 'Double baked pls ?': 1, 'Double baked again pls ?': 1, 'can you mixed the cheddar with Alfredo sauce ': 1, 'Classic Mac (Cheddar': 8, 'Texas BBQ (Pepper Jack': 4, 'Chicken Bacon Ranch (Cheddar': 4, 'Please give utensils.': 1, 'Garlic Bread (Feeds 10)': 3, 'Small Shirt': 1, 'Medium Shirt': 1, 'Doritos': 15, 'Can you add alfredo as well please?': 1, 'Lays Classic': 7, 'could you guys add more cheese plz and thank you': 1, 'Call me when you get here. (303)829-0937': 1, '': 1, 'Extra sauce please!': 1, 'add cheddar cheese with pepper Jack': 1, 'extra extra corn and bell peppers extra.  ': 1, 'MIXED Melted Cheese': 1, 'please add all the cheeses': 1, 'No drizzle please': 1, 'mix cheddar and Alfredo': 1, 'can i have a mix of pepper jack and cheddar please': 1, '  extra extra bell peppers extra extra corn extra ': 1, 'can i please get buffalo on the side ': 1, '(Please label for Aidan)': 2, 'NO CHEESE': 1, 'a little extra breadcrumbs for the crust please': 1, 'PLEASE No ice in Powerade and side of basil ': 1, 'please mark each meal so we can tell whose it is': 1, 'xtra sauce/cheese please! thanks!': 1, 'hot honey on side': 1, 'Dine In. Fountain drink. ': 1, 'Chicken Alfredo (Alfredo': 2, 'can i get extra pesto': 1, 'extra extra extra viggie ': 1, 'please add extra pineapples (for dine in)': 1, 'Extra drizzle of hot honey please!': 1, 'Extra onions': 1, 'Cheesy Broccoli': 1, 'I want that cheese pull :)': 1, '2X Shirt': 1, 'drizzles on the side please can': 1, 'can you add extra cheese and cup of melted cheddar': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "This is Octobers's data set in this format: modifier : counts {'Garden Mac (Cheddar': 3, 'Chicken Alfredo (Alfredo': 5, 'Texas BBQ (Pepper Jack': 2, 'Chicken Bacon Ranch (Cheddar': 6, 'Buffalo Chicken (Cheddar': 3, 'Classic Mac (Cheddar': 6, 'Regular': 3753, 'Cheddar': 2788, 'Brisket': 1339, 'Mushrooms': 900, 'Parmesan': 2423, 'Breadcrumbs': 2211, 'BBQ': 950, 'No Side': 2835, 'Cheesy Garlic Bread': 870, 'No Drink': 2578, 'Unlimited Fountain Drinks': 1206, 'Pepper Jack': 1087, 'Grilled Chicken': 1310, 'Ham': 175, 'Onions': 1281, 'Bell Peppers': 862, 'Cheesecake': 137, 'Bacon': 842, 'Garlic Parmesan': 1373, 'I DO NOT NEED UTENSILS (Save waste!)': 223, 'Broccoli': 904, 'Jalapenos': 849, 'Tomatoes': 747, 'Buffalo': 552, 'MIX': 938, 'Hot Honey': 466, 'Alfredo': 1000, 'No Drizzle': 823, 'Garlic Bread': 388, 'Ranch': 778, 'Corn': 1020, 'No Meat': 852, 'Minute Maid Lemonade': 28, 'Pesto': 567, 'Coke': 42, 'Sprite': 56, 'Pineapple': 259, 'Gluten-Free (ask store for safe toppings)': 95, 'No Toppings': 462, 'Water': 22, 'Diet Coke': 45, 'Dr. Pepper': 81, 'Barq's Root Beer': 37, 'Pulled Pork': 356, 'Melted Cheddar': 217, 'Cheddar Mac': 113, 'NO CHEESE': 7, 'Melted Pepper Jack': 81, 'Apple Juice': 26, 'No Mac': 171, 'Doritos': 14, 'Large Chocolate Chunk Cookie': 61, 'Lays Classic': 7, 'Pepper Jack Mac': 33, 'Melted Parmesan': 23, 'if possible': 1, 'Alfredo Mac': 41, 'Any Bag Of Chips': 67, 'Cheetos': 17, 'only a light drizzle of garlic Parmesan ': 1, 'extra hot honey drizzle plz': 1, 'XL Shirt': 1, 'Powerade - Blue Mountain Berry Blast': 34, 'Water Bottle': 119, 'Extra pesto please!': 1, 'Cheesy Broccoli': 1, 'not to toasted please :)': 1, 'Fanta Orange': 13, 'Lays Barbecue': 9, 'Double bake please!': 1, 'Double bake please if you feel like there's enough ingredients that it could be cold inside. I saw something about it on Google reviews and it's my first time as a customer with you guys. I don't want it overcooked but I also don't want it cold in the middle. Thanks!': 1, 'extra garlic drizzle': 1, 'alfredo and pepper jack please': 1, 'BBQ drizzle on only half would be great ': 1, 'extra extra extra viggie. ': 1, '2X Shirt': 1, 'Light on the jalapeÃ±os please!': 1, 'Garlic Parmesan on side': 1, 'light on the pesto drizzle please ! ': 1, 'Gouda': 6, 'Melted Parm': 20, 'extra extra hot honey please': 1, 'MIXED Melted Cheese': 4, 'Garlic Bread (Feeds 10)': 3, 'extra cheese please!': 1, 'Allergic to all citrus and vegetarian ': 1, 'not too heavy on the sauces': 1, 'Light PJ': 1, 'Drizzles on the SIDE please!! Ranch & Buffalo!!!!': 1, 'Extra drizzle of hot honey please!': 1, 'can you put every cheese on': 1, 'all 3 cheese': 1, 'Light JalapeÃ±os': 1, 'Light JalapeÃ±os please': 1}"}]
        #prompts for parents
        st.session_state.messages += [{"role": "system", "content": "This is April's data set for this format: ParentMenuSelection : Counts {'Mac and Cheese': 521, 'Grilled Cheese Sandwich': 332, 'Sides/Desserts': 131, 'Drinks': 72, 'MIX': 20, 'Mac and Cheese Party Tray (Plus FREE Garlic Bread': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "This is May's data set for this format: ParentMenuSelection : Counts {'Grilled Cheese Sandwich': 424, 'Mac and Cheese': 648, 'Drinks': 51, 'Sides/Desserts': 154, 'MIX': 49, 'Jalapenos': 3, 'Bacon': 3, 'Garlic Parmesan': 2, 'Mac and Cheese Party Tray (Plus FREE Garlic Bread': 1, 'Garlic Bread (Party Size': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "This is June's data set for this format: ParentMenuSelection : Counts {'Mac and Cheese': 363, 'Grilled Cheese Sandwich': 227, 'Sides/Desserts': 84, 'Drinks': 52, 'MIX': 41, 'Garlic Parmesan': 1, 'Onions': 1, 'Garlic Bread (Party Size': 2, 'Jalapenos': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "This is July's data set for this format: ParentMenuSelection : Counts {'Mac and Cheese': 627, 'Grilled Cheese Sandwich': 199, 'Sides/Desserts': 73, 'MIX': 323, 'Drinks': 54, 'Broccoli': 1, 'Garlic Parmesan': 2, 'Tomatos': 1, 'Jalapenos': 1, 'Onions': 1, 'Bacon': 1, 'Mac and Cheese Party Tray (Plus FREE Garlic Bread': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "This is August's data set for this format: ParentMenuSelection : Counts {'Mac and Cheese': 1294, 'MIX': 860, 'Grilled Cheese Sandwich': 306, 'Sides/Desserts': 98, 'Onions': 3, 'Jalapenos': 4, 'Tomatos': 3, 'Bacon': 3, 'Garlic Parmesan': 6, 'Mac and Cheese Party Tray (Plus FREE Garlic Bread': 1, 'Drinks': 51, 'Garlic Bread (Party Size': 1, 'Broccoli': 2}"}]
        st.session_state.messages += [{"role": "system", "content": "This is September's data set for this format: ParentMenuSelection : Counts {'Mac and Cheese': 1582, 'Grilled Cheese Sandwich': 337, 'MIX': 1073, 'Drinks': 75, 'Sides/Desserts': 136, 'Onions': 4, 'Garlic Parmesan': 5, 'Jalapenos': 4, 'Bacon': 4, 'Garlic Bread (Party Size': 3, 'Broccoli': 1, 'and breadcrumbs.': 1, 'Mac and Cheese Party Tray (Plus FREE Garlic Bread': 1}  "}]
        st.session_state.messages += [{"role": "system", "content": "This is October's data set for this format: ParentMenuSelection : Counts {'Tomatos': 2, 'Broccoli': 4, 'Jalapenos': 2, 'Bacon': 5, 'Onions': 3, 'Garlic Parmesan': 5, 'Mac and Cheese': 1344, 'Sides/Desserts': 91, 'MIX': 929, 'Drinks': 57, 'Grilled Cheese Sandwich': 298, 'Garlic Bread (Party Size': 1}"}]
        #prompts for prices
        st.session_state.messages += [{"role": "system", "content": "This is the prices for everything that Ronis MacBar at College station charges: {'Grilled Cheese Sandwich' : 8.99, 'Mac and Cheese' : 8.99, 'Pulled Pork' : 1.99, 'Grilled Chicken' : 1.99, 'Brisket' : 1.99, 'Bacon' : 1.99, 'Ham' : 1.99,'Garlic Bread' : 1.99,'Cheesy Garlic Bread' : 1.99,'Cheesecake' : 4.99,'Large Chocolate Chunk Cookie' : 4.99,'Doritos' : 1.99,'Cheetos' : 1.99,'Lays Barbecue' : 1.99,'Lays Classic' : 1.99,'Cheesy Broccoli' : 2.99,'Water' : 1.49,'Apple Juice' : 2.49,'Coke' : 1.99,'Dr. Pepper' : 1.99,'Sprite' : 1.99,'Diet Coke' : 1.99,'Powerade - Blue Mountain Berry Blast' : 1.99,'Minute Maid Lemonade' : 1.99,'XL Shirt' : 19.95,'Medium Shirt' : 19.95,'Shirt' : 19.95,'Small Shirt' : 19.95,'2X Shirt': 19.95,'Cheddar Mac' :  1.99,'Pepper Jack Mac' : 1.99,'Alfredo Mac' : 1.99'Mac and Cheese Party Tray (Plus FREE Garlic Bread)' : 39.99}"}]
        #prompts for total sales
        st.session_state.messages += [{"role": "system", "content": "the total sales of all months: 171261.63"}]
        st.session_state.messages += [{"role": "system", "content": "total sales of april: 26159.86"}]
        st.session_state.messages += [{"role": "system", "content": "total sales of may: 27400.600000000006"}]
        st.session_state.messages += [{"role": "system", "content": "total sales of june: 13510.430000000004"}]
        st.session_state.messages += [{"role": "system", "content": "total sales of july: 16614.77"}]
        st.session_state.messages += [{"role": "system", "content": "total sales of august: 27997.300000000003"}]
        st.session_state.messages += [{"role": "system", "content": "total sales of october: 27441.960000000003"}]
        st.session_state.messages += [{"role": "system", "content": "The most profitable month according to the data provided is september"}]
        #
        st.session_state.messages += [{"role": "system", "content": "Make sure that all the math you do is correct"}]
        #Sales throughout the day data
        st.session_state.messages += [{"role": "system", "content": "Here is April's data set for this format: TimeByHour : Number orders {'11:00': 401, '12:00': 719, '13:00': 553, '14:00': 518, '15:00': 483, '16:00': 366, '17:00': 456, '18:00': 567, '19:00': 616, '20:00': 438, '21:00': 272, '22:00': 45}"}]
        st.session_state.messages += [{"role": "system", "content": "Here is May's data set for this format: TimeByHour : Number orders {'11:00': 339, '12:00': 639, '13:00': 552, '14:00': 439, '15:00': 375, '16:00': 360, '17:00': 474, '18:00': 566, '19:00': 672, '20:00': 528, '21:00': 224, '22:00': 19, '09:00': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "Here is June's data set for this format: TimeByHour : Number orders {'11:00': 251, '12:00': 376, '13:00': 265, '14:00': 184, '15:00': 192, '16:00': 179, '17:00': 244, '18:00': 326, '19:00': 257, '20:00': 144, '21:00': 4, '00:00': 1, '09:00': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "Here is July's data set for this format: TimeByHour : Number orders {'11:00': 293, '12:00': 438, '13:00': 342, '14:00': 234, '15:00': 172, '16:00': 206, '17:00': 289, '18:00': 350, '19:00': 310, '20:00': 170, '10:00': 10, '22:00': 2, '00:00': 1}"}]
        st.session_state.messages += [{"role": "system", "content": "Here is August's data set for this format: TimeByHour : Number orders {'10:00': 8, '11:00': 365, '12:00': 531, '13:00': 470, '14:00': 357, '15:00': 339, '16:00': 290, '17:00': 406, '18:00': 509, '19:00': 602, '20:00': 374, '21:00': 6}"}]
        st.session_state.messages += [{"role": "system", "content": "Here is September's data set for this format: TimeByHour : Number orders {'11:00': 394, '12:00': 600, '13:00': 485, '14:00': 449, '15:00': 374, '16:00': 388, '17:00': 430, '18:00': 583, '19:00': 758, '20:00': 411, '07:00': 1, '10:00': 15, '09:00': 2, '21:00': 2}"}]
        st.session_state.messages += [{"role": "system", "content": "Here is October's data set for this format: TimeByHour : Number orders {'11:00': 398, '12:00': 531, '13:00': 408, '14:00': 464, '15:00': 379, '16:00': 386, '17:00': 380, '18:00': 484, '19:00': 561, '20:00': 283, '10:00': 3, '09:00': 1, '21:00': 8, '22:00': 1}"}]

        st.session_state.messages += [{"role": "system", "content": "If prompted about trends or Google Trends or Ronis Cstat Search trends, respond with : You can utilize Roni bots Handydandy 'Internet Trends Tool' located on the sidebar!"}]
        #st.session_state.messages += [{"role": "system", "content": ""}]
        
    for message in st.session_state.messages[35:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})


# fig=px.bar(x='total_bill',y='day', orientation='h')
# st.write(fig)
# data = 1
# # predict_inv = pd.DataFrame(list(data.items()), columns=['Product', 'Frequency'])

# # # Apply a 10% growth rate to predict next month's demand
# # growth_rate = 1.10
# # df['Predicted Next Month'] = df['Frequency'] * growth_rate
# # Display the DataFrame in Streamlit
# st.write("### Predicted Next Month's Demand")
# st.write(df)

# # Convert the DataFrame back to a dictionary with product names as keys and predicted frequencies as values
# predicted_data = pd.Series(df['Predicted Next Month'].values, index=df['Product']).to_dict()

# # Optionally, you can display the predicted data as a dictionary
# st.write("### Predicted Data (Dictionary Format)")
# st.write(predicted_data)