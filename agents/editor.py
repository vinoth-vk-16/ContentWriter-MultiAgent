# agents/editor.py
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

editor = Agent(
    role="Editor",
    goal="Review drafts for grammar, tone consistency, and clarity, producing a polished version suitable for web display.",
    backstory="A meticulous editor who enhances drafts to be engaging and error-free for online publication.",
    verbose=True,
    llm=llm
)