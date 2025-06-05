from flask import Blueprint, render_template, request, redirect, flash, session
from app.models.product import Product
from app.globals import orders, users, products
from app.utils.json_helpers import save_all_products
from app.utils.decorators import admin_required  # ✅ Decorator imported

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def admin_dashboard():
    total_orders = len(orders)
    total_revenue = sum(order.total_amount for order in orders)

    product_counts = {}
    for order in orders:
        for pid in order.product_ids:
            product_counts[pid] = product_counts.get(pid, 0) + 1

    best_selling_id = max(product_counts, key=product_counts.get, default=None)
    best_selling = next((p for p in products if p.id == best_selling_id), None)

    return render_template(
        'admin_dashboard.html',
        total_orders=total_orders,
        total_revenue=total_revenue,
        best_selling=best_selling
    )

@admin_bp.route('/products')
@admin_required
def product_list():
    return render_template('admin_products.html', products=products)

@admin_bp.route('/products/new', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        category = request.form['category']

        new_product = Product(
            id=len(products) + 1,
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category
        )

        products.append(new_product)
        save_all_products()
        flash("Product added successfully!", "success")
        return redirect('/admin/products')

    return render_template('add_product.html')

@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        flash("Product not found.", "danger")
        return redirect('/admin/products')

    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.category = request.form['category']
        save_all_products()
        flash("Product updated successfully!", "success")
        return redirect('/admin/products')

    return render_template('edit_product.html', product=product)

@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@admin_required
def delete_product(product_id):
    global products
    product_to_delete = next((p for p in products if p.id == product_id), None)

    if product_to_delete:
        products.remove(product_to_delete)
        save_all_products()
        flash("Product deleted successfully!", "success")
    else:
        flash("Product not found.", "danger")

    return redirect('/admin/products')

@admin_bp.route('/orders')
@admin_required
def view_all_orders():
    enriched_orders = []
    for order in orders:
        customer = next((u for u in users if u.id == order.customer_id), None)
        ordered_products = [next((p for p in products if p.id == pid), None) for pid in order.product_ids]
        enriched_orders.append({
            'id': order.id,
            'customer': customer.name if customer else "Unknown",
            'total': order.total_amount,
            'products': ordered_products
        })
    return render_template('admin_orders.html', orders=enriched_orders)

@admin_bp.route('/report')
@admin_required
def sales_report():
    total_orders = len(orders)
    total_revenue = sum(order.total_amount for order in orders)

    product_counts = {}
    for order in orders:
        for pid in order.product_ids:
            product_counts[pid] = product_counts.get(pid, 0) + 1

    best_selling_id = max(product_counts, key=product_counts.get, default=None)
    best_selling = next((p for p in products if p.id == best_selling_id), None)

    return render_template(
        'report.html',
        total_orders=total_orders,
        total_revenue=total_revenue,
        best_selling=best_selling,
        product_counts=product_counts
    )


