import pandas as pd
import os
import sys
import json
from colorama import Fore, Style


# -------------------------------------------------------------------------
#  Bundle these functions to clean up MAIN function


def for_each_day_find(cleaned_df):
    # 6 values to find for each day
    total_income_daily(cleaned_df)
    max_cost_analysis(cleaned_df)
    average_cost_basket(cleaned_df)
    best_selling_item(cleaned_df)
    worst_selling_item(cleaned_df)
    mvp_staff_member(cleaned_df)
    # Data for Daily Graphs
    product_popularity_count(cleaned_df)
    payment_methods_analysis(cleaned_df)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#                        For Each Day find:
#    -Total income        -Highest Spend        -Average Basket Spend
#    -Best Selling Item   -Worst Selling Item   -MVP Staff Member
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# -------------------------------------------------------------------------
#    Total income Daily


def total_income_daily(df):
    total_cost = df["Cost"].sum()
    print(f"Todays Total Income: {total_cost:.2f}")
    print()


# -------------------------------------------------------------------------
#    Highest Spend of a transaction


def max_cost_analysis(df):
    max_cost = df["Cost"].max()
    print(f"The highest Basket spend was: {max_cost:.2f}")
    print()


# -------------------------------------------------------------------------
#    Average Basket Spend


def average_cost_basket(df):
    average_cost = df["Cost"].mean()
    print(f"The average cost in a basket is: {average_cost:.2f}")
    print()


# -------------------------------------------------------------------------
#    Best Selling item


def best_selling_item(df):

    item_counts = pd.Series(
        [item for sublist in df["Basket"] for item in sublist]
    ).value_counts()
    max_count = item_counts.max()
    most_popular_items = item_counts[item_counts == max_count].index.tolist()
    if len(most_popular_items) > 1:
        print(f"\nThere are {len(most_popular_items)} most popular items.")
        print("They are:", most_popular_items)
    else:
        print("\nThe most popular item is:", most_popular_items[0])


# -------------------------------------------------------------------------
#    Worst Selling Item


def worst_selling_item(df):
    item_counts = pd.Series(
        [item for sublist in df["Basket"] for item in sublist]
    ).value_counts()

    min_count = item_counts.min()

    least_popular_items = item_counts[item_counts == min_count].index.tolist()

    if len(least_popular_items) > 1:
        print(f"\nThere is a tie for the least popular items.")
        print("They are:", least_popular_items)
    else:
        print("\nThe least popular item is:", least_popular_items[0])


# -------------------------------------------------------------------------
#    MVP Staff Member

# Check if there are multiple modes (multiple MVP staff members)


def mvp_staff_member(df):
    staff_mode = df["Staff"].mode()
    cost_summary = df.groupby("Staff")["Cost"].sum()
    transaction_counts = df["Staff"].value_counts()

    if not staff_mode.empty:
        if len(staff_mode) > 1:
            print("\nThere are multiple modes for MVP staff (Most Transactions):")
            print(staff_mode.tolist())
        else:
            staff_mode_value = staff_mode.iloc[0]
            transactions_for_mode = transaction_counts.get(staff_mode_value, 0)
            print("\nMVP staff member (Most Transactions):")
            print(f"{staff_mode_value} with {transactions_for_mode} Transactions")

    else:
        print("\nNo sales data available for Most Transactions.")

    cost_mode = cost_summary.idxmax()
    if cost_mode:
        highest_cost_value = cost_summary.loc[cost_mode]
        print("\nMVP staff member (Most Accumulated Cost):")
        print(f"{cost_mode}  with  £{highest_cost_value:.2f} of sales")
    else:
        print("\nNo sales data available for Most Accumulated Cost.")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# For each day also produce a chart showing:
# -Popularity of items sold
# -Different Payment Methods
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# -------------------------------------------------------------------------
# Function to find item Popularity


def product_popularity_count(df):
    # Count the occurrences of each individual item
    item_counts = pd.Series(
        [item for sublist in df["Basket"] for item in sublist]
    ).value_counts()

    # Print the frequency of each item
    print("\nNumber of sales for each Item:")
    print(item_counts)

    item_distribution = pd.Series(
        [item for sublist in df["Basket"] for item in sublist]
    ).value_counts(normalize=True)

    # Print the proportion of sales belonging to each item as percentages
    print("\nProportion of sales belonging to each item:")
    print((item_distribution * 100).round(2).astype(str) + "%")


# -------------------------------------------------------------------------
# function analysing Payment Methods


def payment_methods_analysis(df):
    # Convert the 'Payment Method' column to lowercase
    df["Payment Method"] = df["Payment Method"].str.capitalize()
    # counts all payment methods
    payment_method = df["Payment Method"].value_counts()
    payment_method.columns = ["Payment Method", "Count"]

    print(f"\nSales by Payment Method:\n{payment_method}")
    print("\n")  # spacing

    # The most common payment method
    most_common_method = df["Payment Method"].mode().iloc[0]
    print(f"The most common payment method is: {most_common_method}")
    print("\n")  # spacing

    # The least common payment method
    least_common_payment = df["Payment Method"].value_counts()
    least_common_payment = min(
        df["Payment Method"].unique(), key=df["Payment Method"].tolist().count
    )
    print(f"The least common payment method is: {least_common_payment}")
    print("\n")  # spacing

    # Number of items sold by each payment method
    items_sold_by_payment_method = (
        df.groupby("Payment Method")["Total Items"].sum().astype(int)
    )
    items_sold_by_payment_method.columns = ["Payment Method", "Total Items Sold"]

    print(f"Items sold by each payment method:\n{items_sold_by_payment_method}")
    print("\n")  # spacing

    # Total cost made by each payment method
    cost_by_payment_method = (
        df.groupby("Payment Method")["Cost"].sum().map("{:.2f}".format)
    )
    cost_by_payment_method.columns = ["Payment Method", "Total Cost"]

    print(f"Total cost made by each payment method:\n{cost_by_payment_method}")
    print("\n")  # spacing


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# For the week Create a Chart showing weekly profit
# -------------------------------------------------------------------------
# Function to calculate Weekly Income


def total_income_week(df):
    total_income = df["Cost"].sum()
    print(f"Week Total Income: {total_income:.2f}")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Investigating the staff member/s responsible for the void transactions

# Are these void transactions attributed to an individual
# or are they distributed amongst the staff
# this function creates a folder to save the result files
# savings as individual daily results is beneficial to allow easy printing
# we can compile results for week?
# need to make a functionn to save graphs into a folder
# save the six reults together then the 2 for graph separately
# -------------------------------------------------------------------------


def void_transaction_data(df):
    void_transactions = df[df["Transaction Type"] == "Void"]
    # Group by 'Staff' and count the occurrences of 'Void' for each staff member
    void_counts_by_staff = void_transactions.groupby("Staff")[
        "Transaction Type"
    ].count()
    # Display the results
    print("Void transaction counts for each staff member:")
    print(void_counts_by_staff)
    return void_counts_by_staff


def save_summary_void_data(void_data_week):
    summary_void_data_week = (
        void_data_week.groupby("Staff")["Number of Void Transactions"]
        .sum()
        .reset_index()
    )
    return summary_void_data_week


# -------------------------------------------------------------------------
