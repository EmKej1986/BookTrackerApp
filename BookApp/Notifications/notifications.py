import smtplib
import json
from datetime import date
from dotenv import load_dotenv
import os

try:

    todays_date = str(date.today())
    users_emails = open(f'..\Scraper\{todays_date}.json', encoding='utf-8')
    data = json.load(users_emails)
    for key, value in data.items():
        for email in value:
            smtp = smtplib.SMTP('smtp.gmail.com', 587)

            smtp.starttls()
            email_address = os.environ['EMAIL']
            email_password = os.environ['PASSWORD']

            smtp.login(email_address, email_password)

            book_title = key.encode("ISO-8859-2")
            subject = f"Your book {book_title}"
            text = f"Your book 1 {book_title} 1 is available to buy in store"

            message = 'Subject: {}\n\n{}'.format(subject, text)

            smtp.sendmail('books.tracker.app@gmail.com', email, message)

            smtp.quit()
            print(key, email, 'Email sent successfully')


except Exception as ex:
    print('Something went wrong...', ex)
