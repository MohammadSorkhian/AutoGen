import os
from _clients._openAI_client import openAI_client
from dotenv import load_dotenv
load_dotenv()

# Retrieve credentials from environment variables
azure_search_deployment_name = os.environ.get("AZURE_SEARCH_DEPLOYMENT_NAME")
vector_dimension = 1536



def embed_text(text) -> str:
    response = openAI_client.embeddings.create(
        input=[text],
        model=azure_search_deployment_name,
        dimensions=vector_dimension
    )
    embedding = response.data[0].embedding
    return embedding