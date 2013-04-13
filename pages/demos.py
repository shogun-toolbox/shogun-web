from django.core.context_processors import csrf
from django.contrib.auth import login as auth_login
from django.contrib.auth import *
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

import numpy
from modshogun import *

import json

class svr:
    def entrance(request):
        return render_to_response("demos/svr/index.html",context_instance=RequestContext(request))
    entrance=staticmethod(entrance)

    def point(request):
        line_dot=[]
        JSONdata = request.GET['data']
        data = json.loads(JSONdata)
        cost = float(request.GET['C'])
        tubeeps = float(request.GET['tube'])
        degree = int(request.GET['d'])
        width = float(request.GET['sigma'])
        kernel_name = request.GET['kernel']
        labels = []
        features = []
    
        for pt in data["points"]:
            labels.append(float(pt["y"]))
            features.append(float(pt["x"]))
        labels = numpy.array(labels, dtype=numpy.float64)
        num = len(features)
        examples = numpy.zeros((1,num))
        
        for i in xrange(num):
            examples[0,i] = features[i]
                
        lab = RegressionLabels(labels)
        train = RealFeatures(examples)
                
        if kernel_name == "line":
            gk = LinearKernel (train, train)
            gk.set_normalizer(IdentityKernelNormalizer())
        elif kernel_name == "poly":
            gk = PolyKernel(train, train, degree, True)
            gk.set_normalizer(IdentityKernelNormalizer())
        elif kernel_name == "gaus":
            gk = GaussianKernel(train, train, width)
                        
        svm = LibSVR(cost, tubeeps, gk, lab)
        svm.train()
        svm.set_epsilon(1e-2)
                        
        x=numpy.linspace(0,8,800)
        y=svm.apply(RealFeatures(numpy.array([x])));
        y=numpy.array(y, dtype=numpy.float64)
        for i in xrange(len(x)):
            line_dot.append({'x_value' : x[i], 'y_value' : y[i]})
        return HttpResponse(json.dumps(line_dot))

    point = staticmethod(point)
