import requests
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

hourly = "https://api.weatherbit.io/v2.0/forecast/hourly?city=Austin,TX&key=0745ae18ce724d1c9daef34b2bf4dc14&hours=24"
daily  = "https://api.weatherbit.io/v2.0/forecast/daily?city=Austin,TX&key=0745ae18ce724d1c9daef34b2bf4dc14"

json_data_hourly = requests.get(hourly).json()
data_hourly = json_data_hourly["data"]

json_data_daily = requests.get(daily).json()
data_daily = json_data_daily["data"]

today = datetime.today().strftime("%Y-%m-%d")
morning = today +"T8:00:00"
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
	messageHTML = 'Low temparture: %s<br> High temparature: %s <br><br> At 8: %s&#37 chance of rain<br>At 5: %s&#37 chance of rain<br><br>Please BRING the umbrella' %(min_temp, max_temp, morning_rain_per, evening_rain_per) 
else:
	messageHTML = 'Low temparture: %s<br> High temparature: %s <br><br> At 8: %s&#37 chance of rain<br>At 5: %s&#37 chance of rain<br><br> You don&#39t need to bring an umbrella'%(min_temp, max_temp, morning_rain_per, evening_rain_per)

email = 'camryutd@gmail.com'
password = "YourPassword"
send_to_email = "YOUR_EMAIL"
subject = "INFO | Today's Weather"


messagePlain = "Today's weather"


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)

msg = MIMEMultipart('alternative')
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject

msg.attach(MIMEText(messagePlain, 'plain'))
msg.attach(MIMEText(messageHTML, 'html'))


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()
