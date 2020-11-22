import time
import requests
import smtplib
import os
import logging

SLEEP_TIME = 60
URL = "https://videoigr.net/catalog/playstation-5-155/pristavki-156/"
GMAIL_HOST = "smtp.gmail.com"
GMAIL_PORT = 587
GMAIL_USER = "mkevac@gmail.com"
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
NAME = "Marko Kevac"
SUCCESS_TEXT = f"Something's up! Go to {URL}"

MESSAGE = """\
From: {NAME} <{GMAIL_USER}>
To: {NAME} <{GMAIL_USER}>
Subject: {subject}

{text}
"""


def send_email(subject, text):
    with smtplib.SMTP(GMAIL_HOST, 587) as smtpobj:
        smtpobj.ehlo()
        smtpobj.starttls()
        smtpobj.login(GMAIL_USER, GMAIL_PASSWORD)
        smtpobj.sendmail(GMAIL_USER, [GMAIL_USER, ],
                         MESSAGE.format(NAME=NAME, GMAIL_USER=GMAIL_USER,
                                        subject=subject, text=text))


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    while True:
        try:
            r = requests.get(URL, timeout=10.0)
        except requests.RequestException:
            logging.error("error while getting URL")
            time.sleep(SLEEP_TIME)
            continue
        if r.status_code != 200:
            logging.error("error code {}".format(r.status_code))
            time.sleep(SLEEP_TIME)
            continue
        if len(r.text) == 0:
            logging.error("empty result")
            time.sleep(SLEEP_TIME)
            continue

        found = 0
        start = 0
        while True:
            i = r.text.find("Нет в наличии", start)
            if i == -1:
                break
            found += 1
            start = i + 1

        logging.info("found {}".format(found))

        if found != 6:
            try:
                send_email(subject="PlayStation 5", text=SUCCESS_TEXT)
            except smtplib.SMTPException:
                print("Error while sending email...")
            print("Sent an email...")

        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
