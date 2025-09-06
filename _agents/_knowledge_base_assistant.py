import os, sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from _clients._search_client import search_client
from _clients._azureOpenAIChatCompletion_client import AzureOpenAIChatCompletionClient
from _utilities._llm_config import llm_config
from _tools._searchDocuments import search_documents
from autogen import AssistantAgent
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



knowledgeBased_assistant = AssistantAgent(
    name="knowledgeBased",
    system_message="""
    You are an special answer finder.
    You find the answer to the user's question based on the knowledge you have.
    Always call the 'search similar_documents' tool to find relevant information from the knowledge.
    After calling, summarize the top solutions and respond with TERMINATE.
    """, 
    llm_config=llm_config,
    # model_client= AzureOpenAIChatCompletionClient,
    # code_execution_config={"use_docker": False},
)


# Register tool with LLM and executor

# 1. LLm knows when to call the tool
knowledgeBased_assistant.register_for_llm(
    name="search_documents",
    description="Searches for top relevant documents from a knowledge base using a vector similarity search. Accepts query and top_k.",
)(search_documents)

# 2. Executed the tool
knowledgeBased_assistant.register_for_execution(
    name="search_similar_solution"
)(search_client)
