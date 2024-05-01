from .nodes import CartItem, ProductNode


class ShoppingCart:
    """
    This class represents a Shopping Cart.

    :param first_item: The first item in the shopping cart.
    :type first_item: CartItem, optional
    """

    def __init__(self):
        """
        Initializes an empty shopping cart.
        """
        self.first_item = None

    def is_empty(self):
        """
        Checks if the shopping cart is empty.

        :return: True if the shopping cart is empty, False otherwise.
        :rtype: bool
        """
        return self.first_item is None

    def add_to_cart(self, item):
        """
        Adds an item to the shopping cart.

        :param item: The item to be added to the shopping cart.
        :type item: str
        """
        new_item = CartItem(item)
        if self.is_empty():
            self.first_item = new_item
        else:
            current_item = self.first_item
            while current_item.next:
                current_item = current_item.next
            current_item.next = new_item


    def remove_from_cart(self, item):
        """ Removes an item from the shopping cart.

        :param item: The item to be removed from the shopping cart.
        :type item: str
        :return: True if the item was successfully removed, False otherwise.
        :rtype: bool
        """
        current_item = self.first_item
        previous_item = None
        while current_item:
            if current_item.product == item:
                if previous_item:
                    previous_item.next = current_item.next
                else:
                    self.first_item = current_item.next
                return True
            previous_item, current_item = current_item, current_item.next
        return False

    def get_cart_items(self):
        """
        Returns a list of all items in the shopping cart.

        :return: A list of all items in the shopping cart.
        :rtype: list
        """
        items = []
        current = self.first_item
        while current:
            items.append(current.product)
            current = current.next
        return items

    def clear_cart(self):
        """
        Clears all items from the shopping cart.
        """
        self.first_item = None


class ProductTree:
    """
    This class represents a product tree in a store. It allows for adding and removing products,
    and retrieving information about the products in the store.
    """

    def __init__(self):
        """
        Initializes a new product tree with a root node named 'store'.
        """
        self.store = ProductNode('store')

    def add_product(self, department, category, product, price, quantity):
        """
        Adds a product to the product tree under the specified department and category.

        :param department: The department under which the product is to be added.
        :type department: str
        :param category: The category under which the product is to be added.
        :type category: str
        :param product: The name of the product to be added.
        :type product: str
        :param price: The price of the product.
        :type price: float
        :param quantity: The quantity of the product.
        :type quantity: int
        """
        department_node = self.get_or_create_node(self.store, department)
        category_node = self.get_or_create_node(department_node, category)

        for p_node in category_node.subcategories:
            if p_node.name == product:
                p_node.price, p_node.quantity = price, quantity
                break
        else:
            category_node.subcategories.append(ProductNode(product, price, quantity))

    def remove_product(self, department, category, product):
        """
        Removes a product from the product tree under the specified department and category.

        :param department: The department under which the product is to be removed.
        :type department: str
        :param category: The category under which the product is to be removed.
        :type category: str
        :param product: The name of the product to be removed.
        :type product: str
        """
        department_node = self.get_or_create_node(self.store, department)
        category_node = self.get_or_create_node(department_node, category)

        for p_node in category_node.subcategories:
            if p_node.name == product:
                p_node.quantity -= 1 if p_node.quantity > 0 else print(f"No more {product} available in stock.")
                break
        else:
            print(f"{product} not found in the inventory.")

    def get_or_create_node(self, parent, name):
        """
        Retrieves a node with the specified name under the given parent node.
        If no such node exists, a new node is created.

        :param parent: The parent node under which to look for the node.
        :type parent: ProductNode
        :param name: The name of the node to retrieve or create.
        :type name: str
        :return: The node with the specified name.
        :rtype: ProductNode
        """
        for child in parent.subcategories:
            if child.name == name:
                return child
        new_node = ProductNode(name)
        parent.subcategories.append(new_node)
        return new_node

    def print_tree(self, node=None, indent=0):
        """
        Prints the product tree starting from the specified node.

        :param node: The node from which to start printing the tree. If None, the root node is used.
        :type node: ProductNode, optional
        :param indent: The number of spaces to use for indentation.
        :type indent: int
        :return: A string representation of the product tree.
        :rtype: str
        """
        if node is None:
            node = self.store
        tree_str = '  ' * indent + '- ' + (node.name if node.name else 'Unnamed') + '\n'
        if node.price is not None:
            tree_str += '  ' * (indent + 1) + '- Price: ${:.2f}\n'.format(node.price)
            tree_str += '  ' * (indent + 1) + '- Quantity: {}\n'.format(node.quantity)
        for child in node.subcategories:
            tree_str += self.print_tree(child, indent + 1)
        return tree_str

    def get_departments(self):
        """
        Retrieves the names of all departments in the store.

        :return: A list of department names.
        :rtype: list
        """
        return [child.name for child in self.store.subcategories]

    def get_categories(self, department):
        """
        Retrieves the names of all categories under the specified department.

        :param department: The department under which to look for categories.
        :type department: str
        :return: A list of category names.
        :rtype: list
        """
        department_node = self.get_or_create_node(self.store, department)
        return [child.name for child in department_node.subcategories]

    def get_products(self, department, category):
        """
        Retrieves all products under the specified department and category, along with their prices and quantities.

        :param department: The department under which to look for products.
        :type department: str
        :param category: The category under which to look for products.
        :type category: str
        :return: A dictionary where the keys are product names and the values are dictionaries with keys 'price' and
        'quantity'.
        :rtype: dict
        """
        department_node = self.get_or_create_node(self.store, department)
        category_node = self.get_or_create_node(department_node, category)

        products = {}
        for product_node in category_node.subcategories:
            products[product_node.name] = {
                "price": product_node.price,
                "quantity": product_node.quantity
            }

        return products
