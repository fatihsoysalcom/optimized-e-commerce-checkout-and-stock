import time
import random

class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

class InventoryManager:
    def __init__(self):
        # Simulate a database of products
        self.products = {
            1: Product(1, "Laptop", 1200.00, 50),
            2: Product(2, "Keyboard", 75.00, 150),
            3: Product(3, "Mouse", 25.00, 200),
            4: Product(4, "Monitor", 300.00, 30)
        }

    def get_product(self, product_id):
        # Simulate fast product retrieval
        time.sleep(0.01) # Minimal delay for simulation
        return self.products.get(product_id)

    def update_stock(self, product_id, quantity_change):
        # Simulate atomic stock update
        product = self.get_product(product_id)
        if product:
            # Simulate a lock or transaction for stock update
            time.sleep(0.02)
            if product.stock + quantity_change >= 0:
                product.stock += quantity_change
                print(f"Stock updated for {product.name}: {product.stock} remaining.")
                return True
            else:
                print(f"Insufficient stock for {product.name}.")
                return False
        return False

class PaymentGateway:
    def process_payment(self, amount, payment_details):
        # Simulate fast payment processing
        time.sleep(0.05) # Simulate network latency and processing
        print(f"Payment of ${amount:.2f} processed successfully.")
        return True

class EcommerceService:
    def __init__(self):
        self.inventory_manager = InventoryManager()
        self.payment_gateway = PaymentGateway()

    def checkout(self, cart_items, payment_details):
        # cart_items is a list of (product_id, quantity)
        total_amount = 0
        
        # --- Fast Checkout Optimization: Pre-check stock and calculate total first ---
        pre_order_items = []
        for product_id, quantity in cart_items:
            product = self.inventory_manager.get_product(product_id)
            if not product:
                print(f"Error: Product ID {product_id} not found.")
                return False
            if product.stock < quantity:
                print(f"Error: Insufficient stock for {product.name}. Available: {product.stock}, Requested: {quantity}")
                return False
            total_amount += product.price * quantity
            pre_order_items.append((product_id, quantity, product.name))

        # --- Fast Checkout Optimization: Process payment before stock update ---
        # This reduces the time the user waits for payment confirmation
        if self.payment_gateway.process_payment(total_amount, payment_details):
            # --- Stock Management: Update stock only after successful payment ---
            for product_id, quantity, product_name in pre_order_items:
                self.inventory_manager.update_stock(product_id, -quantity)
            print("Checkout complete!")
            return True
        else:
            print("Payment failed. Checkout aborted.")
            return False

# --- Example Usage ---
if __name__ == "__main__":
    ecommerce_service = EcommerceService()

    # Simulate a customer's cart
    customer_cart = [
        (1, 1), # 1 Laptop
        (2, 2)  # 2 Keyboards
    ]
    
    payment_info = {
        "card_number": "**** **** **** 1234",
        "expiry": "12/25",
        "cvv": "***"
    }

    print("Starting checkout process...")
    start_time = time.time()
    success = ecommerce_service.checkout(customer_cart, payment_info)
    end_time = time.time()

    if success:
        print(f"Checkout took {end_time - start_time:.2f} seconds.")
    else:
        print("Checkout failed.")

    print("\nAttempting to checkout with insufficient stock:")
    customer_cart_low_stock = [
        (4, 35) # Requesting 35 monitors, only 30 available
    ]
    ecommerce_service.checkout(customer_cart_low_stock, payment_info)
