import requests
import smtplib
from datetime import datetime as dt
import time

MY_EMAIL = ""
MY_PASSWORD = ""

NAMUR_LAT = 50.467388
NAMUR_LNG = 4.871985


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if NAMUR_LAT - 5 <= iss_latitude <= NAMUR_LAT + 5 and NAMUR_LNG - 5 <= iss_longitude <= NAMUR_LNG + 5:
        return True


def is_night():
    parameters = {
        "lat": NAMUR_LAT,
        "lng": NAMUR_LNG,
        "formatted": 0
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = dt.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:ISS Notification!\n\nThe ISS is above you in the night sky!"
            )
