import os
from _tools._10_SearchResultScoring_tool import SearchResultScoring_tool
from _tools._05_searchDocuments_tool import searchDocuments_tool
from dotenv import load_dotenv

load_dotenv()

# Retrieve credentials from environment variables
azure_openAI_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
azure_openAI_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
azure_openAI_deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
azure_openAI_api_version = os.environ.get("AZURE_OPENAI_API_VERSION")
azure_search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
azure_search_key = os.environ.get("AZURE_SEARCH_KEY")
azure_search_deployment_name = os.environ.get("AZURE_SEARCH_DEPLOYMENT_NAME")
vector_dimension = 1536  # Dimension for text-embedding-3-small
datafile = "./Data"
azure_search_index_name = "rag-1756588180789"
azure_openAI_api_version = "2023-07-01-Preview"


async def AISearchFinalResult_tool(
    query: str, top_k: int = 10, thresholdFilter: int = 50
) -> list[dict[str, str]]:
    """
    This function searches for documents related to a user query and evaluates their relevance.

    Parameters:
        query (str): The user's search query.
        top_k (int): The number of top similar documents to retrieve and evaluate.

    Returns (list[dict[str, str]]):
        A list of dictionaries containing search results and their corresponding scores, sorted by score in descending order.

    Example:
        query = "What is Template J used for?",
        top_k = 5

        return = [
            {"Score": 85, "SearchResult": "Template J is used for generating reports."},
            {"Score": 60, "SearchResult": "Template J is a type of document"},
            {"Score": 10, "SearchResult": "Template J is not related to the query."}
            ]
    """

    # Step 1: Search for documents
    searchResults = await searchDocuments_tool(query, top_k)

    # Step 2: Evaluate and score the search results
    AISearchAndEvaluator = await SearchResultScoring_tool(query, searchResults)

    trimmed_searchResult = []

    for r in AISearchAndEvaluator:
        if r["Score"] >= thresholdFilter:
            trimmed_searchResult.append(r)

    return trimmed_searchResult
