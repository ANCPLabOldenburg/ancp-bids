import math
from typing import Union

from torch.utils.data import Dataset, random_split, DataLoader
import ancpbids


class TorchDataset(Dataset):
    def __init__(self, *bids_dataset_paths, **query_kwargs):
        self.data_events_files = []

        for bids_dataset_path in bids_dataset_paths:
            bids_dataset = ancpbids.load_dataset(bids_dataset_path)
            if query_kwargs is None:
                query_kwargs = {}
            # limit scope to raw as the user is most probably not interested in derivatives
            query_kwargs.setdefault("scope", "raw")
            data_files = bids_dataset.query(**query_kwargs)

            def load_contents(data_file) -> dict or None:
                sidecar = data_file.sidecar(suffix="events", extension=".tsv")
                if len(sidecar) > 0:
                    return sidecar[0].load_contents()
                return {}

            self.data_events_files += [
                (data_file.get_absolute_path(), load_contents(data_file)) for data_file in data_files]

    def __len__(self):
        return len(self.data_events_files)

    def __getitem__(self, idx):
        return self.data_events_files[idx]

    def split(self, *args: float):
        sum_ratios = sum(args)
        if not math.isclose(sum_ratios, 1.0):
            raise ValueError("sum of split ratios should be 1.0")

        size_dataset = len(self)
        return random_split(self, [round(size_dataset * ratio) for ratio in args])
