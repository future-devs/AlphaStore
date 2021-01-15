from Website.utilities import *


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
