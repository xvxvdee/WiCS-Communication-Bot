import re
import pandas as pd

class TextFormattingHandler:

    def readme_to_dataframe(self, text):
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


    # Format text for Embeddings # job posting channel
    def internship_embed_formatter(self):
        pass

    # Format text for resources #resource channel
    def resource_embed_formatter(self):
        pass

    # Format text for hackathon #communication channel
    def hackathon_forum_formatter(self):
        pass 

    # Format text for hackathon #communication channel
    def news_forum_formatter(self):
        pass 