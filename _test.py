import os, asyncio
# from _agents._classifier_assiatent import get_classifier_agent
# from _agents._userProxyAgent import get_user_proxy_agent
# from _tools._searchDocuments import search_documents
# from _agents._knowledge_base_assistant import knowledgeBased_assistant
from AutoGen._tools._AISearchResultEvaluator_tools import AISearchResultEvaluator

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



# # 1. First agent testing
# def run_test():

#     user = get_user_proxy_agent()
#     classifier = get_classifier_agent()
    
#     for q in sample_query:
#         print(f"\nQuery: {q}")
#         user.initiate_chat(
#             recipient=classifier, 
#             message=f"Classify this query: {q}", 
#             max_turns=1
#         )


# # # 2. Second agent testing
# # def run_kb_test():

# #     user = get_user_proxy_agent()

# #     # ✅ Register tool for execution with *this* user instance
# #     user.register_for_execution(name="searchDocuments")(search_documents)


# #     user.initiate_chat(
# #         recipient=knowledgeBased_assistant,
# #         message="Use the tool search_documents to find the fix for: My Outlook crashes every time I open it. Category is Software Bug",
# #         max_turns=2,
# #     )


# if __name__ == "__main__":
#     # 1. test the classify agent
#     # run_test()

# #     # 2. test the KB agent
# #     run_kb_test()




# if __name__ == "__main__":
#     query = "waht is template J for?"
#     AISearchResults = [
#         "Template J is not related to the query.",
#         "Template J is used for generating reports.",
#         "Template J is a type of document format.",
#     ]
#     output = asyncio.run(AISearchResultEvaluator(query, AISearchResults))
#     print(output)