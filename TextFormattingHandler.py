import re
import pandas as pd
import json
from datetime import datetime
from mdplain import plain
from bs4 import BeautifulSoup

class TextFormattingHandler:

    def readme_to_dataframe(self, text): # Formats internships and new grad readmes
        # Locate readme table
        result = text.split("Please leave a one line gap between this and the table TABLE_START (DO NOT CHANGE THIS LINE) -->\\n\\n")
        table_top = result[1]
        markdown_table = table_top.split("\\n\\n<!-- Please leave a one line gap between this and the table TABLE_END (DO NOT CHANGE THIS LINE) -->")    
        markdown_table_rows = markdown_table[0].split("\\n")[2:] 
        table = [re.split('\|', x) for x in markdown_table_rows]

        # Create dataframe
        df = pd.DataFrame(table,columns=["EmptyFront","Company","Role","Location","Application Link","Date Posted","EmptyBack"])
        df["Number"] = range(len(df))
        df.set_index('Number', inplace=True)

        # Drop empty columns
        df = df.drop("EmptyFront",axis=1)
        df = df.drop("EmptyBack",axis=1)
        return df
    
    def readme_offseason_to_dataframe(self, text): # Formats offseason readme
        # Locate readme table
        result = text.split("Please leave a one line gap between this and the table TABLE_START (DO NOT CHANGE THIS LINE) -->\\n\\n")
        table_top = result[1]
        markdown_table = table_top.split("\\n\\n<!-- Please leave a one line gap between this and the table TABLE_END (DO NOT CHANGE THIS LINE) -->")    
        markdown_table_rows = markdown_table[0].split("\\n")[2:] 
        table = [re.split('\|', x) for x in markdown_table_rows]

        # Create dataframe
        df = pd.DataFrame(table,columns=["EmptyFront","Company","Role","Location","Terms","Application Link","Date Posted","EmptyBack"])
        df["Number"] = range(len(df))
        df.set_index('Number', inplace=True)

        # Drop empty columns
        df = df.drop("EmptyFront",axis=1)
        df = df.drop("EmptyBack",axis=1)
        return df

    def json_to_dataframe(self,json_data): # Json from zobjobs endpoint to dataframe
        data = json.loads(json_data)
        df = pd.DataFrame.from_dict(data["jobs"], orient='columns')
        
        # Drop unnecessary columns
        df = df.drop("sourced",axis=1)
        df = df.drop("unique",axis=1)
        return df

    def update_titles(self,df): # Remove arrows from the company column in dataframe
        for i, row in df.iterrows():
            # Check for arrows as company (means previous company is current)
            if "\\xc3\\xa2\\xe2\\x80\\xa0\\xc2\\xb3" in row["Company"]: 
                df.at[i,"Company"] = df["Company"][i-1]
        return df

    def get_title_text(self,text,df): # Gets title text from df which was formatted in markdown
        return plain(text)

    def get_title_link(self,text): # Gets title link from df formatted in markdown
        try:
            start_index = text.index("]")+2 # +2 to avoid  ](
            return text[start_index:len(text)-3] # -3 to remove )**
        except:
            return "None"
        
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
        except:
            return text

    def format_timestamp(self,datetime_str): # Formats ISO timestamp to readable time
        # Conver to datetime object
        datetime_obj = datetime.fromisoformat(datetime_str) 
        # Format into readable string
        readable_dt_str = datetime_obj.strftime("%B %d, %Y")
        return readable_dt_str
