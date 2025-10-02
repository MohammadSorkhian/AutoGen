import os
from azure.search.documents.indexes import SearchIndexClient
from dotenv import load_dotenv
load_dotenv()

azure_search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
azure_search_key = os.environ.get("AZURE_SEARCH_KEY")



index_client = SearchIndexClient(
    endpoint=azure_search_endpoint,
    credential=azure_search_key
)