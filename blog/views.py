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

from PIL import Image, ExifTags

# from pillow_heif import register_heif_opener

# register_heif_opener()


def resize_image(f):
    img = Image.open(f)
    exif = img._getexif()
    orientation = None
    for tag, value in exif.items():
        if ExifTags.TAGS.get(tag) == "Orientation":
            orientation = value
            break

    max_width = 1024
    aspect_ratio = max_width / float(img.size[0])
    new_height = int(float(img.size[1]) * float(aspect_ratio))
    img.thumbnail(
        (
            max_width,
            new_height,
        )
    )
    # preserve orientation
    if orientation and orientation in [3, 6, 8]:
        rotations = {3: 180, 6: 270, 8: 90}
        img = img.rotate(rotations[orientation])
    original_format = img.format or "JPEG"
    output = BytesIO()
    img.save(output, format=original_format)
    output.seek(0)
    return InMemoryUploadedFile(
        file=output,
        field_name=None,
        name=f.name,
        content_type=f.content_type,
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
            return JsonResponse({"error": {"message": f"{ex}"}})
        if form.is_valid():
            f = request.FILES["upload"]
            # the following line is the only difference between this
            # function and django_ckeditor_5.views.upload_file
            resized = resize_image(f)
            url = handle_uploaded_file(resized)
            return JsonResponse({"url": url})
    raise Http404(_("Page not found."))
