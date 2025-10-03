from autogen_agentchat.agents import AssistantAgent
from _utilities._prompts import classifier_prompt
from _clients._openAI_client import openAI_client
from _clients._azureOpenAIChatCompletion_client import model_client
from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()


class classifierOutputSchema(BaseModel):
    general: str
    RAG: str


classifier_assistantAgent = AssistantAgent(
    name="ClassifierAgent",
    model_client=model_client,
    system_message=classifier_prompt,
    output_content_type=classifierOutputSchema,
)
