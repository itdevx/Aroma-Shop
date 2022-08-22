from django.shortcuts import render
from django.views import generic



class BlogView(generic.View):
    template_name = 'blog.html'

    def get(self, request):
        return render(request, self.template_name)


class SingleBlog(generic.View):
    template_name = 'single-blog.html'

    def get(self, request):
        return render(request, self.template_name)
    