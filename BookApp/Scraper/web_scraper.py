from bs4 import BeautifulSoup
from lxml import etree
import requests
from db_handler import DatabaseConnection
import asyncio
import aiohttp


class HttpRequestSender:
    async def get(self, session, url):
        async with session.get(url) as response:
            return await response.content.read()


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
    def __init__(self):
        print(Executor.retrieve_title())

    # def retrieve_titles(self):
    #
    #     soup = BeautifulSoup(webpage.content, 'html.parser')
    #     dom = etree.HTML(str(soup))
    #
    #             try:
    #                 found_title = dom.xpath('// html[1] / body[1] / div[5] / section[1] / div[2] / div[2]'
    #                                         ' / article[1] / ul[1] / li[1] / div[1] / div[2] / div[1] / div[1] / div[1]'
    #                                         ' / h2[1] / a[1]')[0].text.strip()
    #
    #                 #print(dom.xpath('//*[@id="pagi-slide"]/li[1]/div/div[2]/div[1]/div[1]/div/h2/a/text()')
    #             except(ValueError, Exception):
    #                 print('Book is not available')
    #             else:
    #                 book_list.append(str.title(found_title))
    #
    #         for book in book_list:
    #             db.get_is_available(book)


class Executor:
    def __init__(self):
        self.http_sender = HttpRequestSender()
        self.scraper = Scraper()

    def __get_urls(self):
        books_urls = []
        with DatabaseConnection(
                r"C:\Users\mkope\PycharmProjects\BookTrackerProject\BookApp\Web\database.sqlite3") as db:
            books = db.get_titles()

        for title in books:
            books_urls.append(f'https://www.taniaksiazka.pl/Szukaj/q-{title}')

        return books_urls

    def get_titles_status(self):
        books_urls = self.__get_urls()
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        responses = asyncio.run(Fetcher.fetch_all(books_urls, self.http_sender.get))
        return responses

    def retrieve_title(self, response_for_scraper):
        return response_for_scraper


e = Executor()
responses_http = e.get_titles_status()
e.retrieve_title(responses_http)

# s = Scraper()

# def web_scraper():
#     with DatabaseConnection(r"C:\Users\mkope\PycharmProjects\BookTrackerProject\BookApp\Web\database.sqlite3") as db:
#         books = db.get_titles()
#         book_list = []
#
#         for title in books:
#             webpage = requests.get(f'https://www.taniaksiazka.pl/Szukaj/q-{title}')
#            -> soup = BeautifulSoup(webpage.content, 'html.parser')
#             dom = etree.HTML(str(soup))
#
#             if title not in book_list:
#
#                 try:
#                     found_title = dom.xpath('// html[1] / body[1] / div[5] / section[1] / div[2] / div[2]'
#                                             ' / article[1] / ul[1] / li[1] / div[1] / div[2] / div[1] / div[1] / div[1]'
#                                             ' / h2[1] / a[1]')[0].text.strip()
#
#                     #print(dom.xpath('//*[@id="pagi-slide"]/li[1]/div/div[2]/div[1]/div[1]/div/h2/a/text()')
#                 except(ValueError, Exception):
#                     print('Book is not available')
#                 else:
#                     book_list.append(str.title(found_title))
#
#         for book in book_list:
#             db.get_is_available(book)




# web_scraper()
