from bs4 import BeautifulSoup 
import urllib.request
import requests 
import base64
import json

class JobScrapingService:
    
    def __init__(self,logger):
        self.summer_internships ="https://raw.githubusercontent.com/SimplifyJobs/Summer2024-Internships/dev/README.md"
        self.offseason_internships = "https://api.github.com/repos/SimplifyJobs/Summer2024-Internships/contents/README-Off-Season.md?ref=dev"
        self.newgrad_internships = "https://api.github.com/repos/SimplifyJobs/New-Grad-Positions/contents/README.md?ref=dev"
        self.logger = logger

    def get_github_internship2024(self):
        URL = self.summer_internships
        request = requests.get(URL) 
        request.encoding = request.apparent_encoding 
        soup = BeautifulSoup(request.text, 'html5lib') 
        self.logger.log_data_scrapped(URL,"Summer roles scraped")
        return str(soup.encode("utf-8"))
    
    def get_github_offseason2024(self):
        URL = self.offseason_internships
        response = requests.get(URL) 
        data = response.json()
        readme_content = base64.b64decode(data['content'])
        self.logger.log_data_scrapped(URL,"Offseason roles scraped")
        return str(readme_content)
    
    def get_github_newgrad2024(self):
        URL = self.newgrad_internships
        response = requests.get(URL) 
        data = response.json()
        readme_content = base64.b64decode(data['content'])
        self.logger.log_data_scrapped(URL,"Newgrad roles scraped")
        return str(readme_content)
