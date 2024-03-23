from io import BytesIO
from json import loads as json_loads
from unittest.mock import patch

from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import (
    SimpleUploadedFile,
    InMemoryUploadedFile,
)
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User

from django_ckeditor_5.views import NoImageException
from PIL import Image

from .services import resize_image
from .views import upload_file


class ImageResizeTestCase(TestCase):
    def test_image_resize(self):
        image_data = BytesIO()
        Image.new("RGB", (1200, 800), (255, 255, 255)).save(
            image_data, format="JPEG"
        )
        image_data.seek(0)
        uploaded_file = SimpleUploadedFile("test.jpg", image_data.getvalue())

        resized_image = resize_image(uploaded_file)

        self.assertIsInstance(resized_image, InMemoryUploadedFile)

        resized_img = Image.open(resized_image)

        self.assertTrue(resized_img.size[0] <= 1024)
        self.assertEqual(resized_img.size[1], int(800 * 1024 / 1200))
        self.assertEqual(resized_img.format, "JPEG")
        self.assertEqual(resized_image.name, "test.jpg")
        self.assertEqual(resized_image.content_type, "img/jpeg")
        self.assertLessEqual(resized_image.size, uploaded_file.size)


class UploadFileTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser", password="12345"
        )
        self.staff_user = User.objects.create_user(
            username="staffuser", password="12345", is_staff=True
        )

    def test_upload_file_post_no_staff(self):
        request = self.factory.post(
            "/upload/", {"upload": SimpleUploadedFile("test.jpg", b"content")}
        )
        request.user = self.user
        response = upload_file(request)

        self.assertIsInstance(response, Http404)

    @patch("blog.views.handle_uploaded_file")
    @patch("blog.views.resize_image")
    @patch("blog.views.image_verify")
    def test_upload_file_post(
        self, mock_image_verify, mock_resize_image, mock_handle_uploaded_file
    ):
        mock_image_verify.return_value = None
        mock_resize_image.return_value = SimpleUploadedFile(
            "test.jpg", b"content", content_type="image/jpeg"
        )
        mock_handle_uploaded_file.return_value = "/media/test.jpg"

        request = self.factory.post(
            "/upload/",
            {
                "upload": SimpleUploadedFile(
                    "test.jpg", b"content", content_type="image/jpeg"
                )
            },
        )
        request.user = self.staff_user
        response = upload_file(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertIn("url", json_loads(response.content))

    @patch("blog.views.image_verify")
    def test_upload_file_post_empty_file(self, mock_image_verify):
        mock_image_verify.return_value = None
        mock_image_verify.side_effect = NoImageException

        request = self.factory.post(
            "/upload/",
            {
                "upload": SimpleUploadedFile(
                    "test.jpg", b"content", content_type="image/jpeg"
                )
            },
        )
        request.user = self.staff_user

        response = upload_file(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", json_loads(response.content))

    def test_upload_file_post_no_file(self):
        request = self.factory.post("/upload/")
        request.user = self.staff_user

        response = upload_file(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", json_loads(response.content))
