from graphsentinel.config import load_config


def test_default_config():
    config = load_config()

    assert config["project"]["name"] == "GraphSentinel"
    assert config["project"]["random_seed"] == 42

    assert config["telemetry"]["identity"] is True
    assert config["telemetry"]["network"] is True
    assert config["telemetry"]["endpoint"] is True

    assert config["models"]["isolation_forest"]["enabled"] is True
    assert config["models"]["one_class_svm"]["enabled"] is True