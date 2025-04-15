# app.py
import streamlit as st
from crewai import Crew, Task
from agents.outline_creator import outline_creator
from agents.seo_optimizer import seo_optimizer
from agents.editor import editor
from agents.calendar_manager import calendar_manager
from tools.keyword_tool import keyword_tool
from tools.calendar_tool import calendar_tool
from tools.file_tool import file_tool
from config import CONTENT_TYPES, TONES, AUDIENCES, WRITING_STYLES
import pandas as pd
import os
from datetime import datetime
import streamlit.components.v1 as components

# Streamlit UI Configuration
st.set_page_config(page_title="AI Content Writer", layout="wide")
st.markdown("<style>{}</style>".format(open("static/styles.css").read()), unsafe_allow_html=True)

# Menu Bar (without buttons)
menu_html = """
<div class="menu-bar"></div>
"""
components.html(menu_html, height=60)

# Main Title
st.markdown('<div id="top"></div>', unsafe_allow_html=True)
st.title("AI-Powered Content Writer")

# Initialize Session State
if "outlines" not in st.session_state:
    st.session_state.outlines = []
if "selected_outline" not in st.session_state:
    st.session_state.selected_outline = None
if "modification_input" not in st.session_state:
    st.session_state.modification_input = ""
if "seo_draft" not in st.session_state:
    st.session_state.seo_draft = ""
if "keywords" not in st.session_state:
    st.session_state.keywords = []
if "edited_draft" not in st.session_state:
    st.session_state.edited_draft = ""
if "scheduling_status" not in st.session_state:
    st.session_state.scheduling_status = ""

# Input Form
with st.form("content_form"):
    st.header("Step 1: Input Content Details")
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Topic", placeholder="e.g., Benefits of AI in Education")
        audience = st.selectbox("Target Audience", AUDIENCES)
        tone = st.selectbox("Tone", TONES)
    with col2:
        writing_style = st.selectbox("Writing Style", WRITING_STYLES)
        content_type = st.selectbox("Content Type", CONTENT_TYPES)
        publish_date = st.date_input("Preferred Publish Date", min_value=datetime.today())
    anecdote = st.text_area("Anecdote (Short Story)", placeholder="Add a relevant short story or leave blank")
    submit = st.form_submit_button("Generate Outlines", type="primary")

# Generate Two Outlines
if submit and topic:
    with st.spinner("Generating outlines..."):
        outline_task = Task(
            description=f"Generate two distinct outlines for '{topic}' aimed at '{audience}' with a '{tone}' tone and '{writing_style}' style. Each outline should have H1-H3 headings and incorporate '{anecdote}' if provided. Format as:\nOutline 1:\n[content]\n\nOutline 2:\n[content]",
            agent=outline_creator,
            expected_output="Two outlines labeled 'Outline 1:' and 'Outline 2:' with H1-H3 headings."
        )
        crew = Crew(agents=[outline_creator], tasks=[outline_task], verbose=True)
        try:
            result = crew.kickoff()
            output = str(result).strip()
            if "\n\nOutline 2:" in output:
                outlines = output.split("\n\nOutline 2:")
                outline1 = outlines[0].replace("Outline 1:", "").strip()
                outline2 = outlines[1].strip()
                st.session_state.outlines = [outline1, outline2]
            else:
                st.session_state.outlines = [output.replace("Outline 1:", "").strip(), ""]
            st.session_state.selected_outline = None
            st.session_state.modification_input = ""
            st.session_state.seo_draft = ""
            st.session_state.keywords = []
            st.session_state.edited_draft = ""
            st.session_state.scheduling_status = ""
        except Exception as e:
            st.error(f"Failed to generate outlines: {e}")
            st.session_state.outlines = []

# Display Outlines and Selection
if st.session_state.outlines:
    st.header("Step 2: Choose an Outline")
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("Outline 1", expanded=True):
            st.markdown(st.session_state.outlines[0] if st.session_state.outlines[0] else "No content generated.")
    with col2:
        with st.expander("Outline 2", expanded=True):
            st.markdown(st.session_state.outlines[1] if st.session_state.outlines[1] else "No second outline generated.")
    
    col_select, col_generate = st.columns([3, 2])
    with col_select:
        selected = st.radio("Select an Outline", ["Outline 1", "Outline 2"], key="outline_selection")
        if selected == "Outline 1" and st.session_state.outlines[0]:
            st.session_state.selected_outline = st.session_state.outlines[0]
        elif selected == "Outline 2" and st.session_state.outlines[1]:
            st.session_state.selected_outline = st.session_state.outlines[1]
    with col_generate:
        st.text_input("Modification (e.g., 'more technical', 'simpler')", key="modification_input")
        if st.button("Generate Differently"):
            with st.spinner("Generating new outlines..."):
                modification = st.session_state.modification_input.strip()
                if modification:
                    outline_task = Task(
                        description=f"Generate two distinct outlines for '{topic}' aimed at '{audience}' with a '{tone}' tone and '{writing_style}' style, modified as '{modification}'. Each outline should have H1-H3 headings and incorporate '{anecdote}' if provided. Format as:\nOutline 1:\n[content]\n\nOutline 2:\n[content]",
                        agent=outline_creator,
                        expected_output="Two outlines labeled 'Outline 1:' and 'Outline 2:' with H1-H3 headings."
                    )
                    crew = Crew(agents=[outline_creator], tasks=[outline_task], verbose=True)
                    try:
                        result = crew.kickoff()
                        output = str(result).strip()
                        if "\n\nOutline 2:" in output:
                            outlines = output.split("\n\nOutline 2:")
                            outline1 = outlines[0].replace("Outline 1:", "").strip()
                            outline2 = outlines[1].strip()
                            st.session_state.outlines = [outline1, outline2]
                        else:
                            st.session_state.outlines = [output.replace("Outline 1:", "").strip(), ""]
                        st.session_state.selected_outline = None
                        st.success("New outlines generated based on your modification!")
                    except Exception as e:
                        st.error(f"Failed to generate new outlines: {e}")
                else:
                    st.warning("Please enter a modification description.")

