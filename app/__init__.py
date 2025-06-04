from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'

    from app.routes.auth_routes import auth_bp
    from app.routes.customer_routes import customer_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(admin_bp)

    return app

create_app = create_app
