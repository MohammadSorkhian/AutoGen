import os, requests, json



serper_API_key = os.environ.get("SERPER_API_KEY")


def web_search_serper(query: str) -> str:
    """
    Perform a web search using the Serper API and return the results.
    """
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query, "gl": "in"})
    headers = {
        "X-API-KEY": serper_API_key,
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"
    return response.text
