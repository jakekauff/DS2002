
"""
@author: Jakob Kauffmann (jgk2qq)
Mongo + Python Lab
"""
import datetime
import pymongo
import pprint
import pgeocode
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Get user input of zipcode
zip = input("Please enter a zipcode: ")

# Convert to lat. and long.
nomi = pgeocode.Nominatim('us')
info = nomi.query_postal_code(zip)

latitude = str(info[9])
longitude = str(info[10])

# Scrape 7 day forecast 
page = requests.get("https://forecast.weather.gov/MapClick.php?lat="+latitude+"&lon="+longitude)
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")

day1 = forecast_items[0] #tonight
img1 = day1.find("img")
desc1 = img1['title']

day2 = forecast_items[1] # tomorrow
img2 = day2.find("img")
desc2 = img2['title']

day3 = forecast_items[2] # tomorrow night
img3 = day3.find("img")
desc3 = img3['title']

day4 = forecast_items[3] # day 3
img4 = day4.find("img")
desc4 = img4['title']

day5 = forecast_items[4] # night 3
img5 = day5.find("img")
desc5 = img5['title']

day6 = forecast_items[5] # day 4
img6 = day6.find("img")
desc6 = img6['title']

day7 = forecast_items[6] # night 4
img7 = day7.find("img")
desc7 = img7['title']

day8 = forecast_items[7] # day 5
img8 = day8.find("img")
desc8 = img8['title']

day9 = forecast_items[8] # night 5
img9 = day9.find("img")
desc9= img9['title']

# Display to user
print("\nThe 7-day forecast for " + zip + " is: \n")
print(desc1 + "\n")
print(desc2 + "\n")
print(desc3 + "\n")
print(desc4 + "\n")
print(desc5 + "\n")
print(desc6 + "\n")
print(desc7 + "\n")
print(desc8 + "\n")
print(desc9 + "\n")


# Create df of 7-day forecast
period_tags = seven_day.select(".tombstone-container .period-name") 
periods = [pt.get_text() for pt in period_tags]
short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc" )]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

weather = pd.DataFrame({
    "period": periods, 
    "short_desc": short_descs, 
    "temp": temps, 
    "desc":descs
    })

# Scrape current conditions
current_conditions = soup.find(id="current-conditions")
current_items = current_conditions.find_all(class_="pull-left")

values = current_items[2].find_all('td')
print(values[1].get_text())

conditionTags = current_conditions.select(".pull-left .text-right")

# Display current conditions to user
print("\nThe current conditions in " + zip + " are: \n")
print(values[0].get_text() + ": " + values[1].get_text())
print(values[2].get_text() + ": " + values[3].get_text())
print(values[4].get_text() + ": " + values[5].get_text())
print(values[6].get_text() + ": " + values[7].get_text())
print(values[8].get_text() + ": " + values[9].get_text())
print(values[10].get_text() + ": " + values[11].get_text())

# mongo
host_name = "localhost"
port = "27017"

atlas_cluster_name = "sandbox"
atlas_default_dbname = "local"

conn_str = {
    "local" : f"mongodb://{host_name}:{port}/"
}

client = pymongo.MongoClient(conn_str["local"])

db_name = "WeatherForecastf" + zip

db = client[db_name]
client.list_database_names()


sevenDayText = desc1 + "/n" + desc2 + "/n" + desc3 + "/n" + desc4 + "/n" + desc5 + "/n" + desc6 + "/n" + desc7 + "/n" + desc8 + "/n" + desc9 
sevenDay = {'title' : 'Seven Day Forecast', 
            'author':'Jakob Kauffmann',
            'text' : sevenDayText,
            "date": datetime.datetime.utcnow()
    }
posts = db.posts

currentText = (values[0].get_text() + " : " +  values[1].get_text() + " ", 
values[2].get_text() + " : " +  values[3].get_text() + " ",
values[4].get_text() + " : " +  values[5].get_text() + " ",
values[6].get_text() + " : " +  values[7].get_text() + " ",
values[8].get_text() + " : " +  values[9].get_text() + " ",
values[10].get_text() + " : " +  values[11].get_text()
                )
currentForecast = {'title':'Current Forecast',
                   'author' : 'Jakob Kauffmann',
                   'text' : currentText,
                   'date' : datetime.datetime.utcnow()
    }
post_id = posts.insert_one(currentForecast).inserted_id
