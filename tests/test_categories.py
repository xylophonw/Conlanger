import unittest

from context import conlanger
from conlanger import core, sce


class TestCategories(unittest.TestCase):

    def test_make_empty_cat(self):
        cat = core.Cat()
        self.assertEqual(str(cat), '')

    def test_make_non_empty_cat(self):
        cat = core.Cat(values='a,b,c')
        self.assertEqual(str(cat), 'a, b, c')

    def test_only_cat_in_target(self):
        ruleset = ['x=a,b', '[x]>c']
        words = sce.apply_ruleset(['abc'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'ccc')

    def test_cat_and_non_cat_in_target(self):
        ruleset = ['x=a,b', 'd[x]>c']
        words = sce.apply_ruleset(['abcdadbdc'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'abcccdc')

    def test_subtract_cat(self):
        ruleset = ['x=b,c', '-[x]']
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
