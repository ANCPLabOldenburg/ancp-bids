from ancpbids import BIDSLayout
from ancpbids.mixins.mixin_dataframe import DataFrameMixin
from ..base_test_case import DS005_DIR


def test_bidslayout_has_to_df_mixin():
    assert issubclass(BIDSLayout, DataFrameMixin)
    assert callable(BIDSLayout.to_df)


def test_to_df_row_count_and_entity_columns():
    layout = BIDSLayout(DS005_DIR)
    df = layout.to_df()
    files = layout.get()
    assert len(df) == len(files)
    for column in ('path', 'subject', 'task', 'run', 'suffix', 'extension'):
        assert column in df.columns
    assert list(df.columns)[0] == 'path'
    assert set(df['subject'].dropna().unique()) == {'%02d' % i for i in range(1, 17)}


def test_to_df_filters():
    layout = BIDSLayout(DS005_DIR)
    df = layout.to_df(subject='01', suffix='bold', scope='raw')
    assert len(df) == 3
    assert set(df['subject'].unique()) == {'01'}
    assert set(df['suffix'].unique()) == {'bold'}


def test_to_df_metadata():
    layout = BIDSLayout(DS005_DIR)
    df = layout.to_df(metadata=True, suffix='bold', extension='.nii.gz', scope='raw')
    assert 'RepetitionTime' in df.columns
    assert 'TaskName' in df.columns
    assert (df['RepetitionTime'] == 2.0).all()
    assert (df['TaskName'] == 'mixed-gambles task').all()
