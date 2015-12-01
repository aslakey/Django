# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from .models import Document
from .forms import DocumentForm

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            #Here is where we could do shit with our image file!!

            return HttpResponseRedirect(reverse('findtext.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()[Document.objects.count()-1]

    # Render list page with the documents and the form
    return render_to_response(
        'findtext/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

def index(request):
    return HttpResponse("Hello, world. You're at the find text index.")
