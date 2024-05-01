class CartItem:
    """
    This class represents an item in the shopping cart.

    :param product: The product in the cart item.
    :type product: str, optional
    """

    def __init__(self, product=None):
        """
        This is where we set up the cart item.

        :param product: The product in the cart item.
        :type product: str, optional
        """

        self.product = product
        self.next = None


class ProductNode:
    """
    This class represents a product.

    :param name: The product's name.
    :type name: str
    :param price: The product's price.
    :type price: float, optional
    :param quantity: The product's quantity.
    :type quantity: int, optional
    """

    def __init__(self, name, price=None, quantity=None):
        """
        This is where we set up the product.

        :param name: The product's name.
        :type name: str
        :param price: The product's price.
        :type price: float, optional
        :param quantity: The product's quantity.
        :type quantity: int, optional
        """

        self.name = name
        self.price = price
        self.quantity = quantity
        self.subcategories = []