import streamlit as st

from ui.views import render_main_page, render_course_detail
from ui.helpers import initialize_app


def main() -> None:
    """Streamlit app entrypoint."""
    st.set_page_config(page_title="Student Enrollment", layout="wide")

    # Ensure DB and session defaults are initialized
    initialize_app()

    page = st.session_state.get("page", "main")
    if isinstance(page, str) and page.startswith("course:"):
        _, course_id = page.split("course:", 1)
        render_course_detail(course_id)
    else:
        render_main_page()


if __name__ == "__main__":
    main()
