from _clients._azureOpenAIChatCompletion_client import model_client
from autogen_agentchat.agents import AssistantAgent

async def AISearchResultEvaluator(query, AISearchResults):
    
    output = []
    
    agent_AISearchResultEvaluator = AssistantAgent(
        name="AISearchResultEvaluator",
        model_client= model_client,
        system_message="You are a helpful assistant. that get a user 'query' and a 'result'. I want you to compare the user query with the result and if the result helps to answer the user query, return an core between o to 100. 0 shows the least relevancy between query and result while 100 shows the most. Your output should be a single intiger between 0 to 100. Do not include any text other than the integer.",
    )

    for r in AISearchResults:
        score = await agent_AISearchResultEvaluator.run(task=f"query: {query} result: {r}")
        score = score.messages[-1].content
        
        try:
            score = int(score)
        except ValueError:
            print("The AISearchResultEvaluator is not a number instead it returned: {score}")
            continue
        
        output.append({"Score": score, "SearchResult": r})
        
    print(output)
        
    output_sorted = sorted(output, key=lambda x: x["Score"], reverse=True)
    
    return output_sorted
        
        
        


