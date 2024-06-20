from django.db import models

    
class PDFFile(models.Model):
    file = models.FileField(upload_to='receipts/')
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.file.name

class ConvertedFile(models.Model):
    pdf_file = models.OneToOneField(PDFFile, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to='receipts/converted_csv/')
    timestamp = models.DateTimeField(auto_now_add=True)
