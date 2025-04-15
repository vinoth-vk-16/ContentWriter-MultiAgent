# agents/content_generator.py
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
    temperature=0.7
)

content_generator = Agent(
    role="Content Generator",
    goal="Generate high-quality drafts based on provided outlines, incorporating topic, audience, tone, and anecdotes.",
    backstory="An expert writer skilled in crafting engaging content tailored to specific audiences and styles.",
    verbose=True,
    llm=llm
)