from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import pymongo
import json

connection_url = "mongodb+srv://admin:chitrank0614@basecluster.syalx.mongodb.net/Website?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_url)
ApiDatabase = client.get_database('Website')

Products = ApiDatabase.Products
SiteData = ApiDatabase.SiteData


def getAllProducts(request):
    query = Products.find()
    output = []
    for x in query:
        del x['_id']
        output.append(x)
    return JsonResponse({'result': output})


def getProductData(request, pid):
    queryObj = {'ProductID': pid}
    query = Products.find_one(queryObj)
    del query['_id']
    return JsonResponse({'result': query})


def getNewPid(request):
    pid = SiteData.find_one({'Data': 'NextProductID'})
    pid = 'P'+str(pid['NextProductID'])
    return JsonResponse({'result': pid})


def increasePid():
    pid = SiteData.find_one({'Data': 'NextProductID'})
    pid['NextProductID'] += 1
    query = SiteData.update_one({'Data': 'NextProductID'}, {
                                '$set': pid}, upsert=True)