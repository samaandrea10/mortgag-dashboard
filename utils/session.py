from typing import Any

import streamlit as st


DEFAULT_PAGE = "home"


def initialize_session() -> None:
    """
    Initialize application session state.
    """
    if "page" not in st.session_state:
        st.session_state.page = DEFAULT_PAGE

    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None


def set_page(page_name: str) -> None:
    """
    Navigate to another page.
    """
    st.session_state.page = page_name
    st.rerun()


def get_page() -> str:
    """
    Return the current page.
    """
    return st.session_state.page


def save_analysis_result(result: dict[str, Any]) -> None:
    """
    Save the mortgage analysis result.
    """
    st.session_state.analysis_result = result


def get_analysis_result() -> dict[str, Any] | None:
    """
    Return the saved mortgage analysis result.
    """
    return st.session_state.analysis_result


def clear_analysis_result() -> None:
    """
    Clear the previous analysis result.
    """
    st.session_state.analysis_result = None