# UI Wireframe — Student Enrollment App (Quick View)

## Overview
Three-column outer layout: `st.columns([1, 4, 1])` — the center column contains the app UI.

---

## Top area (above course list)
Row: `st.columns([3, 1])`
- Left (wide): `st.title("Course Enrollment")`
- Right (narrow): `st.button("Enroll in a Course")`

Below title: a metrics row (single or small columns)
- `st.metric("Enrolled", <count>)`
- (optional) `st.metric("Total Records", <count>)`

---

## Main content (center column)
A vertical list of course containers:

For each course -> use `st.container()` with inner columns `st.columns([3, 1])`

Left column (3 parts wide):
- `st.markdown("### {Course Title}")`
- `st.markdown("**{Instructor} — {Course ID}**")`
- small status or short subtitle (e.g., `**Enrolled**`)

Right column (1 part wide):
- `st.button("View")`  — navigates to course detail page

Visual (ASCII):

| Spacer | Center column (content)                        | Spacer |
|--------|------------------------------------------------|--------|
|        | Title: Course Enrollment    [Enroll button]    |        |
|        | Metric: Enrolled: 2                          |        |
|        | -------------------------------------------- |        |
|        | [ Course Container ]  [ View ]               |        |
|        | ### Python for Business Analytics            |        |
|        | **Dr. Rivera — MISY350**                     |        |
|        | -------------------------------------------- |        |
|        | [ Course Container ]  [ View ]               |        |
|        | ### Web Apps With Streamlit                  |        |
|        | **Dr. Chen — WEB220**                        |        |

---

## Course detail page (simple placeholder)
- Title: `st.markdown("### {Course Title}")`
- Notice: `st.info("This page is under construction — basic info shown here.")`
- Enrollment record: show `get_student_course_record(...)` fields
- Action: `st.button("Unenroll")` -> calls `soft_unenroll_student(...)`

Navigation: use `st.session_state['page']` values:
- `main` — main list
- `course:{course_id}` — detail view

---

## Notes
- UI lives in `streamlit_app.py` + `ui/views.py` + `ui/helpers.py` (adapters only).
- Enrollment key input should be normalized (`strip().upper()`) before submitting to service.
- Keep service code (`enrollment_starter.py`) unchanged; UI calls adapter helpers to interact with services.

---

Quick and small — tell me if you want this embedded into `UI_PLAN.md` or implemented as `streamlit_app.py` next.