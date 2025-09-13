from autogen_agentchat.agents import AssistantAgent
from _utilities._prompts import classifier_prompt
from _clients._openAI_client import openAI_client

from dotenv import load_dotenv
load_dotenv()



classifier_assistantAgent = AssistantAgent(
    name="ClassifierAgent",
    model_client=openAI_client,
    system_message = classifier_prompt
)