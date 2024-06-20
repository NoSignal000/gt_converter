from django.urls import path
from .views import upload_file, get_all_result,index,delete_view, delete

urlpatterns = [
    path('',index),
    path("api/upload", upload_file, name="upload"),
    path("api/get-all", get_all_result, name="get-all"),
    path("api/rm", delete_view, name="delete_view"),
    path("api/delete/", delete, name="delete"),
]