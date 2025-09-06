from autogen import UserProxyAgent


def get_user_proxy_agent():
    user = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        code_execution_config=False,
    )
    return user