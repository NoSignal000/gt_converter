from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse ,HttpResponse
from django.shortcuts import render
from .models import ConvertedFile
from .signals import convert_file
from datetime import datetime
from datetime import *
import requests

BACKEND_URL = 'http://localhost:8000/media/'
# BACKEND_URL = 'https://file-converter-0ndt.onrender.com/media/'


# def index(request):
#     print("Testing1")
#     response = requests.get('https://file-converter-0ndt.onrender.com/api/get-all')
#     print("Testing2")
#     # response = requests.get('https://file-converter-0ndt.onrender.com/api/get-all')
#     print("Testing3")
#     api_data = response.json()
#     print(api_data['data'])
#     context = {
#         'receipt_files':api_data["data"]
#     }
#     return render(request,'convert.html')

def fetch_data():
    try:
        response = requests.get('https://file-converter-0ndt.onrender.com/api/get-all', timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()  # Directly return the JSON data
    except requests.exceptions.RequestException as e:
        # Handle the error or log it
        print(f"RequestException: {e}")
        return None

def index(request):
    try:
        print("Testing1")
        api_data = fetch_data()
        
        if api_data is None:
            print("No data received from the API.")
            return HttpResponse("Failed to retrieve data from the API.", status=500)

        print("Testing2")
        print("Testing3")
        print(api_data.get('data'))  # Use .get to avoid KeyError if 'data' key is missing

        context = {
            'receipt_files': api_data.get("data", [])  # Provide a default empty list if 'data' key is missing
        }
        return render(request, 'convert.html', context)
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return HttpResponse("Failed to retrieve data from the API.", status=500)
    except KeyError as e:
        print(f"Key error: {e}")
        return HttpResponse("Unexpected response structure from the API.", status=500)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return HttpResponse("An unexpected error occurred.", status=500)





@csrf_exempt
def get_all_result(request):
    if request.method == 'GET':
        try:
            converted_files = ConvertedFile.objects.all().order_by('-timestamp')
            
            # Serialize the model instances into dictionaries
            converted_files_data = []
            for converted_file in converted_files:
                timestamp_obj = timestamp = datetime.fromisoformat(converted_file.pdf_file.timestamp.isoformat()[:-6])
                formatted_time = timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")
                converted = {
                    'pdf_file': {
                        'id': converted_file.pdf_file.id,
                        'file': converted_file.pdf_file.file.url,
                        'timestamp': formatted_time,
                    },
                    'csv_file': converted_file.csv_file.url,
                    'timestamp': converted_file.timestamp.isoformat(),
                }
                converted_files_data.append(converted)            
            return JsonResponse({'status': True,'data':converted_files_data},status=200)
        except Exception as e:
            return JsonResponse({'status': False},status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=500)



@csrf_exempt
def upload_file(request):
    if request.method == 'POST':       
        pdf_file = request.FILES['pdf_file']
        leftMargin = request.POST.get("x1")
        bottomMargin = request.POST.get("y2")
        rightMargin = request.POST.get("x2")
        topMargin = request.POST.get("y1")

        return convert_file(pdf_file,int(leftMargin),int(bottomMargin),int(rightMargin),int(topMargin))
    