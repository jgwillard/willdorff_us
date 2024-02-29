from django.views.generic import ListView

from blog.models import Post


class HomePageView(ListView):
    template_name = "core/home.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-pub_date"]
    paginate_by = 3
