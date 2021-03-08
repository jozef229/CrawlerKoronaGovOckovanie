#%%
import requests
import smtplib
import time
from random import randint

password = 'XXX'
sender = "XXX"
receiver = "XXX"
message = "V tomto meste je aktualne dostupnych ockovacich miest.\nPrihlasenie je mozne na stranke :https://www.old.korona.gov.sk/covid-19-vaccination-form.php"
subject = "Ockovanie je dostupne v meste ."
message = 'Subject: {}\n\n{}'.format(subject, message)
try:
    session = smtplib.SMTP('smtp.gmail.com',587)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(sender,password)
    session.sendmail(sender,receiver,message)
    session.quit()
except smtplib.SMTPException:
    print('Error')


# %%


# %%
