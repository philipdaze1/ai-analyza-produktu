import streamlit as st
import fitz  # PyMuPDF
import openai
from PIL import Image
import requests
from io import BytesIO

# ⚠️ Dočasně nastavený OpenAI API klíč
openai.api_key = st.secrets["OPENAI_API_KEY"]

