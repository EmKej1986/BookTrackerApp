from bs4 import BeautifulSoup
from db_handler import DatabaseConnection
import asyncio
import aiohttp


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
        for idx, webpage in enumerate(responses):
            soup = BeautifulSoup(webpage.decode('utf-8', errors="ignore"), 'html.parser')
            try:
                print(soup)
                selected_title = soup.select_one(".ecommerce-datalayer").decode()
                # selected_url = soup.
            except AttributeError:
                print(f"Book {books[idx][0]} not found")
            else:
                selected_title = selected_title.lower()
                is_found = True if selected_title.find(f'data-name="{books[idx][0].lower()}"') != -1 else False
                href_attr_pos = selected_title.find('href=')
                url = "https://www.taniaksiazka.pl" \
                      + selected_title[href_attr_pos: selected_title.find('.html', href_attr_pos)].replace('href="', '') \
                      + ".html"
                with DatabaseConnection(
                        r"C:\Users\mkope\PycharmProjects\BookTrackerProject\BookApp\Web\database.sqlite3") as db:
                    db.set_is_available(books[idx][0], is_found)
                    db.set_url(books[idx][0], url)


class Executor:
    def __init__(self):
        self.http_sender = HttpRequestSender()
        self.scraper = Scraper()
        self.books = []

    def __get_urls(self):
        books_urls = []
        with DatabaseConnection(
                r"C:\Users\mkope\PycharmProjects\BookTrackerProject\BookApp\Web\database.sqlite3") as db:
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
