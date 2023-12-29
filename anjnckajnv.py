import streamlit as st
import stripe

# Set your Stripe API key
stripe.api_key = "your_stripe_secret_key"

# Sample product data with image URLs
products = [
    {"name": "Apple", "price": 10.99, "category": "Fruits", "image_url": "https://example.com/apple.jpg"},
    {"name": "Banana", "price": 19.99, "category": "Fruits", "image_url": "https://example.com/banana.jpg"},
    {"name": "Cherry", "price": 5.99, "category": "Fruits", "image_url": "https://example.com/cherry.jpg"},
    {"name": "Laptop", "price": 999.99, "category": "Electronics", "image_url": "https://example.com/laptop.jpg"},
]

# Shopping cart to keep track of selected items
shopping_cart = []

# Streamlit app
def main():
    st.set_page_config(page_title="Shop Swiftly", page_icon="🛒")

    st.title("Welcome to Shop Swiftly!")

    # Display product categories
    categories = set(product["category"] for product in products)
    selected_category = st.selectbox("Select Category", ["All"] + list(categories))

    # Search functionality
    search_term = st.text_input("Search for products:")
    filtered_products = filter_products(products, selected_category, search_term)

    # Display products based on category and search term
    st.header("Products")

    selected_items = []
    for product in filtered_products:
        col1, col2, col3 = st.columns([1, 1, 3])  # Adjust the column ratios based on your preference
        quantity = col1.number_input(f"Quantity for {product['name']} (${product['price']:.2f} each)", value=1, min_value=1, step=1)
        
        # Display product image
        col2.image(product["image_url"], caption=product["name"], use_column_width=True)

        if quantity > 0:
            selected_items.extend([product.copy() for _ in range(int(quantity))])

    # Add selected items to the cart
    if st.button("Add Selected Items to Cart", key="add_to_cart") and selected_items:
        for item in selected_items:
            add_item_to_cart(item)
            st.success(f"{item['name']} (Price: ${item['price']:.2f}) added to cart!")

    # Display shopping cart
    st.header("Shopping Cart")

    if not shopping_cart:
        st.warning("Your cart is empty.")
    else:
        total_cost = sum(item["price"] * item["quantity"] for item in shopping_cart)
        with st.expander("View Cart Details"):
            st.write("### Cart Items:")
            for item in shopping_cart:
                st.markdown(f"- {item['name']} (Quantity: {item['quantity']}, Total: ${item['price'] * item['quantity']:.2f})")
            st.write(f"### Total Cost: ${total_cost:.2f}")

            # Checkout button for payment
            if st.button("Checkout", key="checkout"):
                handle_payment(total_cost)

def filter_products(products, selected_category, search_term):
    filtered_products = []
    for product in products:
        category_match = selected_category == "All" or product["category"] == selected_category
        search_match = search_term.lower() in product["name"].lower()
        if category_match and search_match:
            filtered_products.append(product)
    return filtered_products

def add_item_to_cart(product):
    # Check if the item is already in the cart
    for item in shopping_cart:
        if item["name"] == product["name"]:
            item["quantity"] += 1
            return

    # If not, add the item to the cart with the specified quantity
    shopping_cart.append({"name": product["name"], "price": product["price"], "quantity": 1, "image_url": product["image_url"]})

def handle_payment(amount):
    # For simplicity, this is a dummy payment confirmation
    # In a real application, you would use the Stripe API for payment processing
    st.success(f"Payment Successful! Amount: ${amount:.2f}")

if __name__ == "__main__":
    main()
