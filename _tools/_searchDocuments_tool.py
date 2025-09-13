import os, requests
from _tools._embedding_tool import embed_text
import asyncio
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
azure_openAI_api_version = '2023-07-01-Preview'


async def searchDocuments_tool(query:str, top_k=8):
    """
    Search for similar documents in Azure Cognitive Search using user query.

    Parameters:
        query (str): The input text query to search for similar documents.
        top_k (int): The number of top similar documents to retrieve.

    Returns:
        list: A list of top_k similar documents.

    Example:
        results = search_documents("How to reset my password?", top_k=5)

        return:[
            "Result 1",
            "Result 2",
            "result 3", 
            "result 4",
            "result 5"
            ]
    """
    embedding = embed_text(query)

    url = f"{azure_search_endpoint}/indexes/{azure_search_index_name}/docs/search?api-version={azure_openAI_api_version}"

    headers = {
        "Content-Type": "application/json", 
        "api-key": azure_search_key
        }

    payload = {
        "count": True,
        "search": "{query}",
        "vector": {"value": embedding, "k": top_k, "fields": "text_vector"},
        "top": top_k,
    }

    response = requests.post(url, headers=headers, json=payload)
    response = response.json().get("value", [])

    response_list = []
    for idx, doc in enumerate(response, 1):
        response_list.append(doc.get('chunk'))
        
    return response_list

