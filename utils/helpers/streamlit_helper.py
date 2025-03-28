import streamlit as st
from urllib.parse import quote
from utils.helpers.recommendations_helper import fetch_active_recommendations_from_db

def _next_idea():
    if st.session_state.idea_count + 1 < len(st.session_state.ideas):
        st.session_state.idea_count += 1

def _previous_idea():
    if st.session_state.idea_count > 0:
        st.session_state.idea_count -= 1

def _get_markdown_content():
    idea = st.session_state.ideas[st.session_state.idea_count]

    with open("utils/markdown_template/idea_template.txt", "r") as file:
        template = file.read()

    markdown_content = template.format(
        project_title=idea['project_title'],
        brief_description=idea['brief_description'],
        stack=idea['stack'],
        steps="\n\n".join(f"    {i+1}. {step}" for i, step in enumerate(idea['steps'])),
        data_sources="\n\n".join(f"    {i+1}. {link}" for i, link in enumerate(idea['link_to_data_source']))
    )

    return markdown_content

def _handle_refresh_button_click():
    pass

def init_streamlit_session_state():
    if 'idea_count' not in st.session_state:
        st.session_state.idea_count = 0

    if 'ideas' not in st.session_state:
        results = fetch_active_recommendations_from_db()
        st.session_state.ideas = [ result['response'] for result in results ]

def render_main_ui():
    st.title("AI/ML Project Ideas")
    st.write("Welcome to the AI/ML Project Ideas generator!")
    st.write("Here you can find a variety of project ideas to work on.")
    st.write("Click 'Next' to see more ideas.")
    st.write("If you like an idea, feel free to explore it further or use it as a starting point for your project.")
    st.write("Don't forget to check the data sources for each idea to find relevant datasets.")
    st.write("Happy coding! 🎉")

    st.divider()

    if st.session_state.ideas:
        st.write(f"Showing Idea {st.session_state.idea_count + 1} of {len(st.session_state.ideas)}")

    col1, _, col2 = st.columns([2, 6, 2])

    with col1:
        st.button("⏮️ Previous", on_click=_previous_idea, disabled=(st.session_state.idea_count == 0))

    with col2:
        st.button("Next ⏭️", on_click=_next_idea, disabled=(st.session_state.idea_count == len(st.session_state.ideas) - 1))

    markdown_content = _get_markdown_content()
    encoded_content = quote(markdown_content)
    chatgpt_url = f"https://chat.openai.com/?q={encoded_content}"

    st.markdown(markdown_content)

    st.markdown(
        f'<a href="{chatgpt_url}" target="_blank"><button style="background-color:#4CAF50;color:white;padding:8px 16px;border:none;border-radius:4px;cursor:pointer;">Continue on ChatGPT</button></a>',
        unsafe_allow_html=True
    )
    
    st.divider()

    st.write("Didn't find what you were looking for?")
    st.write("Feel free to refresh the ideas to get new recommendations using the button below.")

    col1, col2 = st.columns([7, 3])

    with col1:
        st.write("")

    with col2:
        st.button("Refresh Ideas 🔁")
