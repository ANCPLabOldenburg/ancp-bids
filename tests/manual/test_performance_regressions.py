from ..base_test_case import *
import ancpbids


class PerformanceRegressionTestCase(BaseTestCase):
    def test_batch_loading(self):
        for i in range(0, 10):
            ds = ancpbids.load_dataset(DS005_DIR)
