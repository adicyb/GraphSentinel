from graphsentinel.utils import get_logger


def test_logger():
    logger = get_logger("test")

    logger.info("GraphSentinel logging test")

    assert logger.name == "test"