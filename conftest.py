import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--rewrite-deposit-truth",
        action="store_true",
        default=False,
        help=(
            "If the input data for test_deposit has changed, this will need "
            "to be used to update the ground truth, assuming deposit logic "
            "is unchanged."
        ),
    )


@pytest.fixture
def rewrite_deposit_truth(request):
    return request.config.getoption("--rewrite-deposit-truth")
