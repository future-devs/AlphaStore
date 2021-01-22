from django.test import TestCase
from Website import views
import random

# Create your tests here.

class WebsiteTestCase(TestCase):
    
    def test_get_random_products(self):
        count = 1
        result = views.getRandomProducts(count)
        self.assertNotEqual(result, None)
        self.assertEqual(str(type(result)), "<class 'list'>")
        self.assertEqual(len(result), count)
        self.assertNotEqual(len(result), 0)
    
    def test_get_random_category_products(self):
        category = "Clothing"
        count = 1
        result = views.getRandomCategoryProducts(category, count)
        self.assertNotEqual(result, None)
        self.assertEqual(str(type(result)), "<class 'list'>")
        self.assertEqual(len(result), count)
        self.assertNotEqual(len(result), 0)
    
    def test_get_product_data(self):
        result = views.getProductData('P19')
        self.assertNotEqual(result, None)
        self.assertEqual(result['Availability'], 'Available')
        self.assertEqual(result['Category'], 'Clothing')
        self.assertEqual(result['Name'], 'Blue Denim')
        self.assertEqual(result['Price'], 418.0)

    def test_get_category_data(self):
        result = views.getCategoryData('Clothing')
        self.assertNotEqual(result, None)
        self.assertEqual(str(type(result)), "<class 'list'>")
        self.assertNotEqual(len(result), 0)
    

