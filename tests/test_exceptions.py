import unittest

from context import conlanger
from conlanger import core, sce


class TestExceptions(unittest.TestCase):

    def test_rule_failed_exception(self):
        rule = sce.Rule(rule='a>b')
        word = core.Word(lexeme='c')
        with self.assertRaises(sce.RuleFailed):
            rule.apply(word)

    def test_word_unchanged_exception(self):
        rule = sce.Rule(rule='a>a')
        word = core.Word(lexeme='a')
        with self.assertRaises(sce.WordUnchanged):
            rule.apply(word)
