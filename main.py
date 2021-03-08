#%%
import requests
import smtplib
import time
from random import randint


def sendEmailWithName(cityName, lock, city, count, email):
    sender = "XXX"
    password = "XXX"
    receiver = email
    message = "V tomto meste je aktualne dostupnych " + str(count) + " ockovacich miest.\nPrihlasenie je mozne na stranke :https://www.old.korona.gov.sk/covid-19-vaccination-form.php"
    subject = "Ockovanie je dostupne v meste " + cityName[city] + "."
    message = 'Subject: {}\n\n{}'.format(subject, message)
    try:
        session = smtplib.SMTP('smtp.gmail.com',587)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(sender,password)
        session.sendmail(sender,receiver,message)
        session.quit()
        lock[city] = True
    except smtplib.SMTPException:
        print('Error')


def countFreePlace(place):
    count = 0
    for date in place["calendar_data"]:
        count = count + date["free_capacity"]
    return count

def controlFreePlace(cityName, lock, place, city, email):
    if place["city"] == city:
        count = countFreePlace(place)
        if count > 0:
            if lock[city] == False:
                sendEmailWithName(cityName, lock, city, count, email)
        else:
            lock[city] = False

def controlAllPlace(lock, cityName):
    try:
        response = requests.get("https://mojeezdravie.nczisk.sk/api/v1/web/get_all_drivein_times_vacc")
        allJson = response.json()
        email_presov = []
        email_trebisov = []
        email_bratislava = []
        for place in allJson["payload"]:
            controlFreePlace(cityName, lock, place, "Prešov", email_presov)
            controlFreePlace(cityName, lock, place, "Trebišov", email_trebisov)
            controlFreePlace(cityName, lock, place, "Bratislava", email_bratislava)
    except:
        print("error json usual")

lock = {"Prešov": False, "Trebišov": False, "Bratislava": False, "Žilina": False }
cityName = {"Prešov": "Presov", "Trebišov": "Trebisov", "Bratislava": "Bratislava", "Žilina": "Zilina" }

while(True):
    controlAllPlace(lock, cityName)
    time.sleep(randint(0, 120) + 200)

# %%


# %%
