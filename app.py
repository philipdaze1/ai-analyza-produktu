import streamlit as st
import fitz  # PyMuPDF
import openai
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import base64
from fpdf import FPDF

# Nastavení aplikace
st.set_page_config(page_title="AI Analýza – Zlatá koruna", page_icon="🧠", layout="centered")

# Stylování rozhraní
st.markdown("""
    <style>
    .reportview-container {
        background-color: #FFA500;
    }
    .main {
        background-color: #FFA500;
        color: #000000;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, .stMarkdown, .stText, .stSubheader, .stTitle {
        color: #000000 !important;
    }
    .stButton>button, .stDownloadButton>button {
        background-color: #ffffff !important;
        color: #FFA500 !important;
        border-radius: 12px;
        font-weight: bold;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #ffd699 !important;
        color: #000000 !important;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Načtení banneru Zlaté koruny a zarovnání na střed s animací a zaoblením
banner_url = "https://www.zlatakoruna.info/sites/default/files/23zk_2_0.png"
banner_response = requests.get(banner_url)
banner_image = Image.open(BytesIO(banner_response.content))
st.markdown("""
    <style>
    .banner-container {
        text-align: center;
        animation: fadeInBanner 1.5s ease-in-out;
    }
    .banner-image {
        border-radius: 20px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
        width: 100%;
        height: auto;
    }
    @keyframes fadeInBanner {
        0% { opacity: 0; transform: scale(0.95); }
        100% { opacity: 1; transform: scale(1); }
    }
    </style>
    <div class="banner-container">
        <img src="https://www.zlatakoruna.info/sites/default/files/23zk_2_0.png" class="banner-image" width="100%"/>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align: center; color: #FFA500; font-weight: bold;'>AI AGENT ZLATÉ KORUNY</h1>
""", unsafe_allow_html=True)
st.markdown("""
    <h3 style='text-align: center; color: #000000;'>Analýza finančního produktu</h3>
    <div style='margin: 20px 0;'>
    <hr style='border: 1px solid #FFA500; width: 100%; margin: auto;'>
</div>
""", unsafe_allow_html=True)
st.write("Nahrajte PDF s analýzou a získejte profesionálně stylizovaný výstup včetně vizualizace a PDF reportu.")

uploaded_file = st.file_uploader("📄 Nahraj PDF s analýzou produktu", type=["pdf"])

if uploaded_file:
    with st.spinner("🔍 Čtu PDF a analyzuji..."):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        prompt = f"""
        Proveď profesionální hodnocení následující analýzy finančního produktu. Výstup uveď v této struktuře a použij výrazné oddělení jednotlivých bodů:

        **1. SILNÉ STRÁNKY PRODUKTU:**
        (přehled silných stránek)

        **2. SLABÉ STRÁNKY PRODUKTU:**
        (přehled slabých stránek)

        **3. SHRNUTÍ HODNOCENÍ PODLE SKUPIN:**
        (komentáře k tomu, jak produkt hodnotily jednotlivé skupiny – finanční instituce, média atd.)

        **4. DOPORUČENÍ PRO ZLEPŠENÍ:**
        (co doporučují odborníci vylepšit)

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

        # Vizualizace jako příklad (fiktivní data)
        st.subheader("📊 Vizualizace hodnocení")
        categories = ["Výnosy", "Kvalita", "Bezpečnost"]
        scores = [4.2, 3.8, 3.1]

        fig, ax = plt.subplots()
        bars = ax.bar(categories, scores, color="#333333")
        ax.set_ylim(0, 5)
        ax.set_ylabel("Průměrná známka")
        st.pyplot(fig)

        st.download_button("💾 Stáhnout výstup jako TXT", data=output, file_name="analyza_vystup.txt")
