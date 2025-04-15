# tools/file_tool.py
from langchain.tools import BaseTool
import os
import re

class FileSaverTool(BaseTool):
    name = "File Saver"
    description = "Saves content to a project folder with a given title and content type, ensuring valid file paths and error handling."

    def _run(self, title: str, content: str, content_type: str, *args, **kwargs) -> str:
        # Log arguments for debugging
        print(f"FileSaverTool._run called with: title='{title}', content_type='{content_type}', content='{content[:50]}...', extra_args={args}, kwargs={kwargs}")
        
        try:
            # Sanitize title
            if not title:
                raise ValueError("Title cannot be empty")
            safe_title = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', title.strip())
            safe_title = safe_title.replace(' ', '_').lower()
            if not safe_title:
                raise ValueError("Sanitized title is empty")

            # Sanitize content_type
            if not content_type:
                raise ValueError("Content type cannot be empty")
            safe_content_type = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', content_type.strip())
            safe_content_type = safe_content_type.replace(' ', '_').lower()
            if not safe_content_type:
                raise ValueError("Sanitized content type is empty")

            # Create folder path
            folder = f"projects/{safe_content_type}"
            os.makedirs(folder, exist_ok=True)

            # Create file path
            file_path = f"{folder}/{safe_title}.md"

            # Validate content
            if not content:
                raise ValueError("Content cannot be empty")

            # Write content to file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content.strip())

            return f"Saved content to {file_path}"
        except Exception as e:
            error_msg = f"Failed to save file: {str(e)}"
            print(error_msg)  # Log error
            return error_msg

    def _arun(self, title: str, content: str, content_type: str):
        raise NotImplementedError("Async not supported for this tool.")

file_tool = FileSaverTool()