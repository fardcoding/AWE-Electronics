from flask import Blueprint, render_template, request, redirect, session, flash
from app.globals import (
    users, products, orders, reviews,
    save_all_users, save_all_products, save_all_reviews, save_all_orders
)
from app.models.order import Order
from app.models.review import Review
from interfaces.card_payment import CardPayment
from interfaces.paypal_payment import PayPalPayment
from app.utils.decorators import login_required  # ✅ Decorator import

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/catalogue')
@login_required
def catalogue():
    return render_template('catalogue.html', products=products, reviews=reviews)

@customer_bp.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    user_id = session['user_id']
    product_id = int(request.form['product_id'])
    customer = next((u for u in users if u.id == user_id), None)
    if customer:
        customer.add_to_cart(product_id)
        save_all_users()
        flash("Product added to cart!", "success")
    else:
        flash("User not found!", "danger")
    return redirect('/catalogue')

@customer_bp.route('/cart')
@login_required
def view_cart():
    customer = next((u for u in users if u.id == session['user_id']), None)
    if not customer:
        flash("User not found.", "danger")
        return redirect('/login')

    cart_items = []
    total = 0
    for product_id in customer.cart:
        product = next((p for p in products if p.id == product_id), None)
        if product:
            cart_items.append(product)
            total += product.price

    return render_template('cart.html', cart_items=cart_items, total=total)

@customer_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    customer = next((u for u in users if u.id == session['user_id']), None)
    if not customer or not customer.cart:
        flash("Cart is empty or user not found.", "danger")
        return redirect('/cart')

    product_ids = customer.cart
    total = 0
    for pid in product_ids:
        product = next((p for p in products if p.id == pid), None)
        if product:
            total += product.price
            product.stock -= 1

    method = request.form.get('payment_method')
    if method == 'card':
        payment = CardPayment(card_number='1234', cvv='123', expiry='12/25')
    elif method == 'paypal':
        payment = PayPalPayment(email=customer.email)
    else:
        flash("Invalid payment method selected.", "danger")
        return redirect('/cart')

    if not payment.pay(total):
        flash("Payment failed. Try again.", "danger")
        return redirect('/cart')

    order = Order(
        id=len(orders) + 1,
        customer_id=customer.id,
        product_ids=product_ids.copy(),
        total_amount=total
    )
    orders.append(order)
    customer.cart.clear()
    if order.id not in customer.order_history:
        customer.order_history.append(order.id)

    save_all_orders()
    save_all_products()
    save_all_users()

    flash("Order placed successfully!", "success")
    return render_template('order_confirmation.html', order=order)

@customer_bp.route('/orders')
@login_required
def order_history():
    if 'user_id' not in session:
        flash("Please log in to view order history.", "warning")
        return redirect('/login')

    customer = next((u for u in users if u.id == session.get('user_id')), None)
    if not customer:
        flash("User not found.", "danger")
        return redirect('/login')

    # ✅ ONLY show the orders this customer placed
    user_orders = [o for o in orders if o.customer_id == customer.id]

    return render_template('order_history.html', orders=user_orders)

@customer_bp.route('/review/<int:product_id>', methods=['GET', 'POST'])
@login_required
def submit_review(product_id):
    customer = next((u for u in users if u.id == session['user_id']), None)
    if not customer:
        flash("User not found.", "danger")
        return redirect('/catalogue')

    ordered_product_ids = []
    for order_id in customer.order_history:
        order = next((o for o in orders if o.id == order_id), None)
        if order:
            ordered_product_ids.extend(order.product_ids)

    if product_id not in ordered_product_ids:
        flash("You can only review products you've purchased.", "danger")
        return redirect('/catalogue')

    if request.method == 'POST':
        rating = int(request.form['rating'])
        comment = request.form['comment']
        review = Review(
            id=len(reviews) + 1,
            product_id=product_id,
            customer_id=customer.id,
            rating=rating,
            comment=comment
        )
        reviews.append(review)
        save_all_reviews()
        flash("Review submitted successfully!", "success")
        return redirect('/catalogue')

    return render_template('submit_review.html', product_id=product_id)

@customer_bp.route('/profile')
@login_required
def profile():
    if session.get('user_email') == 'admin@awestore.com':
        flash("Admin does not have a profile.", "warning")
        return redirect('/admin/products')

    customer = next((u for u in users if u.id == session['user_id']), None)
    if not customer:
        flash("User not found.", "danger")
        return redirect('/login')

    return render_template('profile.html', user=customer)

@customer_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if session.get('user_email') == 'admin@awestore.com':
        flash("Admin profile cannot be edited.", "warning")
        return redirect('/admin/products')

    customer = next((u for u in users if u.id == session['user_id']), None)
    if not customer:
        flash("User not found.", "danger")
        return redirect('/login')

    if request.method == 'POST':
        customer.name = request.form['name']
        customer.address = request.form['address']
        save_all_users()
        flash("Profile updated successfully!", "success")
        return redirect('/profile')

    return render_template('edit_profile.html', user=customer)
