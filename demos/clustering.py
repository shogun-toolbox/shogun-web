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
    return render_to_response("demos/clustering/index.html", context_instance=RequestContext(request))

def cluster(request):
    try:
        arguments = read_data(request)
        kmeans = train_clustering(*arguments)
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

