import requests
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def weatherCheck():
	hourly = "https://api.weatherbit.io/v2.0/forecast/hourly?city=Austin,TX&key=0745ae18ce724d1c9daef34b2bf4dc14&hours=24"
	daily  = "https://api.weatherbit.io/v2.0/forecast/daily?city=Austin,TX&key=0745ae18ce724d1c9daef34b2bf4dc14"

	json_data_hourly = requests.get(hourly).json()
	data_hourly = json_data_hourly["data"]

	json_data_daily = requests.get(daily).json()
	data_daily = json_data_daily["data"]

	today = datetime.today().strftime("%Y-%m-%d")
	morning = today +"T10:00:00"
	evening = today +"T17:00:00"

	morning_stat = [element for element in data_hourly if element["timestamp_local"] == morning]
	morning_rain_per = ((morning_stat)[0]["pop"])

	evening_stat = [element for element in data_hourly if element["timestamp_local"] == evening]
	evening_rain_per = ((evening_stat)[0]["pop"])

	daily_stat = [element for element in data_daily if element["datetime"] == today]
	today_rain_per = daily_stat[0]["pop"]
	min_temp_data = daily_stat[0]["low_temp"]
	max_temp_data = daily_stat[0]["max_temp"]
	min_temp = str (round(min_temp_data * (9/5) + 32)) + "F"
	max_temp = str (round(max_temp_data * (9/5) + 32)) + "F"

	if (morning_rain_per > 30) or (evening_rain_per > 30):
		body = f'Low temparture: {min_temp}\n High temparature: {max_temp}\n\nAt 8: {morning_rain_per}% chance of rain\nAt 5: {evening_rain_per}% chance of rain\n\nPlease BRING the umbrella'
	else:
		body = f'Low temparture: {min_temp}\n High temparature: {max_temp}\n\nAt 8: {morning_rain_per}% chance of rain\nAt 5: {evening_rain_per}% chance of rain\n\n You don\'t need to bring an umbrella'

	send_mail(body)

def send_mail(body):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	server.login("camryutd@gmail.com", "762261Pf!")

	subject = "Today's Weather"

	msg = f"Subject: {subject}\n\n{body}"
	server.sendmail(
		'camryutd@gmail.com',
		'vudatderek@gmail.com',
		msg
	)
	server.quit()

weatherCheck()