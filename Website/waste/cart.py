from Website.utilities import *


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
