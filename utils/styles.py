import streamlit as st


def load_styles() -> None:
    st.markdown(
        """
        <style>

        /* =========================================================
           GLOBAL
        ========================================================= */

        .stApp {
            background:
                radial-gradient(
                    circle at top left,
                    rgba(28, 68, 120, 0.22),
                    transparent 35%
                ),
                linear-gradient(
                    135deg,
                    #06111f 0%,
                    #0a1a2e 50%,
                    #071522 100%
                );
            color: #f5f7fb;
        }

        html,
        body,
        [class*="css"] {
            font-family:
                Inter,
                Arial,
                sans-serif;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* =========================================================
           STREAMLIT ELEMENTS
        ========================================================= */

        header[data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stToolbar"] {
            display: none;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        footer {
            visibility: hidden;
        }

        #MainMenu {
            visibility: hidden;
        }

        /* =========================================================
           TYPOGRAPHY
        ========================================================= */

        h1,
        h2,
        h3 {
            color: #ffffff;
            letter-spacing: -0.02em;
        }

        p {
            color: #b9c4d4;
            line-height: 1.7;
        }

        .nova-kicker {
            margin-bottom: 0.8rem;
            color: #d7b76c;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }

        .nova-title {
            margin: 0;
            color: #ffffff;
            font-size: clamp(2.7rem, 6vw, 5.6rem);
            font-weight: 800;
            line-height: 0.98;
            letter-spacing: -0.055em;
        }

        .nova-title-accent {
            color: #d7b76c;
        }

        .nova-subtitle {
            max-width: 720px;
            margin-top: 1.4rem;
            margin-bottom: 0;
            color: #b9c4d4;
            font-size: 1.08rem;
            line-height: 1.8;
        }

        /* =========================================================
           HERO
        ========================================================= */

        .nova-hero {
            padding: 2.5rem 0 2rem;
        }

        .nova-logo-wrap {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 1.5rem;
        }

        .nova-hero-copy {
            text-align: center;
        }

        /* =========================================================
           GLASS CARDS
        ========================================================= */

        .nova-card {
            height: 100%;
            padding: 1.7rem;
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 24px;
            background:
                linear-gradient(
                    145deg,
                    rgba(255, 255, 255, 0.08),
                    rgba(255, 255, 255, 0.035)
                );
            box-shadow:
                0 20px 60px rgba(0, 0, 0, 0.28),
                inset 0 1px 0 rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            transition:
                transform 0.25s ease,
                border-color 0.25s ease,
                box-shadow 0.25s ease;
        }

        .nova-card:hover {
            transform: translateY(-4px);
            border-color: rgba(215, 183, 108, 0.42);
            box-shadow:
                0 24px 70px rgba(0, 0, 0, 0.34),
                0 0 0 1px rgba(215, 183, 108, 0.06);
        }

        .nova-card-icon {
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.1rem;
            border: 1px solid rgba(215, 183, 108, 0.35);
            border-radius: 15px;
            background: rgba(215, 183, 108, 0.10);
            color: #e8ca83;
            font-size: 1.35rem;
        }

        .nova-card-title {
            margin-bottom: 0.65rem;
            color: #ffffff;
            font-size: 1.28rem;
            font-weight: 750;
        }

        .nova-card-text {
            margin: 0;
            color: #aeb9ca;
            font-size: 0.97rem;
            line-height: 1.65;
        }

        /* =========================================================
           BUTTONS
        ========================================================= */

        .stButton > button {
            width: 100%;
            min-height: 52px;
            border: 1px solid rgba(215, 183, 108, 0.55);
            border-radius: 15px;
            background:
                linear-gradient(
                    135deg,
                    #d7b76c,
                    #b98e37
                );
            color: #07111f;
            font-size: 0.98rem;
            font-weight: 800;
            letter-spacing: 0.01em;
            box-shadow:
                0 10px 30px rgba(185, 142, 55, 0.22);
            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease,
                filter 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            border-color: #ead49a;
            color: #07111f;
            filter: brightness(1.05);
            box-shadow:
                0 14px 38px rgba(185, 142, 55, 0.32);
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        .stButton > button:focus {
            outline: none;
            box-shadow:
                0 0 0 3px rgba(215, 183, 108, 0.20),
                0 12px 34px rgba(185, 142, 55, 0.25);
        }

        /* =========================================================
           FORM ELEMENTS
        ========================================================= */

      /* ---------- INPUTS ---------- */

[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
}

[data-testid="stNumberInput"] input::placeholder,
[data-testid="stTextInput"] input::placeholder {
    color: #6b7280 !important;
}
        [data-testid="stTextInput"] input:focus,
        [data-testid="stNumberInput"] input:focus {
            border-color: rgba(215, 183, 108, 0.75);
            box-shadow: 0 0 0 2px rgba(215, 183, 108, 0.12);
        }

        [data-testid="stWidgetLabel"] p {
            color: #dce3ed;
            font-weight: 650;
        }

        /* =========================================================
           DIVIDERS & BADGES
        ========================================================= */

        .nova-divider {
            height: 1px;
            margin: 1.8rem 0;
            background:
                linear-gradient(
                    90deg,
                    transparent,
                    rgba(215, 183, 108, 0.35),
                    transparent
                );
        }

        .nova-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.45rem 0.75rem;
            border: 1px solid rgba(215, 183, 108, 0.26);
            border-radius: 999px;
            background: rgba(215, 183, 108, 0.08);
            color: #e4c67d;
            font-size: 0.79rem;
            font-weight: 700;
        }

        /* =========================================================
           RESULTS
        ========================================================= */

        .nova-result-positive {
            padding: 1.4rem;
            border: 1px solid rgba(92, 212, 156, 0.35);
            border-radius: 18px;
            background: rgba(92, 212, 156, 0.08);
        }

        .nova-result-negative {
            padding: 1.4rem;
            border: 1px solid rgba(255, 110, 110, 0.35);
            border-radius: 18px;
            background: rgba(255, 110, 110, 0.08);
        }

        .nova-result-title {
            margin-bottom: 0.35rem;
            color: #ffffff;
            font-size: 1.2rem;
            font-weight: 800;
        }

        /* =========================================================
           RESPONSIVE
        ========================================================= */

        @media (max-width: 768px) {
            .block-container {
                padding-top: 1rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .nova-hero {
                padding-top: 1rem;
            }

            .nova-title {
                font-size: 3rem;
            }

            .nova-subtitle {
                font-size: 0.98rem;
            }

            .nova-card {
                padding: 1.3rem;
                border-radius: 20px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )