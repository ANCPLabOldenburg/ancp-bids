
import sys
import pytest
from ..base_test_case import *

OPENNEURO_DS001734 = os.path.join(os.environ.get('TEST_DATASETS', os.path.expanduser('~/datasets')), 'ds001734')

if not os.path.isdir(OPENNEURO_DS001734):
    print('test dataset not found: ' + OPENNEURO_DS001734)
    sys.exit(1)



def _assert_on(layout_type):
    layout = layout_type(OPENNEURO_DS001734, derivatives=True)
    subjects = layout.get_subjects(scope="raw")
    assert 108 == len(subjects)
    assert 0 == len(layout.get_sessions())

    bold_run1 = layout.get(scope="raw", suffix='bold', run='01', extension='.nii.gz', return_type='filename')
    assert 108 == len(bold_run1)

def test_ancpbids_openneuro_ds001734():
    import ancpbids
    _assert_on(ancpbids.BIDSLayout)

def test_pybids_measure_scan_ds001734():
    import bids
    _assert_on(bids.BIDSLayout)
