"""Request interfaces."""
import requests
from scrapeghost import SchemaScraper

class HttpRequestInterface:
    """It defines the expected interface that a request interface sholhd
    have to interact with estela wrapper"""
    def request(self, *args, **kwargs):
        pass


class RequestsInterface(HttpRequestInterface):

    def request(self, *args, **kwargs):
        return requests.request(*args, **kwargs)


class ScrapeGhostInterface(HttpRequestInterface):
    scraper: SchemaScraper
    def create_schema_scraper(self, *args, **kwargs):
        self.scraper = SchemaScraper(*args, **kwargs)

    def request(self, *args, **kwargs):
        return self.scraper(*args, **kwargs)
