import unittest

from context import conlanger
from conlanger import core, sce


class TestTargetSpecialChars(unittest.TestCase):

    def test_basic_metathesis(self):
        words = sce.apply_ruleset(['abba'], 'ab><')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'baba')

    def test_right_category_metathesis(self):
        ruleset = ['x=a,b', '[x]c><']
        words = sce.apply_ruleset(['acbccbdca'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'cacbcbdca')

    def test_left_category_metathesis(self):
        ruleset = ['x=a,b', 'c[x]><']
        words = sce.apply_ruleset(['acbccbdca'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'acbcbcdac')

    def test_category_metathesis(self):
        ruleset = ['x=a,b', 'y=c,d', '[x][y]><']
        words = sce.apply_ruleset(['acbccbdca'], ruleset)
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'cacbcdbca')

    def test_nonce_category_metathesis(self):
        words = sce.apply_ruleset(['acbccbdca'], '[a,b][c,d]><')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'cacbcdbca')


    def test_at_symbol_with_0_index(self):
        words = sce.apply_ruleset(['aaaa'], 'a@0>b')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'baaa')

    def test_at_symbol_with_positive_index(self):
        words = sce.apply_ruleset(['aaaa'], 'a@2>b')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'aaba')

    def test_at_symbol_with_negative_index(self):
        words = sce.apply_ruleset(['aaaa'], 'a@-1>b')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'aaab')

    def test_at_symbol_with_pipe(self):
        words = sce.apply_ruleset(['aaaa'], 'a@0|2>b')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'baba')


    def test_simple_multrep_in_tar(self):
        words = sce.apply_ruleset(['cacbc'], 'a,b>d')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'cdcdc')

    def test_complex_multrep_in_tar(self):
        words = sce.apply_ruleset(['cacabc'], 'a@-1,b>d')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'cacddc')

    def test_simple_multrep_in_tar_and_rep(self):
        words = sce.apply_ruleset(['cacbc'], 'a,b>d,e')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'cdcec')

    def test_complex_multrep_in_tar_and_rep(self):
        words = sce.apply_ruleset(['cacabc'], 'a@-1,b>d,e')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'cacdec')
