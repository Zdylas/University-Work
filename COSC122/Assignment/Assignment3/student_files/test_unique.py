""" Tests for the unique module """
import os
import shutil
from stats import IS_MARKING_MODE
import unittest
from stats import StatCounter, PLATE_COMPS
from unique import uniques_by_merge_opp
from classes3 import NumberPlate
from utilities import read_unique_test_data, plates_from_strings


DATA_DIR = './test_data/'
DEF_SEED = 'a'
FILE_TEMPLATE = 'unique-{len1}-{len2}-{n_expected}-{seed}.txt'


def real_comparisons(counter):
    """ calling real_comparisons will be
        equivalent to calling StatCounter.get_count
    """
    return StatCounter.get_count(counter)




class BaseTester(unittest.TestCase):

    def setUp(self):
        """Runs before every test case"""
        StatCounter.reset_counts()

    def check_file_result_list(
            self, len1, len2, n_expected, min_comps, max_comps, seed=DEF_SEED):
        base_filename = FILE_TEMPLATE.format(len1=len1, len2=len2,
                                             n_expected=n_expected, seed=seed)
        filename = DATA_DIR + base_filename
        list1, list2, expected_uniques = read_unique_test_data(filename)
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertGreaterEqual(comparisons, min_comps)
        self.assertLessEqual(comparisons, max_comps)
        return True

    def check_file_comps(self, len1, len2, n_expected,
                         min_comps, max_comps, seed=DEF_SEED):
        base_filename = FILE_TEMPLATE.format(len1=len1, len2=len2,
                                             n_expected=n_expected, seed=seed)
        filename = DATA_DIR + base_filename
        list1, list2, expected_uniques = read_unique_test_data(filename)
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertGreaterEqual(comparisons, min_comps)
        self.assertLessEqual(comparisons, max_comps)
        return True

    def check_file_real_comps(
            self, len1, len2, n_expected, min_comps, max_comps, seed=DEF_SEED):
        base_filename = FILE_TEMPLATE.format(len1=len1, len2=len2,
                                             n_expected=n_expected, seed=seed)
        filename = DATA_DIR + base_filename
        list1, list2, expected_uniques = read_unique_test_data(filename)
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertEqual(comparisons, real_comparisons(PLATE_COMPS))
        return True



