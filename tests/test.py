import unittest
from unittest.mock import patch

import shopping
from shopping.gui import GUI


class TestNode(unittest.TestCase):
    def test_node_creation_data(self):
        node = shopping.engine.nodes.CartItem(10)
        self.assertEqual(node.product, 10)

    def test_node_creation_next(self):
        node = shopping.engine.nodes.CartItem()
        self.assertIsNone(node.next)

    def test_node_next_pointer(self):
        node1 = shopping.engine.nodes.CartItem(10)
        node2 = shopping.engine.nodes.CartItem(20)
        node1.next = node2
        self.assertEqual(node1.next, node2)


class TestProductNode(unittest.TestCase):
    def test_product_node_creation_name(self):
        product_node = shopping.engine.nodes.ProductNode("Test Product")
        self.assertEqual(product_node.name, "Test Product")

    def test_product_node_creation_price(self):
        product_node = shopping.engine.nodes.ProductNode("Test", price=10.99)
        self.assertEqual(product_node.price, 10.99)

    def test_product_node_creation_quantity(self):
        product_node = shopping.engine.nodes.ProductNode("Test", quantity=5)
        self.assertEqual(product_node.quantity, 5)

    def test_product_node_creation_children(self):
        product_node = shopping.engine.nodes.ProductNode("Test")
        self.assertEqual(product_node.subcategories, [])


class TestProductTree(unittest.TestCase):
    def setUp(self):
        self.tree = shopping.engine.structures.ProductTree()

    def test_add_product_creates_department_node(self):
        self.tree.add_product('Electronics', 'Laptops', 'MacBook', 2000, 10)
        self.assertEqual(len(self.tree.store.subcategories), 1)

    def test_add_product_creates_category_node(self):
        self.tree.add_product('Electronics', 'Laptops', 'MacBook', 2000, 10)
        self.assertEqual(len(self.tree.store.subcategories[0].subcategories), 1)

    def test_add_product_creates_product_node(self):
        self.tree.add_product('Electronics', 'Laptops', 'MacBook', 2000, 10)
        self.assertEqual(self.tree.store.subcategories[0].subcategories[0].name, 'Laptops')


class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.cart = shopping.engine.structures.ShoppingCart()

    def test_add_to_cart_not_empty(self):
        self.cart.add_to_cart("Item 1")
        self.assertFalse(self.cart.is_empty())

    def test_add_to_cart_items(self):
        self.cart.add_to_cart("Item 1")
        self.assertEqual(self.cart.get_cart_items(), ["Item 1"])

    def test_remove_from_cart(self):
        self.cart.add_to_cart("Item 1")
        self.cart.add_to_cart("Item 2")
        self.cart.remove_from_cart("Item 1")
        self.assertEqual(self.cart.get_cart_items(), ["Item 2"])

    def test_get_cart_items(self):
        self.cart.add_to_cart("Item 1")
        self.cart.add_to_cart("Item 2")
        self.cart.add_to_cart("Item 3")
        self.assertEqual(self.cart.get_cart_items(), ["Item 1", "Item 2", "Item 3"])


class GUI(unittest.TestCase):
    @patch('tkinter.Tk')
    @patch('shopping.gui.csv_to_products')
    @patch('shopping.gui.ShoppingCart')
    def gui_initialization(self, mock_tk, mock_csv_to_products, mock_shopping_cart):
        gui = GUI(mock_tk)
        self.assertIsNotNone(gui)

    @patch('tkinter.Tk')
    @patch('shopping.gui.csv_to_products')
    @patch('shopping.gui.ShoppingCart')
    def add_to_cart_updates_cart(self, mock_tk, mock_csv_to_products, mock_shopping_cart):
        gui = GUI(mock_tk)
        gui.add_to_cart('product')
        gui.shopping_cart.add_to_cart.assert_called_with('product')

    @patch('tkinter.Tk')
    @patch('shopping.gui.csv_to_products')
    @patch('shopping.gui.ShoppingCart')
    def checkout_clears_cart(self, mock_tk, mock_csv_to_products, mock_shopping_cart):
        gui = GUI(mock_tk)
        gui.checkout()
        gui.shopping_cart.clear_cart.assert_called()


if __name__ == "__main__":
    unittest.main()
