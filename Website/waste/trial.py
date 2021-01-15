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
                {'Username': username, "Useremail": useremail, "Password": password, "Cart": {}})
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


@csrf_exempt
def logoutRequest(request):
    clientIp = getClientIp(request)
    session = getSession(clientIp)
    useremail = session['Useremail']

    deleteSession(useremail)
    output = {
        "Found": 1,
        "Message": "Logout Successful"
    }
    return JsonResponse(output)


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


@csrf_exempt
def addToCart(request):
    productID = request.POST['productID']
    clientIp = getClientIp(request)
    session = getSession(clientIp)

    if(session['Found']):
        useremail = session['Useremail']
        query = Users.find_one({"Useremail": useremail})
        cart = query['Cart']
        if(productID not in cart.keys()):
            cart[productID] = 1

        query = Users.update_one({"Useremail": useremail}, {
                                 "$set": {"Cart": cart}})

        output = {
            "Added": 1,
            "Message": "Added to the cart"}
    else:
        output = {
            "Added": 0,
            "Message": "Please login first"}
    return JsonResponse(output)


@csrf_exempt
def showCart(request):
    clientIp = getClientIp(request)
    session = getSession(clientIp)

    if session['Found'] == 1:
        useremail = session["Useremail"]
        query = Users.find_one({"Useremail": useremail})
        cart = query['Cart']
        return getCartPage(request, cart)
    else:
        output = {
            "Added": 0,
            "Message": "Please login first"}
        return JsonResponse(output)


@csrf_exempt
def changeCartValue(request):
    clientIp = getClientIp(request)
    session = getSession(clientIp)
    productID = request.POST["productID"]
    change = 1 if request.POST['change'] == 'inc' else -1

    if(session['Found'] == 1):
        useremail = session['Useremail']
        query = Users.find_one({"Useremail": useremail})
        cart = query['Cart']
        cart[productID] += change

        if cart[productID] == 0:
            cart.pop(productID)

        query = Users.update_one({"Useremail": useremail}, {
                                 "$set": {"Cart": cart}})
        return getCartPage(request, cart)
    else:
        output = {
            "Added": 0,
            "Message": "Please login first"}
        return JsonResponse(output)


def getCartPage(request, cart):
    products = []
    cartEmpty = True
    totalPrice = 0

    if cart:
        cartEmpty = False
        item = {}
        for productID in cart.keys():
            itemData = getProductData(productID)
            item['Name'] = itemData['Name']
            item['ProductID'] = itemData['ProductID']
            item['Price'] = itemData['Price']
            item['Quantity'] = cart[productID]
            totalPrice += item['Price']*item['Quantity']
            products.append(dict(item))

    return render(request, "Website/cart.html", {"products": products, "cartEmpty": cartEmpty, "totalPrice": totalPrice})


@csrf_exempt
def getOrderSummary(request):
    shippingDetails = {}
    shippingDetails['Name'] = request.POST['name']
    shippingDetails['Address'] = request.POST['address']
    shippingDetails['Landmark'] = request.POST['landmark']
    shippingDetails['Pincode'] = request.POST['pincode']
    shippingDetails['PhoneNumber'] = request.POST['phoneNumber']

    clientIp = getClientIp(request)
    session = getSession(clientIp)

    if session['Found'] == 1:
        useremail = session["Useremail"]
        query = Users.find_one({"Useremail": useremail})
        cart = query['Cart']
        products = []
        cartEmpty = True
        totalPrice = 0

        if cart:
            cartEmpty = False
            item = {}
            for productID in cart.keys():
                itemData = getProductData(productID)
                item['Name'] = itemData['Name']
                item['ProductID'] = itemData['ProductID']
                item['Price'] = itemData['Price']
                item['Quantity'] = cart[productID]
                totalPrice += item['Price']*item['Quantity']
                products.append(dict(item))

            query = SiteData.find_one({"Data": "NextOrderID"})
            newOrderID = query["NextOrderID"]
            query = SiteData.update_one({"Data": "NextOrderID"}, {
                                        "$set": {"NextOrderID": newOrderID+1}})

            query = Users.find_one({"Useremail": useremail})
            orders = query['Orders']
            orderData = {"OrderID": newOrderID, "ShippingDetails": shippingDetails, "Products": products,
                         "DateTime": datetime.datetime.now(), "TotalPrice": totalPrice}

            if orders is None:
                orders = []
            orders.append(orderData)

            query = Users.update_one({"Useremail": useremail}, {
                                     "$set": {"Orders": orders, "Cart": {}}})

            return render(request, "Website/order.html", orderData)

        else:
            output = {
                "Added": 0,
                "Message": "Cart is Empty"}
            return JsonResponse(output)
    else:
        output = {
            "Added": 0,
            "Message": "Please login first"}
        return JsonResponse(output)


@csrf_exempt
def getAccountPage(request):
    clientIp = getClientIp(request)
    session = getSession(clientIp)
    if session['Found']:
        useremail = session['Useremail']
        query = Users.find_one({"Useremail": useremail})
        return render(request, "Website/account.html", {"enableLogin": session['Found'], "useremail": session['Useremail'], "found": session['Found'], "userData": query})
    else:
        return render(request, "Website/account.html", {"enableLogin": session['Found'], "useremail": session['Useremail'], "found": session['Found']})


@csrf_exempt
def saveAccountChanges(request):
    clientIp = getClientIp(request)
    session = getSession(clientIp)
    if session['Found']:
        useremail = session['Useremail']
        newUsername = request.POST['newUsername']
        query = Users.update_one({"Useremail": useremail}, {
                                 "$set": {"Username": newUsername}})

        query = Users.find_one({"Useremail": useremail})
        return render(request, "Website/accountTemplate.html", {"found": session['Found'], "userData": query})
    else:
        return render(request, "Website/accountTemplate.html", {"found": session['Found']})


@csrf_exempt
def changePassword(request):
    clientIp = getClientIp(request)
    session = getSession(clientIp)
    if session['Found']:
        useremail = session['Useremail']
        newPassword = request.POST['newPassword']
        query = Users.update_one({"Useremail": useremail}, {
                                 "$set": {"Password": newPassword}})

        query = Users.find_one({"Useremail": useremail})
        return render(request, "Website/accountTemplate.html", {"found": session['Found'], "userData": query})
    else:
        return render(request, "Website/accountTemplate.html", {"found": session['Found']})


@csrf_exempt
def cancelOrder(request):
    clientIp = getClientIp(request)
    session = getSession(clientIp)
    if session['Found']:
        useremail = session['Useremail']
        orderID = request.POST['orderID']
        print(orderID)
        query = Users.find_one({"Useremail": useremail})
        orders = query['Orders']

        for order in orders:
            if(order['OrderID'] == int(orderID)):
                orders.remove(order)
                break

        query = Users.update_one({"Useremail": useremail}, {
                                 "$set": {"Orders": orders}})

        query = Users.find_one({"Useremail": useremail})
        return render(request, "Website/accountTemplate.html", {"found": session['Found'], "userData": query})
    else:
        return render(request, "Website/accountTemplate.html", {"found": session['Found']})
