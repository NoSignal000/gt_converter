from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse ,HttpResponse
from django.shortcuts import render,redirect
from .models import ConvertedFile
from .signals import convert_file
from datetime import datetime
from datetime import *
import os


def index(request):
    # print("Testing1")
    # response = requests.get('https://file-converter-0ndt.onrender.com/api/get-all')
    converted_files = ConvertedFile.objects.all().order_by('-timestamp')[:10]
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
                'name':os.path.basename(converted_file.csv_file.url),
                'csv_file': converted_file.csv_file.url,
                'timestamp': converted_file.timestamp.isoformat(),
                }
        converted_files_data.append(converted)
    # api_data = response.json()
    context = {
        # 'receipt_files':api_data["data"]
        'receipt_files':converted_files_data
    }
    return render(request,'convert.html',context)
    # return render(request,'convert.html')



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


@csrf_exempt
def delete_view(request):
    converted_files = ConvertedFile.objects.all().order_by('-timestamp')
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
                'name':os.path.basename(converted_file.csv_file.url),
                'csv_file': converted_file.csv_file.url,
                'timestamp': converted_file.timestamp.isoformat(),
                }
        converted_files_data.append(converted)
    context = {
        'receipt_files':converted_files_data
    }
    return render(request,'delete_view.html',context)

@csrf_exempt
def delete(request):
    id = request.GET.get('id')
    print(id)
    print(type(id))
    data = ConvertedFile.objects.filter(id=id)
    data.delete()    


    print(data)
    return redirect("/api/rm")