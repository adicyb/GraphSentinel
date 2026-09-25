import random

import numpy as np

from graphsentinel.utils import set_seed


def test_reproducibility():
    set_seed(42)

    python_value_1 = random.random()
    numpy_value_1 = np.random.random()

    set_seed(42)

    python_value_2 = random.random()
    numpy_value_2 = np.random.random()

    assert python_value_1 == python_value_2
    assert numpy_value_1 == numpy_value_2