import os
from dotenv import load_dotenv
load_dotenv()

# Retrieve credentials from environment variables
azure_openAI_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
azure_openAI_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
azure_openAI_deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
azure_openAI_api_version = os.environ.get("AZURE_OPENAI_API_VERSION")

azure_search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
azure_search_key = os.environ.get("AZURE_SEARCH_KEY")
azure_search_deployment_name = os.environ.get("AZURE_SEARCH_DEPLOYMENT_NAME") 

vector_dimension = 1536  # Dimension for text-embedding-3-small
datafile = "./Data"
azure_search_index_name = "rag-1756588180789"



llm_config={
    "temperature": 0,
    "config_list": [
        {
            "model": azure_openAI_deployment_name,  # This should match your deployment name
            "api_key": azure_openAI_api_key,
            "base_url": azure_openAI_endpoint,
            "api_type": "azure",
            "api_version": azure_openAI_api_version
        }
    ]
}