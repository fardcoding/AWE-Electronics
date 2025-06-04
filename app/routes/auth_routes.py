from flask import Blueprint, render_template, request, redirect, session, flash
from app.models.account import Account
from app.globals import users
from app.utils.json_helpers import save_all_users

auth_bp = Blueprint('auth', __name__)

# ✅ Redirect root to login page
@auth_bp.route('/')
def root():
    return redirect('/login')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Account.authenticate(email, password, users)
        if user:
            # ✅ Store essential session data
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['is_admin'] = (user.email == "admin@awestore.com")

            flash(f"Welcome, {user.name}!", "success")
            return redirect('/admin/dashboard' if session['is_admin'] else '/catalogue')
        else:
            flash("Invalid credentials.", "danger")
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()  # ✅ Clears everything
    flash("You have been logged out.", "info")
    return redirect('/login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']

        if any(u.email == email for u in users):
            flash("Email already registered.", "warning")
            return redirect('/register')

        from app.models.customer import Customer
        new_user = Customer(
            id=len(users) + 1,
            name=name,
            email=email,
            password=password,
            address=address
        )
        users.append(new_user)
        save_all_users()
        flash("Registration successful. Please log in.", "success")
        return redirect('/login')

    return render_template('register.html')
