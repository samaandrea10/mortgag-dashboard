import streamlit as st

from pages.about import show_about
from pages.approval import show_approval
from pages.advisor import show_ai_advisor
from pages.data_insights import show_data_insights
from pages.detailed_analysis import show_detailed_analysis
from pages.home import show_home
from pages.model_feedback import show_model_feedback
from pages.model_performance import show_model_performance
from pages.results import show_results
from pages.simulator import show_simulator
from utils.session import get_page, initialize_session
from utils.styles import load_styles


st.set_page_config(
    page_title="NOVA Mortgage Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main() -> None:
    """
    Initialize and display the NOVA application.
    """

    initialize_session()
    load_styles()

    current_page = get_page()

    if current_page == "home":
        show_home()

    elif current_page == "approval":
        show_approval()

    elif current_page == "results":
        show_results()

    elif current_page == "model_performance":
        show_model_performance()

    elif current_page == "data_insights":
        show_data_insights()

    elif current_page == "model_feedback":
        show_model_feedback()

    elif current_page == "detailed_analysis":
        show_detailed_analysis()

    elif current_page == "simulator":
        show_simulator()

    elif current_page == "advisor":
        show_ai_advisor()

    elif current_page == "about":
        show_about()

    else:
        st.session_state.page = "home"
        st.rerun()


if __name__ == "__main__":
    main()