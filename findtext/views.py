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

def plotResults(request):
    from PIL import Image
    import glob
    from skimage import io
    from scipy.misc import toimage
    from sklearn import svm
    import numpy as np
    from skimage.io import imread
    from skimage.filters import threshold_otsu
    from skimage.transform import resize
    #import cPickle
    from matplotlib import pyplot as plt
    from skimage.morphology import closing, square
    from skimage.measure import regionprops
    from skimage import restoration
    from skimage import measure
    from skimage.color import label2rgb
    import matplotlib.patches as mpatches
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    import os
    import skimage
    from skimage import io
    from skimage.viewer import ImageViewer
    from scipy.misc import toimage
    from skimage import feature
    import scipy.ndimage as ndi
    from skimage.feature import hog
    from random import randint
    import random
    
    # Load last image
    documents = Document.objects.all()[Document.objects.count()-1]
    
    #read in image
    url= ('http://aslakey.pythonanywhere.com' + documents.docfile.url)
    chk = io.imread(url,as_grey = True)

    #Process one Denoise and Increase Contrast
    image = restoration.denoise_tv_chambolle(chk, weight=0.1) #Denoises using total variation: http://scikit-image.org/docs/dev/api/skimage.restoration.html

    thresh = threshold_otsu(image) #Thresholding returns a binary image (black or white) on a greyscale image
    bw = closing(image > thresh, square(2))

    #This keeps the edges really crisp (and is simple) should we use this??
    binary = image > thresh
    #toimage(binary).show()

    cleared = bw.copy()

    label_image = measure.label(cleared)
    borders = np.logical_xor(bw,cleared)
    label_image[borders] = -1

    coordinates =[]
    i = 0
    for region in regionprops(label_image):
        if region.area > 10:
            minr, minc, maxr, maxc = region.bbox
            margin = 3
            minr, minc, maxr, maxc = minr-margin, minc-margin, maxr+margin, maxc+margin
            roi = image[minr:maxr, minc:maxc]
            if roi.shape[0]*roi.shape[1] == 0:
                continue
            else:
                if i==0:
                    samples = resize(roi, (20,20))
                    coordinates.append(region.bbox)
                    i+=1
                elif i==1:
                    roismall = resize(roi, (20,20))
                    samples = np.concatenate((samples[None,:,:], roismall[None,:,:]), axis=0)
                    coordinates.append(region.bbox)
                    i+=1
                else:
                    roismall = resize(roi, (20,20))
                    samples = np.concatenate((samples[:,:,:], roismall[None,:,:]), axis=0)
                    coordinates.append(region.bbox)

    candidates = coordinates[:]

    image_list = candidates[:]
    for i in range(len(image_list)):
        image_list[i] = resize(image[candidates[i][0]:candidates[i][2],candidates[i][1]:candidates[i][3]],(20,20))

    #Creating HOG curves
    copyOfList = image_list[:]
    for i in range(len(image_list)):
        fd, copyOfList[i] = hog(copyOfList[i],orientations = 8, pixels_per_cell = (10,10),cells_per_block = (1,1),visualise = True)


    for i in range(len(copyOfList)):
        copyOfList[i] = copyOfList[i].reshape(1,400)

    a = copyOfList[0]
    for i in range(1,len(copyOfList)):
        a = np.append(a,copyOfList[i],axis = 0)

    from sklearn.externals import joblib
    import os
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'pickle FIles/filename.pkl')
    xyz = joblib.load(file_path)
    predicted = xyz.predict(a)

    candidatesFinal = []
    ind = np.where(predicted == 1)[0]
    for i in range(len(ind)):
        candidatesFinal.append(candidates[ind[i]])

    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(image)

    for i in range(len(candidatesFinal)):

    # draw rectangle around each region
        rect = mpatches.Rectangle((candidatesFinal[i][1],candidatesFinal[i][0]), candidatesFinal[i][3] - candidatesFinal[i][1], candidatesFinal[i][2]- candidatesFinal[i][0],
                              fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')

    canvas.print_png(response)
    return response