from utilities import *


@csrf_exempt
def getProductPage(request):
    clientIp = getClientIp(request)
    session = getSession(clientIp)
    updateSession(clientIp)

    pid = request.GET['pid']
    item = getProductData(pid)
    sliderItems = getRandomProducts(10)
    return render(request, "Website/product.html", {"enableLogin": session['Found'], "useremail": session['Useremail'], 'item': item, 'sliderItems': sliderItems})
