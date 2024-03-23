from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image

from pillow_heif import register_heif_opener

register_heif_opener()


def resize_image(f: InMemoryUploadedFile):
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
