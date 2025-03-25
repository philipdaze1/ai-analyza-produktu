import streamlit as st
import fitz  # PyMuPDF
import openai
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO

# ⚠️ Bezpečné načtení API klíče ze Streamlit secrets

# Nastavení barvy a rozhraní
st.set_page_config(page_title="AI Analýza – Zlatá koruna", page_icon="🧠", layout="centered")
st.markdown("""
    <style>
    .main {
        background-color: #fff9f0;
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        padding: 2rem;
    }
    .stButton>button {
        background-color: #FFA500 !important;
        color: white;
        border-radius: 12px;
        font-size: 1rem;
        height: 3em;
        width: 100%;
    }
    .stDownloadButton>button {
        background-color: #FFA500 !important;
        color: white;
        border-radius: 12px;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Načtení loga Zlaté koruny
image_url = "https://www.zlatakoruna.info/sites/default/files/zk_0.png"
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))
st.image(image, width=200)

st.title("🧠 AI Agent – Analýza finančního produktu")
st.subheader("Zlatá koruna")
st.write("Nahrajte PDF s analýzou a získejte okamžitě strukturovanou zpětnou vazbu.")

uploaded_file = st.file_uploader("📄 Nahraj PDF s analýzou produktu", type=["pdf"])

if uploaded_file:
    with st.spinner("🔍 Čtu PDF a analyzuji..."):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        prompt = f"""
        Proveď profesionální hodnocení následující analýzy finančního produktu. Výstup uveď v této struktuře:

        1. 📌 Silné stránky produktu
        2. ⚠️ Slabé stránky produktu
        3. 🧠 Shrnutí hodnocení podle skupin (finanční společnosti, média, akademici atd.)
        4. ✅ Doporučení pro zlepšení

        Analýza:
        {text}
        """

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        output = response.choices[0].message.content
        st.subheader("📄 Výstup AI agenta")
        st.markdown(output)

        st.download_button("💾 Stáhnout výstup jako TXT", data=output, file_name="analyza_vystup.txt")
