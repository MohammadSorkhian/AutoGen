from _clients._azureOpenAIChatCompletion_client import model_client
from autogen_agentchat.agents import AssistantAgent


async def AISearchResultEvaluator_tool(query:str, AISearchResults:list) -> list[dict[str, str]]:
    """
    This function evaluates and scores retrieved AI search results based on their relevance to a user query.

    Parameters:
        query (str): The user's search query.
        AISearchResults (list): A list of search results to be evaluated.

    Returns:
        A list of dictionaries containing search results and their corresponding scores, sorted by score in descending order.

    Example:
        query = "What is Template J used for?",
        AISearchResults = [
            "Template J is used for generating reports.",
            "Template J is a type of document format.",
            "Template J is not related to the query."
            ]
                
        return = [
            {"Score": 85, "SearchResult": "Template J is used for generating reports."},
            {"Score": 60, "SearchResult": "Template J is a type of document"},
            {"Score": 10, "SearchResult": "Template J is not related to the query."}
            ]
    """

    output = []

    agent_AISearchResultEvaluator = AssistantAgent(
        name="AISearchResultEvaluator",
        model_client=model_client,
        system_message="You are a helpful assistant. that get a user 'user query' and a 'search result'. I want you to compare the user query with the result and if the result helps to answer the user query, return an core between o to 100. 0 shows the least relevancy between query and result while 100 shows the most. Your output should be a single intiger between 0 to 100. Do not include any text other than the integer.",
    )

    for r in AISearchResults:
        score = await agent_AISearchResultEvaluator.run(
            task=f"user query: {query} search result: {r}"
        )
        score = score.messages[-1].content

        try:
            score = int(score)
        except ValueError:
            print(
                "The AISearchResultEvaluator is not a number instead it returned: {score}"
            )
            continue

        output.append({"Score": score, "SearchResult": r})

    output_sorted = sorted(output, key=lambda x: x["Score"], reverse=True)

    return output_sorted
