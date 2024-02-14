import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_item_popularity_chart(df, day_name, ax):
  item_counts = pd.Series(
      [item for sublist in df["Basket"] for item in sublist]).value_counts()

  # Generate numerical indices for items
  item_indices = np.arange(len(item_counts))
  colors = plt.cm.tab10(np.arange(len(item_indices)))

  ax.bar(item_indices, item_counts.values, color=colors)
  ax.set_title(f"Item Popularity Chart for {day_name}")
  ax.set_xlabel("Item")
  ax.set_ylabel("Count")
  ax.set_xticks(item_indices)
  ax.set_xticklabels(item_counts.index, rotation=45, ha="right")


def overall_week_item_popularity_chart(compiled_data):
  overall_week_data = compiled_data[["Basket"]].explode("Basket",
                                                        ignore_index=False)
  overall_week_item_counts = overall_week_data["Basket"].value_counts()
  overall_week_item_indices = np.arange(len(overall_week_item_counts))

  plt.figure(figsize=(12, 6))
  plt.bar(
      overall_week_item_indices,
      overall_week_item_counts.values,
      color=plt.cm.tab10(np.arange(len(overall_week_item_indices))),
  )
  plt.title("Overall Week Item Popularity Chart")
  plt.xlabel("Item")
  plt.ylabel("Count")
  plt.xticks(
      overall_week_item_indices,
      overall_week_item_counts.index,
      rotation=45,
      ha="right",
  )
  plt.show()


def payment_methods_pie_chart(df):
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
  plt.show()
