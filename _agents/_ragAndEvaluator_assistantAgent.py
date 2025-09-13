import os, sys
from _tools._searchDocuments_tool import search_documents
from _tools._AISearchResultEvaluator_tool import AISearchResultEvaluator
from _clients._azureOpenAIChatCompletion_client import AzureOpenAIChatCompletionClient
from _tools._searchDocuments_tool import search_documents
from autogen_agentchat.agents import AssistantAgent
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



ragAndEvaluator_assistantAgent = AssistantAgent(
    name="ragAndEvaluator_assistantAgent",
    model_client=op,
    tools=[writer_tool],
    system_message="You are a helpful assistant."
)


