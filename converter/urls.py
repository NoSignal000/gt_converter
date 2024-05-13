from django.urls import path
from .views import upload_file, get_all_result,index

urlpatterns = [
    path('',index),
    path("api/upload", upload_file, name="upload"),
    path("api/get-all", get_all_result, name="get-all"),
]