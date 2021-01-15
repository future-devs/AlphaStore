from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import pymongo
import json
import datetime

connection_url = "mongodb+srv://admin:chitrank0614@basecluster.syalx.mongodb.net/Website?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_url)
ApiDatabase = client.get_database('Website')

Products = ApiDatabase.Products
SiteData = ApiDatabase.SiteData
Sessions = ApiDatabase.Sessions
Users = ApiDatabase.Users

# Sessions.create_index("CreatedAt", expireAfterSeconds=12*60*60)


def websiteTest(request):
    # print(render(request, "Website/test.html"))
    return render(request, "Website/product.html")


def getRandomProducts(count):
    query = Products.aggregate([{"$sample": {"size": count}}])
    output = []
    for x in query:
        item = {}
        if x['ImageURLs']:
            item['ImageURL'] = x['ImageURLs'][0]
        else:
            continue
        item['Name'] = x['Name']
        item['ProductURL'] = 'product?pid='+x['ProductID']
        item['Category'] = x['Category'].upper()
        output.append(item)
    return output


def getRandomCategoryProducts(category, count):
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
        item['ProductURL'] = 'product?pid='+x['ProductID']
        item['Category'] = x['Category'].upper()
        output.append(item)
    return output


def getProductData(pid):
    queryObj = {'ProductID': pid}
    query = Products.find_one(queryObj)
    return query


def getClientIp(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def createSession(useremail, clientIp):
    query = Sessions.find_one({"Useremail": useremail})
    if query is None or query['ClientIP'] != clientIp:
        Sessions.insert_one(
            {"Useremail": useremail, "ClientIP": clientIp, "CreatedAt": datetime.datetime.now()})


def getSession(clientIp):
    query = Sessions.find_one({"ClientIP": clientIp})
    if(query is not None):
        output = {
            "Found": 1,
            "Useremail": query["Useremail"],
        }
    else:
        output = {"Found": 0,
                  "Useremail": "No Login"
                  }
    return output


def updateSession(clientIp):
    query = Sessions.update_one({"ClientIP": clientIp}, {"$set": {
                                "CreatedAt": datetime.datetime.now()}})


def deleteSession(useremail):
    query = Sessions.remove({"Useremail": useremail})
