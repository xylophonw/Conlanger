import unittest

from context import conlanger
from conlanger import core, sce


class TestMainChange(unittest.TestCase):

    def test_standard_change(self):
        rule = sce.Rule(rule='a>b')
        word = core.Word(lexeme='a')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'b')


    def test_global_addition_change(self):
        rule = sce.Rule(rule='+b')
        word = core.Word(lexeme='ac')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'babcb')

    def test_initial_addition_change(self):
        rule = sce.Rule(rule='+b/#_')
        word = core.Word(lexeme='ac')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'bac')

    def test_medial_addition_change(self):
        rule = sce.Rule(rule='+b/a_c')
        word = core.Word(lexeme='ac')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'abc')

    def test_final_addition_change(self):
        rule = sce.Rule(rule='+b/_#')
        word = core.Word(lexeme='ac')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'acb')


    def test_global_subtraction_change(self):
        rule = sce.Rule(rule='-b')
        word = core.Word(lexeme='babc')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'ac')

    def test_initial_subtraction_change(self):
        rule = sce.Rule(rule='-b/#_')
        word = core.Word(lexeme='babc')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'abc')

    def test_medial_subtraction_change(self):
        rule = sce.Rule(rule='-b/a_c')
        word = core.Word(lexeme='babc')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'bac')

    def test_final_subtraction_change(self):
        rule = sce.Rule(rule='-b/_#')
        word = core.Word(lexeme='bacb')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'bac')


    def test_word_unchanged_exception(self):
        rule = sce.Rule(rule='b>a')
        word = core.Word(lexeme='a')
        with self.assertRaises(sce.WordUnchanged):
            rule.apply(word)


class TestCategories(unittest.TestCase):

    def test_make_empty_cat(self):
        cat = core.Cat()
        self.assertEqual(str(cat), '')

    def test_make_non_empty_cat(self):
        cat = core.Cat(values='a,b,c')
        self.assertEqual(str(cat), 'a, b, c')

    def test_only_cat_in_target(self):
        cat = core.Cat(values='a,b')
        rule = sce.Rule(rule='[x]>c',
                        cats={'x': cat})
        word = core.Word(lexeme='abc')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'ccc')

    def test_cat_and_non_cat_in_target(self):
        cat = core.Cat(values='a,b')
        rule = sce.Rule(rule='d[x]>c',
                        cats={'x': cat})
        word = core.Word(lexeme='abcdadbdc')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'abcccdc')

    def test_subtract_cat(self):
        cat = core.Cat(values='b,c')
        rule = sce.Rule(rule='-[x]',
                        cats={'x': cat})
        word = core.Word(lexeme='abcd')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'ad')

    def test_only_unnamed_cat_in_target(self):
        rule = sce.Rule(rule='[a,b]>c')
        word = core.Word(lexeme='abc')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'ccc')

    def test_unnamed_cat_and_non_cat_in_target(self):
        rule = sce.Rule(rule='[a,b]c>d')
        word = core.Word(lexeme='abacbccc')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'abddcc')

    def test_subtract_unnamed_cat(self):
        rule = sce.Rule(rule='-[b,c]')
        word = core.Word(lexeme='abcd')
        changed_word = str(rule.apply(word))
        self.assertEqual(changed_word, 'ad')


all_tests = unittest.TestSuite()
all_tests.addTest(unittest.makeSuite(TestMainChange))
all_tests.addTest(unittest.makeSuite(TestCategories))

unittest.TextTestRunner(verbosity=2).run(all_tests)
