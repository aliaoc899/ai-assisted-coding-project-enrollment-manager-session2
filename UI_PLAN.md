# Streamlit UI Plan — Student Enrollment App

Goal: Draft a clear, actionable plan to build the Streamlit UI that uses the existing enrollment services and database. This document focuses on layout, interactions, session state, integration points, and acceptance criteria for a two-page app (main + course details).

## High-level layout
- Page container: three-column layout using `st.columns([1, 4, 1])`.
- Center column: vertical list of course rows implemented with `st.container()` per course.
  - Each course row contains two columns: `st.columns([3, 1])`.
  - Left column (vertical stack): `st.markdown('### {course_name}')` and `st.markdown('**{subtitle}**')` for instructor or short status.
  - Right column: a `st.button('Open')` (or `st.button('View')`) to navigate to course detail page.
- Top area (above the list): a two-column row `st.columns([3, 1])`.
  - Left: `st.title('Course Enrollment')`.
  - Right: `st.button('Enroll in a Course')` that opens an enrollment form modal or shows form inline.

## Pages
1. Main page (index)
  - Shows all available enrollments for the current student (only `status == enrolled`).
  - Shows enrollment history summary counts (total, enrolled, unenrolled) — use `get_student_summary(user_id)`.
  - Enrollment button flow: open form to select course (dropdown of `get_available_course_keys()`) and enter enrollment key text input. On submit, call backend `enroll_with_key(user_id, email, key)` and show success or error messages.
  - On successful enroll: update session state and re-render list.
2. Course detail page
  - Displays full enrollment record and course info. Uses `get_student_course_record(user_id, course_id)` and course details via `get_course_by_key()` or `get_available_course_keys()`.
  - Provide an action button to `Unenroll` which calls `soft_unenroll_student(user_id, course_id)` and then returns to main page updating session state.

## Session state
- Use `st.session_state` keys:
  - `session_state['current_user']` — pre-seeded with the existing `CURRENT_STUDENT` object (assume logged-in).
  - `session_state['enrollments']` — list of current enrollments (refresh from DB on important actions).
  - `session_state['page']` — 'main' or `course:{course_id}` to handle simple navigation.
  - `session_state['flash']` — temporary messages for success/error.
- On app start: set `session_state['current_user']` from `CURRENT_STUDENT` and load `session_state['enrollments'] = get_student_enrollments(user_id)`.

## Integration with existing services (no DB changes)
- Use the provided functions in `enrollment_starter.py`:
  - `get_available_course_keys()` for dropdown options.
  - `get_student_enrollments(user_id)` for rendering main list.
  - `enroll_with_key(user_id, email, key)` for enroll action.
  - `get_student_course_record(user_id, course_id)` and `get_course_by_key(key)` for detail view.
  - `soft_unenroll_student(user_id, course_id)` for unenroll actions.
- Do not modify service functions unless a missing helper is discovered; prefer to add a small adapter in the UI layer.

## UX and validation
- Normalization: enrollment key input should `strip()` and `upper()` before passing to service.
- Validate presence of `@` in email (the service already checks for email format but UI should pre-validate).
- Show clear, dismissible success and error messages using `st.success()` / `st.error()` and `session_state['flash']`.
- Disable enroll button while request is in progress to avoid duplicate submissions.

## Error handling and edge cases
- If `enroll_with_key` returns `None`, show a helpful message: "Invalid key or enrollment failed.".
- If `soft_unenroll_student` returns `False`, show an error and do not change session state.
- If DB read calls return empty lists, show friendly empty-state UI with guidance to use the Enroll button.

## Acceptance criteria
- The main page renders a three-column layout with centered course list matching the described structure.
- Enrollment flow accepts a selected course and key, validates, calls `enroll_with_key`, and updates the list without manual reload.
- Course detail page shows enrollment record and allows soft unenroll, updating main page state on success.
- Session state persists navigation and local UI state while the Streamlit app runs.

## Implementation steps (technical)
1. Create `streamlit_app.py` scaffold with routing via `st.session_state['page']`.
2. Implement `render_main_page()` with top row and course list containers.
3. Implement `render_enroll_form()` (modal or inline) integrated with `enroll_with_key()`.
4. Implement `render_course_detail(course_id)` and unenroll action.
5. Add helper adapter functions in `ui_helpers.py` that call the existing functions in `enrollment_starter.py`.
6. Add a small test harness or manual run instructions in `README.md`.

## Testing & manual checks
- Manual run: `streamlit run streamlit_app.py` and verify:
  - Main page lists current student enrollments.
  - Enroll flow with correct key adds a course.
  - Unenroll flow marks status `unenrolled` and removes from active list.
- Add a few unit tests around adapter functions that mock DB calls (optional for this phase).

## Next steps & review
- I'll implement the UI scaffold next if you want — create `streamlit_app.py` and `ui_helpers.py` that import the existing services.
- Request your review of this plan; I will adjust the layout or flow per feedback.

---
Plan recorded for review. If this looks good, I will start implementing the Streamlit scaffold and adapters.