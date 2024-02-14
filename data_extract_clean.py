import pandas as pd
import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Data extraction and cleaning
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# -------------------------------------------------------------------------
# Function used in extract and clean function


def split_basket(basket_str):  # splitting string into an actual list
  elements = basket_str.split(",")
  stripped_elements = [e.strip() for e in elements]
  return stripped_elements


# -------------------------------------------------------------------------
# Function used in extract and clean function


def remove_punctuation(
    basket):  # Function Remove the punctuation from the list
  basket = str(basket)
  basket = basket.replace("[", "")
  basket = basket.replace("]", "")
  basket = basket.replace("'", "")
  return basket


# -------------------------------------------------------------------------
# Fuction to convert string list into an actual list


def convert_string_to_list(df):
  df["Basket"] = df["Basket"].apply(remove_punctuation)
  df["Basket"] = df["Basket"].apply(split_basket)
  df = df.explode("Basket", ignore_index=False)
  return df


# -------------------------------------------------------------------------
# Function to extract data and clean


def extract_and_clean(df):
  # Clean data from values we do not want to include
  df = df.drop(columns=["Unnamed: 0"])
  if (df["Transaction ID"] == 23).any() and (df["Cost"] == 700).any():
    # Update 'Cost' to 7.00 where the conditions are met
    df.loc[(df["Transaction ID"] == 23) & (df["Cost"] == 700), "Cost"] = 7.00
  df = df.drop([0])
  df = df.dropna(how="any")
  convert_string_to_list(df)
  return df


# -------------------------------------------------------------------------
# Function to extract the day name from the filepath


def extract_day_name(file_name):
  day_name = os.path.basename(file_name)
  return day_name.replace("_data.xlsx", "")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
