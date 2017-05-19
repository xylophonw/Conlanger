import unittest

from context import conlanger
from conlanger import core, sce


class TestBasicChanges(unittest.TestCase):

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
