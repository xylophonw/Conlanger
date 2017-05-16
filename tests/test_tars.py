import unittest

from context import conlanger


class TestMainChange(unittest.TestCase):

    def test_standard_change(self):
        rule = conlanger.sce.Rule(rule='a>b')
        word = conlanger.core.Word(lexeme='a')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'b')

    def test_global_addition_change(self):
        rule = conlanger.sce.Rule(rule='+b')
        word = conlanger.core.Word(lexeme='ac')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'babcb')

    def test_initial_addition_change(self):
        rule = conlanger.sce.Rule(rule='+b/#_')
        word = conlanger.core.Word(lexeme='ac')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'bac')

    def test_medial_addition_change(self):
        rule = conlanger.sce.Rule(rule='+b/a_c')
        word = conlanger.core.Word(lexeme='ac')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'abc')

    def test_final_addition_change(self):
        rule = conlanger.sce.Rule(rule='+b/_#')
        word = conlanger.core.Word(lexeme='ac')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'acb')

    def test_global_subtraction_change(self):
        rule = conlanger.sce.Rule(rule='-b')
        word = conlanger.core.Word(lexeme='babc')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'ac')

    def test_initial_subtraction_change(self):
        rule = conlanger.sce.Rule(rule='-b/#_')
        word = conlanger.core.Word(lexeme='babc')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'abc')

    def test_medial_subtraction_change(self):
        rule = conlanger.sce.Rule(rule='-b/a_c')
        word = conlanger.core.Word(lexeme='babc')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'bac')

    def test_final_subtraction_change(self):
        rule = conlanger.sce.Rule(rule='-b/_#')
        word = conlanger.core.Word(lexeme='bacb')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'bac')

    def test_word_unchanged_exception(self):
        rule = conlanger.sce.Rule(rule='b>a')
        word = conlanger.core.Word(lexeme='a')
        with self.assertRaises(conlanger.sce.WordUnchanged):
            rule.apply(word)



suite = unittest.TestLoader().loadTestsFromTestCase(TestMainChange)
unittest.TextTestRunner(verbosity=2).run(suite)
