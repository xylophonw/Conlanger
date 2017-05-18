import unittest

from context import conlanger
from conlanger import core, sce


class TestMainChange(unittest.TestCase):

    def test_standard_change(self):
        words = sce.apply_ruleset(['a'], 'a>b')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'b')


    def test_global_addition_change(self):
        words = sce.apply_ruleset(['ac'], '+b')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'babcb')

    def test_initial_addition_change(self):
        words = sce.apply_ruleset(['ac'], '+b/#_')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bac')

    def test_medial_addition_change(self):
        words = sce.apply_ruleset(['ac'], '+b/a_c')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'abc')

    def test_final_addition_change(self):
        words = sce.apply_ruleset(['ac'], '+b/_#')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'acb')


    def test_global_subtraction_change(self):
        words = sce.apply_ruleset(['babc'], '-b')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'ac')

    def test_initial_subtraction_change(self):
        words = sce.apply_ruleset(['babc'], '-b/#_')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'abc')

    def test_medial_subtraction_change(self):
        words = sce.apply_ruleset(['babc'], '-b/a_c')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bac')

    def test_final_subtraction_change(self):
        words = sce.apply_ruleset(['bacb'], '-b/_#')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bac')


class TestCategories(unittest.TestCase):

    def test_make_empty_cat(self):
        cat = core.Cat()
        self.assertEqual(str(cat), '')

    def test_make_non_empty_cat(self):
        cat = core.Cat(values='a,b,c')
        self.assertEqual(str(cat), 'a, b, c')

    def test_only_cat_in_target(self):
        ruleset = '\n'.join(['x=a,b',
                             '[x]>c'])
        words = sce.apply_ruleset(['abc'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'ccc')

    def test_cat_and_non_cat_in_target(self):
        ruleset = '\n'.join(['x=a,b',
                             'd[x]>c'])
        words = sce.apply_ruleset(['abcdadbdc'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'abcccdc')

    def test_subtract_cat(self):
        ruleset = '\n'.join(['x=b,c',
                             '-[x]'])
        words = sce.apply_ruleset(['abcd'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'ad')

    def test_only_unnamed_cat_in_target(self):
        words = sce.apply_ruleset(['abc'], '[a,b]>c')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'ccc')

    def test_unnamed_cat_and_non_cat_in_target(self):
        words = sce.apply_ruleset(['abacbccc'], '[a,b]c>d')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'abddcc')

    def test_subtract_unnamed_cat(self):
        words = sce.apply_ruleset(['abcd'], '-[b,c]')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'ad')


class TestFlags(unittest.TestCase):

    def test_single_rule_with_ignore_flag(self):
        words = sce.apply_ruleset(['a'], 'a>b ignore')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'a')

    def test_multiple_rules_with_single_ignore_flag(self):
        ruleset = '\n'.join(['a>b',
                             'b>c ignore',
                             'c>d'])
        words = sce.apply_ruleset(['abcd'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bbdd')

    def test_unconditional_stop_flag(self):
        ruleset = '\n'.join(['a>b stop',
                             'b>c'])
        words = sce.apply_ruleset(['abc'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bbc')

    def test_matching_conditional_stop_flag(self):
        ruleset = '\n'.join(['a>b/_# stop',
                             'b>c'])
        words = sce.apply_ruleset(['abca'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'abcb')

    def test_non_matching_conditional_stop_flag(self):
        ruleset = '\n'.join(['a>b/_# stop',
                             'b>c'])
        words = sce.apply_ruleset(['abc'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'acc')

    def test_matching_ditto_flag(self):
        ruleset = '\n'.join(['a>b/#_',
                             '+d ditto'])
        words = sce.apply_ruleset(['abc'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'dbdbdcd')

    def test_non_matching_ditto_flag(self):
        ruleset = '\n'.join(['a>b/_#',
                             '+d ditto'])
        words = sce.apply_ruleset(['abc'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'abc')


    def test_given_value_repeat_flag(self):
        words = sce.apply_ruleset(['baaa'], 'a>b/b_ repeat:2')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bbba')

    def test_null_value_repeat_flag(self):
        words = sce.apply_ruleset(['baaa'], 'a>b/b_ repeat')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bbbb')

    def test_overflowing_repeat_flag(self):
        words = sce.apply_ruleset(['baaa'], 'a>b/c_ repeat')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'baaa')

    def test_given_value_age_flag(self):
        ruleset = '\n'.join(['a>b age:2',
                             'b>a'])
        words = sce.apply_ruleset(['aaa'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bbb')

    def test_null_value_age_flag(self):
        ruleset = '\n'.join(['a>b age',
                             '+a/_b',
                             '+a/_b',
                             '+a/_b'])
        words = sce.apply_ruleset(['a'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bbbbbbbb')

    def test_chained_age_flag(self):
        ruleset = '\n'.join(['a>b age:3',
                             '+a/_b age:3'])
        words = sce.apply_ruleset(['a'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'babababa')


class TestExceptions(unittest.TestCase):

    def test_word_unchanged_exception(self):
        rule = sce.Rule(rule='b>a')
        word = core.Word(lexeme='a')
        with self.assertRaises(sce.WordUnchanged):
            rule.apply(word)


all_tests = unittest.TestSuite()
all_tests.addTest(unittest.makeSuite(TestMainChange))
all_tests.addTest(unittest.makeSuite(TestCategories))
all_tests.addTest(unittest.makeSuite(TestFlags))
all_tests.addTest(unittest.makeSuite(TestExceptions))

unittest.TextTestRunner(verbosity=2).run(all_tests)
