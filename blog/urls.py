from django.urls import path

from .views import upload_file, HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("image_upload/", upload_file, name="ck_editor_5_upload_file"),
]
