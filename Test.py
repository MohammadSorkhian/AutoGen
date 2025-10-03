import os, asyncio, json

# from _agents._classifier_assiatent import get_classifier_agent
# from _agents._userProxyAgent import get_user_proxy_agent
# from _tools._searchDocuments import search_documents
# from _agents._knowledge_base_assistant import knowledgeBased_assistant
from autogen_agentchat.agents import AssistantAgent
from _clients._azureOpenAIChatCompletion_client import AzureOpenAIChatCompletionClient
from _tools._10_SearchResultScoring_tool import AISearchResultEvaluator_tool
from _tools._15_AISearchFinalResult_tool import AISearchAndEvaluator_tool
from _tools._05_searchDocuments_tool import searchDocuments_tool
from _tools._45_webScraper import WebScraper, ScraperConfig
from _agents._classifier_assiatentAgent import classifier_assistantAgent
from autogen_agentchat.tools import AgentTool
from autogen_core.tools import FunctionTool
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


# query = "write a bio for mohammad?"
# query = "how can we create a business case for DischargeHUB to expand it to new jurisdictions in Canada?"

# Step 1: Search for documents
# searchResults = asyncio.run(searchDocuments_tool(query, 3))

# Step 2: Evaluate and score the search results
# scoredSearchResults = asyncio.run(AISearchResultEvaluator_tool(query, searchResults))

# classifiedSearchResult = asyncio.run(classifier_assistantAgent.run(task=query))

# result = classifiedSearchResult.messages[-1].content
# print(result)

# result = asyncio.run(
#     AISearchCleaner_tool(
#         query="What is Template J for",
#         searchResult=[
#             {"Score": 85, "SearchResult": "Template J is used for generating reports."},
#             {"Score": 60, "SearchResult": "Template J is a type of document"},
#             {"Score": 10, "SearchResult": "Template J is not related to the query."},
#         ],
#     )
# )

# for x in result:
# print(x)


async def main():
    config = ScraperConfig(include_html=True)
    scraper = WebScraper(config)
    results = await scraper.scrape("Who is Mohammad?")

    for r in results:
        print(f"\n--- {r.url} ---")
        print(f"Status: {r.status}")
        print(f"Title: {r.title}")
        print(f"Language: {r.language}")
        print(f"Text Preview: {r.text[:500] if r.text else 'No text extracted'}")
        print(f"Error: {r.error}")


if __name__ == "__main__":
    asyncio.run(main())



print("\nDone!")
