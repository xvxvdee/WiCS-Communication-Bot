#import BeautifulSoup as bs4
import urllib.request

class JobScrappingService:

    def __init__(self):
        pass
    
    def get_remote_jobs(self): # Returns remote jobs in CA and USA in a JSON Format
        contents = urllib.request.urlopen("https://zobjobs.com/api/jobs/").read()
        return contents




scrapper = JobScrappingService()
print(scrapper.get_remote_jobs())