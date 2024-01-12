from datetime import datetime, timedelta
from mdplain import plain
from bs4 import BeautifulSoup
from TextFormattingHandler import TextFormattingHandler

class DataFrameAccessor:
    def __init__(self):
        self.arrow = "\\xc3\\xa2\\xe2\\x80\\xa0\\xc2\\xb3"
        self.formatter = TextFormattingHandler()
        self.date_posted_column = "Date Posted"

    def update_company_column(self,df): # Remove arrows from the company column in dataframe
        for i, row in df.iterrows():
            # Check for arrows as company (means previous company is current)
            if self.arrow in row["Company"]: 
                df.at[i,"Company"] = df["Company"][i-1]
        return df

    def get_title_text(self,text,df): # Gets title text from df which was formatted in markdown
        return plain(text)

    def get_title_link(self,text): # Gets title link from df formatted in markdown
        try:
            start_index = text.index("]")+2 # +2 to avoid  ](
            return text[start_index:len(text)-3] # -3 to remove )**
        except(ValueError):
            return None
        
    def get_application_link(self,text): # Gets application link from df formatted in markdown
        soup = BeautifulSoup(text, 'html.parser')
        link_tag = soup.find("a")
        href = link_tag.get("href")
        return href

    def get_locations(self,text): # Gets nested locations and returns a string of locations
        try:
            soup = BeautifulSoup(text, 'html.parser')
            details_tag = soup.find("details")

            # Ignore <Summary> tag
            content = details_tag.contents[1:]

            # Create a list of locations based on the content excluding the html
            locations = [str(x) for x in content if str(x)!="<br/>"]
            return " | ".join(locations)
        except(AttributeError):
            return text
        
    def get_reccent_postings(self,df): # Returns a dataframe of internship/new grad role from yesterday
        # Check dates match and date in dataframe
        yesterday = self.formatter.get_previous_date(datetime.today())
        prev_post_date = self.formatter.get_previous_date(df[self.date_posted_column][0])

        # Condition for there to be new postings
        new_postings = (yesterday == prev_post_date) and (str(prev_post_date) in df[self.date_posted_column].values)

        if (new_postings):
            df_postings = df.loc[df[self.date_posted_column]==str(prev_post_date)]
            return df_postings
        else:
            return None