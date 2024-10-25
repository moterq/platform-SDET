def test_get_all_orders(orders_endpoints):
    order_data = [
        {"symbol": "AAPL", "quantity": 10, "price": 150.0},
        {"symbol": "GOOGL", "quantity": 5, "price": 2800.0},
        {"symbol": "MSFT", "quantity": 7, "price": 299.0}
    ]

    # Storage of all created orders
    created_order_ids = []

    for order in order_data:
        response = orders_endpoints.create_order(symbol=order["symbol"], quantity=order["quantity"],
                                                 price=order["price"])
        assert response.status_code == 200
        created_order_ids.append(str(response.json()["order_id"]))  # Приводим order_id к строке

    # Get all orders
    response = orders_endpoints.get_orders()
    assert response.status_code == 200
    all_orders = response.json()

    # Check that all orders exists in list
    retrieved_order_ids = [str(order_id) for order_id in all_orders.keys()]  # order_id's to str
    for order_id in created_order_ids:
        assert order_id in retrieved_order_ids, f"Order ID {order_id} not found in the list of orders"


def test_get_order_by_id_success(orders_endpoints):
    create_response = orders_endpoints.create_order(symbol="AAPL", quantity=10, price=150.0)
    order_id = create_response.json()["order_id"]

    response = orders_endpoints.get_order_by_id(order_id)

    assert response.status_code == 200
    data = response.json()
    assert data["order"]["symbol"] == "AAPL"
    assert data["order"]["quantity"] == 10
    assert data["order"]["price"] == 150.0


def test_get_order_by_id_not_found(orders_endpoints):
    response = orders_endpoints.get_order_by_id(order_id=9999)  # As example of not existing ID

    assert response.status_code == 404
    error_data = response.json()
    assert "Order not found" in error_data["detail"]
