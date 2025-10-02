import os, asyncio
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core.models import UserMessage
from dotenv import load_dotenv
load_dotenv()

# Retrieve credentials from environment variables
azure_openAI_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
azure_openAI_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
azure_openAI_deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
azure_openAI_api_version = os.environ.get("AZURE_OPENAI_API_VERSION")



model_client = AzureOpenAIChatCompletionClient(
    azure_endpoint=azure_openAI_endpoint,
    model=azure_openAI_deployment_name,
    api_key=azure_openAI_api_key,
    api_version=azure_openAI_api_version,
)



if __name__ == "__main__":
    result = asyncio.run(model_client.create([UserMessage(content="This is a test message reply with 'Hello World!'", source="user")]))
    print(result.content)
    
 