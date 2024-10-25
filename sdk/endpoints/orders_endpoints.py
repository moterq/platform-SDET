import allure
import requests

from sdk.base import BaseHttpRequester
from config import BASE_URL


class OrdersEndpoints(BaseHttpRequester):
    def __init__(self):
        super().__init__(base_url=BASE_URL, uri_prefix="/")

    @allure.step("Create order")
    def create_order(
            self,
            payload=None,
            symbol=None,
            quantity=None,
            price=None
    ) -> requests.Response:
        payload = {
            "symbol": symbol,
            "quantity": quantity,
            "price": price
        }
        return self._do_post("orders", json=payload)

    @allure.step("Get all orders")
    def get_orders(self, query: dict = None) -> requests.Response:
        return self._do_get("orders", params=query)

    @allure.step("Get order by ID")
    def get_order_by_id(self, order_id=None, query: dict = None) -> requests.Response:
        return self._do_get(f"orders/{order_id}", params=query)

    @allure.step("Delete order")
    def delete_order(self, order_id=None) -> requests.Response:
        return self._do_delete(f"orders/{order_id}")


orders_endpoints = OrdersEndpoints()