# AI-Powered Content Writer

Welcome to the **AI-Powered Content Writer** project! This repository contains a multi-agent system built using **CrewAI** to streamline the process of content creation, optimization, and scheduling. The application is designed to generate high-quality content based on user inputs, optimize it for SEO, verify grammar and tone, and save the final draft. The project leverages agents, tools, and tasks to achieve these goals in a structured and efficient manner.

---

## Features

1. **Multi-Agent System**: Built with CrewAI, the project uses specialized agents to handle different stages of content creation.
2. **Customizable Content Generation**: Users can input their requirements (topic, audience, tone, style, etc.) to generate tailored content outlines.
3. **SEO Optimization**: The SEO agent suggests keywords and incorporates them into the content for better web visibility.
4. **Grammar and Tone Verification**: The Editor agent ensures the content is grammatically correct and consistent with the selected tone.
5. **Content Scheduling and Saving**: The Calendar Manager agent schedules the content in a CSV calendar and saves it to the appropriate project folder.
6. **Streamlit Web Interface**: A user-friendly web interface for seamless interaction with the system.

---


## How It Works

### 1. **Input Content Details**
- Users provide the following inputs via the Streamlit web interface:
  - **Topic**: The subject of the content.
  - **Target Audience**: Selected from predefined options in `config.py`.
  - **Tone**: The tone of the content (e.g., Formal, Conversational).
  - **Writing Style**: The style of the content (e.g., Persuasive, Narrative).
  - **Content Type**: The type of content (e.g., Blog Post, Social Media Post).
  - **Preferred Publish Date**: The desired date for publishing the content.
  - **Anecdote**: An optional short story to include in the content.

### 2. **Generate Outlines**
- The **Outline Creator Agent** generates two distinct content outlines based on the user inputs.
- Users can select one of the outlines or request modifications for a new set of outlines.

### 3. **SEO Optimization**
- The selected outline is passed to the **SEO Optimizer Agent**, which:
  - Suggests 5-7 SEO-friendly keywords.
  - Incorporates the keywords into a full draft.

### 4. **Grammar and Tone Verification**
- The draft is reviewed by the **Editor Agent**, which:
  - Ensures grammatical correctness.
  - Verifies consistency with the selected tone.
  - Provides a polished version of the draft.

### 5. **Schedule and Save**
- The **Calendar Manager Agent**:
  - Schedules the content in a CSV calendar.
  - Saves the final draft to the appropriate folder in the `projects/` directory.

### 6. **Content Calendar**
- The scheduled content is displayed in a table format within the Streamlit app.
- The calendar is also available as a downloadable CSV file.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vinoth-vk-16/ContentWriter-MultiAgent.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the `.env` file:
   - Create a `.env` file in the root directory.
   - Add your Google API Key for the `langchain-google-genai` library.

4. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## Configuration

The `config.py` file defines the following options:
- **CONTENT_TYPES**: Types of content (e.g., Blog Post, Social Media Post).
- **TONES**: Available tones for the content (e.g., Formal, Humorous).
- **AUDIENCES**: Target audiences (e.g., Tech Enthusiasts, Students).
- **WRITING_STYLES**: Writing styles (e.g., Persuasive, Narrative).

You can customize these options to suit your requirements.

---

## Agents and Tools

### Agents
- **Outline Creator**: Generates content outlines.
- **SEO Optimizer**: Optimizes content for SEO.
- **Editor**: Verifies grammar and tone.
- **Calendar Manager**: Schedules and saves content.

### Tools
- **Keyword Tool**: Generates SEO-friendly keywords.
- **Calendar Tool**: Schedules content in a CSV calendar.
- **File Tool**: Saves content to project folders.

---

## Dependencies

The project uses the following Python libraries:
- `crewai`: Multi-agent framework for task orchestration.
- `streamlit`: Web interface for user interaction.
- `google-generativeai`: Integration with Google's Generative AI models.
- `python-dotenv`: Environment variable management.
- `pandas`: Data manipulation for the content calendar.
- `langchain`: Framework for building LLM-powered applications.

Refer to the `requirements.txt` file for the complete list of dependencies.

---

## Future Enhancements

- Add support for additional content types and tones.
- Integrate more advanced SEO tools for keyword analysis.
- Enable asynchronous task execution for faster processing.
- Provide analytics for content performance.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

- CrewAI for the multi-agent framework.
- Streamlit for the web interface.
- Google Generative AI for LLM integration.

---

## Contact

For questions or feedback, please open an issue or contact imvinothvk521@gmail.com
