from base_test_case import *
import bids


class QueryTestCase(BaseTestCase):
    def test_bidslayout(self):
        layout = bids.BIDSLayout(DS005_DIR)

        subjects = layout.get_subjects()
        subjects_expected = ['sub-%02d' % i for i in range(1, 17)]
        self.assertListEqual(subjects_expected, subjects)

        sessions = layout.get_sessions()
        self.assertEqual(0, len(sessions))

        tasks = layout.get_tasks()
        self.assertListEqual(['mixedgamblestask'], tasks)

if __name__ == '__main__':
    unittest.main()
