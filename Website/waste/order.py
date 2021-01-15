from utilities import *


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
