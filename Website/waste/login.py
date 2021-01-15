
from utilities import *


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
