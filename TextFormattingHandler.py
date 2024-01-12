import re
import pandas as pd
import json
from datetime import datetime, timedelta

class TextFormattingHandler:
    def __init__(self):
        self.table_start="Please leave a one line gap between this and the table TABLE_START (DO NOT CHANGE THIS LINE) -->\\n\\n"
        self.table_end ="\\n\\n<!-- Please leave a one line gap between this and the table TABLE_END (DO NOT CHANGE THIS LINE) -->"

    def readme_to_dataframe(self, text): # Formats internships and new grad readmes
        # Locate readme table
        result = text.split(self.table_start)
        table_top = result[1]
        markdown_table = table_top.split(self.table_end)    
        markdown_table_rows = markdown_table[0].split("\\n")[2:] 
        table = [re.split('\|', x) for x in markdown_table_rows]

        # Create dataframe
        df = pd.DataFrame(table,columns=["EmptyFront","Company","Role","Location","Application Link","Date Posted","EmptyBack"])
        df["Number"] = range(len(df))
        df.set_index('Number', inplace=True)

        # Fix date format
        df["Date Posted"] = [self.format_timestamp(d) for d in df["Date Posted"]]
        
        # Drop empty columns
        df = df.drop("EmptyFront",axis=1)
        df = df.drop("EmptyBack",axis=1)
        return df
    
    def readme_offseason_to_dataframe(self, text): # Formats offseason readme
        # Locate readme table
        result = text.split(self.table_start)
        table_top = result[1]
        markdown_table = table_top.split(self.table_end)    
        markdown_table_rows = markdown_table[0].split("\\n")[2:] 
        table = [re.split('\|', x) for x in markdown_table_rows]

        # Create dataframe
        df = pd.DataFrame(table,columns=["EmptyFront","Company","Role","Location","Terms","Application Link","Date Posted","EmptyBack"])
        df["Number"] = range(len(df))
        df.set_index('Number', inplace=True)

        # Fix date format
        df["Date Posted"] = [self.format_timestamp(d) for d in df["Date Posted"]]
        
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
        
    def format_timestamp(self,text): # Format date in df
        date = text.strip()
        try:
            # Create datetime object for MM/DD format
            date = datetime.strptime(date,'%b %d').strftime("%m/%d")
            return date
        except(TypeError): 
            # Create datetime object for MM/YYYY format
            date = datetime.strptime(date,'%b %Y').strftime("%m/%d")
            return date
        except(ValueError):
            return text

    def get_previous_date(self,text): # Get one day ago given a date
        try: # Create datetime object 
            date_object = datetime.strptime(text + '/' + str(datetime.now().year), '%m/%d/%Y')
            yesterday = date_object - timedelta(days=1)
            # Format into readable string
            readable_dt_str = yesterday.strftime("%m/%d")
            return readable_dt_str
        except(TypeError): # Given a datetime object
            yesterday = text - timedelta(days=1)
            # Format into readable string
            readable_dt_str = yesterday.strftime("%m/%d")
            return readable_dt_str
        except(ValueError):
            return text
