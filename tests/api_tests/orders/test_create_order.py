import pytest


def test_create_order_success(orders_endpoints):
    response = orders_endpoints.create_order(symbol="AAPL", quantity=10, price=150.0)

    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert data["order_id"] > 0


@pytest.mark.parametrize("symbol, quantity, price, expected_status", [
    (None, 10, 150.0, 422),   # Missed Symbol Data
    ("AAPL", None, 150.0, 422),   # Missed Quantity Data
    ("AAPL", 10, None, 422),   # Missed Price Data
    ("AAPL", "invalid_quantity", 150.0, 422),  # Invalid Quantity
    ("AAPL", 10, "invalid_price", 422)  # Invalid Price
])
def test_create_order_invalid(orders_endpoints, symbol, quantity, price, expected_status):
    response = orders_endpoints.create_order(symbol=symbol, quantity=quantity, price=price)
    assert response.status_code == expected_status
