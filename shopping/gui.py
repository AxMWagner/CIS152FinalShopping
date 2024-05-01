import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk

from .engine.structures import ShoppingCart
from .store_products import csv_to_products


class GUI:
    """
    Shopping cart application GUI.

    Attributes:
        root (tk.Tk): The root window of the application.
        product_tree: Product data structure.
        shopping_cart: Shopping cart instance.
        bg_color (str): Background color for frames.
        text_color (str): Text color for labels and buttons.
    """

    def __init__(self, root):
        """
        Args:
            root (tk.Tk): The root window of the application.
        """
        self.product_tree = csv_to_products()
        self.shopping_cart = ShoppingCart()
        self.root = root
        self.root.title("Shopping Cart")
        self.root.geometry("800x600")  # Set initial window size

        # Define colors
        self.bg_color = "#CCFFFF"
        self.text_color = "#000000"

        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background=self.bg_color, foreground=self.text_color)

        self.create_notebook()
        self.create_cart_widgets()
        self.create_store_widgets()

    def create_notebook(self):
        """Creates the notebook widget."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.store_frame = self.create_frame_with_notebook(self.notebook)
        self.cart_frame = self.create_frame_with_notebook(self.notebook)

        self.notebook.add(self.store_frame, text='Store')
        self.notebook.add(self.cart_frame, text='Cart')

    def create_frame_with_notebook(self, parent):
        """Creates a frame with a notebook inside."""
        frame = ttk.Frame(parent, style="Custom.TFrame")
        notebook = ttk.Notebook(frame)
        notebook.pack(expand=True, fill="both")
        frame.notebook = notebook
        return frame

    def create_store_widgets(self):
        """Creates widgets for store content."""

        self.product_labels = {}
        department_tabs = ttk.Notebook(self.store_frame)
        department_tabs.pack(expand=True, fill="both")

        departments = self.product_tree.get_departments()
        for i, department in enumerate(departments):
            department_frame = ttk.Frame(department_tabs, style="Custom.TFrame")
            department_frame.pack(expand=True, fill="both")
            department_tabs.add(department_frame, text=department)

            category_tabs = ttk.Notebook(department_frame)
            category_tabs.pack(expand=True, fill="both")

            categories = self.product_tree.get_categories(department)
            for j, category in enumerate(categories):
                category_frame = ttk.Frame(category_tabs, style="Custom.TFrame")
                category_frame.pack(expand=True, fill="both", padx=10, pady=5)
                category_tabs.add(category_frame, text=category)

                products = self.product_tree.get_products(department, category)
                for k, (product, details) in enumerate(products.items()):
                    product_frame = ttk.Frame(category_frame, style="Custom.TFrame")
                    product_frame.pack(fill="both", padx=10, pady=5)

                    product_label = ttk.Label(product_frame, text=product, background=self.bg_color,
                                              foreground=self.text_color)
                    product_label.grid(row=0, column=0, sticky="w")

                    price_label = ttk.Label(product_frame, text=f'Price: ${details["price"]}', background=self.bg_color,
                                            foreground=self.text_color)
                    price_label.grid(row=0, column=1, padx=(10, 0), sticky="w")

                    quantity_label = ttk.Label(product_frame, text=f'Quantity: {details["quantity"]}',
                                               background=self.bg_color, foreground=self.text_color)
                    quantity_label.grid(row=0, column=2, padx=(10, 0), sticky="w")

                    add_to_cart_button = ttk.Button(product_frame, text='Add to Cart',
                                                    command=lambda prod=product: self.add_to_cart(prod),
                                                    style="Custom.TButton")
                    add_to_cart_button.grid(row=0, column=3, padx=(10, 0), sticky="e")

                    self.product_labels[product] = quantity_label

    def create_cart_widgets(self):
        """Creates widgets for cart content."""
        self.cart_listbox = tk.Listbox(self.cart_frame, width=50, bg=self.bg_color, fg=self.text_color)
        self.cart_listbox.pack(expand=True, fill="both", padx=10, pady=10)

        self.total_price_label = ttk.Label(self.cart_frame, text="Total Price: ", background=self.bg_color,
                                           foreground=self.text_color)
        self.total_price_label.pack(padx=10, pady=5, anchor="w")

        self.total_quantity_label = ttk.Label(self.cart_frame, text="Total Quantity: ", background=self.bg_color,
                                              foreground=self.text_color)
        self.total_quantity_label.pack(padx=10, pady=5, anchor="w")

        self.checkout_button = ttk.Button(self.cart_frame, text="Checkout", command=self.checkout)
        self.checkout_button.pack(padx=10, pady=5, anchor="w")

        self.remove_from_cart_button = ttk.Button(self.cart_frame, text="Remove Selected",
                                                  command=self.remove_from_cart)
        self.remove_from_cart_button.pack(padx=10, pady=5, anchor="w")

        self.update_total_labels()

    def add_to_cart(self, product):
        """Adds a product to the shopping cart."""
        self.shopping_cart.add_to_cart(product)
        self.decrement_quantity_in_gui(product)
        self.refresh_cart()
        self.update_total_labels()

    def increment_quantity_in_gui(self, product):
        """Increments the quantity of a product displayed in the GUI."""
        if product in self.product_labels:
            current_quantity = int(self.product_labels[product]['text'].split(": ")[1])
            new_quantity = current_quantity + 1
            self.product_labels[product]['text'] = f'Quantity: {new_quantity}'
            product_frame = self.product_labels[product].master
            for child in product_frame.winfo_children():
                child['state'] = 'normal'

    def remove_from_cart(self):
        """Removes the selected product from the shopping cart."""
        try:
            selected_product = self.cart_listbox.get(self.cart_listbox.curselection())
            removed = self.shopping_cart.remove_from_cart(selected_product)
            if removed:
                self.increment_quantity_in_gui(selected_product)
                self.refresh_cart()
                self.update_total_labels()
        except tk.TclError:
            pass

    def decrement_quantity_in_gui(self, product):
        """Decrements the quantity of a product displayed in the GUI."""
        if product in self.product_labels:
            current_quantity = int(self.product_labels[product]['text'].split(": ")[1])
            new_quantity = current_quantity - 1
            self.product_labels[product]['text'] = f'Quantity: {new_quantity}'
            if new_quantity == 0:
                product_frame = self.product_labels[product].master
                for child in product_frame.winfo_children():
                    child['state'] = 'disabled'

    def update_total_labels(self):
        """Updates the total price and total quantity labels."""
        cart_items = self.shopping_cart.get_cart_items()
        total_price = 0
        total_quantity = len(cart_items)  # Count the total number of items in the cart

        for item in cart_items:
            department, category = self.find_department_and_category(item)
            product_details = self.product_tree.get_products(department, category).get(item)
            if product_details:
                total_price += product_details.get('price', 0)

        # Update total price label
        self.total_price_label.config(text=f"Total Price: ${total_price:.2f}")

        # Update total quantity label
        self.total_quantity_label.config(text=f"Total Quantity: {total_quantity}")

        # Handle case when cart is empty
        if total_quantity == 0:
            self.total_price_label.config(text="Total Price: $0.00")
            self.total_quantity_label.config(text="Total Quantity: 0")

    def find_department_and_category(self, item):
        """Finds the department and category of a given product."""
        for department in self.product_tree.get_departments():
            for category in self.product_tree.get_categories(department):
                if item in self.product_tree.get_products(department, category):
                    return department, category
        return None, None

    def refresh_cart(self):
        """Refreshes the cart listbox with updated cart items."""
        self.cart_listbox.delete(0, tk.END)
        cart_items = self.shopping_cart.get_cart_items()
        self.cart_listbox.insert(tk.END, *cart_items)

        # Disable the "Remove from Cart" button if there are no items in the cart
        if not cart_items:
            self.remove_from_cart_button['state'] = 'disabled'
        else:
            self.remove_from_cart_button['state'] = 'normal'

    def checkout(self):
        """Checkout method for the shopping cart."""
        # Clear the cart
        self.shopping_cart.clear_cart()

        # Update the cart GUI
        self.refresh_cart()

        # Reset total price and total quantity labels to 0
        self.total_price_label.config(text="Total Price: $0.00")
        self.total_quantity_label.config(text="Total Quantity: 0")

        # Display popup message
        messagebox.showinfo("Checkout Successful", "Your items have been checked out.")


def start():
    """Starts the shopping cart application."""
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
