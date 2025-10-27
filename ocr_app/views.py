from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from .ocr_processor import OCRProcessor
import os

def index(request):
    return render(request, 'ocr_app/index.html')

@csrf_exempt
def process_ocr(request):
    if request.method == 'POST':
        try:
            processor = OCRProcessor(output_dir='media/output')
            
            # Check if file or URL
            if 'file' in request.FILES:
                uploaded_file = request.FILES['file']
                input_path = f'media/uploads/{uploaded_file.name}'
                
                # Save uploaded file
                os.makedirs('media/uploads', exist_ok=True)
                with open(input_path, 'wb+') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)
                
                # Process OCR
                output_path = processor.process_file(input_path)
                
            elif 'url' in request.POST:
                url = request.POST['url']
                output_path = processor.process_from_url(url)
            else:
                return JsonResponse({'error': 'No file or URL provided'}, status=400)
            
            return JsonResponse({
                'success': True,
                'message': 'OCR completed successfully!',
                'output_path': output_path
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)