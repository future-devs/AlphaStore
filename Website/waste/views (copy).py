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
Sessions = ApiDatabase.Sessions


def websiteTest(request):
    # print(render(request, "Website/test.html"))
    return render(request, "Website/product.html")


@csrf_exempt
def index(request):
    return render(request, "Website/index.html")


@csrf_exempt
def getRandomProducts(request):
    query = Products.aggregate([{"$sample": {"size": 8}}])
    output = []
    for x in query:
        item = {}
        if x['ImageURLs']:
            item['ImageURL'] = x['ImageURLs'][0]
        else:
            continue
        item['Name'] = x['Name']
        item['ProductID'] = x['ProductID']
        item['Category'] = x['Category'].upper()
        output.append(item)
    return JsonResponse({'result': output})


@csrf_exempt
def getRandomCategoryProducts(request, count, category):
    query = Products.aggregate(
        [{"$match": {"Category": category}}, {"$sample": {"size": count}}])
    output = []
    for x in query:
        item = {}
        if x['ImageURLs']:
            item['ImageURL'] = x['ImageURLs'][0]
        else:
            continue
        item['Name'] = x['Name']
        item['ProductID'] = x['ProductID']
        item['Category'] = x['Category'].upper()
        output.append(item)
    return JsonResponse({'result': output})


@csrf_exempt
def getProductData(request, pid):
    queryObj = {'ProductID': pid}
    query = Products.find_one(queryObj)
    del query['_id']
    return JsonResponse({'result': query})


@csrf_exempt
def getProductPage(request, pid):
    queryObj = {'ProductID': pid}
    query = Products.find_one(queryObj)

    name = query["Name"]
    category = query["Category"]
    imageURLs = query["ImageURLs"]
    specifications = query["Specifications"]
    tags = query["Tags"]
    availability = query["Availability"]
    price = query["Price"]
    quantity = query['Quantity']
