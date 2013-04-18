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
import traceback

class svr():
    @staticmethod
    def entrance(request):
        return render_to_response("demos/svr/index.html",context_instance=RequestContext(request))

    @staticmethod
    def point(request):
        try:
            arguments = svr.read_data(request)
            svm=svr.train_svr(*arguments)
            x=numpy.linspace(0, 1, 800)
            y=numpy.array(svm.apply(RealFeatures(numpy.array([x]))).get_labels(), dtype=numpy.float64)
            line_dot = []
            for i in xrange(len(x)):
                line_dot.append({'x_value' : x[i], 'y_value' : y[i]})
                return HttpResponse(json.dumps(line_dot))
        except:
            return HttpResponseNotFound()

    @staticmethod
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

    @staticmethod
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

class clustering():
    @staticmethod
    def entrance(request):
        return render_to_response("demos/clustering/index.html", context_instance=RequestContext(request))

    @staticmethod
    def cluster(request):
        try:
            arguments = clustering.read_data(request)
            kmeans = clustering.train_clustering(*arguments)
            centers = kmeans.get_cluster_centers()
            radi = kmeans.get_radiuses()
            result = {'circle': []}
            for i in xrange(arguments[3]): # arguments[3] is k
                result['circle'].append({'x': centers[0,i],
                                         'y': centers[1,i],
                                         'r': radi[i]})
            return HttpResponse(json.dumps(result))
        except:
            return HttpResponseNotFound()

    @staticmethod
    def read_data(request):
        k = int(request.POST['number_of_clusters'])
        if k > 500:
            raise TypeError
        positive = json.loads(request.POST['positive'])['points']
        negative = json.loads(request.POST['negative'])['points']
        distance_name = request.POST['distance_name']
        
        if len(positive) == 0 and len(negative) == 0:
            raise TypeError
        return (positive, negative, distance_name, k)

    @staticmethod
    def train_clustering(positive, negative, distance_name, k):
        labels = numpy.array([1]*len(positive) + [-1]*len(negative), dtype=numpy.float64)
        num_pos = len(positive)
        num_neg = len(negative)
        features = numpy.zeros((2, num_pos+num_neg))
        
        for i in xrange(num_pos):
            features[0, i] = positive[i]['x']
            features[1, i] = positive[i]['y']
            
        for i in xrange(num_neg):
            features[0, i+num_pos] = negative[i]['x']
            features[1, i+num_pos] = negative[i]['y']
                 
        lab = BinaryLabels(labels)
        train = RealFeatures(features)
                
        if distance_name == "eucl":
            distance = EuclideanDistance(train, train)
        elif distance_name == "manh":
            distance = ManhattanMetric(train, train)
        elif distance_name == "jens":
            distance = JensenMetric(train, train)
        else:
            raise TypeError
                    
        kmeans = KMeans(k, distance)
        kmeans.train()

        return kmeans

