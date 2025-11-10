import pytest
from project_task.main import (
    Product,
    DigitalProduct,
    Cart,
    Customer,
    CreditCardPayment,
    PayPalPayment,
    Order,
    OrderProcessor,
)


@pytest.fixture
def sample_product():
    return Product("Помидор", 29.50, 10)


@pytest.fixture
def sample_digital_product():
    return DigitalProduct("Фильм 'Назад в будущее'", 49.50, 2048)


@pytest.fixture
def sample_cart(sample_product):
    cart = Cart()
    cart.add_item(sample_product, 2)
    return cart


@pytest.fixture
def sample_customer():
    return Customer("Иван Иванов", "ivan@example.com", "Москва, пр-кт Ленина, д. 1")


@pytest.fixture
def sample_credit_card_payment():
    return CreditCardPayment("12345678901234510")


@pytest.fixture
def sample_paypal_payment():
    return PayPalPayment("ivan@example.com")


@pytest.fixture
def sample_order(sample_customer, sample_cart):
    return Order(sample_customer, sample_cart)


def test_product_creation(sample_product):
    assert sample_product.name == "Помидор"
    assert sample_product.price == 29.50
    assert sample_product.stock == 10


def test_product_stock_update(sample_product):
    sample_product.stock = 5
    assert sample_product.stock == 5


def test_product_negative_stock(sample_product):
    with pytest.raises(ValueError):
        sample_product.stock = -1


def test_digital_product_creation(sample_digital_product):
    assert sample_digital_product.name == "Фильм 'Назад в будущее'"
    assert sample_digital_product.price == 49.50
    assert sample_digital_product.file_size == 2048
    assert sample_digital_product.stock == 1


def test_cart_add_item(sample_product, sample_cart):
    assert sample_product in sample_cart.items
    assert sample_cart.items[sample_product] == 2


def test_cart_add_item_insufficient_stock(sample_product):
    cart = Cart()
    sample_product.stock = 1
    with pytest.raises(ValueError):
        cart.add_item(sample_product, 2)


def test_cart_remove_item(sample_product, sample_cart):
    sample_cart.remove_item(sample_product)
    assert sample_product not in sample_cart.items


def test_cart_get_total(sample_cart, sample_product):
    assert sample_cart.get_total() == 29.50 * 2


def test_cart_apply_stock_changes(sample_product, sample_cart):
    sample_cart.apply_stock_changes()
    assert sample_product.stock == 8


def test_customer_creation(sample_customer):
    assert sample_customer.name == "Иван Иванов"
    assert sample_customer.email == "ivan@example.com"
    assert sample_customer.address == "Москва, пр-кт Ленина, д. 1"


def test_credit_card_payment(sample_credit_card_payment, capsys):
    assert sample_credit_card_payment.pay(100.0) is True
    captured = capsys.readouterr()
    assert (
        "Обработка платежа по кредитной карте (3456) на сумму 100.00..." in captured.out
    )


def test_paypal_payment(sample_paypal_payment, capsys):
    assert sample_paypal_payment.pay(100.0) is True
    captured = capsys.readouterr()
    assert (
        "Обработка платежа PayPal (ivan@example.com) на сумму 100.00..." in captured.out
    )


def test_order_creation(sample_order, sample_customer, sample_cart):
    assert sample_order.status == "создано"
    assert sample_order.cart == sample_cart


def test_order_process(sample_order, sample_credit_card_payment, sample_product):
    sample_order.set_payment(sample_credit_card_payment)
    sample_order.process()
    assert sample_order.status == "обработано"
    assert sample_product.stock == 8


def test_order_processor(sample_order, sample_credit_card_payment, capsys):
    OrderProcessor.process_order(sample_order, sample_credit_card_payment)
    captured = capsys.readouterr()
    assert "Заказ успешно обработан!" in captured.out
    assert sample_order.status == "обработано"
