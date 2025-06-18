from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def index_view(request):
    return render(request, "index.html")  

def home_view(request):
    return render(request, "home.html")  

@csrf_exempt  # For simplicity in demo, consider proper CSRF handling in production
def upload_resume(request):
    if request.method == 'POST' and request.FILES.getlist('files'):
        response_data = []
        
        for file in request.FILES.getlist('files'):
            # Save file to database
            resume = ResumeFile(file=file)
            if request.user.is_authenticated:
                resume.user = request.user
            resume.save()
            
            # Process file
            text_content = ""
            try:
                if file.name.lower().endswith('.pdf'):
                    # Process PDF
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text()
                elif file.name.lower().endswith('.docx'):
                    # Process DOCX
                    text_content = docx2txt.process(file)
                
                resume.processed_text = text_content
                resume.processed = True
                resume.save()
                
                response_data.append({
                    'name': file.name,
                    'status': 'processed',
                    'id': resume.id
                })
            except Exception as e:
                response_data.append({
                    'name': file.name,
                    'status': 'error',
                    'message': str(e)
                })
        
        return JsonResponse({'files': response_data})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)