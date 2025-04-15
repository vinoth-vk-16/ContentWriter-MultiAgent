# agents/calendar_manager.py
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

calendar_manager = Agent(
    role="Calendar Manager",
    goal="Schedule content in a local CSV calendar and save it to a file using exactly title, content, and content_type for the file tool, ensuring clear confirmation for web display.",
    backstory="A precise planner who schedules content and saves it reliably with correct tool inputs, confirming actions clearly for users.",
    verbose=True,
    llm=llm
)