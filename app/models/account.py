class Account:
    @staticmethod
    def authenticate(email: str, password: str, users: list):
        for user in users:
            if user.email == email and user.password == password:
                return user
        return None

    @staticmethod
    def update_profile(customer, name=None, email=None, address=None):
        if name:
            customer.name = name
        if email:
            customer.email = email
        if address:
            customer.address = address
        return customer
