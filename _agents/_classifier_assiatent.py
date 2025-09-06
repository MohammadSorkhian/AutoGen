from autogen import AssistantAgent
from _utilities._prompts import classifier_prompt
from _utilities._llm_config import llm_config

from dotenv import load_dotenv
load_dotenv()



def get_classifier_agent():

    agent_cls = AssistantAgent(
        name="ClassifierAgent",
        llm_config=llm_config,
        system_message = classifier_prompt
    )
    return agent_cls