import os, asyncio

# from _agents._classifier_assiatent import get_classifier_agent
# from _agents._userProxyAgent import get_user_proxy_agent
# from _tools._searchDocuments import search_documents
# from _agents._knowledge_base_assistant import knowledgeBased_assistant
from autogen_agentchat.agents import AssistantAgent
from _clients._azureOpenAIChatCompletion_client import AzureOpenAIChatCompletionClient
from _tools._AISearchResultEvaluator_tool import AISearchResultEvaluator_tool
from _tools._AISearchAndEvaluator_tool import AISearchAndEvaluator_tool
from _tools._searchDocuments_tool import searchDocuments_tool
from autogen_agentchat.tools import AgentTool
from autogen_core.tools import FunctionTool
import time
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


sample_query = [
    "write a bio for mohammad?",
]


# result = asyncio.run(searchDocuments_tool("What is Template J used for?", top_k=5))
# result2 = asyncio.run(
# AISearchResultEvaluator_tool("What is Template J used for?", result)
# )

result2 = asyncio.run(AISearchAndEvaluator_tool("who is mohammad", top_k=5))

print(result2[0])

print("\nDone!")
