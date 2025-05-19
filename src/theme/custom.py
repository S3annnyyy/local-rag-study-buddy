def set_custom_theme(is_dark_mode, st):
    # Define theme variables
    dark_theme = {
        "background_color": "#0e1117",
        "text_color": "#e0e0e0",
        "sidebar_bg": "#161a21",
        "input_bg": "#1e222a",
        "button_bg": "#2a2e36",
        "button_hover_bg": "#3c3f45",
        "border_color": "#3c3f45",
        "chat_color": "#2a2e36",
    }

    light_theme = {
        "background_color": "#ffffff",
        "text_color": "#000000",
        "sidebar_bg": "#f5f5f5",
        "input_bg": "#ffffff",
        "button_bg": "#e0e0e0",
        "button_hover_bg": "#cccccc",
        "border_color": "#dddddd",
        "chat_color": "#2a2e36",
    }

    theme = dark_theme if is_dark_mode else light_theme

    css = f"""
    <style>
    /* Top header bar */
    header[data-testid="stHeader"] {{
        background-color: {theme['background_color']};
        color: {theme['text_color']};
    }}
    body, .stApp {{
        background-color: {theme['background_color']};
        color: {theme['text_color']};
    }}
    section[data-testid="stSidebar"] {{
        background-color: {theme['sidebar_bg']};
        color: {theme['text_color']};
    }}
    section[data-testid="stSidebar"] * {{
        color: {theme['text_color']} !important;
    }}
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] .stNumberInput input {{
        background-color: {theme['input_bg']};
        color: {theme['text_color']} !important;
        border: 1px solid {theme['border_color']};
    }}
    section[data-testid="stSidebar"] .stNumberInput button {{
        background-color: {theme['button_bg']};
        color: {theme['text_color']} !important;
        border: 1px solid {theme['border_color']};
    }}
    section[data-testid="stSidebar"] .stNumberInput button:hover {{
        background-color: {theme['button_hover_bg']};
        color: #ffffff !important;
    }}
    div[data-testid="stBottomBlockContainer"] {{
        background-color: {theme['background_color']};
        color: {theme['text_color']} !important;
    }}   

    /* The file drop text */
    div[data-testid="stFileUploader"] label {{
        color: {theme['text_color']} !important;
    }}

    /* Uploader area hover state (if any) */
    div[data-testid="stFileUploader"]:hover {{
        background-color: {theme['sidebar_bg']};
    }}

    /* Chat Input Container */
    div[data-testid="stChatInputContainer"] {{
        background-color: {theme['sidebar_bg']};
        border-top: 1px solid {theme['border_color']};
    }}

    /* Textarea inside chat input */
    textarea[data-testid="stChatInputTextArea"] {{
        color: {theme['text_color']} !important;
        border: 1px solid {theme['border_color']} !important;
    }}

    /* Send button */
    button[data-testid="stChatInputSubmitButton"] {{
        color: {theme['text_color']} !important;
        border: 1px solid {theme['border_color']} !important;
    }}

    /* Send button on hover */
    button[data-testid="stChatInputSubmitButton"]:hover {{
        color: #ffffff !important;
    }}

    /* Send button when disabled */
    button[data-testid="stChatInputSubmitButton"]:disabled {{
        color: {theme['text_color']} !important;
        opacity: 0.5;
    }}
    button[data-testid="stChatInputSubmitButton"]:disabled {{
        color: {theme['text_color']} !important;
        opacity: 0.5;
    }}
    .stChatMessage {{
        background-color: {theme['sidebar_bg']};
        color: {theme['text_color']};
    }}
    .stButton button {{
        background-color: {theme['input_bg']};
        color: {theme['text_color']} !important;
        border: 1px solid {theme['border_color']};
    }}
    .stTextInput input {{
        background-color: {theme['input_bg']};
        color: {theme['text_color']} !important;
        border: 1px solid {theme['border_color']};
    }}
    .stMarkdown, .stMarkdown p {{
        color: {theme['text_color']};
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)