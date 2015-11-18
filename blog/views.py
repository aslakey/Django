from django.shortcuts import render

# Views are the logic of the website
#pass to a template

def post_list(request):
    return render(request, 'blog/post_list.html', {})