# Generate SEO-Optimized Draft
if st.session_state.selected_outline:
    if st.button("Optimize with SEO", type="primary"):
        with st.spinner("Optimizing draft with SEO..."):
            seo_task = Task(
                description=f"Optimize this outline for SEO: '{st.session_state.selected_outline}'. Suggest 5-7 SEO keywords for '{topic}' and incorporate them into a full draft. List keywords first as '- keyword', followed by the draft.",
                agent=seo_optimizer,
                tools=[keyword_tool],
                expected_output="Keywords listed as '- keyword' followed by an SEO-optimized draft."
            )
            crew = Crew(agents=[seo_optimizer], tasks=[seo_task], verbose=True)
            try:
                result = crew.kickoff()
                output = str(result).strip()
                lines = output.split("\n")
                keywords = [line.strip() for line in lines if line.strip().startswith("- ")]
                draft = "\n".join([line for line in lines if not line.strip().startswith("- ")])
                st.session_state.keywords = keywords
                st.session_state.seo_draft = draft.strip()
                st.session_state.edited_draft = draft.strip()
                st.session_state.scheduling_status = ""
            except Exception as e:
                st.error(f"Failed to optimize draft: {e}")
                st.session_state.seo_draft = ""
                st.session_state.keywords = []

# Display SEO Draft and Keywords
if st.session_state.seo_draft:
    st.header("Step 3: SEO-Optimized Draft")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Draft")
        st.markdown(st.session_state.seo_draft)
    with col2:
        st.subheader("Keywords")
        if st.session_state.keywords:
            for kw in st.session_state.keywords:
                st.write(kw)
        else:
            st.write("No keywords generated.")

    # Verification and Editing
    st.header("Step 4: Verify and Edit Draft")
    with st.form("edit_form"):
        st.subheader("Edit Draft")
        edited_draft = st.text_area("", value=st.session_state.seo_draft, height=400, key="draft_textarea")
        verify_button = st.form_submit_button("Verify Grammar and Tone", type="primary")
        
        if verify_button:
            with st.spinner("Verifying draft..."):
                edit_task = Task(
                    description=f"Review this draft for grammar, tone consistency ('{tone}'), and suggest improvements: '{edited_draft}'. Return the improved draft.",
                    agent=editor,
                    expected_output="An improved draft with grammar and tone corrections."
                )
                crew = Crew(agents=[editor], tasks=[edit_task], verbose=True)
                try:
                    result = crew.kickoff()
                    st.session_state.edited_draft = str(result).strip()
                except Exception as e:
                    st.error(f"Failed to verify draft: {e}")
                    st.session_state.edited_draft = edited_draft

    # Display Edited Draft
    if st.session_state.edited_draft:
        st.subheader("Verified Draft")
        edited_draft_input = st.text_area("", value=st.session_state.edited_draft, height=400, key="final_draft")
        st.session_state.edited_draft = edited_draft_input

# Schedule and Save
if st.session_state.edited_draft:
    st.header("Step 5: Schedule and Save")
    if st.button("Schedule and Save", type="primary"):
        with st.spinner("Scheduling and saving content..."):
            schedule_task = Task(
                description=(
                    f"Use the calendar tool to schedule content with:\n"
                    f"- Title: '{topic}'\n"
                    f"- Content Type: '{content_type}'\n"
                    f"- Publish Date: '{publish_date}'\n"
                    f"Then use the file tool to save the content with:\n"
                    f"- Title: '{topic}'\n"
                    f"- Content: '{st.session_state.edited_draft}'\n"
                    f"- Content Type: '{content_type}'"
                ),
                agent=calendar_manager,
                tools=[calendar_tool, file_tool],
                expected_output=f"Content '{topic}' scheduled for {publish_date} and saved to projects/{content_type.lower().replace(' ', '_')}/{topic.lower().replace(' ', '_')}.md"
            )
            crew = Crew(agents=[calendar_manager], tasks=[schedule_task], verbose=True)
            try:
                result = crew.kickoff()
                output = str(result).strip()
                st.session_state.scheduling_status = output
                if "Failed to save file" in output.lower():
                    st.error(output)
                else:
                    st.success(f"Content scheduled and saved: {output}")
            except Exception as e:
                st.error(f"Failed to schedule or save content: {e}")
                st.session_state.scheduling_status = ""

# Display Content Calendar
if os.path.exists("content_calendar.csv"):
    st.markdown('<div id="calendar-section"></div>', unsafe_allow_html=True)
    st.header("Content Calendar")
    try:
        df = pd.read_csv("content_calendar.csv")
        st.table(df)
    except Exception as e:
        st.error(f"Failed to load calendar: {e}")