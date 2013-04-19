from django.http import HttpResponse, HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response
from modshogun import *

import numpy
import json
import re

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


class classification(object):
    @staticmethod
    def binary(request):
        return render_to_response("demos/classification/binary.html", context_instance=RequestContext(request))

    @staticmethod
    def multiclass(request):
        return render_to_response("demos/classification/multiclass.html", context_instance=RequestContext(request))

    @staticmethod
    def index(request):
        return render_to_response("demos/classification/index.html", context_instance=RequestContext(request))

    @staticmethod
    def run_binary(request):
        points = json.loads(request.GET["points"])
        C = json.loads(request.GET["C"])

        try:
            features, labels = _get_binary_features(points)
        except ValueError as e:
            return HttpResponse(json.dumps({"status": repr(e)}))

        try:
            x, y, z = classify(LibSVM, features, labels, C)
        except Exception as e:
            return HttpResponse(json.dumps({"status": repr(e)}))

        data = {"status": "ok", "domain": [-1, 1], "max": numpy.max(z), "min": numpy.min(z), "z": z.tolist()}

        return HttpResponse(json.dumps(data))

    @staticmethod
    def run_multiclass(request):
        points = json.loads(request.GET["points"])
        C = json.loads(request.GET["C"])

        try:
            features, labels = _get_multi_features(points)
        except ValueError as e:
            return HttpResponse(json.dumps({"status": e.message}))

        x, y, z = classify(GMNPSVM, features, labels, C)

        # Conrec hack: add tiny noise
        z = z + numpy.random.rand(*z.shape) * 0.01

        data = {"status": "ok", "domain": [0, 4], "max": numpy.max(z), "min": numpy.min(z), "z": z.tolist()}

        return HttpResponse(json.dumps(data))


def classify(classifier, features, labels, C=5, kernel_name=None, kernel_args=None):
    sigma = 10000
    kernel = GaussianKernel(features, features, sigma)

    svm = classifier(C, kernel, labels)
    svm.train(features)
    x_size = 640
    y_size = 400
    size = 100
    x1 = numpy.linspace(0, x_size, size)
    y1 = numpy.linspace(0, y_size, size)
    x, y = numpy.meshgrid(x1, y1)

    test = RealFeatures(numpy.array((numpy.ravel(x), numpy.ravel(y))))
    kernel.init(features, test)

    out = svm.apply(test).get_values()
    if not len(out):
        out = svm.apply(test).get_labels()
    z = out.reshape((size, size))
    z = numpy.transpose(z)

    return x, y, z


def _get_coordinates(data):
    regex = re.match(r"translate\((?P<x>.*),(?P<y>.*)\)", data)

    x = float(regex.group("x"))
    y = float(regex.group("y"))

    return (x, y)


def _get_binary_features(data):
    A = numpy.transpose(numpy.array(map(_get_coordinates, data.get("a", []))))
    B = numpy.transpose(numpy.array(map(_get_coordinates, data.get("b", []))))

    if not len(A):
        if not len(B):
            raise ValueError("0-labels")
        else:
            raise ValueError("1-class-labels")
    else:
        if not len(B):
            raise ValueError("1-class-labels")
        else:
            features = numpy.concatenate((A, B), axis=1)
            labels = numpy.concatenate((numpy.ones(A.shape[1]), -numpy.ones(B.shape[1])), axis=1)

    features = RealFeatures(features)
    labels = BinaryLabels(labels)

    return features, labels


def _get_multi_features(data):
    v = {"a": None, "b": None, "c": None, "d": None}
    empty = numpy.zeros((2, 0))
    for key in v:
        if key in data:
            v[key] = numpy.transpose(numpy.array(map(_get_coordinates, data[key])))
        else:
            v[key] = empty

    n = len(set(["a", "b", "c", "d"]) & set(data.keys()))

    if not n:
        raise ValueError("0-labels")
    elif n == 1:
        raise ValueError("1-class-labels")
    else:
        features = numpy.concatenate(tuple(v.values()), axis=1)
        labels = numpy.concatenate((numpy.zeros(v["a"].shape[1]), numpy.ones(v["b"].shape[1]), 2 * numpy.ones(v["c"].shape[1]), 3 * numpy.ones(v["d"].shape[1])), axis=1)

    features = RealFeatures(features)
    labels = MulticlassLabels(labels)

    return features, labels
