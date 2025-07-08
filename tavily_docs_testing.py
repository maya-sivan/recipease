
from tavily import TavilyClient
from langchain_openai import ChatOpenAI
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

tavily_client = TavilyClient(TAVILY_API_KEY)

search_response = tavily_client.search("Who is Leo Messi?")


extract_response = tavily_client.extract([
    "https://en.wikipedia.org/wiki/Lionel_Messi",
    "https://www.fcbarcelona.com/en/",
    "https://www.intermiamicf.com/news/"
])


topics = [
    "United States Politics",
]
context = []

for topic in topics:

  search_response = tavily_client.search(topic, topic="news", time_range="day")

  context.append({
      "topic": topic,
      "results": [
          { "url": result["url"], "title": result["title"], "content": result["content"] } for result in search_response["results"]
      ]
  })




gpt_4o = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o", temperature=0.0)

prompt = """
    You are a Journalist agent.

    - Generate a daily news digest. Today's date is {date}.
    - Use only the following sources to get accurate information for each topic and write a short article about it:
      {context}.
    """

formatted_prompt = prompt.format(context=context, date=datetime.now().strftime("%Y-%m-%d"))
gpt_4o_response = gpt_4o.invoke(formatted_prompt)

print(gpt_4o_response.content)
