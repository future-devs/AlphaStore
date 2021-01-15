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


@csrf_exempt
def index(request):
    clientIp = getClientIp(request)
    session = getSession(clientIp)
    updateSession(clientIp)

    sliderItems = getRandomProducts(10)
    clothingItems = getRandomCategoryProducts('Clothing', 5)
    accessoriesItems = getRandomCategoryProducts('Accessories', 5)
    productsItems = getRandomCategoryProducts('Products', 5)
    otherItems = getRandomCategoryProducts('Other', 5)
    return render(request, "Website/index.html", {"enableLogin": session['Found'], "useremail": session['Useremail'], "sliderItems": sliderItems, "clothingItems": clothingItems, "accessoriesItems": accessoriesItems, "productItems": productsItems, "otherItems": otherItems})


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


@csrf_exempt
def getProductPage(request):
    clientIp = getClientIp(request)
    session = getSession(clientIp)
    updateSession(clientIp)

    pid = request.GET['pid']
    item = getProductData(pid)
    sliderItems = getRandomProducts(10)
    return render(request, "Website/product.html", {"enableLogin": session['Found'], "useremail": session['Useremail'], 'item': item, 'sliderItems': sliderItems})


def getProductData(pid):
    queryObj = {'ProductID': pid}
    query = Products.find_one(queryObj)
    return query


@csrf_exempt
def getCategoryPage(request):
    clientIp = getClientIp(request)
    session = getSession(clientIp)
    updateSession(clientIp)

    category = request.GET['category']
    items = getCategoryData(category)
    sliderItems = getRandomProducts(10)
    return render(request, 'Website/category.html', {"enableLogin": session['Found'], "useremail": session['Useremail'], "category": category, "items": items, 'sliderItems': sliderItems, "numOfItems": len(items)})


def getCategoryData(category):
    queryObj = {'Category': category}
    query = Products.find(queryObj)
    output = []
    for x in query:
        item = {}
        if x['ImageURLs']:
            item['ImageURL'] = x['ImageURLs'][0]
        else:
            item['ImageURL'] = ""
        item['Name'] = x['Name']
        item['ProductURL'] = 'product?pid='+x['ProductID']
        output.append(item)
    return output


@csrf_exempt
def getTagPage(request):
    clientIp = getClientIp(request)
    session = getSession(clientIp)
    updateSession(clientIp)

    query = request.GET['query']
    tags = query.split(" ")
    items = getTagData(tags)
    sliderItems = getRandomProducts(10)
    return render(request, 'Website/tag.html', {"enableLogin": session['Found'], "useremail": session['Useremail'], "searchTag": query, "items": items, 'sliderItems': sliderItems, "numOfItems": len(items)})


def getTagData(tags):
    output = []
    for x in range(0, len(tags)):
        tags[x] = tags[x].upper()

    queryObj = {'Tags': {"$in": tags}}
    query = Products.find(queryObj)

    for x in query:
        item = {}
        if x['ImageURLs']:
            item['ImageURL'] = x['ImageURLs'][0]
        else:
            item['ImageURL'] = ""
        item['Name'] = x['Name']
        item['ProductURL'] = 'product?pid='+x['ProductID']
        output.append(item)
    return output


@csrf_exempt
def signupRequest(request):
    username = request.POST['username']
    useremail = request.POST['useremail'].lower()
    password = request.POST['password']

    if(username == "" or useremail == "" or password == ""):
        output = {
            'message': "Enter All Details"
        }
    else:
        query = Users.find_one({'Useremail': useremail})

        if query is not None:
            output = {
                'message': "User Already Exist"
            }
        else:
            query = Users.insert_one(
                {'Username': username, "Useremail": useremail, "Password": password, "Cart": {}, "Orders": []})
            output = {
                'message': "User Registered Successfully"
            }
    return JsonResponse(output)


@csrf_exempt
def loginRequest(request):
    useremail = request.POST['useremail'].lower()
    password = request.POST['password']

    if(useremail == "" or password == ""):
        output = {
            'message': "Enter All Details",
            'data': None
        }
    else:
        query = Users.find_one({'Useremail': useremail})
        if query is None:
            output = {
                "message": "User Does Not Exist",
                "data": None
            }
        elif(query['Password'] != password):
            output = {
                'message': "Wrong Password",
                "data": None
            }
        else:
            clientIp = getClientIp(request)
            createSession(useremail, clientIp)
            session = getSession(clientIp)
            return render(request, "Website/header.html", {"enableLogin": session['Found'], "useremail": session['Useremail']})
    return JsonResponse(output)