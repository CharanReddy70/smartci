from ml.predict import estimate
from scripts.route_tests import select_tests
from scripts.summarize_log import diagnostic_excerpt


def test_pricing_reaches_the_cart_integration():
    assert select_tests(["src/pricing.py"]) == ["tests/test_cart.py", "tests/test_pricing.py"]


def test_independent_inventory_change():
    assert select_tests(["src/inventory.py"]) == ["tests/test_inventory.py"]


def test_test_file_and_global_inputs():
    assert select_tests(["tests/test_cart.py"]) == ["tests/test_cart.py"]
    assert select_tests(["requirements.lock", "tests/test_cart.py"]) == ["tests"]
    assert select_tests(["src/removed.py"]) == ["tests"]
    assert select_tests([]) == ["tests"]


def test_sparse_prediction_groups():
    assert estimate([(True, True)], True) == (2 / 3, 1)
    assert estimate([(True, True)], False) == (0.5, 0)


def test_failure_excerpt_keeps_assertion():
    log = "setup\n" * 4000 + "=== FAILURES ===\nassert 100 == 101"
    assert "assert 100 == 101" in diagnostic_excerpt(log)
    assert len(diagnostic_excerpt(log)) <= 4000
