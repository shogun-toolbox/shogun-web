from django.core.context_processors import csrf
from django.contrib.auth import login as auth_login
from django.contrib.auth import *
from django.template import Context, loader
from django.http import HttpResponse
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
        labels = []
        features = []
        try:
            JSONdata = request.POST['data']
            data = json.loads(JSONdata)
            cost = float(request.POST['C'])
            tubeeps = float(request.POST['tube'])
            degree = int(request.POST['d'])
            width = float(request.POST['sigma'])
            kernel_name = request.POST['kernel']
            for pt in data["points"]:
                labels.append(float(pt["y"]))
                features.append(float(pt["x"]))
        except:
            return HttpResponse()

        labels = numpy.array(labels, dtype=numpy.float64)
        num = len(features)
        if num == 0:
            return HttpResponse()
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
        else:
            return HttpResponse()
                        
        svm = LibSVR(cost, tubeeps, gk, lab)
        svm.train()
        svm.set_epsilon(1e-2)
                        
        x=numpy.linspace(0,1,800)
        y=svm.apply(RealFeatures(numpy.array([x]))).get_labels()
        y=numpy.array(y, dtype=numpy.float64)
        for i in xrange(len(x)):
            line_dot.append({'x_value' : x[i], 'y_value' : y[i]})
        return HttpResponse(json.dumps(line_dot))

    point = staticmethod(point)

class clustering:
    def entrance(request):
        return render_to_response("demos/clustering/index.html",context_instance=RequestContext(request))

    entrance = staticmethod(entrance)

    def cluster (request):
        try:
            k = int(request.POST['number_of_clusters'])
            positive = json.loads(request.POST['positive'])['points']
            negative = json.loads(request.POST['negative'])['points']
            distance_name = request.POST['distance_name']
        except:
            return HttpResponse()

        if len(positive) == 0 and len(negative) == 0:
            return HttpResponse()

        labels = numpy.array([1]*len(positive) + [-1]*len(negative), dtype=numpy.float64)
        num_pos = len(positive)
        num_neg = len(negative)
        features = numpy.zeros((2,num_pos+num_neg))
    
        for i in xrange(num_pos):
            features[0,i] = positive[i]['x']
            features[1,i] = positive[i]['y']
        
        for i in xrange(num_neg):
            features[0,i+num_pos] = negative[i]['x']
            features[1,i+num_pos] = negative[i]['y']

        lab = BinaryLabels(labels)
        train = RealFeatures(features)


        if distance_name == "eucl":
            distance = EuclideanDistance(train, train)
        elif distance_name == "manh":
            distance = ManhattanMetric(train, train)
        elif distance_name == "jens":
            distance = JensenMetric(train, train)
        else:
            return HttpResponse()

        kmeans = KMeans(k , distance)
        kmeans.train()
        centers = kmeans.get_cluster_centers()
        radi = kmeans.get_radiuses()

        result = {'circle': []}
        delta = 100
        for i in xrange(k):
            for t in range( int(2*numpy.pi*delta)):
                result['circle'].append({'x': centers[0,i],
                                         'y': centers[1,i],
                                         'r': radi[i]})

        return HttpResponse(json.dumps(result))
    cluster = staticmethod(cluster)
