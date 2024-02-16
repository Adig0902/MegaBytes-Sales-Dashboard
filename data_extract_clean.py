import sys
import os
import matplotlib.pyplot as plt


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


def remove_punctuation(basket):  # Function Remove the punctuation from the list
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

# Save to specified folders within website for future dev
# allows site to update data stats and graphs when given new data sets
# if that function was developed, timestamp would be needed to differentiate


def save_output_to_file(output_function, folder, filename, *args, **kwargs):
    """
    Save the output of a function to a file in a specified folder.

    Parameters:
        output_function (callable): The function whose output needs to be saved.
        folder (str): The folder where the file should be saved.
        filename (str): The name of the file to save the output.
        *args: Positional arguments to pass to the output_function.
        **kwargs: Keyword arguments to pass to the output_function.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)  # Create the folder if it doesn't exist

    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as f:
        sys.stdout = f  # Redirect stdout to the file
        output_function(*args, **kwargs)
        sys.stdout = sys.__stdout__  # Reset stdout to the console


def save_graph_to_folder(figure, folder, filename):
    """
    Save a matplotlib graph to a specified folder with a specified filename.

    Parameters:
        figure (matplotlib.figure.Figure): The matplotlib figure to save.
        folder (str): The folder where the graph should be saved.
        filename (str): The name of the file to save the graph.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)  # Create the folder if it doesn't exist

    filepath = os.path.join(folder, filename)
    figure.savefig(filepath)
    plt.close(figure)  # Close the figure to free up resources
