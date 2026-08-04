from typing import Any

import streamlit as st


DEFAULT_PAGE = "home"


def initialize_session() -> None:
    """
    Initialize the application session state.
    """

    if "page" not in st.session_state:
        st.session_state.page = DEFAULT_PAGE

    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None

    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = False

    if "last_feedback_record" not in st.session_state:
        st.session_state.last_feedback_record = None


def set_page(page_name: str) -> None:
    """
    Navigate to another application page.
    """

    st.session_state.page = page_name
    st.rerun()


def get_page() -> str:
    """
    Return the current application page.
    """

    return st.session_state.page


def save_analysis_result(result: dict[str, Any]) -> None:
    """
    Save the current mortgage analysis result.

    A new analysis resets the feedback status because the new
    prediction has not yet received a verified actual outcome.
    """

    st.session_state.analysis_result = result
    st.session_state.feedback_submitted = False
    st.session_state.last_feedback_record = None


def get_analysis_result() -> dict[str, Any] | None:
    """
    Return the saved mortgage analysis result.
    """

    return st.session_state.analysis_result


def clear_analysis_result() -> None:
    """
    Clear the previous mortgage analysis and feedback state.
    """

    st.session_state.analysis_result = None
    st.session_state.feedback_submitted = False
    st.session_state.last_feedback_record = None


def mark_feedback_submitted(
    feedback_record: dict[str, Any],
) -> None:
    """
    Mark the current prediction as having received feedback.
    """

    st.session_state.feedback_submitted = True
    st.session_state.last_feedback_record = feedback_record


def was_feedback_submitted() -> bool:
    """
    Return whether feedback was submitted for the current prediction.
    """

    return bool(st.session_state.feedback_submitted)


def get_last_feedback_record() -> dict[str, Any] | None:
    """
    Return the most recently submitted feedback record.
    """

    return st.session_state.last_feedback_record