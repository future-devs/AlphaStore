from utilities import *


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
