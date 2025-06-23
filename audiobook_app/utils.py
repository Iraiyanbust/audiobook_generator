from PyPDF2 import PdfReader
from gtts import gTTS
import os

def convert_pdf_to_audio(pdf_path, audio_path, lang="en"):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    if not text.strip():
        raise ValueError("No readable text found in the PDF.")

    tts = gTTS(text=text, lang=lang)
    tts.save(audio_path)
