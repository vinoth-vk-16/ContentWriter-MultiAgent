# agents/seo_optimizer.py
from crewai import Agent
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

seo_optimizer = Agent(
    role="SEO Optimizer",
    goal="Optimize a provided outline with 5-7 SEO keywords and produce a full, web-displayable draft with keywords listed as '- keyword' at the start.",
    backstory="An expert SEO specialist who crafts clear, keyword-rich drafts optimized for web visibility.",
    verbose=True,
    llm=llm
)