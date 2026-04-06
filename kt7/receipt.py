from dataclasses import dataclass
from typing import List


VAT_RATE = 0.2


@dataclass
class Service:
    name: str
    quantity: int
    price: float

    def total(self) -> float:
        if self.price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if self.quantity <= 0:
            raise ValueError("Количество должно быть больше 0")
        return self.quantity * self.price


class Receipt:
    def __init__(self, services: List[Service], discount: float = 0.0, vat: float = VAT_RATE):
        if not services:
            raise ValueError("Корзина не может быть пустой")
        if discount < 0 or discount > 50:
            raise ValueError("Скидка должна быть от 0 до 50%")

        self.services = services
        self.discount = discount
        self.vat = vat

    def subtotal(self) -> float:
        return sum(s.total() for s in self.services)

    def discount_amount(self) -> float:
        return self.subtotal() * (self.discount / 100)

    def total_without_vat(self) -> float:
        return self.subtotal() - self.discount_amount()

    def vat_amount(self) -> float:
        return self.total_without_vat() * self.vat

    def total(self) -> float:
        return self.total_without_vat() + self.vat_amount()

    def generate_receipt(self, payment_method: str) -> str:
        lines = []
        lines.append('СПОРТИВНЫЙ КОМПЛЕКС "ОЛИМПИЯ"')
        lines.append("-----------------------------------------")
        lines.append("Услуга        Кол-во   Цена   Сумма")

        for s in self.services:
            lines.append(f"{s.name:<15}{s.quantity:<8}{s.price:<7}{s.total()}")

        lines.append("-----------------------------------------")
        lines.append(f"Подытог: {self.subtotal():>25.2f}")
        lines.append(f"Скидка ({self.discount}%): {-self.discount_amount():>15.2f}")
        lines.append(f"Итого без НДС: {self.total_without_vat():>17.2f}")
        lines.append(f"НДС ({int(self.vat*100)}%): {self.vat_amount():>18.2f}")
        lines.append("=" * 40)
        lines.append(f"К ОПЛАТЕ: {self.total():>22.2f} ₽")
        lines.append(f"Способ оплаты: {payment_method}")
        lines.append("Спасибо за визит!")
        lines.append("=" * 40)

        return "\n".join(lines)
