# tools/keyword_tool.py
from langchain.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Explicitly load .env file
load_dotenv()

# Verify GOOGLE_API_KEY
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file. Please set it with a valid Gemini API key.")

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    google_api_key=google_api_key,
    temperature=0.5
)

class KeywordGeneratorTool(BaseTool):
    name = "Keyword Generator"
    description = "Generates SEO-friendly keywords for a given topic."

    def _run(self, topic: str) -> list:
        prompt = f"Suggest 5-7 SEO-friendly keywords for the topic: {topic}"
        response = llm.invoke(prompt)
        keywords = response.content.split("\n")
        return [kw.strip() for kw in keywords if kw.strip()]

    def _arun(self, topic: str):
        raise NotImplementedError("Async not supported for this tool.")

keyword_tool = KeywordGeneratorTool()