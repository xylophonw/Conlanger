import unittest

from context import conlanger
from conlanger import core, sce


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
