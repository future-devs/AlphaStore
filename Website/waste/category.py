from utilities import *


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
