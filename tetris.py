import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Tetris Game", layout="wide")

st.title("🎮 Tetris Game")
st.markdown("### Play the classic Tetris game with dark/light mode toggle!")

# Display the HTML game
with open("tetris.html", "r") as f:
    html_content = f.read()

components.html(html_content, height=800, scrolling=False)

st.markdown("""
## 🎯 **How to Play:**
- **← →** Arrow Keys: Move pieces left/right
- **↓** Down Arrow: Soft drop (faster falling)
- **↑** Up Arrow: Rotate piece
- **Space**: Hard drop (instant drop)
- **T**: Toggle between dark/light theme
- **R**: Restart game

## ✨ **Features:**
- 🌙☀️ **Dark/Light Mode Toggle** - Switch themes anytime!
- 🏆 **Progressive Scoring** - Points increase with level
- 📊 **Real-time Stats** - Track score, lines, and level
- 🎯 **Next Piece Preview** - Plan your strategy
- 📱 **Responsive Design** - Works on all screen sizes
- 🎮 **Classic Tetris Feel** - All 7 original piece types
""")

       

   
