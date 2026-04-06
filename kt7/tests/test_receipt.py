import pytest
import allure

from receipt import Service, Receipt


@allure.feature("Кассовый модуль")
class TestReceipt:

    @allure.story("Расчёт стоимости")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_total_calculation(self):
        services = [
            Service("Бассейн", 2, 500),
            Service("Шкафчик", 1, 150)
        ]

        receipt = Receipt(services, discount=10)

        assert receipt.subtotal() == 1150
        assert receipt.discount_amount() == 115
        assert receipt.total_without_vat() == 1035
        assert receipt.vat_amount() == 207
        assert receipt.total() == 1242

    @allure.story("Валидация")
    def test_negative_price(self):
        with pytest.raises(ValueError):
            Service("Бассейн", 1, -100).total()

    @allure.story("Валидация")
    def test_empty_cart(self):
        with pytest.raises(ValueError):
            Receipt([], discount=10)

    @allure.story("Валидация")
    def test_discount_over_limit(self):
        services = [Service("Зал", 1, 500)]
        with pytest.raises(ValueError):
            Receipt(services, discount=60)

    @allure.story("Расчёт стоимости")
    @pytest.mark.parametrize("payment_method", [
        "Наличные",
        "Безналичный расчёт",
        "Карта"
    ])
    def test_receipt_generation(self, payment_method):
        services = [Service("Зал", 1, 500)]
        receipt = Receipt(services)

        result = receipt.generate_receipt(payment_method)

        assert payment_method in result
        assert "К ОПЛАТЕ" in result

    @allure.story("Граничные случаи")
    def test_single_service(self):
        services = [Service("Йога", 1, 1000)]
        receipt = Receipt(services, discount=0)

        assert receipt.total() == 1200  # с НДС 20%

    @allure.story("Граничные случаи")
    def test_max_discount(self):
        services = [Service("Зал", 1, 1000)]
        receipt = Receipt(services, discount=50)

        assert receipt.total_without_vat() == 500

    @allure.story("Граничные случаи")
    def test_zero_vat(self):
        services = [Service("Зал", 1, 1000)]
        receipt = Receipt(services, discount=0, vat=0)

        assert receipt.total() == 1000

    @allure.story("Граничные случаи")
    def test_long_service_name(self):
        services = [Service("Очень длинное название услуги фитнес центра", 1, 500)]
        receipt = Receipt(services)

        result = receipt.generate_receipt("Карта")

        assert "Очень длинное" in result
