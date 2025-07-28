import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Enhanced Tetris", layout="wide")
st.title("🎮 Enhanced Tetris Game")

with open("tetris.html", "r") as f:
    html_content = f.read()

components.html(html_content, height=800, scrolling=False)
