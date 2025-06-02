class CLI:
    @staticmethod
    def display_main_menu():
        print("\n=== Welcome to AWE Electronics Store ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

    @staticmethod
    def get_user_choice():
        choice = input("Enter your choice (1-3): ")
        return choice
