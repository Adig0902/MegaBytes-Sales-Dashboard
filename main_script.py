import pandas as pd
from colorama import Fore, Style
import sys
import os
import matplotlib.pyplot as plt
from data_extract_clean import *
from analysis_functions import *
from graphs import *

# -------------------------------------------------------------------------
# Filepaths for Excel till data

sale_data_file_names = [
    "data\\monday_data.xlsx",
    "data\\tuesday_data.xlsx",
    "data\\wednesday_data.xlsx",
    "data\\thursday_data.xlsx",
    "data\\friday_data.xlsx",
    "data\\saturday_data.xlsx",
    "data\\sunday_data.xlsx",
]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN Function
# -to pull Data from database, extract day names, concatonate to week data
# -to apply other functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# -------------------------------------------------------------------------
# MAIN Function
def main_analysis(file_names):
    void_data_week = pd.DataFrame(columns=["Staff", "Number of Void Transactions"])
    week_data = pd.DataFrame()  # Dataframe to store results for whole week

    for file_name in file_names:
        day_name = extract_day_name(file_name)
        df = pd.read_excel(file_name)
        df_void = df.copy()

        # Handle void data calculations before cleaning database
        print(f"Void Data For {day_name}:")
        void_data = void_transaction_data(df_void)
        new_void_data = pd.DataFrame(
            {"Staff": void_data.index, "Number of Void Transactions": void_data.values}
        )
        void_data_week = pd.concat([void_data_week, new_void_data], ignore_index=True)
        # Call the plot graph function
        plot_void_transaction_data(void_data, day_name)
        cleaned_df = extract_and_clean(df)
        # show what day it is related to
        cleaned_df["Day of Week"] = day_name

        # Concatenate current df with week data
        week_data = pd.concat([week_data, cleaned_df], ignore_index=True)

        # analysis functions for individual day
        print(f"\nData for {Fore.BLUE}{day_name.capitalize()}{Style.RESET_ALL}\n\n")

        # 6 Values for each day bundle
        for_each_day_find(cleaned_df)
        save_output_to_file(
            for_each_day_find,
            r"website\static\data_results\daily_insights_folder",
            f"daily_results_{day_name}",
            cleaned_df,
        )

    # analysis for the week
    print(f"{Fore.GREEN}Data For Whole Week{Style.RESET_ALL}\n\n")
    payment_methods_analysis(week_data)
    save_output_to_file(
        payment_methods_analysis,
        r"website\static\data_results\week_insight_folder",
        f"payments_methods_analysis_week.txt",
        week_data,
    )
    max_cost_analysis(week_data)
    save_output_to_file(
        max_cost_analysis,
        r"website\static\data_results\week_insight_folder",
        f"max_cost_analysis_week.txt",
        week_data,
    )
    product_popularity_count(week_data)
    save_output_to_file(
        product_popularity_count,
        r"website\static\data_results\week_insight_folder",
        f"product-popularity_count_week.txt",
        week_data,
    )
    mvp_staff_member(week_data)
    save_output_to_file(
        mvp_staff_member,
        r"website\static\data_results\week_insight_folder",
        f"mvp_staff_member_week.txt",
        week_data,
    )

    # Week income graph
    total_income_week(week_data)
    # Void data for week
    save_summary_void_data(void_data_week)
    save_output_to_file(
        save_summary_void_data,
        r"website\static\data_results\week_insight_folder",
        f"void_transaction_data_week.txt",
        void_data_week,
    )
    print(f"Void Data For Week:\n{save_summary_void_data(void_data_week)}")
    # Store results in the week dataframe

    return week_data, void_data_week


###########################################################################
# Create graphs for daily insights
# Call the function
week_data, void_data_week = main_analysis(sale_data_file_names)


for day_name in week_data["Day of Week"].unique():
    day_data = week_data[week_data["Day of Week"] == day_name]

    # Create a new figure for each day
    fig, ax = plt.subplots(figsize=(15, 8))

    # Plot item popularity chart
    plot_item_popularity_chart(day_data, day_name, ax)

    # Plot payment methods pie chart
    plot_payment_methods_pie_chart(day_data, day_name)

    plt.close(fig)

# create graphs for week insights
plot_item_popularity_chart_week(week_data)

plot_payment_methods_pie_chart_week(week_data)

plot_void_transaction_data_week(void_data_week)

###########################################################################
