import os
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

# Retrieve credentials from environment variables
azure_openAI_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
azure_openAI_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
azure_openAI_api_version = os.environ.get("AZURE_OPENAI_API_VERSION")



openAI_client = AzureOpenAI(
    azure_endpoint=azure_openAI_endpoint,
    api_key=azure_openAI_api_key,
    api_version=azure_openAI_api_version
    )