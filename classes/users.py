import hashlib
import uuid


class User:
    """
    Базовый класс, представляющий пользователя.
    """
    users = []  # Список для хранения всех пользователей

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        """
        Хеширование пароля с использованием соли.
        """
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ":" + salt

    @staticmethod
    def check_password(stored_password, provided_password):
        """
        Проверка пароля.
        """
        password, salt = stored_password.split(":")
        return password == hashlib.sha256(salt.encode() + provided_password.encode()).hexdigest()

    def get_details(self):
        return f"Пользователь: {self.username}, Email: {self.email}"


class Customer(User):
    """
    Класс, представляющий клиента, наследующий класс User.
    """
    def __init__(self, username, email, password, address):
        super().__init__(username, email, password)
        self.address = address

    def get_details(self):
        return f"Клиент: {self.username}, Email: {self.email}, Адрес: {self.address}"


class Admin(User):
    """
    Класс, представляющий администратора, наследующий класс User.
    """
    def __init__(self, username, email, password, admin_level):
        super().__init__(username, email, password)
        self.admin_level = admin_level

    def get_details(self):
        return f"Admin: {self.username}, Email: {self.email}, Admin-Level: {self.admin_level}"

    @staticmethod
    def list_users():
        """
        Выводит список всех пользователей.
        """
        return "\n".join([user.get_details() for user in User.users])

    @staticmethod
    def delete_user(username):
        """
        Удаляет пользователя по имени пользователя.
        """
        for user in User.users:
            if user.username == username:
                User.users.remove(user)
                return f"Пользователь {username} удален."
        return f"Пользователь {username} не найден."


class AuthenticationService:
    """
    Сервис для управления регистрацией и аутентификацией пользователей.
    """
    def __init__(self):
        self.current_user = None

    def register(self, user_class, username, email, password, *args):
        """
        Регистрация нового пользователя.
        """
        if any(user.username == username for user in User.users):
            return f"Пользователь с именем {username} уже существует."
        new_user = user_class(username, email, password, *args)
        User.users.append(new_user)
        return f"Пользователь {username} успешно зарегистрирован."

    def login(self, username, password):
        """
        Аутентификация пользователя.
        """
        for user in User.users:
            if user.username == username and User.check_password(user.password, password):
                self.current_user = user
                return f"Пользователь {username} успешно вошел в систему."
        return "Неверное имя пользователя или пароль."

    def logout(self):
        """
        Выход пользователя из системы.
        """
        if self.current_user:
            user = self.current_user.username
            self.current_user = None
            return f"Пользователь {user} успешно вышел из системы."
        return "Нет текущего пользователя для выхода."

    def get_current_user(self):
        """
        Возвращает текущего вошедшего пользователя.
        """
        if self.current_user:
            return f"Текущий пользователь: {self.current_user.get_details()}"
        return "Нет текущего пользователя."


# Пример использования
auth_service = AuthenticationService()

# Регистрация пользователей
print(auth_service.register(Customer, "ivan", "ivan@example.com", "password123", "Moscow"))
print(auth_service.register(Admin, "admin", "admin@example.com", "adminpassword", 1))

# Повторная регистрация того же пользователя
print(auth_service.register(Customer, "ivan", "ivan@example.com", "password123", "Moscow"))

# Аутентификация
print(auth_service.login("ivan", "password123"))
print(auth_service.get_current_user())

# Выход из системы
print(auth_service.logout())

# Вход от имени администратора
print(auth_service.login("admin", "adminpassword"))

# Администратор просматривает список пользователей
print(Admin.list_users())

# Администратор удаляет пользователя
print(Admin.delete_user("ivan"))
print(Admin.list_users())
