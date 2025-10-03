from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from modelsAndClients.azureOpenAIChatCompletion_model import AzureOpenAI_model
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

# Defining the steps
# 1. Interviewer Agent  -> Assistant Agent
# 2. Candidate Agent  -> User Proxy Agent
# 3. Career Coach Agent -> Assistant Agent
# 4. Group Chat

job_position = "Software Developer"

##### 1. Interviewer Agent #####
interviewer_agent = AssistantAgent(
    name="InterviewerAgent",
    model_client=AzureOpenAI_model,
    description=f"""You are an interviewer conducting a job interview for a {job_position} position.""",
    system_message=f"""
    You are a professional interviewer for a {job_position} position.
    Ask one clear question at a time and wait for the candidate's response.
    Ask five questions in total covering technical skills and experience, problem-solving abilities, cultural fit, and career aspirations.
    After asking three questions, say 'TERMINATE' at the end of the interview.
    """,
)

##### 2. Candidate Agent #####
candidate_agent = UserProxyAgent(
    name="CandidateAgent",
    description=f"""You are a candidate interviewing for a {job_position} position.""",
)

##### 3. Career Coach Agent #####
career_coach_agent = AssistantAgent(
    name="CareerCoachAgent",
    model_client=AzureOpenAI_model,
    description=f"""You are a career coach for a {job_position} position.""",
    system_message=f"""
    you are a career coach helping candidates prepare for interviews for a {job_position} position.
    Provide constructive feedback on their answers, and overall presentation.
    After the interview is terminated, provide a summary of the candidate's strengths and areas for improvement.
    """,
)

##### 4. Group Chat #####
group_chat = RoundRobinGroupChat(
    participants=[interviewer_agent, candidate_agent, career_coach_agent],
    termination_condition=TextMentionTermination(text="TERMINATE"),
    max_turns=15
)
