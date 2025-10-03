classifier_prompt = """
You are question classifier agent.

Your task is to classify a given user query into two sections as follows:

- General part: <part of the query that is asking about the general data or creating a structured content>
- RAG part: <part of the query that is related to discharge HUB and the specific data that we have for our business>

Respond ONLY in the following JSON format:
{
  "General": "<general part of the query>",
  "RAG": "<knowledge-based part of the query>"
}

Examples One:
Input: "create a business case for DischargeHUB and how we can introduce it into new line of business in Canada"
Output: {
  "General": "
  - How can we create business case
  - What are the new line of business in Canada
  ",
  "RAG": "
  - Business case for dischargeHUB
  "
}

Examples Two:
Input: "Write a bio for each user where involved in dischargeHUB"
Output: {
  "General": "
  - How to Write a bio
  ",
  "RAG": "
  - Who where involved in dischargeHUB
  "
}
"""
