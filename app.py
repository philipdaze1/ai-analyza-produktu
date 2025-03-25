import streamlit as st
import fitz  # PyMuPDF
import openai

st.set_page_config(page_title="Analýza produktu – Zlatá koruna", layout="centered")
st.title("📊 AI Analýza finančního produktu")
st.write("Nahrajte PDF s analýzou a získejte okamžitě strukturovanou zpětnou vazbu.")

openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else ""

uploaded_file = st.file_uploader("Nahraj PDF s analýzou produktu", type=["pdf"])

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

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        output = response.choices[0].message.content
        st.subheader("📄 Výstup AI agenta")
        st.markdown(output)

        st.download_button("💾 Stáhnout výstup jako TXT", data=output, file_name="analyza_vystup.txt")
