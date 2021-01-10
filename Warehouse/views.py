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


@csrf_exempt
def addProduct(request):
    jsonData = json.loads(request.body)
    pid = jsonData['PID']
    queryObj = {
        'ProductID': pid,
        'Name': jsonData['Name'],
        'Category': jsonData['Category'],
        'Specifications': jsonData['Specifications'],
        'ImageURLs': jsonData['Images'],
        'Tags': jsonData['Tags'],
        'Price': float(jsonData['Price']),
        'Quantity': int(jsonData['Quantity']),
        'Availability': jsonData['Availability']
    }
    query = Products.update_one(
        {'ProductID': pid}, {'$set': queryObj}, upsert=True)

    output = {'result': 'Added'}
    increasePid()
    return JsonResponse(output)


@csrf_exempt
def deleteProduct(request):
    jsonData = json.loads(request.body)
    pid = jsonData['PID']
    queryObj = {'ProductID': pid}
    query = Products.delete_one(queryObj)
    return JsonResponse({'result': 'Data Deleted...'})


@csrf_exempt
def saveDetails(request):
    jsonData = json.loads(request.body)
    queryObj = {
        'Data': 'Details',
        'Details': {'Name': jsonData['Name'],
                    'Address': jsonData['Address'],
                    'PhoneNumber': jsonData['PhoneNumber'],
                    'Email': jsonData['Email']
                    }
    }
    query = SiteData.update_one(
        {'Data': 'Details'}, {'$set': queryObj}, upsert=True)
    return JsonResponse({'result': 'Saved Successfully'})


def getDetails(request):
    query = SiteData.find_one({'Data': 'Details'})
    query = query['Details']
    output = {}

    output['Name'] = query['Name']
    output['Address'] = query['Address']
    output['Email'] = query['Email']
    output['PhoneNumber'] = query['PhoneNumber']
    return JsonResponse({'result': output})


def warehouseHome(request):
    return render(request, "Warehouse/index.html")


def warehouseTest(request):
    return HttpResponse("Hello Warehouse Here.")
