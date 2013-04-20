from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from modshogun import RealFeatures, BinaryLabels, MulticlassLabels
from modshogun import GaussianKernel
from modshogun import LibSVM, GMNPSVM

import numpy as np
import json
import re


def binary(request):
    return render_to_response("demos/classification/binary.html", context_instance=RequestContext(request))


def multiclass(request):
    return render_to_response("demos/classification/multiclass.html", context_instance=RequestContext(request))


def index(request):
    return render_to_response("demos/classification/index.html", context_instance=RequestContext(request))


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

    data = {"status": "ok", "domain": [-1, 1], "max": np.max(z), "min": np.min(z), "z": z.tolist()}

    return HttpResponse(json.dumps(data))


def run_multiclass(request):
    points = json.loads(request.GET["points"])
    C = json.loads(request.GET["C"])

    try:
        features, labels = _get_multi_features(points)
    except ValueError as e:
        return HttpResponse(json.dumps({"status": e.message}))

    x, y, z = classify(GMNPSVM, features, labels, C)

    # Conrec hack: add tiny noise
    z = z + np.random.rand(*z.shape) * 0.01

    data = {"status": "ok", "domain": [0, 4], "max": np.max(z), "min": np.min(z), "z": z.tolist()}

    return HttpResponse(json.dumps(data))


def classify(classifier, features, labels, C=5, kernel_name=None, kernel_args=None):
    sigma = 10000
    kernel = GaussianKernel(features, features, sigma)

    svm = classifier(C, kernel, labels)
    svm.train(features)
    x_size = 640
    y_size = 400
    size = 100
    x1 = np.linspace(0, x_size, size)
    y1 = np.linspace(0, y_size, size)
    x, y = np.meshgrid(x1, y1)

    test = RealFeatures(np.array((np.ravel(x), np.ravel(y))))
    kernel.init(features, test)

    out = svm.apply(test).get_values()
    if not len(out):
        out = svm.apply(test).get_labels()
    z = out.reshape((size, size))
    z = np.transpose(z)

    return x, y, z


def _get_coordinates(data):
    regex = re.match(r"translate\((?P<x>.*),(?P<y>.*)\)", data)

    x = float(regex.group("x"))
    y = float(regex.group("y"))

    return (x, y)


def _get_binary_features(data):
    A = np.transpose(np.array(map(_get_coordinates, data.get("a", []))))
    B = np.transpose(np.array(map(_get_coordinates, data.get("b", []))))

    if not len(A):
        if not len(B):
            raise ValueError("0-labels")
        else:
            raise ValueError("1-class-labels")
    else:
        if not len(B):
            raise ValueError("1-class-labels")
        else:
            features = np.concatenate((A, B), axis=1)
            labels = np.concatenate((np.ones(A.shape[1]), -np.ones(B.shape[1])), axis=1)

    features = RealFeatures(features)
    labels = BinaryLabels(labels)

    return features, labels


def _get_multi_features(data):
    v = {"a": None, "b": None, "c": None, "d": None}
    empty = np.zeros((2, 0))
    for key in v:
        if key in data:
            v[key] = np.transpose(np.array(map(_get_coordinates, data[key])))
        else:
            v[key] = empty

    n = len(set(["a", "b", "c", "d"]) & set(data.keys()))

    if not n:
        raise ValueError("0-labels")
    elif n == 1:
        raise ValueError("1-class-labels")
    else:
        features = np.concatenate(tuple(v.values()), axis=1)
        labels = np.concatenate((np.zeros(v["a"].shape[1]), np.ones(v["b"].shape[1]), 2 * np.ones(v["c"].shape[1]), 3 * np.ones(v["d"].shape[1])), axis=1)

    features = RealFeatures(features)
    labels = MulticlassLabels(labels)

    return features, labels
