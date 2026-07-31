# ==========================================================
# Online Shopping and Order Processing System
# Developed using Python Object-Oriented Programming (OOP)
#
# Features:
# - Product Management
# - Inventory Management
# - Shopping Cart
# - Customer Discounts
# - Billing with GST
# - Payment Validation
# ==========================================================


# ---------------------- Product Class ----------------------
# Represents a product available in the inventory.
# Demonstrates Encapsulation using private attributes
# (__price and __stock).
class Product:

    # Constructor to initialize product details
    def __init__(self, pid, name, category, price, stock):
        self.pid = pid
        self.name = name
        self.category = category
        self.__price = price
        self.__stock = stock

    # Returns the product price
    def get_price(self):
        return self.__price

    # Returns available stock
    def get_stock(self):
        return self.__stock

    # Reduces stock after purchase
    def reduce_stock(self, qty):
        if qty > self.__stock:
            raise Exception("Out of Stock!")
        self.__stock -= qty

    # Increases stock when items are removed from cart
    def increase_stock(self, qty):
        self.__stock += qty

    # Returns formatted product information
    def __str__(self):
        return f"{self.pid} | {self.name} | {self.category} | ₹{self.__price} | Stock:{self.__stock}"


# ---------------------- Inventory Class ----------------------
# Stores and manages all available products.
class Inventory:

    # Dictionary stores products using Product ID as key
    def __init__(self):
        self.products = {}

    # Adds a new product into inventory
    def add_product(self, product):
        if product.pid in self.products:
            raise Exception("Duplicate Product ID")
        self.products[product.pid] = product

    # Searches product using Product ID
    def search(self, pid):
        if pid not in self.products:
            raise Exception("Product Not Found")
        return self.products[pid]

    # Displays all products sorted by price
    def display_products(self):
        print("\nAvailable Products")
        print("-" * 50)

        # Lambda function sorts products based on price
        for p in sorted(self.products.values(),
                        key=lambda x: x.get_price()):
            print(p)


# ---------------------- Cart Class ----------------------
# Handles shopping cart operations.
class Cart:

    # Dictionary stores cart items
    def __init__(self):
        self.items = {}

    # Adds product into cart
    def add_item(self, product, qty):

        # Quantity validation
        if qty <= 0:
            raise Exception("Invalid Quantity")

        # Stock validation
        if qty > product.get_stock():
            raise Exception("Out of Stock")

        # Reduce inventory stock
        product.reduce_stock(qty)

        # If product already exists, increase quantity
        if product.pid in self.items:
            self.items[product.pid]["qty"] += qty

        # Otherwise create a new cart entry
        else:
            self.items[product.pid] = {
                "product": product,
                "qty": qty
            }

    # Removes product from cart
    def remove_item(self, pid):

        if pid not in self.items:
            raise Exception("Product not in Cart")

        # Restore stock back to inventory
        item = self.items.pop(pid)
        item["product"].increase_stock(item["qty"])

    # Updates quantity of an existing cart item
    def update_quantity(self, pid, new_qty):

        if pid not in self.items:
            raise Exception("Product not in Cart")

        if new_qty <= 0:
            raise Exception("Invalid Quantity")

        item = self.items[pid]
        product = item["product"]

        old_qty = item["qty"]

        # If quantity increased, reduce inventory stock
        if new_qty > old_qty:
            diff = new_qty - old_qty
            product.reduce_stock(diff)

        # If quantity decreased, restore inventory stock
        elif new_qty < old_qty:
            diff = old_qty - new_qty
            product.increase_stock(diff)

        item["qty"] = new_qty


# ---------------------- Customer Classes ----------------------
# Base class demonstrating Polymorphism.
# Different customer types override the discount() method.

class Customer:

    # Default customer gets no discount
    def discount(self, total):
        return 0


# Regular Customer receives 5% discount
class RegularCustomer(Customer):

    def discount(self, total):
        return total * 0.05


# Premium Customer receives 10% discount
class PremiumCustomer(Customer):

    def discount(self, total):
        return total * 0.10


# VIP Customer receives 20% discount
class VIPCustomer(Customer):

    def discount(self, total):
        return total * 0.20


# ---------------------- Billing Class ----------------------
# Generates invoice and calculates GST.
class Billing:

    # GST is common for all bills (Class Variable)
    GST = 0.18

    # Static method because billing does not depend
    # on Billing class objects.
    @staticmethod
    def generate(cart, customer):

        subtotal = 0

        print("\n============== INVOICE ==============")
        print(f"{'Product':15}{'Qty':5}{'Price':10}{'Total'}")

        # Calculate total amount for each cart item
        for item in cart.items.values():

            p = item["product"]
            qty = item["qty"]
            amount = qty * p.get_price()

            subtotal += amount

            print(f"{p.name:15}{qty:<5}{p.get_price():<10}{amount}")

        # Apply customer-specific discount
        discount = customer.discount(subtotal)

        # Amount after discount
        after_discount = subtotal - discount

        # GST calculation
        gst = after_discount * Billing.GST

        # Final payable amount
        final = after_discount + gst

        print("-" * 40)
        print("Subtotal :", subtotal)
        print("Discount :", discount)
        print("GST (18%):", round(gst, 2))
        print("Final Bill:", round(final, 2))
        print("Savings:", discount)

        return final


# ==========================================================
#                     Main Program
# ==========================================================

# Create inventory object
inventory = Inventory()

# Add sample products into inventory
inventory.add_product(Product(101, "Laptop", "Electronics", 60000, 5))
inventory.add_product(Product(102, "Phone", "Electronics", 30000, 10))
inventory.add_product(Product(103, "Shoes", "Fashion", 2000, 15))
inventory.add_product(Product(104, "Watch", "Accessories", 5000, 8))

# Display all available products
inventory.display_products()

# Create shopping cart
cart = Cart()

# Add products into cart
try:
    cart.add_item(inventory.search(101), 1)
    cart.add_item(inventory.search(103), 2)
    cart.add_item(inventory.search(104), 1)

# Handle cart-related exceptions
except Exception as e:
    print(e)

# Create Premium customer
customer = PremiumCustomer()

# Generate invoice
amount = Billing.generate(cart, customer)

# Payment processing
try:
    payment = float(input("\nEnter Payment Amount: "))

    # Validate payment amount
    if payment < amount:
        raise Exception("Insufficient Payment")

    # Display remaining balance
    print("Balance:", round(payment - amount, 2))

# Handle invalid numeric input
except ValueError:
    print("Invalid Amount")

# Handle insufficient payment
except Exception as e:
    print(e)
