from utilities import *


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
