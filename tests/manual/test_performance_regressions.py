from ..base_test_case import *
import ancpbids



import pytest

def test_batch_loading():
    for i in range(0, 10):
        ds = ancpbids.load_dataset(DS005_DIR)
