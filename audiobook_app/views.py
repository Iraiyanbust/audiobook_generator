from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from gtts import gTTS
from PyPDF2 import PdfReader
import os
import uuid

def index(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        lang = request.POST.get("lang", "en")
        uid = str(uuid.uuid4())
        pdf_path = f"media/{uid}.pdf"
        mp3_path = f"media/{uid}.mp3"

        with open(pdf_path, 'wb+') as dest:
            for chunk in pdf_file.chunks():
                dest.write(chunk)

        try:
            reader = PdfReader(pdf_path)
            text = "".join([page.extract_text() or "" for page in reader.pages])
            if not text.strip():
                raise ValueError("No text found in PDF.")

            tts = gTTS(text, lang=lang)
            tts.save(mp3_path)

            response = FileResponse(open(mp3_path, 'rb'), as_attachment=True, filename='audiobook.mp3')
            return response

        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)

    return render(request, 'index.html')
