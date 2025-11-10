from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime


class Product:
    def __init__(self, name: str, price: float, stock: int):
        self.__name = name
        self.__price = price
        self.__stock = stock

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, value: int):
        if value < 0:
            raise ValueError("Количество не должно быть отрицательным")
        self.__stock = value

    def __str__(self) -> str:
        return f"Продукт: {self.__name}, цена = {self.__price:.2f}, количество = {self.__stock}"


class DigitalProduct(Product):
    def __init__(self, name: str, price: float, file_size: int):
        super().__init__(name, price, stock=1)
        self.__file_size = file_size

    @property
    def file_size(self) -> int:
        return self.__file_size

    def __str__(self) -> str:
        return f"Цифровой продукт: {self.name}, цена = {self.price:.2f}, размер файла = {self.__file_size} МБ"


class Cart:
    def __init__(self):
        self.__items: Dict[Product, int] = {}

    def add_item(self, product: Product, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        if product.stock < quantity:
            raise ValueError(f"Недостаточно запасов для продукта '{product.name}'")
        self.__items[product] = self.__items.get(product, 0) + quantity

    def remove_item(self, product: Product) -> None:
        if product in self.__items:
            del self.__items[product]

    def clear(self) -> None:
        self.__items.clear()

    def get_total(self) -> float:
        return sum(p.price * q for p, q in self.__items.items())

    def apply_stock_changes(self) -> None:
        for product, quantity in self.__items.items():
            product.stock -= quantity

    def __str__(self) -> str:
        if not self.items:
            return "Корзина пуста"
        items_str = "\n".join(
            f"{p.name} x {q} = {p.price * q:.2f}" for p, q in self.__items.items()
        )
        return f"Корзина:\n{items_str}\nИтого: {self.get_total():.2f}"

    @property
    def items(self) -> Dict[Product, int]:
        return self.__items


class Customer:
    def __init__(self, name: str, email: str, address: str):
        self.__name = name
        self.__email = email
        self.__address = address
        self.__orders: List["Order"] = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email

    @property
    def address(self) -> str:
        return self.__address

    def add_order(self, order: "Order") -> None:
        self.__orders.append(order)

    def __str__(self) -> str:
        return (
            f"Клиент: {self.__name}, email = {self.__email}, адрес = {self.__address}"
        )


class Payment(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass


class CreditCardPayment(Payment):
    def __init__(self, card_number: str):
        self.__card_number = card_number

    def pay(self, amount: float) -> bool:
        print(
            f"Обработка платежа по кредитной карте ({self.__card_number[-4:]}) на сумму {amount:.2f}..."
        )
        return True


class PayPalPayment(Payment):
    def __init__(self, email: str):
        self.__email = email

    def pay(self, amount: float) -> bool:
        print(f"Обработка платежа PayPal ({self.__email}) на сумму {amount:.2f}...")
        return True


class Order:
    def __init__(self, customer: Customer, cart: Cart):
        self.__datecreated: str = datetime.now().strftime("%Y%m%d%H%M%S")
        self.__customer = customer
        self.__cart = cart
        self.__status: str = "создано"
        self.__payment: Optional[Payment] = None

    @property
    def status(self) -> str:
        return self.__status

    @property
    def cart(self) -> Cart:
        return self.__cart

    def set_payment(self, payment: Payment) -> None:
        self.__payment = payment

    def process(self) -> None:
        if not self.__payment:
            raise ValueError("Оплата должна быть установлена")
        self.__cart.apply_stock_changes()
        self.__status = "обработано"

    def __str(self) -> str:
        return (
            f"Заказ: дата = {self.__datecreated}, статус = {self.__status}, "
            f"клиент = {self.__customer.name}, сумма = {self.__cart.get_total():.2f}"
        )


class OrderProcessor:
    @staticmethod
    def process_order(order: Order, payment: Payment) -> None:
        try:
            amount = order.cart.get_total()
            if payment.pay(amount):
                order.set_payment(payment)
                order.process()
                print("Заказ успешно обработан!")
            else:
                print("Оплата не удалась.")
        except Exception as e:
            print(f"Ошибка обработки заказа: {e}")


if __name__ == "__main__":
    product = Product("Помидор", 29.50, 10)
    film = DigitalProduct("Фильм 'Назад в будущее'", 49.50, 2048)
    cart = Cart()
    cart.add_item(product, 2)
    cart.add_item(film)
    print(product)
    print(film)
    print(cart)
    customer = Customer("Иван Иванов", "ivan@example.com", "Москва, пр-кт Ленина, д. 1")
    print(customer)
    order = Order(customer, cart)
    payment = CreditCardPayment("1234567890123456")
    OrderProcessor.process_order(order, payment)
    print("\nОстаток на складе после заказа:")
    print(product)
