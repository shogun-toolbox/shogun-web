from django.core.context_processors import csrf
from django.contrib.auth import login as auth_login
from django.contrib.auth import *
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response
from modshogun import *

import numpy
import json

def entrance(request):
    return render_to_response("demos/svr/index.html",context_instance=RequestContext(request))
    
def point(request):
    try:
        arguments = read_data(request)
        svm=train_svr(*arguments)
        x=numpy.linspace(0, 1, 800)
        y=numpy.array(svm.apply(RealFeatures(numpy.array([x]))).get_labels(), dtype=numpy.float64)
        line_dot = []
        for i in xrange(len(x)):
            line_dot.append({'x_value' : x[i], 'y_value' : y[i]})
        return HttpResponse(json.dumps(line_dot))
    except:
        return HttpResponseNotFound()
            
def read_data(request):
    labels = []
    features = []
    data = json.loads(request.POST['data'])
    cost = float(request.POST['C'])
    tubeeps = float(request.POST['tube'])
    degree = int(request.POST['d'])
    width = float(request.POST['sigma'])
    kernel_name = request.POST['kernel']
    for pt in data["points"]:
        labels.append(float(pt["y"]))
        features.append(float(pt["x"]))
    return (cost, tubeeps, degree, width, kernel_name, labels, features)
                
def train_svr(cost, tubeeps, degree, width, kernel_name, labels, features):
    labels = numpy.array(labels, dtype=numpy.float64)
    num = len(features)
    if num == 0:
        raise TypeError
    examples = numpy.zeros((1,num))
                
    for i in xrange(num):
        examples[0,i] = features[i]
                    
    lab = RegressionLabels(labels)
    train = RealFeatures(examples)
                
    if kernel_name == "line":
        gk = LinearKernel(train, train)
        gk.set_normalizer(IdentityKernelNormalizer())
    elif kernel_name == "poly":
        gk = PolyKernel(train, train, degree, True)
        gk.set_normalizer(IdentityKernelNormalizer())
    elif kernel_name == "gaus":
        gk = GaussianKernel(train, train, width)
    else:
        raise TypeError
                    
    svm = LibSVR(cost, tubeeps, gk, lab)
    svm.train()
    svm.set_epsilon(1e-2)
    return svm
