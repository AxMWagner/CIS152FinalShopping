import csv
import os

from .engine.structures import ProductTree


def csv_to_products():
    product_tree = ProductTree()
    csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'StoreDatabase.csv')
    with open(csv_file_path, 'r', encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            department, category, product = row.get('Department'), row.get('Category'), row.get('Product')
            price = float(row.get('Price', '0').replace(',', ''))
            quantity = int(row.get('Quantity', '0'))

            product_tree.add_product(department, category, product, price, quantity)
    return product_tree
