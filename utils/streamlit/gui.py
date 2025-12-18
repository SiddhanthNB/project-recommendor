import datetime as dt
from typing import Any, Dict, List
from urllib.parse import quote

import streamlit as st

from config.logger import logger
import utils.constants as constants
from utils.helpers.corenest import generate_ideas
from utils.helpers.sheets import append_rows, ensure_header, get_sheets_client


def _init_session_state():
    st.session_state.setdefault("ideas", [])
    st.session_state.setdefault("idea_pointer_index", 0)
    st.session_state.setdefault("is_generating", False)
    st.session_state.setdefault("pending_sheet_append", [])


def _next_idea():
    if st.session_state.idea_pointer_index + 1 < len(st.session_state.ideas):
        st.session_state.idea_pointer_index += 1


def _previous_idea():
    if st.session_state.idea_pointer_index > 0:
        st.session_state.idea_pointer_index -= 1


def _get_markdown_content():
    idea = st.session_state.ideas[st.session_state.idea_pointer_index]
    with open("utils/streamlit/templates/idea.md", "r") as file:
        template = file.read()

    steps = idea.get("steps") or []
    if isinstance(steps, str):
        steps = [steps]
    links = idea.get("link_to_data_source") or []
    if isinstance(links, str):
        links = [links]

    stack_items = _coerce_list(idea.get("stack"))
    stack = "\n".join(f"- {item}" for item in stack_items) if stack_items else ""

    markdown_content = template.format(
        project_title=idea.get("project_title", ""),
        brief_description=idea.get("brief_description", ""),
        stack=stack,
        steps="\n".join(f"{i+1}. {step}" for i, step in enumerate(steps)),
        data_sources="\n".join(f"- {link}" for link in links),
    )
    return markdown_content


def _coerce_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, str):
        return [value]
    return [str(value)]


def _format_stack(stack: Any) -> str:
    stack_list = _coerce_list(stack)
    return "\n".join(f"- {item}" for item in stack_list)


def _format_steps(steps: Any) -> str:
    if isinstance(steps, str):
        return steps.strip()
    steps_list = _coerce_list(steps)
    return "\n".join(f"{idx + 1}) {step}" for idx, step in enumerate(steps_list))


def _format_links(links: Any) -> str:
    links_list = _coerce_list(links)
    return "\n".join(link.strip() if isinstance(link, str) else str(link) for link in links_list)


def _build_sheet_rows(ideas: List[Dict[str, Any]]) -> List[List[str]]:
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat()
    rows: List[List[str]] = []
    for idea in ideas:
        rows.append(
            [
                timestamp,
                idea.get("project_title", ""),
                idea.get("brief_description", ""),
                _format_stack(idea.get("stack")),
                _format_steps(idea.get("steps")),
                _format_links(idea.get("link_to_data_source")),
            ]
        )
    return rows


def _append_ideas_to_sheet(ideas: List[Dict[str, Any]]) -> None:
    if not ideas:
        return
    spreadsheets = get_sheets_client()
    header = ["generated_at", "project_title", "brief_description", "stack", "steps", "data_sources"]
    ensure_header(spreadsheets, constants.GOOGLE_SPREADSHEET_ID, constants.GOOGLE_SHEET_NAME, header)
    append_rows(
        spreadsheets,
        constants.GOOGLE_SPREADSHEET_ID,
        constants.GOOGLE_SHEET_NAME,
        _build_sheet_rows(ideas),
    )


def _append_pending_to_sheet():
    ideas = st.session_state.get("pending_sheet_append", [])
    if not ideas:
        return
    try:
        _append_ideas_to_sheet(ideas)
    except Exception as exc:
        logger.warning("Failed to append ideas to Sheets: %s", exc, exc_info=True)
    finally:
        st.session_state["pending_sheet_append"] = []


def _fetch_ideas():
    st.session_state.is_generating = True
    try:
        with st.spinner("Generating new ideas..."):
            ideas = generate_ideas()
        if not ideas:
            st.warning("No ideas returned. Try again.")
            return
        st.session_state.ideas = ideas
        st.session_state.idea_pointer_index = 0
        st.session_state.pending_sheet_append = ideas
    except Exception as exc:
        logger.error("Failed to generate ideas: %s", exc, exc_info=True)
        st.error("Failed to generate ideas. Please try again.")
    finally:
        st.session_state.is_generating = False


def _render_idea_carousel():
    if not st.session_state.ideas:
        return

    st.write(f"Showing Idea {st.session_state.idea_pointer_index + 1} of {len(st.session_state.ideas)}")

    col1, _, col2 = st.columns([2, 6, 2])

    with col1:
        st.button(
            "⏮️ Previous",
            key="prev_button",
            on_click=_previous_idea,
            disabled=st.session_state.idea_pointer_index == 0,
        )

    with col2:
        st.button(
            "Next ⏭️",
            key="next_button",
            on_click=_next_idea,
            disabled=st.session_state.idea_pointer_index == len(st.session_state.ideas) - 1,
        )

    markdown_content = _get_markdown_content()
    prefixed_content = f"You are a helpful assistant. Help me work on this project:\n\n{markdown_content}"
    encoded_content = quote(prefixed_content)
    chatgpt_url = f"https://chat.openai.com/?q={encoded_content}"

    st.markdown(markdown_content)
    st.markdown(
        f'<a href="{chatgpt_url}" target="_blank">'
        '<button style="background-color:#4CAF50;color:white;padding:8px 16px;'
        'border:none;border-radius:4px;cursor:pointer;">Continue on ChatGPT</button></a>',
        unsafe_allow_html=True,
    )


def render_main_ui():
    _init_session_state()
    st.title("AI/ML Project Ideas")
    st.write("Discover hands-on AI/ML project suggestions with clear steps and real data sources.")
    st.write("Perfect for learners and enthusiasts looking to build practical skills.")

    st.divider()

    if not st.session_state.ideas:
        st.write("Tap the button to generate project ideas.")
        if st.button("Generate ideas", type="primary", disabled=st.session_state.is_generating):
            _fetch_ideas()
        return

    _render_idea_carousel()

    st.divider()
    st.write("Want a different set? Try generating more ideas.")
    if st.button("Generate more ideas", type="primary", disabled=st.session_state.is_generating):
        _fetch_ideas()

    # Append to Sheets after rendering so the UI stays responsive.
    _append_pending_to_sheet()
