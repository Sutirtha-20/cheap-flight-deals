from twilio.rest import Client
import smtplib
from data_manager import DataManager


datamanager = DataManager()

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    my_email = "guhamohit123@gmail.com"
    password = "Thehindu@2016"

    def sendnotification(self,flight):
        account_sid = "AC3274fdc5ef3edf41ea8977388c8cad21"
        auth_token = "e6c0ba57f1c541eb887b62d8663a4afe"
        client = Client(account_sid, auth_token)
        msg = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        msg += f""
        if flight.stop_over>0:
            msg += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
        message = client.messages \
            .create(
            body=msg,
            from_='+15017122661',
            to='+15558675310'
        )

        print(message.sid)

    def send_mail(self,flight):
        msg = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
        msg += link
        if flight.stop_over > 0:
            msg += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        user_list = datamanager.get_user_data()
        for user in user_list:
            # name=user["name"]
            mail = user["email"]

            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=self.my_email,password=self.password)
                connection.sendmail(from_addr=self.my_email,to_addrs=mail,msg=msg)
                print(f"mail sent to {mail}")
