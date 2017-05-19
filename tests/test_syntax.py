import unittest

from context import conlanger
from conlanger import core, sce


class TestSyntax(unittest.TestCase):

    def test_tar(self):
        words = sce.apply_ruleset(['a'], 'a>')
        changed_word = str(words[0])
        self.assertEqual(changed_word, '')

    def test_tar_rep(self):
        words = sce.apply_ruleset(['a'], 'a>b')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'b')

    def test_tar_env(self):
        words = sce.apply_ruleset(['aba'], 'a>/_#')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'ab')

    def test_tar_exc(self):
        words = sce.apply_ruleset(['aba'], 'a>!_#')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'ba')

    def test_tar_rep_env(self):
        words = sce.apply_ruleset(['aba'], 'a>b/_#')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'abb')

    def test_tar_rep_exc(self):
        words = sce.apply_ruleset(['aba'], 'a>b!_#')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bba')

    def test_tar_env_exc(self):
        words = sce.apply_ruleset(['baba'], 'a>/b_!_#')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bba')

    def test_tar_env_else(self):
        words = sce.apply_ruleset(['abaa'], 'a>/b_>c')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'cbc')

    def test_tar_exc_else(self):
        words = sce.apply_ruleset(['aaa'], 'a>!_#>c')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'c')

    def test_tar_rep_env_exc(self):
        words = sce.apply_ruleset(['baba'], 'a>b/b_!_#')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bbba')

    def test_tar_rep_exc_else(self):
        words = sce.apply_ruleset(['aaa'], 'a>b!_#>c')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bbc')

    def test_tar_env_exc_else(self):
        words = sce.apply_ruleset(['baba'], 'a>/b_!_#>c')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bbc')

    def test_tar_rep_env_exc_else(self):
        words = sce.apply_ruleset(['baba'], 'a>d/b_!_#>c')
        changed_word = str(words[0])
        self.assertEqual(changed_word, 'bdbc')
