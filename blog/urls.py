from django.urls import path

from .views import upload_file, HomePageView, PostView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("posts/<slug:slug>/", PostView.as_view(), name="post"),
    path("image_upload/", upload_file, name="ck_editor_5_upload_file"),
]
