import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_extract_clean import save_graph_to_folder
import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ITEM POPULARITY CHARTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# to be used in for loop to print daily graph for item popularity
def plot_item_popularity_chart(df, day_name, ax):
    item_counts = pd.Series(
        [item for sublist in df["Basket"] for item in sublist]
    ).value_counts()

    # Generate numerical indices for items
    item_indices = np.arange(len(item_counts))
    colors = plt.cm.tab10(np.arange(len(item_indices)))

    # Use barh for horizontal bar chart
    ax.barh(item_indices, item_counts.values, color=colors)

    ax.set_title(f"Item Popularity Chart for {day_name}")
    ax.set_ylabel("Item")
    ax.set_xlabel("Count")
    ax.set_yticks(item_indices)
    ax.set_yticklabels(item_counts.index)

    # adding padding around graph so labels aren't cut off
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

    current_figure = plt.gcf()
    filename = f"item_popularity_chart_{day_name}.png"
    folder_name = "website\\static\\images\\Graphs_folder\\item_popularity"
    os.makedirs(folder_name, exist_ok=True)
    save_graph_to_folder(current_figure, folder_name, filename)


def plot_item_popularity_chart_week(compiled_data):
    overall_week_data = compiled_data[["Basket"]].explode("Basket", ignore_index=False)
    overall_week_item_counts = overall_week_data["Basket"].value_counts()
    overall_week_item_indices = np.arange(len(overall_week_item_counts))

    plt.figure(figsize=(12, 6))

    # Use barh for horizontal bar chart
    plt.barh(
        overall_week_item_indices,
        overall_week_item_counts.values,
        color=plt.cm.tab10(np.arange(len(overall_week_item_indices))),
    )

    plt.title("Overall Week Item Popularity Chart")
    plt.ylabel("Item")
    plt.xlabel("Count")

    # adding padding around graph so labels aren't cut off
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

    # Save the graph
    current_figure = plt.gcf()
    filename = f"item_popularity_chart_week.png"
    folder_name = "website\\static\\images\\Graphs_folder\\week_insight_graphs"
    os.makedirs(folder_name, exist_ok=True)
    save_graph_to_folder(current_figure, folder_name, filename)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PAYMENT METHODS CHARTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# to be used in for loop to print daily graph for payment methods
def plot_payment_methods_pie_chart(df, day_name):
    payment_method_counts = df["Payment Method"].value_counts()
    plt.pie(
        payment_method_counts,
        labels=payment_method_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],
    )
    plt.title(f"Payment Methods Distribution for {day_name}")
    current_figure = plt.gcf()
    filename = f"Payment_methods_piechart_{day_name}.png"
    folder_name = "website\\static\\images\\Graphs_folder\\payment_methods"
    os.makedirs(folder_name, exist_ok=True)
    save_graph_to_folder(current_figure, folder_name, filename)


def plot_payment_methods_pie_chart_week(df):
    payment_method_counts = df["Payment Method"].value_counts()
    plt.figure(figsize=(10, 8))
    plt.pie(
        payment_method_counts,
        labels=payment_method_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"],
    )
    plt.title("Payment Methods Distribution")
    current_figure = plt.gcf()
    filename = f"Payment_methods_piechart_week_.png"
    folder_name = "website\\static\\images\\Graphs_folder\\week_insight_graphs"
    os.makedirs(folder_name, exist_ok=True)
    save_graph_to_folder(current_figure, folder_name, filename)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# VOID TRANSACTION CHARTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def plot_void_transaction_data(void_data, day_name):
    # Assuming void_data is a DataFrame with "Staff", "Number of Void Transactions", and "Total Number of Transactions"
    colors = plt.cm.tab10(np.arange(len(void_data)))
    void_data.plot(kind="bar", color=colors)

    # Add labels and title
    plt.xlabel("Staff")
    plt.ylabel("Void Transaction Count")
    plt.title(f"Void Transaction Data for {day_name}")

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45, ha="right")

    # adding padding around graph so labels arent cut off
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

    current_figure = plt.gcf()
    filename = f"Void_transactions_graph_for_{day_name}.png"
    folder_name = "website\\static\\images\\Graphs_folder\\void_transactions"
    os.makedirs(folder_name, exist_ok=True)
    save_graph_to_folder(current_figure, folder_name, filename)


def plot_void_transaction_data_week(void_data_week):
    if not void_data_week.empty:
        void_data_agg = (
            void_data_week.groupby("Staff")["Number of Void Transactions"]
            .sum()
            .reset_index()
        )

        colors = plt.cm.tab10(np.arange(len(void_data_agg)))

        void_data_agg.plot(
            kind="bar",
            x="Staff",
            y="Number of Void Transactions",
            legend=None,
            color=colors,
        )
        plt.title("Void Transaction Data for the Week")
        plt.xlabel("Staff")
        plt.ylabel("Number of Void Transactions")

        # Rotate x-axis labels for better visibility
        plt.xticks(rotation=45, ha="right")

        # adding padding around graph so labels arent cut off
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

        current_figure = plt.gcf()
        filename = f"Void_transactions_graph_for_week.png"
        folder_name = "website\\static\\images\\Graphs_folder\\week_insight_graphs"
        os.makedirs(folder_name, exist_ok=True)
        save_graph_to_folder(current_figure, folder_name, filename)
    else:
        print("No void transaction data for the week.")
