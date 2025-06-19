import os
import magic
import tempfile
from pdfminer.high_level import extract_text
from docx import Document
import google.generativeai as genai
from django.conf import settings

def parse_resume(file):
    text = ""
    file_type = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    
    if file_type == 'application/pdf':
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            for chunk in file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name
        text = extract_text(tmp_path)
        os.unlink(tmp_path)
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        doc = Document(file)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    elif file_type == 'text/plain':
        text = file.read().decode('utf-8')
    
    return text

def generate_cold_mail(job_desc, resume_text, tone='professional'):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Write a professional cold email for a job application using:
    - Job description: {job_desc}
    - Resume content: {resume_text}
    - Tone: {tone}
    
    Provide the subject line and email body separately.
    """
    
    try:
        response = model.generate_content(prompt)
        parts = response.text.split('\n\n', 1)
        subject = parts[0].replace('Subject:', '').strip()
        body = parts[1] if len(parts) > 1 else ""
        return subject, body
    except Exception as e:
        raise Exception(f"Failed to generate content: {str(e)}")
