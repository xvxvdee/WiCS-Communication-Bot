from datetime import datetime, timedelta
from mdplain import plain
from bs4 import BeautifulSoup
from TextFormattingHandler import TextFormattingHandler
import hashlib
class DataFrameAccessor:
    def __init__(self,logger):        
        self.EMOJI = "\\x"
        self.formatter = TextFormattingHandler()
        self.DATE_POSTED = "Date Posted"
        self.NO_SPONSORSHIP = "\\xf0\\x9f\\x9b\\x82"
        self.US_CITIZEN_ONLY = "\\xf0\\x9f\\x87\\xba\\xf0\\x9f\\x87\\xb8"
        self.logger = logger

    def update_company_column(self,df): # Remove arrows from the company column in dataframe
        for i, row in df.iterrows():
            # Check for arrows as company (means previous company is current)
            if self.EMOJI in row["Company"]: 
                df.at[i,"Company"] = df["Company"][i-1]
        return df

    def get_reccent_postings(self,df): # Returns a dataframe of internship/new grad role from yesterday
        
        yesterday = self.formatter.get_previous_date(datetime.today())
        # Condition for there to be new postings
        new_postings = yesterday in df[self.DATE_POSTED].values

        if (new_postings):
            # Filter for the day before and avoid closed applications
            df_postings = df.loc[(df[self.DATE_POSTED] == str(yesterday))&(df["Application Link"].str.contains("https"))]# & (df["Application Link"] !=self.LOCK_EMOJI_1) & (df["Application Link"] !=self.LOCK_EMOJI_2)]
            df_postings = df_postings.copy()
            df_postings["Shared"] = False
            return df_postings
        else:
            return None
        
    def get_company_text(self,row): # Gets company text from df which was formatted in markdown
        text = row ["Company"]
        return plain(str(text))
    
    def get_company_link(self,row): # Gets company link from df formatted in markdown
        text = row["Company"]
        try:
            start_index = text.index("]")+2 # +2 to avoid  ](
            return text[start_index:len(text)-4] # -3 to remove )**
        except(ValueError) as err:
            self.logger.log_data_accessor_exception(row,"No company link",err)
            return None
    
    def get_role(self,row): # Gets role
        text = plain(str(row["Role"]))
        if (self.NO_SPONSORSHIP in text):
            role = text.split(self.EMOJI)
            return role[0] +" (DOES NOT OFFER SPONSORSHIP)"
        elif (self.US_CITIZEN_ONLY in text):
            role = text.split(self.EMOJI)
            return role[0] +" (US CITIZENS ONLY)"
        elif (self.EMOJI in text):
            return text.split(self.EMOJI)[0].strip()
        else:
            return plain(str(text))
    
    def get_date_posted(self,row): # Gets role
        return row["Date Posted"]

    def get_terms(self,row): # Returns offseason terms
        return row["Terms"]
    
    def get_application_link(self,row): # Gets application link from df formatted in markdown
        text = row["Application Link"]
        try:
            if "<a href" in text:
                soup = BeautifulSoup(text, 'html.parser')
                link_tag = soup.find("a")
                href = link_tag.get("href")
                return href
        except(AttributeError) as err: # No link tag
            self.logger.log_data_accessor_exception(row,"No link tag",err)
            return None

    def get_locations(self,row): # Gets nested/singular locations and returns a string of locations
        text = row["Location"]
        soup = BeautifulSoup(text, 'html.parser')
        try:
            details_tag = soup.find("details")

            # Ignore <Summary> tag
            content = details_tag.contents[1:]

            # Create a list of locations based on the content excluding the html
            locations = [str(x.get_text(" ")) for x in content if len(x)>1]
            return " | ".join(locations)
        except(AttributeError) as err: # No details tag
            locations = soup.get_text(" | ")
            self.logger.log_data_accessor_exception(row,"No details tag",err)
            return locations

    def create_id(self,job_type,row):
        combined_string = (job_type+row["Role"]+ row["Company"] + row["Date Posted"]+row["Location"]).encode()
        unique_id = hashlib.sha256(combined_string).hexdigest()
        return unique_id 
