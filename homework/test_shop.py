"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(100)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        quantity = product.quantity
        product.buy(100)
        assert product.quantity == quantity - 100

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(1100)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_cart_add_product(self, product, cart):
        cart.add_product(product)
        assert product in cart.products
        cart.add_product(product, buy_count=4)
        assert cart.products.get(product) == 5
        assert cart.products.__len__() == 1

    def test_remove_product(self, product, cart):
        cart.add_product(product, 100)
        cart.remove_product(product, 100)
        assert product not in cart.products

    def test_remove_product_count_less(self, product, cart):
        cart.add_product(product, 5)
        cart.remove_product(product, 2)
        assert cart.products[product] == 3

    def test_remove_product_count_more(self, product, cart):
        cart.add_product(product, 2)
        cart.remove_product(product, 5)
        assert cart.products == {}

    def test_remove_product_from_empty_cart(self, product, cart):
        with pytest.raises(KeyError):
            cart.remove_product(product)

    def test_clear_cart(self, product, cart):
        cart.add_product(product, 10)
        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, product, cart):
        cart.add_product(product, 10)
        assert cart.get_total_price() == product.price * 10

        cart.add_product(product, 5)
        assert cart.get_total_price() == product.price * 15

    def test_buy_enough_quantity(self, product, cart):
        cart.add_product(product, 100)
        cart.buy()
        assert cart.products == {}
        assert product.quantity == 900

    def test_buy_with_error(self, product, cart):
        cart.add_product(product, product.quantity + 1)
        with pytest.raises(ValueError):
            cart.buy()
