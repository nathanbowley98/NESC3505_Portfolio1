'''
This program uses world health organization data to analyse trends in mortality rates.
Although this is not novel in nature it does give insight into my current python programming
ability and data processing skills.
author: Nathanael Bowley (github @nathanbowley98)
course: NESC3505
source: https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
retrieved 10/30/2020
'''

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

df = pd.read_csv("ExcelFiles/data.csv")
print("made by nathanael bowley. Github @nathanbowley98")
print("Check what we have to deal with as data")
df.info()

print("\nlets check the head of the data\n")
print(df.head())

print("\nI need to re-adjust pandas settings to display all the rows and columns as currently I cant see all my data\n"
      "Achieved behind the scenes using:\n "
      "\tpd.set_option('display.max_rows', None) \n"
      "\tpd.set_option('display.max_columns', None) \n"
      "\tpd.set_option('display.width', None)\n"
      "\tpd.set_option('display.max_colwidth', None)\n")

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("we can check to see the head of the data frame as the ecdc would have seen it")
print(df.head(), '\n')

print("do we have any null or na values? How many?")
print(df.isna().sum(), '\n')

print("We need to remove the null / na values.")
df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

print("\nRechecking dataframe head and how many null / na values:")
print(df.head(), "\n\nNumber of null / na values:")
print(df.isna().sum(), '\n')

print("I want to see cases:deaths ratios for each country each day to see if certain countries had or have a higher "
      "death ratio trend:")
df.loc[:, "case_death_ratio"] = df.cases / df.deaths
print(df.head())

# get all the areas in the data:
areas = df.countriesAndTerritories.unique()


# recursive method to get all the countries (faster than a for loop)
def recursive_countries(list, n):
    #base case to start
    if n == 0:
        print("\nThese are all the countries you can choose from:")
    #base case to escape
    if n == len(list):
        print("No more countries to show!")
    #recursive case
    else:
        print("•", list[n])
        return recursive_countries(list, n + 1)

#default country name
country = ""

#program loop
while True:
    print("Enter in a country name: (Type areas for list of areas)")
    user_in = input()
    if user_in == 'areas':
        recursive_countries(list=areas, n=0)
    elif user_in in areas:
        country = user_in
    #user input is acceptable
    if country == user_in:
        print("You have chosen", country + ", nice choice! Lets see the data.")
        country_df = df[df.countriesAndTerritories == country]

        print("This is the head of the data for Zimbabwe")
        print(country_df)

        country_df.loc[:,"dateRep"] = pd.to_datetime(country_df['dateRep'], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")

        fig, ax = plt.subplots(nrows=2, ncols=1)
        fig.suptitle("Cases and Deaths for Data Date Range for " + country)
        plt.setp(ax[0].xaxis.get_majorticklabels(), rotation=25)

        ax[0].plot(country_df.dateRep, country_df.cases)
        ax[0].set_xlabel("Date since data collection in " + country + "(interval: 15 days)")
        ax[0].set_ylabel("Cases in " + country)
        #ax[0].grid(True)
        plt.setp(ax[1].xaxis.get_majorticklabels(), rotation=25)
        ax[1].plot(country_df.dateRep, country_df.deaths)

        ax[1].set_xlabel("Date since data collection in " + country + "(interval: 15 days)")
        ax[1].set_ylabel("Deaths in " + country)
        #fig.autofmt_xdate()
        days = mdates.DayLocator(interval=15)
        ax[0].xaxis.set_major_locator(days)
        ax[1].xaxis.set_major_locator(days)
        fig.tight_layout()

        plt.show(block=True)

    #user need to retry.
    elif country != user_in and user_in != "areas":
        print("Error: Incorrect country spelling. Type areas for list of countries and try again.")


# case_death_ratio = pd.DataFrame([df.cases, df.deaths, df.countriesAndTerritories, ])
