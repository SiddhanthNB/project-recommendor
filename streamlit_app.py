import config.mongo
from config.logger import logger
from utils.helpers.streamlit_helper import init_streamlit_session_state, render_main_ui

if __name__ == "__main__":
    try:
        init_streamlit_session_state()
        render_main_ui()
    except Exception as e:
        logger.error(f"Error: {e}", exc_info = True)
        raise e
