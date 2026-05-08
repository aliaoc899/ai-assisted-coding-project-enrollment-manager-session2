from __future__ import annotations

import streamlit as st
from typing import Any, Optional

import enrollment_starter as svc


def initialize_app() -> None:
    """Prepare database and session state defaults."""
    # ensure DB exists and sample data seeded for demo purposes
    try:
        svc.create_tables()
        svc.seed_sample_data()
    except Exception:
        # keep UI resilient if DB already exists or seeding fails
        pass

    if "current_user" not in st.session_state:
        st.session_state["current_user"] = svc.CURRENT_STUDENT

    if "page" not in st.session_state:
        st.session_state["page"] = "main"

    # load enrollments for the current user
    user_id = st.session_state["current_user"]["user_id"]
    st.session_state["enrollments"] = svc.get_student_enrollments(user_id)


def get_current_user() -> dict[str, Any]:
    return st.session_state.get("current_user", svc.CURRENT_STUDENT)


def reload_enrollments() -> list[dict[str, Any]]:
    user = get_current_user()
    enrollments = svc.get_student_enrollments(user["user_id"])
    st.session_state["enrollments"] = enrollments
    return enrollments


def get_available_course_keys() -> list[dict[str, Any]]:
    return svc.get_available_course_keys()


def enroll_with_key(user_id: str, email: str, enrollment_key: str) -> Optional[dict[str, Any]]:
    if not enrollment_key:
        return None
    key = enrollment_key.strip().upper()
    record = svc.enroll_with_key(user_id, email, key)
    if record:
        reload_enrollments()
    return record


def get_student_course_record(user_id: str, course_id: str) -> Optional[dict[str, Any]]:
    return svc.get_student_course_record(user_id, course_id)


def soft_unenroll_student(user_id: str, course_id: str) -> bool:
    ok = svc.soft_unenroll_student(user_id, course_id)
    if ok:
        reload_enrollments()
    return ok


def get_student_summary(user_id: str) -> dict[str, int]:
    return svc.get_student_summary(user_id)
