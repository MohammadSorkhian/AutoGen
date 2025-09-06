import os, requests
import requests
from _clients._openAI_client import openAI_client
import os, sys
from azure.search.documents.indexes import SearchIndexClient

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



def embed_text(text):
    response = openAI_client.embeddings.create(
        input=[text],
        model=azure_search_deployment_name
    )
    embedding = response.data[0].embedding
    return embedding



def search_documents(query=[], top_k=3):

    embedding = embed_text(query)

    url= f"{azure_search_endpoint}/indexes/{azure_search_index_name}/docs/search?api-version={'2023-07-01-Preview'}"

    headers = {
        "Content-Type": "application/json",
        "api-key": azure_search_key
    }

    payload = {
        "count": True,
        "search":"{query}",
        "vector": {
            "value": embedding,
            "k": top_k,
            "fields": "text_vector"
        },
        "top": top_k
    }

    response = requests.post(url, headers=headers, json=payload)
    response = response.json().get("value", [])

    response_text = ""
    for idx, doc in enumerate(response, 1):
        response_text += (
            f"\nResult {idx}:\n"
            f"{doc.get('chunk')}\n"
        )

    return response_text
