from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext_lazy as _
from django.http import Http404, JsonResponse

from django_ckeditor_5.views import (
    UploadFileForm,
    NoImageException,
    image_verify,
    handle_uploaded_file,
)

from PIL import Image

from pillow_heif import register_heif_opener

register_heif_opener()


def resize_image(f):
    img = Image.open(f)
    max_width = 1024
    aspect_ratio = max_width / float(img.size[0])
    new_height = int(float(img.size[1]) * float(aspect_ratio))
    img.thumbnail(
        (
            max_width,
            new_height,
        ),
        Image.Resampling.LANCZOS,
    )
    output = BytesIO()
    img.save(output, format="JPEG")
    output.seek(0)
    return InMemoryUploadedFile(
        file=output,
        field_name=None,
        name=f.name,
        content_type="img/jpeg",
        size=output.tell(),
        charset=None,
    )


# copied from django_ckeditor_5.views
def upload_file(request):
    if request.method == "POST" and request.user.is_staff:
        form = UploadFileForm(request.POST, request.FILES)
        try:
            image_verify(request.FILES["upload"])
        except NoImageException as ex:
            return JsonResponse({"error": {"message": f"{ex}"}}, status=400)
        if form.is_valid():
            f = request.FILES["upload"]
            # the following line is the only difference between this
            # function and django_ckeditor_5.views.upload_file
            resized = resize_image(f)
            url = handle_uploaded_file(resized)
            return JsonResponse({"url": url})
    raise Http404(_("Page not found."))
