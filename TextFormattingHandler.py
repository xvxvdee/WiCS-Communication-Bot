import re
import pandas as pd
from pandas import json_normalize
import json
from datetime import datetime

class TextFormattingHandler:

    def readme_to_dataframe(self, text): # Formats internships and new grad readmes
        # Locate readme table
        result = text.split("Please leave a one line gap between this and the table TABLE_START (DO NOT CHANGE THIS LINE) -->\\n\\n")
        table_top = result[1]
        markdown_table = table_top.split("\\n\\n<!-- Please leave a one line gap between this and the table TABLE_END (DO NOT CHANGE THIS LINE) -->")    
        markdown_table_rows = markdown_table[0].split("\\n")[2:] 
        table = [re.split('\|', x) for x in markdown_table_rows]

        # Create dataframe
        df = pd.DataFrame(table,columns=["EmptyFront","Company","Role","Location","Application/Link","Date Posted","EmptyBack"])
        df.set_index('Company', inplace=True)

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
        df = pd.DataFrame(table,columns=["EmptyFront","Company","Role","Location","Terms","Application/Link","Date Posted","EmptyBack"])
        df.set_index('Company', inplace=True)

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

    def get_title_text(self,text): # Gets title text from df which was formatted in markdown
        pass

    def get_title_link(self,text): # Gets title link from df formatted in markdown
        pass

    def get_application_link(self,text): #  Gets application link from df formatted in markdown
        pass

    def format_timestamp(self,datetime_str): # Formats ISO timestamp to readable time
        # Conver to datetime object
        datetime_obj = datetime.fromisoformat(datetime_str) 
        # Format into readable string
        readable_dt_str = datetime_obj.strftime("%B %d, %Y")
        return readable_dt_str


    # # Format text for Embeddings # job posting channel
    # def internship_embed_formatter(self):
    #     pass

    # # Format text for resources #resource channel
    # def resource_embed_formatter(self):
    #     pass

    # # Format text for hackathon #communication channel
    # def hackathon_forum_formatter(self):
    #     pass 

    # # Format text for hackathon #communication channel
    # def news_forum_formatter(self):
    #     pass 

