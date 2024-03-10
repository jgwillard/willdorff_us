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

from PIL import Image, ExifTags, ImageOps

# from pillow_heif import register_heif_opener

# register_heif_opener()


# copied from django-resized
# https://github.com/un1t/django-resized/blob/master/django_resized/forms.py
def normalize_rotation(image):
    """
    Find orientation header and rotate the actual data instead.
    Adapted from http://stackoverflow.com/a/6218425/723090
    """
    try:
        image._getexif()
    except AttributeError:
        # No exit data; this image is not a jpg and can be skipped
        return image

    for orientation in ExifTags.TAGS.keys():
        # Look for orientation header, stop when found
        if ExifTags.TAGS[orientation] == "Orientation":
            break
    else:
        # No orientation header found, do nothing
        return image
    # Apply the different possible orientations to the data; preserve format
    format = image.format
    exif = image._getexif()
    if exif is None:
        return image
    action_nr = exif.get(orientation, None)
    if action_nr is None:
        # Empty orientation exif data
        return image
    if action_nr in (3, 4):
        image = image.rotate(180, expand=True)
    elif action_nr in (5, 6):
        image = image.rotate(270, expand=True)
    elif action_nr in (7, 8):
        image = image.rotate(90, expand=True)
    if action_nr in (2, 4, 5, 7):
        image = ImageOps.mirror(image)
    image.format = format
    return image


def resize_image(f):
    img = Image.open(f)
    # img = normalize_rotation(img)
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
    thumb = img
    original_format = img.format or "JPEG"
    output = BytesIO()
    thumb.save(output, format=original_format, **img.info)
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
            return JsonResponse({"error": {"message": f"{ex}"}}, status=400)
        if form.is_valid():
            f = request.FILES["upload"]
            # the following line is the only difference between this
            # function and django_ckeditor_5.views.upload_file
            resized = resize_image(f)
            url = handle_uploaded_file(resized)
            return JsonResponse({"url": url})
    raise Http404(_("Page not found."))
