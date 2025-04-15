# tools/calendar_tool.py
from langchain.tools import BaseTool
import pandas as pd
import os

CALENDAR_FILE = "content_calendar.csv"

class CalendarSchedulerTool(BaseTool):
    name = "Calendar Scheduler"
    description = "Schedules content in a local CSV calendar with title, type, and publish date."

    def _run(self, title: str, content_type: str, publish_date: str) -> str:
        data = {"Title": title, "Content Type": content_type, "Publish Date": publish_date}
        if os.path.exists(CALENDAR_FILE):
            df = pd.read_csv(CALENDAR_FILE)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        else:
            df = pd.DataFrame([data])
        df.to_csv(CALENDAR_FILE, index=False)
        return f"Scheduled '{title}' for {publish_date}"

    def _arun(self, title: str, content_type: str, publish_date: str):
        raise NotImplementedError("Async not supported for this tool.")

calendar_tool = CalendarSchedulerTool()