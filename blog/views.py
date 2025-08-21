from django.utils.translation import gettext_lazy as _
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import DetailView, ListView
from django.http import Http404, JsonResponse

from django_ckeditor_5.views import (
    UploadFileForm,
    NoImageException,
    image_verify,
    handle_uploaded_file,
)

from .models import Post
from .services import resize_image


class HomePageView(ListView):
    template_name = "blog/home.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-published_date"]
    paginate_by = 3
    queryset = Post.objects.filter(is_published=True)

class PostView(DetailView):
    template_name = "blog/post.html"
    model = Post
    context_object_name = "post"


# copied from django_ckeditor_5.views
def upload_file(request):
    if request.method == "POST" and request.user.is_staff:
        form = UploadFileForm(request.POST, request.FILES)
        try:
            image_verify(request.FILES["upload"])
        except NoImageException as ex:
            return JsonResponse({"error": {"message": f"{ex}"}}, status=400)
        except MultiValueDictKeyError as ex:
            return JsonResponse({"error": {"message": f"{ex}"}}, status=400)
        if form.is_valid():
            f = request.FILES["upload"]
            # the following line is the main difference between this
            # function and django_ckeditor_5.views.upload_file
            resized = resize_image(f)
            url = handle_uploaded_file(resized)
            return JsonResponse({"url": url})
    return Http404(_("Page not found."))
