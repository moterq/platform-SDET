import pytest


def test_delete_order_success(orders_endpoints):
    create_response = orders_endpoints.create_order(symbol="AAPL", quantity=10, price=150.0)
    order_id = create_response.json()["order_id"]

    # Delete the order
    response = orders_endpoints.delete_order(order_id)
    assert response.status_code == 200
    assert "Order canceled and deleted" in response.json()["message"]

    # Verify the order has been deleted
    response = orders_endpoints.get_order_by_id(order_id)
    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]


@pytest.mark.parametrize("order_id, expected_status, expected_error_message", [
    (9999, 404, "Order not found"),  # Not existed order ID
    (0, 404, "Order not found"),     # Invalid ID
])
def test_delete_order_invalid(orders_endpoints, order_id, expected_status, expected_error_message):
    response = orders_endpoints.delete_order(order_id)
    assert response.status_code == expected_status
    assert expected_error_message in response.json()["detail"]
