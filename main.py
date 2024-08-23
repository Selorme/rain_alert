import requests
from twilio.rest import Client
import os

# you need to get the endpoint of whichever weather apps API you will use. I used open weather map
OWM_ENDPOINT = os.environ["OWM_ENDPOINT"]
API_KEY = os.environ["API_KEY"]
ACCOUNT_SID = os.environ["ACCOUNT_SID"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]
PHONE_NUMBER = os.environ["PHONE_NUMBER"]
# create an account on Twilio to get a phone number and be able to send text messages
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]

weather_params = {
    # You have to use your own latitude and longitude which you can get from latlong.net
    "lat": 47.230686,
    "lon": 16.621843,
    "appid": API_KEY,
    "cnt": 4,
}

response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False
# Iterate over each item in the forecast list and get their weather condition IDs
for forecast in weather_data["list"]:
    weather_id = forecast["weather"][0]["id"]
    if weather_id < 700:
        will_rain = True

if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        from_=TWILIO_NUMBER,
        body="Rainy day ahead, bring your umbrella!",
        to=PHONE_NUMBER
    )
    print(message.status)
