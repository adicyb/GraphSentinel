import random

import numpy as np


def set_seed(seed: int) -> None:
    """
    Set random seeds used by GraphSentinel.

    This makes experiments more reproducible by controlling
    Python's and NumPy's pseudo-random number generators.
    """

    random.seed(seed)
    np.random.seed(seed)