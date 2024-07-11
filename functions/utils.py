import requests
from bs4 import BeautifulSoup as bs4

class DensitiesUFRGS:

    def __init__(self):
        self.base_url = "https://www.ufrgs.br/vestibular/cv"

    def clear(self):
        self.year = None
        self.request_ufrgs = None

    def build_url(self):
        return self.base_url + self.year + "/densidade/"

    def request_url(self):
        self.request_ufrgs = requests.get(self.build_url())

    def run_extraction(self, years):
        for year in years:
            self.year = year.__str__()
            self.request_url()
