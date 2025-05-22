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
        "file_drop_bg": "#161a21",
        "file_drop_txt": "#ffffff",
        "file_drop_subtxt": "#e0e0e0"
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
        "file_drop_bg": "#ffffff",
        "file_drop_txt": "#000000",
        "file_drop_subtxt": "#31333F99"
    }

    theme = dark_theme if is_dark_mode else light_theme

    css = f"""
    <style>
    /* Top header bar and bottom bar and main body  */
    header[data-testid="stHeader"], div[data-testid="stBottomBlockContainer"], .stApp {{
        background-color: {theme['background_color']};
        color: {theme['text_color']};
    }}

    section[data-testid="stSidebar"] svg circle,
    section[data-testid="stSidebar"] svg path,
    section[data-testid="stSidebar"] svg line {{
        stroke: {theme['text_color']};
    }}

    /* Sidebar */
    section[data-testid="stSidebar"], section[data-testid="stSidebar"] p {{
        background-color: {theme['sidebar_bg']};
        color: {theme['text_color']} !important;
    }}
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] .stNumberInput input {{
        background-color: {theme['input_bg']};
        color: {theme['text_color']} !important;
        border: 1px solid {theme['border_color']};
    }}
    section[data-testid="stSidebar"] .stNumberInput button {{
        background-color: {theme['input_bg']};
        color: {theme['text_color']} !important;
    }}
    section[data-testid="stSidebar"] .stNumberInput button:hover {{
        background-color: {theme['button_hover_bg']};
        color: #ffffff !important;
    }}

    /* File drop widget */
    section[data-testid="stFileUploaderDropzone"] {{
        background-color: {theme['file_drop_bg']};
        border: 1px solid #ffffff;
    }}
    section[data-testid="stFileUploaderDropzone"] span {{
        color: {theme['file_drop_txt']} !important;
    }}
    section[data-testid="stFileUploaderDropzone"] small {{
        color: {theme['file_drop_subtxt']} !important;
    }}    

    /* Buttons */
    .stButton button {{
        background-color: {theme['input_bg']};
        color: {theme['text_color']} !important;
        border: 1px solid {theme['border_color']};
    }}

    /* Chat messages */
    .stChatMessage, .stMarkdown {{
        background-color: {theme['sidebar_bg']};
        color: {theme['text_color']};
    }}

    /* User input */
    textarea[data-testid="stChatInputTextArea"],
    textarea[data-testid="stChatInputTextArea"]::placeholder {{
        background-color: {theme['sidebar_bg']};
        color: {theme['text_color']} !important;
        padding-left: 10px;
    }}
    .st-emotion-cache-yd4u6l, .e1togvvn1 {{
        background-color: {theme['sidebar_bg']};
    }}  
    /* Send button */
    button[data-testid="stChatInputSubmitButton"] {{
        color: {theme['text_color']} !important;        
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
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)