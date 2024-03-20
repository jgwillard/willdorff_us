from django.urls import path

from .views import upload_file

urlpatterns = [
    path("image_upload/", upload_file, name="ck_editor_5_upload_file"),
]
