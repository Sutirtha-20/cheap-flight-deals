#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import datetime as dt


datamanager = DataManager()
flightsearch = FlightSearch()
notification = NotificationManager()



#get incomplete data from google sheets
sheet_data = datamanager.get_data()
for data in sheet_data:
    if data["iataCode"] == "":
        # data["iataCode"] = datamanager.update_iata()
        data["iataCode"] = flightsearch.getiatacode(data["city"])

datamanager.data_manager = sheet_data
datamanager.update_sheet()
#crrct data in added in data_manager variable
ORIGIN_CITY_IATA = "LON"
from_date = dt.datetime.now() + dt.timedelta(days=1)
six_month_from_today = dt.datetime.now() + dt.timedelta(days=(6*30))

# print("Welcome to the Flight club")
# first_name = input("PLease provide your name")
# email1 = input("Please provide your email")
# email2 = input("PLease provide your email again")
# if email1 == email2:
#     op = datamanager.update_user_sheet_date(first_name,email1)
#     if op:
#         print("Welcome to flight club")

for destination in sheet_data:
    loc = data["iataCode"]
    flight = flightsearch.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_date,
        six_month_from_today
    )
    if flight is not None:
        if flight.price < destination["lowestPrice"]:
            #sending sms to mobile number via twilio
            # notification.sendnotification(flight)
            notification.send_mail(flight)
    else:
        continue
    # print(price)

#getting user cred
