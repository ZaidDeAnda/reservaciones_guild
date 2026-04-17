import base64
from pathlib import Path
from PIL import Image
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "logo.png"


def load_logo():
    return Image.open(LOGO_PATH)


def set_page(page_title: str, layout: str = "wide"):
    icon = load_logo()
    st.set_page_config(
        page_title=page_title,
        page_icon=icon,
        layout=layout,
    )


def get_logo_base64() -> str:
    with open(LOGO_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode()


def render_brand_header(
    title: str = "La Mesa del Dragón",
    subtitle: str = "Juegos de mesa · Reservaciones",
):
    img_b64 = get_logo_base64()
    st.markdown(
        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:14px;
            margin-bottom:1.2rem;
            background:#181818;
            padding:0.9rem 1rem;
            border-radius:14px;
            border:1px solid rgba(0,207,209,0.22);
            box-shadow:0 4px 18px rgba(0,0,0,0.18);
        ">
            <img src="data:image/png;base64,{img_b64}" width="54" style="border-radius:10px;">
            <div>
                <div style="
                    font-size:1.25rem;
                    font-weight:700;
                    color:#00e5e7;
                    line-height:1.1;
                ">
                    {title}
                </div>
                <div style="
                    font-size:0.84rem;
                    color:#8fdfe0;
                    margin-top:0.15rem;
                ">
                    {subtitle}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )