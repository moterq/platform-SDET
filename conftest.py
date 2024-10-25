import pytest

from sdk.logger import logger
from sdk.on_failure_printer import on_failure_printer
from sdk.endpoints.orders_endpoints import OrdersEndpoints
import logging

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


@pytest.fixture
def orders_endpoints() -> OrdersEndpoints:
    return OrdersEndpoints()


@pytest.fixture(autouse=True)
def when_test_ended():
    yield

    logger.requests_counter = 0


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def on_failure(request):
    yield

    setup_failed = hasattr(request.node, "rep_setup") and request.node.rep_setup.failed
    test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if setup_failed or test_failed:
        logger.move_log_to_status_dir("/failed")
        on_failure_printer.print_additional_info()
    else:
        logger.move_log_to_status_dir("/passed")
