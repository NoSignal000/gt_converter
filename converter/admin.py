from django.contrib import admin
from .models import PDFFile,ConvertedFile

@admin.register(PDFFile)
class ReceiptFileAdmin(admin.ModelAdmin):
    list_display = ("id", 'file','timestamp')

@admin.register(ConvertedFile)
class ReceiptFileAdmin(admin.ModelAdmin):
    list_display = ("id",'pdf_file_id' ,'csv_file','pdf_file','timestamp')