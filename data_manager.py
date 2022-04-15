import requests

SHEETY_GET_ENDPOINT = "https://api.sheety.co/1f31a1f21f5dd41f20306b272dac994a/copyOfFlightDeals/prices"


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.data_manager = {}
        self.user_data = {}

    def get_data(self):
        res = requests.get(SHEETY_GET_ENDPOINT)
        res = res.json()["prices"]
        return res

    def get_user_data(self):
        user_url = "https://api.sheety.co/1f31a1f21f5dd41f20306b272dac994a/copyOfFlightDeals/users"
        res = requests.get(user_url)
        res = res.json()["users"]
        return res

    def update_iata(self):
        return "TESTING"

    def update_sheet(self):
        for data in self.data_manager:
            sheety_params = {
                "price": {
                    "iataCode": data["iataCode"]
                }
            }
            put_url = f"{SHEETY_GET_ENDPOINT}/{data['id']}"
            new_res = requests.put(url=put_url,json=sheety_params)
            # print(new_res)


    #this will be implemented in separate space
    def update_user_sheet_date(self,name,email):
        USER_ADD_ENDPOINT = "https://api.sheety.co/1f31a1f21f5dd41f20306b272dac994a/copyOfFlightDeals/users"
        header = {"Content-Type": "application/json"}
        params = {
            "user": {
                "name": name,
                "email": email
            }
        }
        res = requests.post(url=USER_ADD_ENDPOINT,json=params,headers= header)
        print(res.text)
