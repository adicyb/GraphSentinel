from graphsentinel.config import load_config
from graphsentinel.utils import get_logger, set_seed


def test_graphsentinel_smoke():
    config = load_config()

    set_seed(config["project"]["random_seed"])

    logger = get_logger("smoke-test")
    logger.info("GraphSentinel smoke test started")

    assert config["project"]["name"] == "GraphSentinel"
    assert logger.name == "smoke-test"