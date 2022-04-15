import requests
from flight_data import FlightData


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    TEQUILA_API_KEY = "1QeIi0F0_j2iee6beKV0nYk8afslNnTJ"
    KIWI_ENDPOINT = "https://tequila-api.kiwi.com"
    KIWI_GET_IATA_ENDPOINT = f"{KIWI_ENDPOINT}/locations/query"

    # kiwi_header = {
    #     "apikey": TEQUILA_API_KEY,
    #     "content-type": "application/json"
    # }
    def getiatacode(self, city):
        location_endpoint = f"{self.KIWI_ENDPOINT}/locations/query"
        headers = {"apikey": self.TEQUILA_API_KEY, "content-type": "application/json"}
        query = {"term": city, "location_types": "city"}
        response = requests.get(url=location_endpoint, params=query, headers=headers)
        response = response.json()["locations"]
        return response[0]["code"]

    # def getprice(self,strtloc,iata,fromdate,todate):
    #     search_endpoint = f"{self.KIWI_ENDPOINT}/v2/search"
    #     headers = {"apikey": self.TEQUILA_API_KEY, "content-type": "application/json"}
    #     query = {
    #         "fly_from": strtloc,
    #         "fly_to": iata,
    #         "date_from": fromdate.strftime("%d/%m/%Y"),
    #         "date_to": todate.strftime("%d/%m/%Y"),
    #         "nights_in_dst_from": 7,
    #         "nights_in_dst_to": 28,
    #         "flight_type": "round",
    #         "one_for_city": 1,
    #         "max_stopovers": 0,
    #         "curr": "GBP"
    #     }
    #     response = requests.get(url=search_endpoint,params=query,headers=headers)
    #     # print(response.text)
    #
    #     try:
    #         data = response.json()["data"][0]
    #     except IndexError:
    #         print(f"No flights found for {iata}.")
    #         return None
    #
    #     flight_data = FlightData(
    #         price=data["price"],
    #         origin_city=data["route"][0]["cityFrom"],
    #         origin_airport=data["route"][0]["flyFrom"],
    #         destination_city=data["route"][0]["cityTo"],
    #         destination_airport=data["route"][0]["flyTo"],
    #         out_date=data["route"][0]["local_departure"].split("T")[0],
    #         return_date=data["route"][1]["local_departure"].split("T")[0]
    #     )
    #     print(f"{flight_data.destination_city}: £{flight_data.price}")
    #     return flight_data

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": self.TEQUILA_API_KEY}
        stopover = 0
        viacity = ""
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        response1 = requests.get(
            url=f"{self.KIWI_ENDPOINT}/v2/search",
            headers=headers,
            params=query,
        )
        if len(response1.json()["data"]) == 0:
            query = {
                "fly_from": origin_city_code,
                "fly_to": destination_city_code,
                "date_from": from_time.strftime("%d/%m/%Y"),
                "date_to": to_time.strftime("%d/%m/%Y"),
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                "flight_type": "round",
                "one_for_city": 1,
                "max_stopovers": 1,
                "curr": "GBP"
            }
            response2 = requests.get(
                url=f"{self.KIWI_ENDPOINT}/v2/search",
                headers=headers,
                params=query,
            )
        try:
            if len(response1.json()["data"][0]) != 0:
                data = response1.json()["data"][0]
            else:
                data = response2.json()["data"][0]
                stopover = 1
                viacity = data["route"][0]["cityTo"]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0],
            stop_over=stopover,
            via_city=viacity
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data
