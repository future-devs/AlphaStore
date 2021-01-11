from django.test import TestCase
from Warehouse import views
import json
# Create your tests here.

class ProductsTestCase(TestCase):
    def test_get_all_products(self):
        response = views.getAllProducts("sample")
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertNotEqual(json.loads(response.content), None)
        self.assertNotEqual(response_content['result'], None)
        self.assertEqual(response_content['result'][0]['ProductID'], 'P19')
        self.assertEqual(response_content['result'][0]['Availability'], 'Available')

    def test_get_all_products(self):
        response = views.getProductData("sample", "P19")
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertNotEqual(json.loads(response.content), None)
        self.assertNotEqual(response_content['result'], None)
        self.assertEqual(response_content['result']['ProductID'], 'P19')
        self.assertEqual(response_content['result']['Availability'], 'Available')
        self.assertEqual(response_content['result']['Category'], 'Clothing')
        self.assertEqual(response_content['result']['Quantity'], 50)
        self.assertEqual(response_content['result']['Name'], 'Blue Denim')

    def test_get_details(self):
        response = views.getDetails("sample")
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertNotEqual(json.loads(response.content), None)
        self.assertNotEqual(response_content['result'], None)
        self.assertEqual(response_content['result']['Name'], 'Alpha Store Warehouse')
        self.assertEqual(response_content['result']['Address'], 'Mumbai')
        self.assertEqual(response_content['result']['Email'], 'alphastore@gmail.com')
    
    def test_warehouse_home(self):
        self.assertEqual(views.warehouseHome('request').status_code, 200)
    
    def test_warehouse_test(self):
        self.assertEqual(views.warehouseTest('request').status_code, 200)

    

