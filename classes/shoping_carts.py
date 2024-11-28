class ShoppingCart:
    """
    Класс, представляющий корзину покупок.
    """
    def __init__(self, buyer_name, registered_by):
        """
        Инициализирует корзину с указанием имени покупателя и регистратора.
        """
        self.buyer_name = buyer_name  # Имя покупателя
        self.registered_by = registered_by  # Имя пользователя, зарегистрировавшего покупку
        self.items = []

    def add_item(self, product, quantity):
        """
        Добавляет продукт в корзину.
        """
        self.items.append({"Продукт": product, "количество": quantity})

    def remove_item(self, product_name):
        """
        Удаляет продукт из корзины по имени.
        """
        self.items = [item for item in self.items if item["Продукт"].name != product_name]

    def get_total(self):
        """
        Возвращает общую стоимость продуктов в корзине.
        """
        total = sum(item["Продукт"].price * item["количество"] for item in self.items)
        return total

    def get_details(self):
        """
        Возвращает детализированную информацию о содержимом корзины, покупателе, пользователе и общей стоимости.
        """
        details = f"Покупатель: {self.buyer_name}\n"
        details += "Корзина покупок:\n"
        for item in self.items:
            details += f"{item['Продукт'].get_details()}, Количество: {item['количество']}\n"
        details += f"Общее: {self.get_total()} руб\n"
        details += f"Покупки зарегистрированы пользователем: {self.registered_by}"
        return details
