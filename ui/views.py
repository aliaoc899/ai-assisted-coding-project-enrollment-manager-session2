from __future__ import annotations

import streamlit as st
from typing import Any

from ui import helpers as ui_helpers


def _page_layout() -> tuple[Any, Any, Any]:
    """Return the three outer columns and the center column for content."""
    left, center, right = st.columns([1, 4, 1])
    return left, center, right


def render_main_page() -> None:
    left, center, right = _page_layout()

    with center:
        # Top row: title and enroll button
        c1, c2 = st.columns([3, 1])
        with c1:
            st.title("Course Enrollment")
        with c2:
            if st.button("Enroll in a Course"):
                st.session_state["show_enroll_form"] = True

        # Metrics
        user = ui_helpers.get_current_user()
        summary = ui_helpers.get_student_summary(user["user_id"])
        enrolled_count = summary.get("enrolled", 0)
        st.metric("Enrolled", enrolled_count)

        # Enrollment form (inline, shown when toggled)
        if st.session_state.get("show_enroll_form"):
            with st.form("enroll_form"):
                available = ui_helpers.get_available_course_keys()
                options = [f"{c['course_name']} ({c['course_id']})" for c in available]
                keys = [c["enrollment_key"] for c in available]
                choice = st.selectbox("Select a course", options)
                idx = options.index(choice) if choice in options else 0
                default_key = keys[idx] if keys else ""
                key_input = st.text_input("Enrollment Key", value=default_key)
                submitted = st.form_submit_button("Submit")
                if submitted:
                    record = ui_helpers.enroll_with_key(user["user_id"], user["email"], key_input)
                    if record:
                        st.success("Enrolled successfully")
                        st.session_state["show_enroll_form"] = False
                    else:
                        st.error("Enrollment failed — invalid key or other error")

        st.write("\n")

        # Course list
        enrollments = st.session_state.get("enrollments", [])
        if not enrollments:
            st.info("No active enrollments. Use 'Enroll in a Course' to join one.")
            return

        for rec in enrollments:
            with st.container():
                c_left, c_right = st.columns([3, 1])
                with c_left:
                    st.markdown(f"### {rec.get('course_name', rec.get('course_id'))}")
                    instructor = rec.get("instructor") or ""
                    st.markdown(f"**{instructor} — {rec.get('course_id')}**")
                with c_right:
                    if st.button("View", key=f"view-{rec['enrollment_id']}"):
                        st.session_state["page"] = f"course:{rec['course_id']}"


def render_course_detail(course_id: str) -> None:
    left, center, right = _page_layout()
    user = ui_helpers.get_current_user()

    with center:
        # Title and placeholder notice
        st.markdown(f"### {course_id}")
        st.info("This page is under construction — basic info shown here.")

        record = ui_helpers.get_student_course_record(user["user_id"], course_id)
        if not record:
            st.error("No enrollment record found for this course.")
            if st.button("Back to main"):
                st.session_state["page"] = "main"
            return

        st.write(record)

        if st.button("Unenroll"):
            ok = ui_helpers.soft_unenroll_student(user["user_id"], course_id)
            if ok:
                st.success("Unenrolled — status set to unenrolled")
                st.session_state["page"] = "main"
            else:
                st.error("Failed to unenroll")

        if st.button("Back to main", key="back-main"):
            st.session_state["page"] = "main"
