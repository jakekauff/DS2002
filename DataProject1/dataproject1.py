import json

import pandas as pd
import requests
import pandas
from datetime import date
import matplotlib.pyplot as plt

# Read in data set, catch file not found error
try:
    df = pd.read_csv(r"/Users/jake/Desktop/BigmacPrice.csv")
except FileNotFoundError:
    print("File not found.")



# Add columns
df[["year", "month", "day"]] = df["date"].str.split("-", expand = True)
print(df)

# Change to JSON
df_json = df.to_json()

#Write to CSV with new columns
df.to_csv('BigMacPrice_Edited.csv')

print("Data has " , df.shape[0], " observations and ", df.shape[1], " columns.")
print(" ")
print("Dataframe: ")
print(df)
print(" ")
print("JSON Format: ")
print(df_json)