class TestTiny(BaseTester):

    def test_001_two_item_lists1(self):
        list1 = plates_from_strings(['AAA111', 'BBB111'])
        list2 = plates_from_strings(['BBB111', 'BBB113'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        expected_uniques = plates_from_strings(['BBB113'])
        expected_comparisons = 4
        self.assertEqual(student_uniques, expected_uniques)
        self.assertEqual(comparisons, expected_comparisons)

    def test_002_two_word_lists1_real_comparisons(self):
        list1 = plates_from_strings(['AAA111', 'BBB111'])
        list2 = plates_from_strings(['AAA112', 'BBB111'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertEqual(comparisons, real_comparisons(PLATE_COMPS))

    def test_005_two_item_lists2(self):
        list1 = plates_from_strings(['AAA112', 'BBB222'])
        list2 = plates_from_strings(['AAA111', 'BBB222'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        expected_uniques = plates_from_strings(['AAA111'])
        expected_comparisons = 5
        self.assertEqual(student_uniques, expected_uniques)
        self.assertEqual(comparisons, expected_comparisons)

    def test_006_two_word_lists2_real_comparisons(self):
        list1 = plates_from_strings(['AAA111', 'BBB222'])
        list2 = plates_from_strings(['AAA111', 'DDD222'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertEqual(comparisons, real_comparisons(PLATE_COMPS))

    def test_010_two_item_lists3(self):
        list1 = plates_from_strings(['AAA111', 'DDD222'])
        list2 = plates_from_strings(['AAA111', 'BBB222'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        expected_uniques = plates_from_strings(['BBB222'])
        expected_comparisons = 3
        self.assertEqual(student_uniques, expected_uniques)
        self.assertEqual(comparisons, expected_comparisons)

    def test_011_two_word_lists3_real_comparisons(self):
        list1 = plates_from_strings(['AAA111', 'BBB222'])
        list2 = plates_from_strings(['AAA111', 'DDD222'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertEqual(comparisons, real_comparisons(PLATE_COMPS))


class TestSmall(BaseTester):

    def test_030_identical_lists(self):
        list1 = plates_from_strings(
            ['AAA111', 'BBB222', 'CCC333', 'DDD444', 'EEE555'])
        list2 = plates_from_strings(
            ['AAA111', 'BBB222', 'CCC333', 'DDD444', 'EEE555'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        expected_uniques = []
        lower_limit, upper_limit = 5, 10
        self.assertEqual(student_uniques, student_uniques)
        self.assertGreaterEqual(comparisons, lower_limit)
        self.assertLessEqual(comparisons, upper_limit)

    def test_040_identical_lists_real_comparisons(self):
        list1 = plates_from_strings(
            ['AAA111', 'BBB222', 'CCC333', 'DDD444', 'EEE555'])
        list2 = plates_from_strings(
            ['AAA111', 'BBB222', 'CCC333', 'DDD444', 'EEE555'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertEqual(comparisons, real_comparisons(PLATE_COMPS))

    def test_050_unique_lists(self):
        list1 = plates_from_strings(
            ['AAA111', 'DDD222', 'EEE333', 'EEE444', 'FFF121'])
        list2 = plates_from_strings(
            ['BBB111', 'CCC222', 'CCC234', 'FFF111', 'FFF123', 'JJJ234'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        expected_uniques = plates_from_strings(
            ['BBB111', 'CCC222', 'CCC234', 'FFF111', 'FFF123', 'JJJ234'])
        lower_limit, upper_limit = 13, 18
        self.assertEqual(student_uniques, expected_uniques)
        self.assertGreaterEqual(comparisons, lower_limit)
        self.assertLessEqual(comparisons, upper_limit)

    def test_060_unique_lists_real_comparisons(self):
        list1 = plates_from_strings(
            ['AAA111', 'DDD222', 'EEE333', 'EEE444', 'FFF121'])
        list2 = plates_from_strings(
            ['BBB111', 'CCC222', 'CCC234', 'FFF111', 'FFF123', 'JJJ234'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertEqual(comparisons, real_comparisons(PLATE_COMPS))


class TestSmall2(BaseTester):

    def test_070_cross_over_lists(self):
        list1 = plates_from_strings(
            ['BBB111', 'BBB222', 'BBB333', 'EEE444', 'FFF121'])
        list2 = plates_from_strings(
            ['AAA121', 'AAA122', 'AAA123', 'BBB111', 'BBB222', 'BBB333'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        expected_uniques = plates_from_strings(['AAA121', 'AAA122', 'AAA123'])
        lower_limit, upper_limit = 9, 12
        self.assertEqual(student_uniques, expected_uniques)
        self.assertGreaterEqual(comparisons, lower_limit)
        self.assertLessEqual(comparisons, upper_limit)

    def test_080_cross_over_lists_real_comparisons(self):
        list1 = plates_from_strings(
            ['BBB111', 'BBB222', 'BBB333', 'EEE444', 'FFF121'])
        list2 = plates_from_strings(
            ['AAA121', 'AAA122', 'AAA123', 'BBB111', 'BBB222', 'BBB333'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertEqual(comparisons, real_comparisons(PLATE_COMPS))

    def test_090_cross_over_lists_2(self):
        list1 = plates_from_strings(
            ['AAA111', 'BBB222', 'CCC333', 'GGG111', 'HHH222'])
        list2 = plates_from_strings(
            ['DDD121', 'EEE122', 'FFF123', 'GGG111', 'HHH222', 'III333', 'JJJ333'])
        #list1 = simple_counter_list(['d', 'e', 'f', 'g', 'h', 'i', 'j'])
        #list2 = simple_counter_list(['a', 'b', 'c', 'g', 'h'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        expected_uniques = plates_from_strings(
            ['DDD121', 'EEE122', 'FFF123', 'III333', 'JJJ333'])
        lower_limit, upper_limit = 13, 14
        self.assertEqual(student_uniques, expected_uniques)
        self.assertGreaterEqual(comparisons, lower_limit)
        self.assertLessEqual(comparisons, upper_limit)

    def test_100_cross_over_lists_2(self):
        list1 = plates_from_strings(
            ['AAA111', 'BBB222', 'CCC333', 'GGG111', 'HHH222'])
        list2 = plates_from_strings(
            ['DDD121', 'EEE122', 'FFF123', 'GGG111', 'HHH222', 'III333', 'JJJ333'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertEqual(comparisons, real_comparisons(PLATE_COMPS))


class TestSmall3(BaseTester):

    def test_110_zig_zag_lists(self):
        list1 = plates_from_strings(
            ['BBB111', 'CCC222', 'EEE333', 'GGG444', 'III121'])
        list2 = plates_from_strings(
            ['AAA121', 'DDD122', 'FFF123', 'HHH111', 'JJJJ222'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        expected_uniques = plates_from_strings(
            ['AAA121', 'DDD122', 'FFF123', 'HHH111', 'JJJJ222'])
        lower_limit, upper_limit = 13, 18
        self.assertEqual(student_uniques, expected_uniques)
        self.assertGreaterEqual(comparisons, lower_limit)
        self.assertLessEqual(comparisons, upper_limit)

    def test_120_zig_zag_lists_real_comparisons(self):
        list1 = plates_from_strings(
            ['BBB111', 'CCC222', 'EEE333', 'GGG444', 'III121'])
        list2 = plates_from_strings(
            ['AAA121', 'DDD122', 'FFF123', 'HHH111', 'JJJJ222'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertEqual(comparisons, real_comparisons(PLATE_COMPS))

    def test_130_zig_zag_lists2(self):
        list1 = plates_from_strings(
            ['AAA121', 'DDD122', 'FFF123', 'HHH111', 'JJJJ222'])
        list2 = plates_from_strings(
            ['BBB111', 'CCC222', 'EEE333', 'GGG444', 'III121'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        expected_uniques = plates_from_strings(
            ['BBB111', 'CCC222', 'EEE333', 'GGG444', 'III121'])
        lower_limit, upper_limit = 13, 18
        self.assertEqual(student_uniques, expected_uniques)
        self.assertGreaterEqual(comparisons, lower_limit)
        self.assertLessEqual(comparisons, upper_limit)

    def test_140_zig_zag_lists2_real_comparisons(self):
        list1 = plates_from_strings(
            ['AAA121', 'DDD122', 'FFF123', 'HHH111', 'JJJJ222'])
        list2 = plates_from_strings(
            ['BBB111', 'CCC222', 'EEE333', 'GGG444', 'III121'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertEqual(comparisons, real_comparisons(PLATE_COMPS))

    def test_150_zig_zag_lists3(self):
        list1 = plates_from_strings(['AAA121', 'DDD122', 'FFF123', 'HHH111'])
        list2 = plates_from_strings(
            ['BBB111', 'CCC222', 'EEE333', 'GGG444', 'III121'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        expected_uniques = plates_from_strings(
            ['BBB111', 'CCC222', 'EEE333', 'GGG444', 'III121'])
        lower_limit, upper_limit = 12, 16
        self.assertEqual(student_uniques, expected_uniques)
        self.assertGreaterEqual(comparisons, lower_limit)
        self.assertLessEqual(comparisons, upper_limit)

    def test_160_zig_zag_lists2_real_comparisons(self):
        list1 = plates_from_strings(['AAA121', 'DDD122', 'FFF123', 'HHH111'])
        list2 = plates_from_strings(
            ['BBB111', 'CCC222', 'EEE333', 'GGG444', 'III121'])
        student_uniques, comparisons = uniques_by_merge_opp(list1, list2)
        self.assertEqual(comparisons, real_comparisons(PLATE_COMPS))




class TestMediumFiles(BaseTester):

    test_list = [(200, 200, 9, 227, 427),
                 (200, 200, 10, 230, 429),
                 (1000, 1000, 90, 1270, 2251),
                 (1000, 1000, 999, 2997, 3995), ]

    def test_500_medium_files(self):
        for n1, n2, n_expected, min_comps, max_comps in self.test_list:
            self.setUp()  # needed as subTest doesn't call it...
            passed = False
            with self.subTest(len1=n1, len2=n2, len_exp=n_expected):
                passed = self.check_file_comps(
                    n1, n2, n_expected, min_comps, max_comps)
            if not passed:
                break  # stop subtests after first failure

    def test_510_medium_files_real_comparisons(self):
        for n1, n2, n_expected, min_comps, max_comps in self.test_list:
            self.setUp()  # needed as subTest doesn't call it...
            passed = False
            with self.subTest(len1=n1, len2=n2, len_exp=n_expected):
                passed = self.check_file_real_comps(
                    n1, n2, n_expected, min_comps, max_comps)
            if not passed:
                break  # stop subtests after first failure


class TestLargeFiles(BaseTester):

    test_list = [(100, 10000, 9999, 10146, 20091),
                 (10000, 1000, 5, 10999, 19993),
                 (10000, 1000, 900, 11873, 21646),
                 (10000, 10000, 200, 10600, 20587),
                 (10000, 10000, 1000, 13000, 22730),
                 (10000, 10000, 9999, 29995, 39993), ]

    def test_600_large_files(self):
        for n1, n2, n_expected, min_comps, max_comps in self.test_list:
            self.setUp()  # needed as subTest doesn't call it...
            passed = False
            with self.subTest(len1=n1, len2=n2, len_exp=n_expected):
                passed = self.check_file_comps(
                    n1, n2, n_expected, min_comps, max_comps)
            if not passed:
                break  # stop subtests after first failure

    def test_610_large_files_real_comparisons(self):
        for n1, n2, n_expected, min_comps, max_comps in self.test_list:
            self.setUp()  # needed as subTest doesn't call it...
            passed = False
            with self.subTest(len1=n1, len2=n2, len_exp=n_expected):
                passed = self.check_file_real_comps(
                    n1, n2, n_expected, min_comps, max_comps)
            if not passed:
                break  # stop subtests after first failure


class TestVeryLargeFiles(BaseTester):

    test_list = [(50000, 1000, 9, 50919, 99829),
                 (50000, 50000, 9, 50027, 100027),
                 (50000, 50000, 1000, 53000, 102938),
                 (50000, 50000, 9999, 79997, 125159),
                 (50000, 50000, 25000, 125000, 149938)]

    def test_540_very_large_files(self):
        for n1, n2, n_expected, min_comps, max_comps in self.test_list:
            self.setUp()  # needed as subTest doesn't call it...
            passed = False
            with self.subTest(len1=n1, len2=n2, len_exp=n_expected):
                passed = self.check_file_comps(
                    n1, n2, n_expected, min_comps, max_comps)
            if not passed:
                break  # stop subtests after first failure

    def test_550_very_large_files_real_comparisons(self):
        for n1, n2, n_expected, min_comps, max_comps in self.test_list:
            self.setUp()  # needed as subTest doesn't call it...
            passed = False
            with self.subTest(len1=n1, len2=n2, len_exp=n_expected):
                passed = self.check_file_real_comps(
                    n1, n2, n_expected, min_comps, max_comps)
            if not passed:
                break  # stop subtests after first failure




def all_tests_suite():
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(TestTiny))

    # uncomment the following when you are ready to rumble
    # suite.addTest(unittest.makeSuite(TestSmall))
    # suite.addTest(unittest.makeSuite(TestSmall2))
    # suite.addTest(unittest.makeSuite(TestSmall3))

    # suite.addTest(unittest.makeSuite(TestMediumFiles))
    # suite.addTest(unittest.makeSuite(TestLargeFiles))
    # suite.addTest(unittest.makeSuite(TestVeryLargeFiles))
    return suite




def main():
    """ Makes a test suite and runs it. Will your code pass? """
    test_runner = unittest.TextTestRunner(verbosity=2)
    all_tests = all_tests_suite()
    test_runner.run(all_tests)


if __name__ == '__main__':
    main()
