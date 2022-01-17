from bs4 import BeautifulSoup
from db_handler import DatabaseConnection
import asyncio
import aiohttp
import operator
import json
from datetime import date


class HttpRequestSender:
    async def get(self, session, url):
        async with session.get(url) as response:
            return await response.read()


class Fetcher:
    @staticmethod
    async def fetch_all(urls: list, inner):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                tasks.append(inner(session, url))

            responses = await asyncio.gather(*tasks, return_exceptions=True)
            return responses


class Scraper:

        def retrieve_info(self, responses, books):
            notification_info = {}
            for idx, webpage in enumerate(responses):
                soup = BeautifulSoup(webpage.decode('ISO-8859-2'), 'html.parser')
                book_title = books[idx][0]
                try:
                    selected_attribute = soup.select_one(".ecommerce-datalayer").decode()
                except AttributeError:
                    print(f"Book {book_title} not found")
                else:
                    selected_attribute = selected_attribute.lower()
                    is_found = True if selected_attribute.find(f'data-name="{books[idx][0].lower()}"') != -1 else False
                    href_attr_pos = selected_attribute.find('href=')
                    selected_title = selected_attribute[href_attr_pos: selected_attribute.find('.html', href_attr_pos)].replace('href="', '')
                    url = "https://www.taniaksiazka.pl" \
                          + selected_title \
                          + ".html"
                    notification_info.update({book_title: []})
                    if is_found:
                        users_emails = AvailabilityValidator.retrieve_email(book_title)
                        notification_info[book_title] += users_emails
                    self.save_book_status(books, is_found, idx, url)

            FileHandler.save_notification_info(notification_info)


        def save_book_status(self, books, is_found, idx, url):
            with DatabaseConnection(
                    "..\Web\database.sqlite3") as db:
                db.set_is_available(books[idx][0], is_found)
                if is_found:
                    db.set_url(books[idx][0], url)


class AvailabilityValidator:

    @staticmethod
    def retrieve_email(selected_title):
        users_emails = []
        with DatabaseConnection("..\Web\database.sqlite3") as db:
            is_available, book_id = db.get_book_by_title(selected_title)
            if not is_available:
                user_profiles = db.get_users_profile_id(book_id)
                users_profile = map(operator.itemgetter(0), user_profiles)
                for profile_id in users_profile:
                    users_email = db.get_users_email(profile_id)
                    users_emails.append(users_email[0])

            return users_emails


class FileHandler:

    @staticmethod
    def save_notification_info(notification_info):
        todays_date = str(date.today())
        with open(f'{todays_date}.json', 'w', encoding='utf-8') as file:
            json.dump(notification_info, file, ensure_ascii=False)


class Executor:
    def __init__(self):
        self.http_sender = HttpRequestSender()
        self.scraper = Scraper()
        self.books = []

    def __get_urls(self):
        books_urls = []
        with DatabaseConnection(
                "..\Web\database.sqlite3") as db:
            self.books = db.get_titles()

        for title in self.books:
            books_urls.append(f'https://www.taniaksiazka.pl/Szukaj/q-{title}')

        return books_urls

    def get_titles_status(self):
        books_urls = self.__get_urls()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        responses = asyncio.run(Fetcher.fetch_all(books_urls, self.http_sender.get))
        return responses

    def retrieve_info(self, response_for_scraper):
        self.scraper.retrieve_info(response_for_scraper, self.books)


e = Executor()
responses_http = e.get_titles_status()
e.retrieve_info(responses_http)
