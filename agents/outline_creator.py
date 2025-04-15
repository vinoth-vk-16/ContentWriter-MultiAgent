# agents/outline_creator.py
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
    temperature=0.7  # Increased for more varied outlines
)

outline_creator = Agent(
    role="Outline Creator",
    goal="Generate two distinct, well-structured content outlines labeled 'Outline 1:' and 'Outline 2:', each with H1-H3 headings, tailored to the topic, audience, tone, and style, for display in a web interface.",
    backstory="A creative strategist skilled at crafting varied, clear, and engaging outlines for user selection in a web application.",
    verbose=True,
    llm=llm
)