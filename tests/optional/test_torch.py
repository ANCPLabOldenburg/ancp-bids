from typing import List, Dict

import torch

from ancpbids.torch import TorchDataset
from ..base_test_case import *


class BasicTestCase(BaseTestCase):
    def test_torch_dataset(self):
        # load the dataset given the directory path, limiting to BOLD files (suffix="bold", extension='.nii.gz')
        torch_ds = TorchDataset(DS005_DIR, suffix="bold")
        train_set, test_set, val_set = torch_ds.split(0.8, 0.1, 0.1)

        assert len(train_set) == 39
        assert len(test_set) == 5
        assert len(val_set) == 5

        train_dl: torch.utils.data.DataLoader = torch.utils.data.DataLoader(train_set, shuffle=True)
        file_path, onset_events = next(iter(train_dl))
        assert os.path.exists(file_path[0])
        assert isinstance(onset_events, list)


if __name__ == '__main__':
    unittest.main()
