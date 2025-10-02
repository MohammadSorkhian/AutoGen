import os
from azure.search.documents import SearchClient 
from azure.core.credentials import AzureKeyCredential   
from dotenv import load_dotenv
load_dotenv()

# Retrieve credentials from environment variables
azure_search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
azure_search_key = os.environ.get("AZURE_SEARCH_KEY")
azure_search_index_name = "rag-1756588180789"



search_client = SearchClient(
    endpoint=azure_search_endpoint,
    index_name=azure_search_index_name,
    credential=AzureKeyCredential(azure_search_key)
)