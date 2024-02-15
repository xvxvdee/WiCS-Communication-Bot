from TextFormattingHandler import TextFormattingHandler
from JobScrapingService import JobScrapingService
from DataFrameAccessor import DataFrameAccessor

class JobPostingFetcher:

    def __init__(self):
        self.formatter = TextFormattingHandler()
        self.scraping_service = JobScrapingService()
        self.data_accessor = DataFrameAccessor()

    def latest_internship_postings(self):
        # Set up dataframe
        data = self.scraping_service.get_github_internship2024()
        df_internships = self.formatter.readme_to_dataframe(data)
        df_internships = self.data_accessor.update_company_column(df_internships)

        # Get latest postings
        posting_type="internship_postings"
        df_postings = self.data_accessor.get_reccent_postings(df_internships)
        df_postings = self.formatter.dataframe_to_csv(df_postings,posting_type)
        return df_postings

    def latest_offseason_postings(self):
        # Set up dataframe
        data = self.scraping_service.get_github_offseason2024()
        df_offseason = self.formatter.readme_offseason_to_dataframe(data)
        df_offseason = self.data_accessor.update_company_column(df_offseason)
        
        # Get latest postings
        posting_type = "offseason_postings"
        df_postings = self.data_accessor.get_reccent_postings(df_offseason)
        df_postings=self.formatter.dataframe_to_csv(df_postings,posting_type)
        return df_postings

    def latest_newgrad_postings(self):
        # Set up dataframe
        data = self.scraping_service.get_github_newgrad2024()
        df_newgrad = self.formatter.readme_to_dataframe(data)
        df_newgrad = self.data_accessor.update_company_column(df_newgrad)
        
        # Get latest postings
        posting_type="newgrad_postings"
        df_postings = self.data_accessor.get_reccent_postings(df_newgrad)
        df_postings=self.formatter.dataframe_to_csv(df_postings,posting_type)
        return df_postings

