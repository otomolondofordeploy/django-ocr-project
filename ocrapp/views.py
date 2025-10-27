from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import ocrmypdf

def home(request):
    context = {}
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        input_path = fs.path(filename)
        output_path = fs.path(f"OCR_{filename}")
        
        try:
            ocrmypdf.ocr(input_path, output_path, deskew=True)
            context['success'] = True
            context['output_file'] = fs.url(f"OCR_{filename}")
        except Exception as e:
            context['error'] = str(e)
    
    return render(request, 'ocrapp/home.html', context)
